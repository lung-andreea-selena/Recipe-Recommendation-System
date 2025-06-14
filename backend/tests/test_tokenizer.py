import re
from utils.phrase_tokenizer import tokenizer

def tokens(text: str):
    return tuple(tokenizer(text))

def test_phrase_join():
    assert tokens("soy sauce sugar") == ("soy_sauce", "sugar")

def test_case_insensitive():
    assert tokens("Brown Sugar") == ("brown_sugar",)

def test_multiple_phrases_and_words():
    txt = "brown sugar salt soy sauce"
    assert tokens(txt) == ("brown_sugar", "salt", "soy_sauce")

def test_punctuation_removed():
    assert tokens("soy sauce, garlic!") == ("soy_sauce", "garlic")

def test_unknown_phrase_is_split():
    assert tokens("fish sauce") == ("fish", "sauce")
         
