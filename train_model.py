# train_model.py
# Simple training script for insurance cost prediction

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import pickle

# Sample dataset (Kaggle-style)
url = "https://raw.githubusercontent.com/stedy/Machine-Learning-with-R-datasets/master/insurance.csv"
data = pd.read_csv(url)

# Encode categorical columns
data.replace({"sex": {"male": 1, "female": 0},
              "smoker": {"yes": 1, "no": 0},
              "region": {"northeast": 0, "northwest": 1, "southeast": 2, "southwest": 3}}, inplace=True)

# Split data
X = data.drop("charges", axis=1)
y = data["charges"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train simple Linear Regression
model = LinearRegression()
model.fit(X_train, y_train)

# Save model
pickle.dump(model, open("model.pkl", "wb"))
print("✅ Model trained and saved successfully as model.pkl")
