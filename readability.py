import pandas as pd
import re

data = pd.read_csv('cleaned_file.csv')

# function to count the number of syllables in a word
def count_syllables(word):
    # using a regular expression to identify vowels (a, e, i, o, u)
    vowels = 'aeiouAEIOU'
    syllable_count = 0
    previous_char_is_vowel = False
    
    for char in word:
        if char in vowels:
            # increment syllable count if the current character is a vowel and the previous is not
            if not previous_char_is_vowel:
                syllable_count += 1
            previous_char_is_vowel = True
        else:
            # resetting the flag if the current character is not a vowel
            previous_char_is_vowel = False
    
    # removing silent 'e' at the end of words 
    if word.endswith('e') and len(word) > 1 and word[-2] not in vowels:
        syllable_count -= 1
    
    # ensuring that the syllable count is at least one for each word
    return max(1, syllable_count)

# function to calculate the Flesch-Kincaid readability score
def calculate_readability(text):
    # calculating the average sentence length
    # replacing ellipses with a placeholder to avoid counting each dot
    text = text.replace('...', 'ELLIPSES')
    sentence_count = text.count('.') + text.count('?') + text.count('!') + text.count('ELLIPSES')
    total_words = len(text.split())
    # handling the zero division error
    if sentence_count == 0:
        return 0
    average_length = total_words / sentence_count
    words = text.split()
    # calculating the total number of syllables in the text
    total_syllables = sum(count_syllables(word) for word in words)
    # calculating average number of syllables per word 
    average_syllable = total_syllables / total_words
    # calculating the readability score using the formula
    readability_score = 206.835 - (1.015 * average_length) - (84.6 * average_syllable)
    
    return readability_score

# applying the calculation to each entry in the 'full_text' column
data['flesch_kincaid_score'] = data['full_text'].apply(calculate_readability)
data.to_csv('flesch_kincaid_scores.csv', index=False)
