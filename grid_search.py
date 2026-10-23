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

# Define a function to evaluate the model's performance
def evaluate_model(model, X_test, y_test):
    """
    Evaluate the model's performance on the test data.
    """
    # Predict the scores for the test set
    predictions = model.predict(X_test)
    
    # Calculate evaluation metrics
    mae = mean_absolute_error(y_test, predictions)   # Mean Absolute Error
    mse = mean_squared_error(y_test, predictions)    # Mean Squared Error
    r2 = r2_score(y_test, predictions)               # R² Score

    # Print evaluation results
    print("Mean Absolute Error (MAE):", mae)
    print("Mean Squared Error (MSE):", mse)
    print("R² Score:", r2)

# Fit the model using the training data
model.fit(X_train, y_train)

# Evaluate the model on the test set
evaluate_model(model, X_test, y_test)
