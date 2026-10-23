import pandas as pd
import string
import re

data = pd.read_csv('cleaned_file.csv')

# function to calculate the average word length
def calculate_average_word_length(text):
    # removing puntuation except for apostrophes and hyphens which might be part of words
    text = re.sub(r'[^\w\s\'-]', '', text)
    # splitting the text into words
    words = text.split()
    # counting the total number of characters (letters only)
    total_characters = sum(len(word) for word in words)
    # counting the total number of words in the text
    total_words = len(words)
    # calculating the average word length
    average_word_length = total_characters / total_words
    return average_word_length

data['average_word_length'] = data['full_text'].apply(calculate_average_word_length)

data.to_csv('word_length.csv', index=False)
