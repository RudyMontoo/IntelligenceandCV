import string
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

punc = string.punctuation
wnet = WordNetLemmatizer()
eng_stopwords = set(stopwords.words("english"))

