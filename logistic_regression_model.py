import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (accuracy_score, recall_score, 
                           roc_auc_score, f1_score, 
                           classification_report, confusion_matrix)
from sklearn.utils.class_weight import compute_class_weight
from imblearn.over_sampling import SMOTE, ADASYN
import numpy as np

# Data loading
data = pd.read_csv('process_data.csv')

# Feature and target variable
X = data.drop('loan_status', axis=1)
y = data['loan_status']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, stratify=y, random_state=42
)

print("\n=== Class weights method ===")
# Compute class weights
classes = np.unique(y_train)
weights = compute_class_weight('balanced', classes=classes, y=y_train)
class_weights = dict(zip(classes, weights))

# Logistic Regression with class weights
model_weighted = LogisticRegression(
    class_weight=class_weights,
    max_iter=1000,
    random_state=42
)

print("\n=== SMOTE method ===")
smote = SMOTE(
    sampling_strategy=0.8,
    random_state=42,
    k_neighbors=3
)
X_train_smote, y_train_smote = smote.fit_resample(X_train, y_train)
model_smote = LogisticRegression(
    max_iter=1000,
    random_state=42,
    class_weight='balanced'
)

print("\n=== ADASYN method ===")
adasyn = ADASYN(
    sampling_strategy=0.8,
    random_state=42,
    n_neighbors=3
)
X_train_adasyn, y_train_adasyn = adasyn.fit_resample(X_train, y_train)
model_adasyn = LogisticRegression(
    max_iter=1000,
    random_state=42,
    class_weight='balanced'
)

# Function to evaluate the model
def evaluate_model(model, X_train, y_train, X_test, y_test, method_name):
    '''Evaluate the model with training and testing data.
    Args:
        model: The model to evaluate.
        X_train: Training features.
        y_train: Training labels.
        X_test: Testing features.
        y_test: Testing labels.
        method_name: Name of the method for logging.
    '''
    # train the model
    model.fit(X_train, y_train)
    
    # predict
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]
    
    # evaluate the model
    print(f"\n{method_name}Evaluate results:")
    print("Accuracy:", accuracy_score(y_test, y_pred))
    print("Recall:", recall_score(y_test, y_pred))
    print("F1:", f1_score(y_test, y_pred))
    print("AUC-ROC:", roc_auc_score(y_test, y_proba))
    print("\n Classification report:")
    print(classification_report(y_test, y_pred))
    print("Confusion matrix:")
    print(confusion_matrix(y_test, y_pred))
    
    return model




# Evaluate models
model_weighted = evaluate_model(
    model_weighted, X_train, y_train, X_test, y_test,'class_weights method'
)

model_smote = evaluate_model(
    model_smote, X_train_smote, y_train_smote, X_test, y_test,'smote method'
)

model_adasyn = evaluate_model(
    model_adasyn, X_train_adasyn, y_train_adasyn, X_test, y_test,'adasyn method'
)

# Model saving
import joblib
joblib.dump(model_weighted, 'credit_risk_model_weighted.pkl')
joblib.dump(model_smote, 'credit_risk_model_smote.pkl')
joblib.dump(model_adasyn, 'credit_risk_model_adasyn.pkl')

