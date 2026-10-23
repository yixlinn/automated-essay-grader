import pandas as pd
import re
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import joblib

# 1. Load the testing dataset (test.csv for prediction after training)
test_data = pd.read_csv('test.csv')

# Function to count the number of syllables in a word
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

# Apply all functions to the test dataset (test.csv) and create their new corresponding columns
test_data['flesch_kincaid_score'] = test_data['full_text'].apply(calculate_readability)
test_data['average_sentence_length'] = test_data['full_text'].apply(calculate_average_sentence_length)
test_data['average_word_length'] = test_data['full_text'].apply(calculate_average_word_length)
test_data['word_count'] = test_data['full_text'].apply(calculate_word_count)
test_data['sentence_count'] = test_data['full_text'].apply(calculate_sentence_count)

# Reload the saved results from your combined dataset
combined_data = pd.read_csv('combined_results.csv')

# Define the feature set (X) and the target variable (y) for training
X = combined_data[['word_count', 'sentence_count', 'average_word_length', 'average_sentence_length', 'flesch_kincaid_score']]
y = combined_data['score']

# Split the dataset into training and testing sets (80% train, 20% test)
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialise the Random Forest Regressor model
model = RandomForestRegressor(
    n_estimators=150,         # Number of trees in the forest
    max_depth=10,             # Maximum depth of each tree
    min_samples_split=5,      # Minimum number of samples required to split an internal node
    min_samples_leaf=1,       # Minimum number of samples required to be at a leaf node
    random_state=42           # Ensure reproducibility
)

# Fit the model using the training data
model.fit(X_train, y_train)

# Make predictions on the validation set (from the same combined dataset)
y_val_pred = model.predict(X_val)

# Calculate the Mean Squared Error (MSE) for model evaluation on the validation set
mse_val = mean_squared_error(y_val, y_val_pred)
print(f"Mean Squared Error (Validation Set): {mse_val}")

# After training your model (e.g., model.fit(X_train, y_train))
joblib.dump(model, 'model.pkl')

# Make predictions on the small test set (test.csv) after training
X_test = test_data[['word_count', 'sentence_count', 'average_word_length', 'average_sentence_length', 'flesch_kincaid_score']]
y_test_pred = model.predict(X_test)

test_results_df = pd.DataFrame({'Predicted Grade': y_test_pred})
test_results_df.to_csv('test_predictions.csv', index=False)

print("Predictions on the test set are saved to 'test_predictions.csv'.")
