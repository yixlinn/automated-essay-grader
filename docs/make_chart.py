import joblib
import matplotlib.pyplot as plt  

model = joblib.load('model.pkl')
features = ['Word count', 'Sentence count', 'Avg word length', 'Avg sentence length', 'Flesch-Kincaid']
importances = model.feature_importances_
order = importances.argsort()

plt.figure(figsize=(8, 4.5))
plt.barh([features[i] for i in order], importances[order], color='#4d6bfe')
plt.xlabel('Importance')
plt.title('Which features drive the predicted score?')
plt.tight_layout()
plt.savefig('docs/feature_importance.png', dpi=150)

