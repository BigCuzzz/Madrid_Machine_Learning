import pandas as pd
import matplotlib.pyplot as plt

from sklearn.inspection import permutation_importance
from sklearn.ensemble import RandomForestClassifier
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, classification_report, ConfusionMatrixDisplay

# Load data
df = pd.read_parquet("csv/processed/rm_features.parquet")

# Convert and sort by date
df["Date"] = pd.to_datetime(df["Date"], dayfirst=True, format="mixed")
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

# Remove rows with missing rolling features
mask = X.notna().all(axis=1)
X = X[mask]
y = y[mask]

print("Number of samples:", len(y))

# Time-based split
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
    ("classifier", RandomForestClassifier(
        n_estimators=100,
        max_depth=None,
        min_samples_split=2,
        min_samples_leaf=1,
        random_state=42,
        class_weight="balanced"
    ))
])

# Fit model
model.fit(X_train, y_train)

# Get Random Forest Model and feature importance
RandomForest = model.named_steps["classifier"]
feature_importance = RandomForest.feature_importances_

#Make a series with feature importance
feature_names = model.named_steps["preprocessor"].get_feature_names_out()
series = pd.Series(feature_importance,index=feature_names)
series = series.sort_values(ascending=False)
series.head(10).sort_values().plot(kind="barh")
#plt.figure(figsize=(12, 8))
plt.yticks(fontsize=8)
plt.show()


# Permutation Importance and series plot
result = permutation_importance(X=X_test,y=y_test,random_state=42,estimator=model,n_repeats=10)
series = pd.Series(result.importances_mean, index=X_test.columns)
series = series.sort_values(ascending=False)
series.head(10).sort_values().plot(kind="barh")
#plt.figure(figsize=(12, 8)).show()
plt.yticks(fontsize=8)
plt.show()
#quit()

# Predict
y_pred_train = model.predict(X_train)
y_pred_test = model.predict(X_test)

# Evaluate
print("Training accuracy:", round(accuracy_score(y_train, y_pred_train), 3))
print("Test accuracy:", round(accuracy_score(y_test, y_pred_test), 3))
print("\nClassification report:\n")
print(classification_report(y_test, y_pred_test))

# Confusion matrix
ConfusionMatrixDisplay.from_predictions(y_test, y_pred_test)
plt.title("Random Forest Confusion Matrix")
plt.show()


test_scores = []

for n in range(10, 101, 10):
    preprocessor = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), numeric_features),
            ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features),
        ]
    )
    model = Pipeline([
        ("preprocessor", preprocessor),
        ("classifier", RandomForestClassifier(
            n_estimators=n,
            max_depth=None,
            min_samples_split=2,
            min_samples_leaf=1,
            random_state=42,
            class_weight="balanced"
        ))
    ])
    model.fit(X_train, y_train)
    score = model.score(X_test, y_test)
    scores = f"Number of estimators: {n} Score: {score:.2%}       "
    print(f"Number of estimators: {n} Score: {score:.2%}\n")
    test_scores.append(scores)
    

#print("Test scores:\n",test_scores)