# Automated Essay Grader

A machine-learning system that scores student essays (0-12) and generates feedback, with a desktop interface for students and a batch dashboard for teachers.

## How it works

Raw essay → tokenisation → feature extraction (word count, sentence count, average word length, average sentence length, Flesch-Kincaid readability) → Random Forest regressor → predicted score + banded feedback.

## Results

| Model | MAE | MSE | R² |
|---|---|---|---|
| Linear Regression | 0.568 | 0.560 | 0.496 |
| Random Forest (150 trees, depth 10) | **0.555** | **0.540** | **0.514** |

Random Forest outperforms Linear Regression on every metric. MAE of 0.55 on a
0–12 scale means predictions land within roughly half a point of the human score.
The model uses surface statistics only — no semantic or argument-quality
features — so it cannot distinguish fluent-but-empty writing from real substance.

![feature_importance](docs/feature_importance.png)

## Setup

```bash
git clone https://github.com/yixlinn/automated-essay-grader.git
cd automated-essay-grader
python -m venv .venv && source .venv/bin/activate # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Download the dataset from Kaggle PERSUADE 2.0 and place train.csv / test.csv in the project root.

```bash
python train_model.py # trains the model, writes model.pkl
python "user-interface/combined.py" # launches the app
```
