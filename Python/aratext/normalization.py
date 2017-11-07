# Normalization function
import re


def normalize_alphabet(text):
    """ Normalize alphabets
    :param text: The given text
    :return: The normalized text after replacements
    """
    text = re.sub("[إأٱآا]", "ا", text)
    text = re.sub("ي", "ی", text)
    # text = re.sub("ؤ", "ء", text)
    text = re.sub("ئ", "ی", text)
    text = re.sub("ة", "ه", text)
    text = re.sub("ك", "ک", text)
    # if text.startswith("ال"):
    #  text = text[2:] 
    return text
