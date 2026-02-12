import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

import joblib
import string
punc = string.punctuation
wnet = WordNetLemmatizer()
eng_stopwords = set(stopwords.words("english"))

def preprocess_text(sentences):
    cleaned_sentences = []

    for sentence in sentences:
        # lowercase
        sentence = sentence.lower()

        # tokenize
        tokens = word_tokenize(sentence)

        # remove punctuation
        tokens = [t for t in tokens if t not in punc]

        # remove stopwords
        tokens = [t for t in tokens if t not in eng_stopwords]

        # lemmatization
        tokens = [wnet.lemmatize(t, "v") for t in tokens]

        cleaned_sentences.append(" ".join(tokens))

    return cleaned_sentences


def predict_intent(user_input):
    vectorizer = joblib.load("tfidf.pkl")
    logistic = joblib.load("intent_clf_model.pkl")


    processed = preprocess_text([user_input])
    user_vector = vectorizer.transform(processed)
    prediction = logistic.predict(user_vector)
    return prediction[0]

print(predict_intent("hola"))