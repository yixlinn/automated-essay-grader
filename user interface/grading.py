import pandas as pd
import re
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import joblib

# loading the model that's been trained previously
model = joblib.load('model.pkl')

# function to count the number of syllables in a word
def count_syllables(word):
    vowels = 'aeiouAEIOU'
    syllable_count = 0
    previous_char_is_vowel = False

    for char in word:
        if char in vowels:
            if not previous_char_is_vowel:
                syllable_count += 1
            previous_char_is_vowel = True
        else:
            previous_char_is_vowel = False

    if word.endswith('e') and len(word) > 1 and word[-2] not in vowels:
        syllable_count -= 1

    return max(1, syllable_count)

# Function to calculate the Flesch-Kincaid readability score
def calculate_readability(text):
    text = text.replace('...', 'ELLIPSES')
    sentence_count = text.count('.') + text.count('?') + text.count('!') + text.count('ELLIPSES')
    total_words = len(text.split())
    
    if sentence_count == 0:
        return 0
    
    average_length = total_words / sentence_count
    words = text.split()
    total_syllables = sum(count_syllables(word) for word in words)
    average_syllable = total_syllables / total_words
    
    readability_score = 206.835 - (1.015 * average_length) - (84.6 * average_syllable)
    return readability_score

# Function to calculate the average sentence length
def calculate_average_sentence_length(text):
    text = text.replace('...', 'ELLIPSES')
    sentence_count = text.count('.') + text.count('?') + text.count('!') + text.count('ELLIPSES')
    total_words = len(text.split())
    
    if sentence_count == 0:
        return 0
    
    average_length = total_words / sentence_count
    return average_length

# Function to calculate the average word length
def calculate_average_word_length(text):
    text = re.sub(r'[^\w\s\'-]', '', text)
    words = text.split()
    total_characters = sum(len(word) for word in words)
    total_words = len(words)
    average_word_length = total_characters / total_words
    return average_word_length

# Function to calculate the word count
def calculate_word_count(text):
    return len(text.split())

# Function to calculate the sentence count
def calculate_sentence_count(text):
    text = text.replace('...', 'ELLIPSES')
    sentence_count = text.count('.') + text.count('?') + text.count('!') + text.count('ELLIPSES')
    return sentence_count

def grade_essay(text):
    features = {
        'word_count': calculate_word_count(text),
        'sentence_count': calculate_sentence_count(text),
        'average_word_length': calculate_average_word_length(text),
        'average_sentence_length': calculate_average_sentence_length(text),
        'flesch_kincaid_score': calculate_readability(text)
    }
     # converting into a DataFrame
    input_df = pd.DataFrame([features])

    # predicting the score using the model
    predicted_score = model.predict(input_df)[0]

    # generate feedback based on the score
    if predicted_score >= 10:
        feedback = "Excellent work! Your writing is clear and well-structured."
    elif predicted_score >= 7:
        feedback = "Good effort! Some improvements could be made in structure or clarity."
    elif predicted_score >= 4:
        feedback = "Fair, but your essay needs better organisation and vocabulary."
    else:
        feedback = "Your essay needs significant improvements in structure and language."

    # return both score and feedback
    return round(predicted_score, 2), feedback
