# README for Validator

## Notes

* testIOBound.py
  * Stores to pyoxigraph.   Looks like it does 10 to 20 per second and would take ~7 hours.
* testThreadPool.py
  * stores to dataframe to serialize later (might have memory issues)
* validateToLance.py
  * does have the logic to store in lance  (single threaded)
* validateToOxigraph.py
  * validate and stores in oxigraph (single threaded)


* store the graphs from the validation in lancedb and then process to quads for loading into a graph from there.
* Or use pyoxigraph from the start?
* A table format for use in KuzuDB?   nice for analytics and path analysis

## Rust option

Lincoln institute, Internet of Water, is using:

https://github.com/rudof-project/rudof?tab=readme-ov-file

This is work checking out.  May need https://lib.rs/crates/rdftk_core to provide
Skolemization.  Though I don't see it in there nor in rudof.   Without that,
it's a bit hard to move over, though it's not an impossible bit of logic
to do in Rust.
