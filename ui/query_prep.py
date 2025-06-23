import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer, WordNetLemmatizer
import re
import argparse

# Download necessary NLTK data (run once)
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

def preprocess_search_string(text):
    # 1. Convert to lowercase
    text = text.lower()

    # 2. Remove punctuation and special characters
    text = re.sub(r'[^\w\s]', '', text) # Keep only alphanumeric and whitespace

    # 3. Tokenize the text
    tokens = word_tokenize(text)

    # 4. Remove stop words
    stop_words = set(stopwords.words('english'))
    filtered_tokens0 = [word for word in tokens if word not in stop_words]

    # 4.5 Remove words too common to allow like data or resource or others
    common = ['ocean', 'data', 'resource']
    filtered_tokens = [word for word in filtered_tokens0 if word not in common]

    # 5. Stemming (or Lemmatization - see note below)
    stemmer = PorterStemmer()
    stemmed_tokens = [stemmer.stem(word) for word in filtered_tokens]

    # Alternatively, for better accuracy, use lemmatization:
    lemmatizer = WordNetLemmatizer()
    lemmatized_tokens = [lemmatizer.lemmatize(word) for word in filtered_tokens]

    # Join the processed tokens back into a string for searching (optional, depends on search engine)
    # processed_string = " ".join(stemmed_tokens) # or lemmatized_tokens below
    processed_string = " ".join(lemmatized_tokens)

    return processed_string

parser = argparse.ArgumentParser()
parser.add_argument("-q", "--query", required=True, help="search query")
args = parser.parse_args()

search_query = args.query
processed_query = preprocess_search_string(search_query)
print(f"Original query: {search_query}")
print(f"Processed query: {processed_query}")