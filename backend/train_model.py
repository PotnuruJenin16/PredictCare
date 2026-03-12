"""
Model Training Script for Disease Prediction System
====================================================
This script trains a RandomForest classifier using TF-IDF vectorization
to predict diseases based on symptom text input.

Algorithm Choice (for viva):
- TF-IDF: Converts text symptoms to numerical features
- RandomForest: Handles multi-class classification, provides probability scores

Author: Predict Care
"""

import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import joblib

# Paths
BASE_DIR = os.path.dirname(__file__)
DATASET_PATH = os.path.join(BASE_DIR, "dataset.csv")
MODEL_DIR = os.path.join(BASE_DIR, "model")


def load_dataset() -> pd.DataFrame:
    """Load the generated dataset."""
    if not os.path.exists(DATASET_PATH):
        raise FileNotFoundError(
            f"Dataset not found at {DATASET_PATH}. "
            "Run dataset_generator.py first!"
        )
    return pd.read_csv(DATASET_PATH)


def preprocess_text(text: str) -> str:
    """
    Basic text preprocessing for symptom input.
    - Convert to lowercase
    - Remove extra whitespace
    """
    return text.lower().strip()


def train_model():
    """
    Main training function.
    
    Steps:
    1. Load dataset
    2. Preprocess text
    3. Create TF-IDF features
    4. Train RandomForest classifier
    5. Evaluate and save model
    """
    print("=" * 60)
    print("Disease Prediction Model Training")
    print("=" * 60)
    
    # ========================================
    # STEP 1: Load Dataset
    # ========================================
    print("\n[Step 1/6] Loading dataset...")
    df = load_dataset()
    print(f"           Loaded {len(df)} samples")
    
    # ========================================
    # STEP 2: Preprocess Data
    # ========================================
    print("[Step 2/6] Preprocessing symptoms text...")
    df['symptoms_clean'] = df['symptoms'].apply(preprocess_text)
    
    # Features and target
    X = df['symptoms_clean']  # Symptom text
    y = df['disease']         # Disease label (target)
    
    # ========================================
    # STEP 3: Split Data (80% train, 20% test)
    # ========================================
    print("[Step 3/6] Splitting into train/test sets...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, 
        test_size=0.2, 
        random_state=42,
        stratify=y  # Ensures balanced split across all diseases
    )
    print(f"           Training samples: {len(X_train)}")
    print(f"           Testing samples: {len(X_test)}")
    
    # ========================================
    # STEP 4: TF-IDF Vectorization
    # ========================================
    print("[Step 4/6] Creating TF-IDF features...")
    
    # TF-IDF Vectorizer configuration
    # - max_features: Limit vocabulary size
    # - ngram_range: Use single words and word pairs
    # - stop_words: Remove common English words
    vectorizer = TfidfVectorizer(
        max_features=500,           # Vocabulary limit
        ngram_range=(1, 2),         # Unigrams and bigrams
        stop_words='english',       # Remove stop words
        lowercase=True              # Convert to lowercase
    )
    
    # Fit on training data and transform both sets
    X_train_tfidf = vectorizer.fit_transform(X_train)
    X_test_tfidf = vectorizer.transform(X_test)
    
    print(f"           TF-IDF features created: {X_train_tfidf.shape[1]}")
    
    # ========================================
    # STEP 5: Train RandomForest Classifier
    # ========================================
    print("[Step 5/6] Training RandomForest classifier...")
    
    # RandomForest configuration
    # - n_estimators: Number of trees in forest
    # - max_depth: Limit tree depth to prevent overfitting
    # - random_state: For reproducibility
    # - n_jobs: Use all CPU cores for faster training
    model = RandomForestClassifier(
        n_estimators=100,           # 100 decision trees
        max_depth=20,               # Max depth per tree
        min_samples_split=5,        # Min samples to split node
        random_state=42,            # Reproducibility
        n_jobs=-1                   # Use all CPU cores
    )
    
    # Train the model
    model.fit(X_train_tfidf, y_train)
    print("           Model training complete!")
    
    # ========================================
    # STEP 6: Evaluate Model
    # ========================================
    print("[Step 6/6] Evaluating model performance...")
    
    # Predictions on test set
    y_pred = model.predict(X_test_tfidf)
    
    # Calculate accuracy
    accuracy = accuracy_score(y_test, y_pred)
    print(f"\n           Test Accuracy: {accuracy:.2%}")

    # Calculate weighted metrics
    from sklearn.metrics import precision_recall_fscore_support, confusion_matrix
    precision, recall, f1, _ = precision_recall_fscore_support(y_test, y_pred, average='weighted')
    
    print("\n" + "=" * 60)
    print("Model Performance Evaluation (Statistical Results)")
    print("=" * 60)
    print("Performance Metrics")
    print(f"• Accuracy:  {accuracy:.2%}")
    print(f"• Precision: {precision:.2%}")
    print(f"• Recall:    {recall:.2%}")
    print(f"• F1-Score:  {f1:.2%}")

    # Calculate Confusion Matrix Summary (Aggregated for Multi-class)
    cm = confusion_matrix(y_test, y_pred)
    
    # For multi-class, we calculate TP/FP/FN/TN for each class and sum them
    FP = cm.sum(axis=0) - np.diag(cm)  
    FN = cm.sum(axis=1) - np.diag(cm)
    TP = np.diag(cm)
    TN = cm.sum() - (FP + FN + TP)

    # Summing them up to give a single "macro" summary value often used in basic reports
    # Note: TN is usually very high in multi-class because it's the sum of "not class X" for all classes
    print("\nConfusion Matrix Summary (Aggregated)")
    print(f"• True Positives (TP):  {int(TP.sum())}")
    print(f"• True Negatives (TN):  {int(TN.sum())}")
    print(f"• False Positives (FP): {int(FP.sum())}")
    print(f"• False Negatives (FN): {int(FN.sum())}")
    print("\n*Note: True Negatives are high because for every single correct prediction,\nit correctly predicts that it is NOT any of the other diseases.*")
    
    # ========================================
    # Save Model and Vectorizer
    # ========================================
    print("\n" + "=" * 60)
    print("Saving Model and Vectorizer")
    print("=" * 60)
    
    # Create model directory if not exists
    os.makedirs(MODEL_DIR, exist_ok=True)
    
    # Save model
    model_path = os.path.join(MODEL_DIR, "disease_classifier.joblib")
    joblib.dump(model, model_path)
    print(f"[✓] Model saved: {model_path}")
    
    # Save vectorizer
    vectorizer_path = os.path.join(MODEL_DIR, "tfidf_vectorizer.joblib")
    joblib.dump(vectorizer, vectorizer_path)
    print(f"[✓] Vectorizer saved: {vectorizer_path}")
    
    # Save disease-risk mapping for the API
    risk_mapping = df[['disease', 'risk_level']].drop_duplicates()
    risk_mapping = dict(zip(risk_mapping['disease'], risk_mapping['risk_level']))
    risk_path = os.path.join(MODEL_DIR, "risk_mapping.joblib")
    joblib.dump(risk_mapping, risk_path)
    print(f"[✓] Risk mapping saved: {risk_path}")
    
    print("\n" + "=" * 60)
    print("Training Complete! Model is ready for predictions.")
    print("=" * 60)
    
    return model, vectorizer


def test_prediction(model, vectorizer):
    """Test the model with sample input."""
    print("\n" + "=" * 60)
    print("Testing Model with Sample Input")
    print("=" * 60)
    
    test_cases = [
        "fever headache body aches chills",
        "itchy skin red patches dry skin",
        "chest pain shortness of breath fatigue"
    ]
    
    for symptoms in test_cases:
        # Transform input
        symptoms_tfidf = vectorizer.transform([symptoms.lower()])
        
        # Predict
        prediction = model.predict(symptoms_tfidf)[0]
        probabilities = model.predict_proba(symptoms_tfidf)[0]
        confidence = max(probabilities)
        
        print(f"\nSymptoms: '{symptoms}'")
        print(f"Predicted Disease: {prediction}")
        print(f"Confidence: {confidence:.2%}")


if __name__ == "__main__":
    model, vectorizer = train_model()
    test_prediction(model, vectorizer)
