import re
import contractions
from typing import Dict, Iterable, Match, Pattern

from nltk.stem.snowball import SnowballStemmer
from spacy import load


class Tokenizer:
    def __init__(self):
        self.nlp = load("en_core_web_sm")
        self.stemmer = SnowballStemmer(language="english")

    def tokenize(self, text: str, remove_stopwords: bool = True) -> Iterable[str]:
        expanded_text = contractions.fix(text)
        lower_text = expanded_text.lower()
        cleaned_text = clean_text(lower_text)
        preprocessed_text = remove_extra_spaces(cleaned_text)
        doc = self.nlp(preprocessed_text)
        result = set()
        for token in doc:
            if token_is_valid(token, remove_stopwords):
                temp = self.stemmer.stem(token.text).lower()
                result.add(temp)
        return result


def remove_extra_spaces(text: str) -> str:
    return re.sub(" +", " ", text)


def clean_text(text: str) -> str:
    text = re.sub(r"\w*\d\w*", "", text)
    text = re.sub("\n", " ", text)
    text = re.sub(r"http\S+", "", text)
    text = re.sub("[^a-z]", " ", text)
    return text


def token_is_valid(token, remove_stopwords: bool) -> bool:
    if remove_stopwords and token.is_stop:
        return False
    if token.is_punct or token.is_space:
        return False
    if token.pos_ in ["ADP", "AUX", "CONJ", "DET", "PART", "PRON", "SCONJ"]:
        return False
    return True
