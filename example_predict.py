import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

data = pd.read_csv('combined_results.csv')

# selecting the target variable
X = data[['word_count', 'sentence_count', 'average_word_length', 'average_sentence_length', 'flesch_kincaid_score']]  
y = data['score']  # target variable

# splitting the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# training the model
model = LinearRegression()
model.fit(X_train, y_train)

predictions = model.predict(X_test)

# selecting the first index of the row I want to check
example = 1

# display the actual and predicted values for the selected row
actual_value = y_test.iloc[example]
predicted_value = predictions[example]

print(f"Actual Score: {actual_value}")
print(f"Predicted Score: {predicted_value}")
