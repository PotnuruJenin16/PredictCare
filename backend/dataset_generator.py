"""
Dataset Generator for Disease Prediction System
================================================
This script generates a synthetic dataset of diseases and their symptoms.
Used for training the ML model in this academic demo project.

Author: Predict Care
"""

import pandas as pd
import random
import os

# ============================================
# DISEASE-SYMPTOM MAPPING (50 Common Diseases)
# ============================================
# Each disease has 6-10 associated symptoms
# This is simplified for academic demonstration

DISEASE_SYMPTOMS = {
    # Respiratory Diseases
    "Common Cold": ["runny nose", "sneezing", "sore throat", "mild fever", "cough", "congestion", "watery eyes"],
    "Influenza (Flu)": ["high fever", "body aches", "chills", "fatigue", "headache", "cough", "sore throat", "runny nose"],
    "Pneumonia": ["high fever", "chest pain", "difficulty breathing", "cough with phlegm", "fatigue", "sweating", "chills"],
    "Bronchitis": ["persistent cough", "mucus production", "chest discomfort", "fatigue", "shortness of breath", "mild fever"],
    "Asthma": ["wheezing", "shortness of breath", "chest tightness", "coughing at night", "difficulty breathing", "rapid breathing"],
    "Tuberculosis": ["persistent cough", "coughing blood", "night sweats", "weight loss", "fatigue", "fever", "chest pain"],
    "Sinusitis": ["facial pain", "nasal congestion", "runny nose", "headache", "cough", "fever", "bad breath"],
    
    # Digestive Diseases
    "Gastroenteritis": ["diarrhea", "vomiting", "nausea", "stomach cramps", "fever", "headache", "dehydration"],
    "Food Poisoning": ["nausea", "vomiting", "diarrhea", "stomach pain", "fever", "weakness", "dehydration"],
    "Acid Reflux (GERD)": ["heartburn", "chest pain", "difficulty swallowing", "regurgitation", "sour taste", "bloating"],
    "Peptic Ulcer": ["stomach pain", "bloating", "heartburn", "nausea", "vomiting", "weight loss", "dark stool"],
    "Irritable Bowel Syndrome": ["abdominal pain", "bloating", "gas", "diarrhea", "constipation", "cramping"],
    "Appendicitis": ["severe abdominal pain", "nausea", "vomiting", "fever", "loss of appetite", "constipation"],
    "Hepatitis": ["fatigue", "nausea", "abdominal pain", "loss of appetite", "jaundice", "dark urine", "joint pain"],
    
    # Cardiovascular Diseases
    "Hypertension": ["headache", "shortness of breath", "nosebleeds", "dizziness", "chest pain", "vision problems"],
    "Heart Disease": ["chest pain", "shortness of breath", "fatigue", "irregular heartbeat", "swollen legs", "dizziness"],
    "Anemia": ["fatigue", "weakness", "pale skin", "shortness of breath", "dizziness", "cold hands", "headache"],
    
    # Neurological Diseases
    "Migraine": ["severe headache", "nausea", "sensitivity to light", "sensitivity to sound", "visual disturbances", "vomiting"],
    "Tension Headache": ["dull headache", "pressure around forehead", "tenderness on scalp", "neck pain", "fatigue"],
    "Vertigo": ["dizziness", "spinning sensation", "nausea", "vomiting", "balance problems", "headache"],
    "Epilepsy": ["seizures", "confusion", "staring spells", "uncontrollable jerking", "loss of consciousness", "anxiety"],
    
    # Infectious Diseases
    "Malaria": ["high fever", "chills", "sweating", "headache", "nausea", "vomiting", "muscle pain", "fatigue"],
    "Dengue": ["high fever", "severe headache", "pain behind eyes", "joint pain", "muscle pain", "rash", "bleeding gums"],
    "Typhoid": ["prolonged fever", "weakness", "stomach pain", "headache", "loss of appetite", "rash", "diarrhea"],
    "Chickenpox": ["itchy rash", "red spots", "blisters", "fever", "fatigue", "headache", "loss of appetite"],
    "Measles": ["high fever", "cough", "runny nose", "red eyes", "rash", "white spots in mouth", "sensitivity to light"],
    "Mumps": ["swollen salivary glands", "fever", "headache", "muscle aches", "fatigue", "loss of appetite", "pain while chewing"],
    
    # Skin Diseases
    "Eczema": ["itchy skin", "red patches", "dry skin", "cracked skin", "swelling", "rough patches"],
    "Psoriasis": ["red patches", "silvery scales", "dry cracked skin", "itching", "burning", "thick nails"],
    "Acne": ["pimples", "blackheads", "whiteheads", "oily skin", "scarring", "skin inflammation"],
    "Dermatitis": ["itchy skin", "redness", "swelling", "blisters", "dry skin", "cracking"],
    "Fungal Infection": ["itching", "redness", "ring-shaped rash", "scaling", "cracking skin", "burning sensation"],
    
    # Musculoskeletal Diseases
    "Arthritis": ["joint pain", "stiffness", "swelling", "reduced range of motion", "redness around joints", "fatigue"],
    "Osteoporosis": ["back pain", "loss of height", "stooped posture", "bone fractures", "joint pain", "weakness"],
    "Muscle Strain": ["muscle pain", "swelling", "bruising", "limited movement", "muscle spasms", "weakness"],
    
    # Endocrine Diseases
    "Diabetes": ["frequent urination", "increased thirst", "weight loss", "fatigue", "blurred vision", "slow healing wounds"],
    "Hyperthyroidism": ["weight loss", "rapid heartbeat", "anxiety", "tremors", "sweating", "difficulty sleeping", "fatigue"],
    "Hypothyroidism": ["fatigue", "weight gain", "cold sensitivity", "dry skin", "depression", "constipation", "muscle weakness"],
    
    # Mental Health
    "Depression": ["persistent sadness", "loss of interest", "fatigue", "sleep problems", "appetite changes", "difficulty concentrating"],
    "Anxiety Disorder": ["excessive worry", "restlessness", "fatigue", "difficulty concentrating", "irritability", "sleep problems", "muscle tension"],
    "Insomnia": ["difficulty falling asleep", "waking up at night", "daytime fatigue", "irritability", "difficulty concentrating", "headache"],
    
    # Urinary Diseases
    "Urinary Tract Infection": ["burning urination", "frequent urination", "cloudy urine", "pelvic pain", "strong urine odor", "fever"],
    "Kidney Stones": ["severe pain in side", "pain during urination", "pink urine", "nausea", "vomiting", "frequent urination"],
    "Kidney Disease": ["fatigue", "swollen ankles", "frequent urination", "blood in urine", "foamy urine", "muscle cramps"],
    
    # Eye Diseases
    "Conjunctivitis": ["red eyes", "itchy eyes", "watery eyes", "discharge from eyes", "sensitivity to light", "gritty feeling"],
    "Glaucoma": ["eye pain", "blurred vision", "halos around lights", "headache", "nausea", "vision loss"],
    
    # Allergies
    "Allergic Rhinitis": ["sneezing", "runny nose", "itchy nose", "nasal congestion", "watery eyes", "itchy throat"],
    "Food Allergy": ["hives", "swelling", "itching", "stomach pain", "nausea", "difficulty breathing", "dizziness"],
    
    # Other Common Conditions
    "Dehydration": ["thirst", "dry mouth", "fatigue", "dizziness", "dark urine", "headache", "dry skin"],
    "Heat Stroke": ["high body temperature", "confusion", "rapid heartbeat", "headache", "nausea", "red skin", "unconsciousness"],
}

# Risk levels based on disease severity (for demo purposes)
DISEASE_RISK = {
    "Common Cold": "LOW",
    "Influenza (Flu)": "MEDIUM",
    "Pneumonia": "HIGH",
    "Bronchitis": "MEDIUM",
    "Asthma": "MEDIUM",
    "Tuberculosis": "HIGH",
    "Sinusitis": "LOW",
    "Gastroenteritis": "MEDIUM",
    "Food Poisoning": "MEDIUM",
    "Acid Reflux (GERD)": "LOW",
    "Peptic Ulcer": "MEDIUM",
    "Irritable Bowel Syndrome": "LOW",
    "Appendicitis": "HIGH",
    "Hepatitis": "HIGH",
    "Hypertension": "HIGH",
    "Heart Disease": "HIGH",
    "Anemia": "MEDIUM",
    "Migraine": "LOW",
    "Tension Headache": "LOW",
    "Vertigo": "MEDIUM",
    "Epilepsy": "HIGH",
    "Malaria": "HIGH",
    "Dengue": "HIGH",
    "Typhoid": "HIGH",
    "Chickenpox": "MEDIUM",
    "Measles": "MEDIUM",
    "Mumps": "MEDIUM",
    "Eczema": "LOW",
    "Psoriasis": "LOW",
    "Acne": "LOW",
    "Dermatitis": "LOW",
    "Fungal Infection": "LOW",
    "Arthritis": "MEDIUM",
    "Osteoporosis": "MEDIUM",
    "Muscle Strain": "LOW",
    "Diabetes": "HIGH",
    "Hyperthyroidism": "MEDIUM",
    "Hypothyroidism": "MEDIUM",
    "Depression": "MEDIUM",
    "Anxiety Disorder": "MEDIUM",
    "Insomnia": "LOW",
    "Urinary Tract Infection": "MEDIUM",
    "Kidney Stones": "HIGH",
    "Kidney Disease": "HIGH",
    "Conjunctivitis": "LOW",
    "Glaucoma": "HIGH",
    "Allergic Rhinitis": "LOW",
    "Food Allergy": "MEDIUM",
    "Dehydration": "MEDIUM",
    "Heat Stroke": "HIGH",
}


def generate_symptom_text(disease: str) -> str:
    """
    Generate a random combination of symptoms for a disease.
    Picks 3-6 symptoms randomly to simulate real patient input.
    """
    symptoms = DISEASE_SYMPTOMS[disease]
    # Randomly select 3-6 symptoms
    num_symptoms = random.randint(3, min(6, len(symptoms)))
    selected = random.sample(symptoms, num_symptoms)
    
    # Join with various separators to simulate natural input
    separators = [", ", " ", " and ", ", ", " "]
    separator = random.choice(separators)
    
    return separator.join(selected)


def generate_dataset(samples_per_disease: int = 20) -> pd.DataFrame:
    """
    Generate synthetic dataset for training.
    
    Args:
        samples_per_disease: Number of samples to generate per disease
        
    Returns:
        DataFrame with columns: symptoms, disease, risk_level
    """
    data = []
    
    for disease in DISEASE_SYMPTOMS.keys():
        for _ in range(samples_per_disease):
            symptoms = generate_symptom_text(disease)
            risk = DISEASE_RISK[disease]
            data.append({
                "symptoms": symptoms,
                "disease": disease,
                "risk_level": risk
            })
    
    # Shuffle the dataset
    df = pd.DataFrame(data)
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)
    
    return df


def main():
    """Main function to generate and save dataset."""
    print("=" * 50)
    print("Disease Prediction Dataset Generator")
    print("=" * 50)
    
    # Generate dataset with 20 samples per disease = 1000 total samples
    print("\n[1/3] Generating synthetic dataset...")
    df = generate_dataset(samples_per_disease=20)
    
    print(f"[2/3] Dataset created with {len(df)} samples")
    print(f"      - Number of diseases: {df['disease'].nunique()}")
    print(f"      - Risk level distribution:")
    print(df['risk_level'].value_counts().to_string())
    
    # Save to CSV
    output_path = os.path.join(os.path.dirname(__file__), "dataset.csv")
    df.to_csv(output_path, index=False)
    print(f"\n[3/3] Dataset saved to: {output_path}")
    
    # Show sample entries
    print("\n" + "=" * 50)
    print("Sample entries from dataset:")
    print("=" * 50)
    print(df.head(5).to_string())
    

if __name__ == "__main__":
    main()
