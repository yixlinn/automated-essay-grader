import pandas as pd

# creating sample data for testing
data = {
    'essay_id': [1, 2, 3,],
    'full_text': ["This is a test sentence.", "Another one!.", "Another 1."]
}

dataframe = pd.DataFrame(data)

# saving the data to a csv file for testing
dataframe.to_csv('tokentest.csv', index=False)
