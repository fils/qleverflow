import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer, WordNetLemmatizer
import re

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
    filtered_tokens = [word for word in tokens if word not in stop_words]

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

# Example usage:
search_query = "What are the best python libraries for natural language processing?"
processed_query = preprocess_search_string(search_query)
print(f"Original query: {search_query}")
print(f"Processed query: {processed_query}")

search_query_2 = "Data related to the acidification of the ocean near coral reefs"
processed_query_2 = preprocess_search_string(search_query_2)
print(f"Original query: {search_query_2}")
print(f"Processed query: {processed_query_2}")