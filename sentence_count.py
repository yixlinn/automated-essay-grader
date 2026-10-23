import pandas as pd

data = pd.read_csv('cleaned_file.csv')

# function to count the number of sentence
def calculate_sentence_count(text):
    # replacing elipses with a placeholder so that it does not count each individual dot
    text = text.replace('...', 'ELLIPSES')
    # counting the number of punctuations
    sentence_count = text.count('.') + text.count('?') + text.count('!') + text.count('ELLIPSES')
    return sentence_count

# applying the function to the column containing the essay text
data['sentence_count'] = data['full_text'].apply(calculate_sentence_count)
# saving the result to a new CSV file
data.to_csv('sentence_count.csv', index=False) 