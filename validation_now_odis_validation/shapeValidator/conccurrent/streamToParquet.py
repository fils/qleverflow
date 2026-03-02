import atexit
import multiprocessing as mp
import time
import threading
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
import requests
import pyarrow as pa
import pyarrow.parquet as pq
from datetime import datetime
import os
from pathlib import Path
from queue import Empty

session: requests.Session

class StreamingParquetWriter:
    """
    Handles writing results to Parquet files in batches to avoid memory issues
    """

    def __init__(self, batch_size=1000, base_filename="responses"):
        self.batch_size = batch_size
        self.base_filename = base_filename
        self.current_batch = []
        self.file_counter = 0
        self.total_written = 0
        self.lock = threading.Lock()

        # Ensure output directory exists
        Path("parquet_output").mkdir(exist_ok=True)

    def add_result(self, result):
        """Add a result to the current batch"""
        with self.lock:
            self.current_batch.append(result)

            # Write batch when it reaches the limit
            if len(self.current_batch) >= self.batch_size:
                self._write_batch()

    def _write_batch(self):
        """Write current batch to a Parquet file"""
        if not self.current_batch:
            return

        filename = f"parquet_output/{self.base_filename}_{self.file_counter:06d}.parquet"

        # Prepare data for PyArrow
        data = {
            'request_id': [r.get('request_id', 0) for r in self.current_batch],
            'url': [r.get('url', '') for r in self.current_batch],
            'status_code': [r.get('status_code', 0) for r in self.current_batch],
            'content': [r.get('content', b'') for r in self.current_batch],
            'content_length': [r.get('content_length', 0) for r in self.current_batch],
            'content_type': [r.get('content_type', 'unknown') for r in self.current_batch],
            'download_time': [r.get('download_time', 0.0) for r in self.current_batch],
            'timestamp': [r.get('timestamp', '') for r in self.current_batch],
            'process_name': [r.get('process_name', '') for r in self.current_batch],
            'error': [r.get('error', '') for r in self.current_batch]
        }

        # Create and write PyArrow table
        table = pa.table(data)
        pq.write_table(table, filename, compression='snappy')

        batch_size = len(self.current_batch)
        self.total_written += batch_size
        self.file_counter += 1

        print(f"Written batch {self.file_counter}: {batch_size} records to {filename}")
        print(f"Total records written so far: {self.total_written:,}")

        # Clear the batch
        self.current_batch.clear()

    def finalize(self):
        """Write any remaining results in the batch"""
        with self.lock:
            if self.current_batch:
                self._write_batch()

        print(f"Finalized: {self.total_written:,} total records in {self.file_counter} files")

        # Optionally combine files into a single dataset
        self._create_dataset_metadata()

    def _create_dataset_metadata(self):
        """Create a dataset metadata file for easy reading"""
        files = list(Path("parquet_output").glob(f"{self.base_filename}_*.parquet"))

        with open("parquet_output/dataset_info.txt", "w") as f:
            f.write(f"Dataset created: {datetime.now()}\n")
            f.write(f"Total files: {len(files)}\n")
            f.write(f"Total records: {self.total_written:,}\n")
            f.write(f"Files:\n")
            for file in sorted(files):
                f.write(f"  {file.name}\n")

# Global writer instance
writer = None

def main():
    """Main function optimized for millions of sites"""

    # For testing, use a smaller number
    # For production, this could be millions
    sites = [
        "https://www.jython.org",
        "http://olympus.realpython.org/dice",
        "https://httpbin.org/json",
        "https://httpbin.org/html",
    ] * 2500  # 10K sites for testing

    print(f"Preparing to download {len(sites):,} sites...")

    global writer
    writer = StreamingParquetWriter(batch_size=500)  # Write every 500 responses

    start_time = time.perf_counter()
    download_all_sites_streaming(sites)
    duration = time.perf_counter() - start_time

    writer.finalize()

    print(f"\nCompleted {len(sites):,} sites in {duration:.2f} seconds")
    print(f"Average: {len(sites)/duration:.1f} sites/second")

def download_all_sites_streaming(sites):
    """
    Stream results directly to disk to avoid memory issues
    Uses multiprocessing.Queue for safe inter-process communication
    """

    manager = mp.Manager()
    # Use multiprocessing.Manager().Queue for robust cross-process sharing
    result_queue = manager.Queue(maxsize=2000)

    # Start background writer thread
    writer_thread = threading.Thread(
        target=background_writer,
        args=(result_queue,),
        daemon=True
    )
    writer_thread.start()

    print(f"Starting downloads with {mp.cpu_count()} processes...")

    try:
        with ProcessPoolExecutor(
            max_workers=mp.cpu_count(),
            initializer=init_process
        ) as executor:

            # Submit all jobs
            futures = [
                executor.submit(download_site_streaming, url, i, result_queue)
                for i, url in enumerate(sites)
            ]

            # Monitor progress
            completed = 0
            for future in futures:
                future.result()
                completed += 1

                if completed % 1000 == 0:
                    print(f"Progress: {completed:,}/{len(sites):,} ({completed/len(sites)*100:.1f}%)")

    finally:
        # Signal writer thread to stop
        result_queue.put(None)  # Poison pill
        writer_thread.join(timeout=30)

def background_writer(result_queue):
    """
    Background thread that continuously writes results to avoid memory buildup
    Uses multiprocessing.Queue which is safe for cross-process communication
    """
    while True:
        try:
            result = result_queue.get(timeout=5)

            if result is None:  # Poison pill - shutdown signal
                break

            writer.add_result(result)

        except Empty:
            # Queue was empty, this is expected, continue waiting
            continue
        except Exception as e:  # Catches all other exceptions
            print(f"Writer thread error: {e}")
            break

def download_site_streaming(url, request_id, result_queue):
    """
    Download a site and put result in queue for background writing
    """
    try:
        start_time = time.perf_counter()

        with session.get(url, timeout=30) as response:
            download_time = time.perf_counter() - start_time

            result = {
                'request_id': request_id,
                'url': url,
                'status_code': response.status_code,
                'content': response.content,
                'content_length': len(response.content),
                'content_type': response.headers.get('content-type', 'unknown'),
                'download_time': download_time,
                'timestamp': datetime.now().isoformat(),
                'process_name': mp.current_process().name,
                'error': ''
            }

            # Put in queue for background writer
            result_queue.put(result)

            # Minimal logging to avoid I/O overhead
            if request_id % 500 == 0:
                print(f"Downloaded: {url} ({len(response.content)} bytes)")

    except Exception as e:
        error_result = {
            'request_id': request_id,
            'url': url,
            'status_code': 0,
            'content': b'',
            'content_length': 0,
            'content_type': 'error',
            'download_time': 0.0,
            'timestamp': datetime.now().isoformat(),
            'process_name': mp.current_process().name,
            'error': str(e)
        }
        result_queue.put(error_result)

def init_process():
    """Initialize each worker process"""
    global session
    session = requests.Session()

    # Optimize session for high-volume scraping
    session.headers.update({
        'User-Agent': 'High-Volume-Scraper/1.0'
    })

    # Connection pooling for efficiency
    adapter = requests.adapters.HTTPAdapter(
        pool_connections=20,
        pool_maxsize=50,
        max_retries=2
    )
    session.mount('http://', adapter)
    session.mount('https://', adapter)

    atexit.register(session.close)

def read_streaming_results():
    """
    Read back all the Parquet files as a single dataset
    """
    try:
        # Read all parquet files in the output directory
        parquet_files = list(Path("parquet_output").glob("responses_*.parquet"))

        if not parquet_files:
            print("No Parquet files found")
            return None

        print(f"Reading {len(parquet_files)} Parquet files...")

        # Read all files into a single table
        tables = []
        for file in sorted(parquet_files):
            table = pq.read_table(file)
            tables.append(table)

        # Combine all tables
        combined_table = pa.concat_tables(tables)
        df = combined_table.to_pandas()

        print(f"Loaded {len(df):,} total records")

        # Show summary stats
        successful = (df['status_code'] == 200).sum()
        total_bytes = df['content_length'].sum()

        print(f"Successful downloads: {successful:,}")
        print(f"Total bytes: {total_bytes:,} ({total_bytes/(1024**2):.1f} MB)")

        return df

    except Exception as e:
        print(f"Error reading results: {e}")
        return None

if __name__ == "__main__":
    main()

    # Read results back
    print("\n" + "="*60)
    print("Reading streaming results:")
    read_streaming_results()
