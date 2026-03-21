import pandas as pd
import matplotlib.pyplot as plt
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from sklearn.metrics import ConfusionMatrixDisplay

# Load data
df = pd.read_parquet("csv/processed/rm_features.parquet")
print(len(df))

#Convert and sort by date
df["Date"] = pd.to_datetime(df["Date"], dayfirst=True,format="mixed")
df = df.sort_values("Date").reset_index(drop=True)

# Choose features and target
feature_cols = [
    "is_home",
    "opponent",
    "points_last_5_games",
    "GD_last_5_games",
    "SD_last_5_games",
    "SoTF_last_5_games"
]

X = df[feature_cols]
y = df["y"]

# Remove missing rows in features
mask = X.notna().all(axis=1)
X = X[mask]
y = y[mask]

# Timebased traning/test split
split_idx = int(len(X) * 0.8)
X_train, X_test = X.iloc[:split_idx], X.iloc[split_idx:]
y_train, y_test = y.iloc[:split_idx], y.iloc[split_idx:]

# Define feature types
categorical_features = ["opponent"]
numeric_features = [
    "is_home",
    "points_last_5_games",
    "GD_last_5_games",
    "SD_last_5_games",
    "SoTF_last_5_games"
]

# Preprocessing
preprocessor = ColumnTransformer(
    transformers=[
        ("num", StandardScaler(), numeric_features),
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features),
    ]
)

# Pipeline
model = Pipeline([
    ("preprocessor", preprocessor),
    ("classifier", LogisticRegression(
        max_iter=5000,
        C=1.0
        #class_weight="balanced"
    ))
])

# Fit
model.fit(X_train, y_train)

# Predict
y_pred_train = model.predict(X_train)
y_pred_test = model.predict(X_test)

# Evaluate
print("Training accuracy:", round(accuracy_score(y_train, y_pred_train), 3))
print("Test accuracy:", round(accuracy_score(y_test, y_pred_test), 3))
print("\nClassification report:\n")
print(classification_report(y_test, y_pred_test))

#Confusion matrix
print("\n\nConfusion Matrix:\n")
ConfusionMatrixDisplay.from_predictions(y_test, y_pred_test)
plt.show()
