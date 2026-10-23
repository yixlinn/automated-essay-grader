import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Load the dataset
data = pd.read_csv('combined_results.csv')

# Define the feature set (X) and the target variable (y)
X = data[['word_count', 'sentence_count', 'average_word_length', 'average_sentence_length', 'flesch_kincaid_score']]
y = data['score']

# Split the dataset into training and testing sets (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize the Random Forest Regressor model with your known optimal hyperparameters
model = RandomForestRegressor(
    n_estimators=150,         # Number of trees in the forest
    max_depth=10,             # Maximum depth of each tree
    min_samples_split=5,      # Minimum number of samples required to split an internal node
    min_samples_leaf=1,       # Minimum number of samples required to be at a leaf node
    random_state=42           # Ensure reproducibility
)

# Fit the model using the training data
model.fit(X_train, y_train)

# making predictions
predictions = model.predict(X_test)

# displaying a few examples of actual vs predicted scores
for i in range(1):  
    actual = y_test.iloc[i]
    predicted = predictions[i]
    print(f"Actual Score: {actual}, Predicted Score: {predicted}")
