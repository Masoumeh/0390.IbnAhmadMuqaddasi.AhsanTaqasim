# Normalization function
import re


def normalize_alphabet(text):
    """ Normalize alphabets
    :param text: The given text
    :return: The normalized text after replacements
    """
    text = re.sub("[إأٱآا]", "ا", text)
    text = re.sub("ى", "ي", text)
    text = re.sub("ؤ", "ء", text)
    text = re.sub("ئ", "ء", text)
    text = re.sub("ه", "ة", text)
    text = re.sub("ک", "ك", text)
    # if text.startswith("ال"):
    #  text = text[2:] 
    return text
