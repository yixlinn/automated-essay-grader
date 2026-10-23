import pandas as pd

data = pd.read_csv('cleaned_file.csv')

# function to calculate the average sentence length
def calculate_average_sentence_length(text):
    # replacing ellipses with a placeholder to avoid counting each dot
    text = text.replace('...', 'ELLIPSES')
    sentence_count = text.count('.') + text.count('?') + text.count('!') + text.count('ELLIPSES')
    total_words = len(text.split())
    # handling the zero division error
    if sentence_count == 0:
        return 0
    # calculating the average sentence length
    average_length = total_words / sentence_count
    return average_length

# creating a new column to store average sentence lengths
data['average_sentence_length'] = data['full_text'].apply(calculate_average_sentence_length)
# saving the result to an existent file
data.to_csv('sentence_count.csv', index=False)
