"""
FastAPI Backend for Predict Care - Disease Prediction System
=============================================================
This is the main API server that:
1. Loads the trained ML model
2. Accepts symptom input via POST /predict
3. Returns disease prediction with confidence and risk level
4. Handles user authentication with JWT
5. Stores prediction history per user
6. Provides doctor recommendations based on disease
7. Manages in-app notifications

Run with: uvicorn main:app --reload --port 8000

Author: Predict Care
"""

import os
import re
from datetime import datetime
from typing import List, Optional
from fastapi import FastAPI, HTTPException, Depends, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session
import joblib
import numpy as np

# Import authentication and database modules
from database import init_db, get_db, User, Doctor, Prediction, EHRRecord, Prescription
from auth import (
    UserCreate, UserLogin, UserResponse, TokenResponse,
    create_user, authenticate_user, get_user_by_email,
    create_access_token, get_current_user
)
from doctor_auth import (
    DoctorLogin, DoctorResponse, DoctorTokenResponse,
    authenticate_doctor, get_current_doctor, create_doctor_access_token
)
from precautions import generate_precautions, format_precautions_for_storage
from doctors import get_recommended_doctors, get_all_doctors, get_doctor_by_id, format_doctor_recommendation
from notifications import (
    create_prediction_notifications, create_welcome_notification,
    get_user_notifications, get_unread_count,
    mark_notification_read, mark_all_read, delete_notification,
    create_ehr_upload_notification, create_ehr_prediction_notification,
    create_doctor_record_notification, create_prescription_notification
)
from ehr import (
    EHRCategory, CATEGORY_NAMES, CATEGORY_ICONS,
    validate_file_type, validate_file_size,
    get_user_upload_dir, generate_unique_filename, get_file_path,
    delete_file, format_ehr_record, create_prediction_ehr_record,
    get_ehr_statistics, ALLOWED_FILE_TYPES, MAX_FILE_SIZE
)

# ============================================
# Initialize FastAPI App
# ============================================
app = FastAPI(
    title="Predict Care API",
    description="ML-based disease prediction from symptoms with doctor recommendations",
    version="2.0.0"
)

# ============================================
# Initialize Database
# ============================================
init_db()

# ============================================
# CORS Middleware (allows frontend to connect)
# ============================================
# This is required for the frontend to make API calls
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # Allow all origins (for local dev)
    allow_credentials=True,
    allow_methods=["*"],        # Allow all HTTP methods
    allow_headers=["*"],        # Allow all headers
)

# ============================================
# Load ML Model and Vectorizer
# ============================================
MODEL_DIR = os.path.join(os.path.dirname(__file__), "model")

try:
    # Load the trained RandomForest model
    model = joblib.load(os.path.join(MODEL_DIR, "disease_classifier.joblib"))
    
    # Load the TF-IDF vectorizer (must be the same one used in training)
    vectorizer = joblib.load(os.path.join(MODEL_DIR, "tfidf_vectorizer.joblib"))
    
    # Load disease-risk mapping
    risk_mapping = joblib.load(os.path.join(MODEL_DIR, "risk_mapping.joblib"))
    
    print("[✓] Model, vectorizer, and risk mapping loaded successfully!")
    
except FileNotFoundError as e:
    print("[✗] Error: Model files not found!")
    print("    Please run: python dataset_generator.py && python train_model.py")
    model = None
    vectorizer = None
    risk_mapping = None


# ============================================
# Request/Response Models (Pydantic)
# ============================================

class SymptomInput(BaseModel):
    """
    Input schema for prediction request.
    Example: {"symptoms": "fever headache body aches"}
    """
    symptoms: str
    
    class Config:
        # Example for API documentation
        json_schema_extra = {
            "example": {
                "symptoms": "fever headache body aches fatigue"
            }
        }


class DoctorRecommendation(BaseModel):
    """Schema for doctor recommendation."""
    id: int
    name: str
    specialization: str
    location: str
    contact: str
    availability: str
    consultation_fee: str
    experience: Optional[str] = None


class PredictionResponse(BaseModel):
    """
    Output schema for prediction response.
    Contains predicted disease, risk level, confidence score, precautions, and doctor recommendations.
    """
    disease: str
    risk: str
    confidence: float
    message: str = ""
    # Precautionary advice fields
    advice_level: str = ""
    precautions: List[str] = []
    dos: List[str] = []
    donts: List[str] = []
    consult_when: List[str] = []
    disclaimer: str = ""
    # Doctor recommendations
    recommended_doctors: List[DoctorRecommendation] = []
    
    class Config:
        json_schema_extra = {
            "example": {
                "disease": "Influenza (Flu)",
                "risk": "MEDIUM",
                "confidence": 0.72,
                "message": "",
                "advice_level": "medium",
                "precautions": ["Rest and stay hydrated"],
                "dos": ["Take medications as prescribed"],
                "donts": ["Don't ignore symptoms"],
                "consult_when": ["If fever persists"],
                "disclaimer": "This is for educational purposes only.",
                "recommended_doctors": []
            }
        }


class PredictionHistoryItem(BaseModel):
    """Schema for prediction history response."""
    id: int
    symptoms_text: str
    predicted_disease: str
    confidence: float
    risk_level: str
    advice_level: Optional[str] = None
    precautions_text: Optional[str] = None
    created_at: str
    recommended_doctors: List[DoctorRecommendation] = []
    
    class Config:
        from_attributes = True


class NotificationItem(BaseModel):
    """Schema for notification response."""
    id: int
    type: str
    icon: str
    title: str
    message: str
    read: bool
    created_at: str


class NotificationResponse(BaseModel):
    """Schema for notifications list response."""
    notifications: List[NotificationItem]
    unread_count: int


# ============================================
# EHR Request/Response Models
# ============================================

class EHRRecordCreate(BaseModel):
    """Schema for creating a text-based EHR record (OP notes, etc.)."""
    title: str
    category: str
    description: Optional[str] = None
    text_content: Optional[str] = None
    record_date: Optional[str] = None  # ISO format date string


class EHRRecordResponse(BaseModel):
    """Schema for EHR record response."""
    id: int
    title: str
    category: str
    category_name: str
    category_icon: str
    description: Optional[str] = None
    file_name: Optional[str] = None
    file_type: Optional[str] = None
    file_type_name: Optional[str] = None
    file_size: Optional[int] = None
    file_size_formatted: Optional[str] = None
    has_file: bool
    text_content: Optional[str] = None
    prediction_id: Optional[int] = None
    record_date: Optional[str] = None
    created_at: str
    is_archived: bool
    # Doctor upload information
    uploaded_by_doctor: bool = False
    doctor_id: Optional[int] = None
    doctor_name: Optional[str] = None


class EHRListResponse(BaseModel):
    """Schema for EHR records list response."""
    records: List[EHRRecordResponse]
    total_count: int
    statistics: dict


# ============================================
# Doctor Dashboard Request/Response Models
# ============================================

class PatientLookupResponse(BaseModel):
    """Schema for patient lookup response."""
    found: bool
    patient_id: Optional[int] = None
    patient_name: Optional[str] = None
    patient_email: Optional[str] = None
    message: str


class DoctorUploadCreate(BaseModel):
    """Schema for doctor uploading text-based records for patient."""
    patient_email: str
    title: str
    category: str  # doctor_prescription, doctor_report, doctor_note
    description: Optional[str] = None
    text_content: Optional[str] = None
    diagnosis: Optional[str] = None
    prescription: Optional[str] = None
    notes: Optional[str] = None
    record_date: Optional[str] = None


class DoctorUploadResponse(BaseModel):
    """Schema for doctor upload response."""
    success: bool
    message: str
    record_id: Optional[int] = None
    patient_name: Optional[str] = None


# ============================================
# Prescription Request/Response Models
# ============================================

class PrescriptionCreate(BaseModel):
    """Schema for creating a prescription (Doctor side)."""
    patient_email: str
    notes: str
    total_days: int

class PrescriptionResponse(BaseModel):
    """Schema for prescription response."""
    id: int
    doctor_name: str
    notes: str
    total_days: int
    completed_days: List[int]
    progress_percentage: int
    is_active: bool
    created_at: str

class PrescriptionProgressUpdate(BaseModel):
    """Schema for updating prescription progress (Patient side)."""
    completed_days: List[int]


# ============================================
# Helper Functions
# ============================================

def calculate_risk_level(confidence: float, base_risk: str) -> tuple[str, str]:
    """
    Calculate risk level based on prediction confidence.
    
    Risk Logic:
    - confidence >= 0.7 → Use disease's base risk
    - confidence 0.4-0.7 → MEDIUM (uncertain prediction)
    - confidence < 0.4 → HIGH (very uncertain, consult doctor)
    
    Args:
        confidence: Model's prediction confidence (0-1)
        base_risk: The disease's inherent risk level from mapping
        
    Returns:
        Tuple of (risk_level, message)
    """
    if confidence >= 0.7:
        # High confidence - use disease's actual risk
        return base_risk, ""
    elif confidence >= 0.4:
        # Medium confidence - be cautious
        return "MEDIUM", "Prediction confidence is moderate. Consider consulting a doctor."
    else:
        # Low confidence - uncertain prediction
        return "HIGH", "⚠️ Low confidence prediction. Please consult a doctor for accurate diagnosis."


def preprocess_symptoms(symptoms: str) -> str:
    """
    Preprocess symptom input text.
    - Convert to lowercase
    - Remove extra whitespace
    """
    return symptoms.lower().strip()


def validate_probability_distribution(probabilities: np.ndarray) -> np.ndarray:
    """Validate that predict_proba returned a usable probability distribution."""
    probs = np.asarray(probabilities, dtype=float)

    if probs.ndim != 1 or probs.size == 0:
        raise ValueError("Model returned an empty probability distribution.")

    if not np.all(np.isfinite(probs)):
        raise ValueError("Model returned non-finite probability values.")

    if np.any(probs < -1e-6) or np.any(probs > 1.0 + 1e-6):
        raise ValueError(
            "Model returned invalid probabilities. This usually means the saved model "
            "was loaded with an incompatible scikit-learn version. Reinstall the "
            "backend dependencies from requirements.txt and restart the server."
        )

    probs = np.clip(probs, 0.0, 1.0)
    total = float(probs.sum())

    if total <= 0:
        raise ValueError("Model returned zero total probability.")

    if not np.isclose(total, 1.0, atol=1e-3):
        probs = probs / total

    return probs


def calculate_prediction_confidence(
    probabilities: np.ndarray,
    processed_symptoms: str,
    predicted_index: int
) -> float:
    """
    Build a user-facing confidence score that is stricter than raw predict_proba.

    RandomForest probabilities on small synthetic multi-class datasets can be poorly
    calibrated. This score combines top-class strength, separation from the runner-up,
    vocabulary coverage, and symptom detail length to avoid reporting unrealistic 100% confidence.
    """
    probs = validate_probability_distribution(probabilities)

    sorted_probs = np.sort(probs)[::-1]
    top_probability = float(probs[predicted_index])
    second_probability = float(sorted_probs[1]) if len(sorted_probs) > 1 else 0.0
    baseline_probability = 1.0 / len(probs)

    relative_top = max(
        0.0,
        (top_probability - baseline_probability) / max(1e-9, 1.0 - baseline_probability)
    )
    margin_ratio = max(
        0.0,
        (top_probability - second_probability) / max(top_probability, 1e-9)
    )

    input_tokens = re.findall(r"[a-z]+", processed_symptoms)
    unique_tokens = set(input_tokens)
    if not unique_tokens:
        return 0.0

    known_token_count = sum(1 for token in unique_tokens if token in vectorizer.vocabulary_)
    coverage = known_token_count / len(unique_tokens)
    detail_factor = min(1.0, len(unique_tokens) / 4.0)

    confidence = (
        np.sqrt(relative_top)
        * (0.6 + 0.4 * margin_ratio)
        * coverage
        * detail_factor
    )

    return float(np.clip(confidence, 0.0, 0.95))


# ============================================
# API Endpoints
# ============================================

@app.get("/")
def root():
    """
    Root endpoint - API health check.
    Returns basic info about the API.
    """
    return {
        "status": "running",
        "message": "Disease Prediction API is active",
        "endpoints": {
            "predict": "POST /predict",
            "health": "GET /health"
        }
    }


@app.get("/health")
def health_check():
    """
    Health check endpoint.
    Verifies if the model is loaded properly.
    """
    if model is None or vectorizer is None:
        return {
            "status": "error",
            "model_loaded": False,
            "message": "Model not loaded. Run training script first."
        }
    return {
        "status": "healthy",
        "model_loaded": True,
        "message": "System is ready for predictions"
    }


# ============================================
# Authentication Endpoints
# ============================================

@app.post("/register", response_model=TokenResponse)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user.
    Returns JWT token on successful registration.
    Also creates a welcome notification.
    """
    # Check if user already exists
    existing_user = get_user_by_email(db, user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
    
    # Create new user
    user = create_user(db, user_data)
    
    # Create welcome notification
    create_welcome_notification(user.id, user.name)
    
    # Generate JWT token
    access_token = create_access_token(data={"sub": user.id})
    
    return TokenResponse(
        access_token=access_token,
        user=UserResponse.model_validate(user)
    )


@app.post("/login", response_model=TokenResponse)
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """
    Login with email and password.
    Returns JWT token on successful login.
    """
    user = authenticate_user(db, credentials.email, credentials.password)
    
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )
    
    # Generate JWT token
    access_token = create_access_token(data={"sub": user.id})
    
    return TokenResponse(
        access_token=access_token,
        user=UserResponse.model_validate(user)
    )


@app.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    """Get current user's profile."""
    return UserResponse.model_validate(current_user)


@app.post("/predict", response_model=PredictionResponse)
def predict_disease(
    input_data: SymptomInput,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Main prediction endpoint (requires authentication).
    
    Takes symptom text and returns:
    - Predicted disease name
    - Risk level (LOW/MEDIUM/HIGH)
    - Confidence score (0-1)
    - Optional warning message
    
    Also saves the prediction to user's history.
    
    Example Request:
        POST /predict
        Authorization: Bearer <token>
        {"symptoms": "fever headache body aches chills"}
    
    Example Response:
        {
            "disease": "Influenza (Flu)",
            "risk": "MEDIUM",
            "confidence": 0.72,
            "message": ""
        }
    """
    # Check if model is loaded
    if model is None or vectorizer is None:
        raise HTTPException(
            status_code=503,
            detail="Model not loaded. Please run the training script first."
        )
    
    # Validate input
    symptoms = input_data.symptoms.strip()
    if not symptoms:
        raise HTTPException(
            status_code=400,
            detail="Symptoms cannot be empty. Please enter your symptoms."
        )
    
    if len(symptoms) < 3:
        raise HTTPException(
            status_code=400,
            detail="Please enter more descriptive symptoms."
        )
    
    try:
        # ========================================
        # Step 1: Preprocess input
        # ========================================
        processed_symptoms = preprocess_symptoms(symptoms)
        
        # ========================================
        # Step 2: Convert to TF-IDF features
        # ========================================
        # Use the same vectorizer from training
        symptoms_tfidf = vectorizer.transform([processed_symptoms])
        
        # ========================================
        # Step 3: Get prediction and probabilities
        # ========================================
        # predict_proba() returns probability for each class
        probabilities = validate_probability_distribution(model.predict_proba(symptoms_tfidf)[0])
        predicted_index = int(np.argmax(probabilities))
        predicted_disease = str(model.classes_[predicted_index])
        confidence = calculate_prediction_confidence(
            probabilities=probabilities,
            processed_symptoms=processed_symptoms,
            predicted_index=predicted_index
        )
        
        # ========================================
        # Step 4: Calculate risk level
        # ========================================
        # Get base risk from mapping, default to MEDIUM if not found
        base_risk = risk_mapping.get(predicted_disease, "MEDIUM")
        
        # Adjust risk based on confidence
        final_risk, message = calculate_risk_level(confidence, base_risk)
        
        # ========================================
        # Step 5: Get user's previous predictions for context
        # ========================================
        previous_predictions = db.query(Prediction).filter(
            Prediction.user_id == current_user.id
        ).order_by(Prediction.created_at.desc()).limit(10).all()
        
        # Check for recurring condition
        is_recurring = sum(
            1 for p in previous_predictions 
            if p.predicted_disease == predicted_disease
        ) >= 2
        
        # ========================================
        # Step 6: Generate personalized precautions
        # ========================================
        precautions_data = generate_precautions(
            disease=predicted_disease,
            confidence=round(confidence, 2),
            risk_level=final_risk,
            user_name=current_user.name.split()[0],  # First name only
            previous_predictions=previous_predictions
        )
        
        # ========================================
        # Step 7: Get doctor recommendations
        # ========================================
        doctors = get_recommended_doctors(
            disease=predicted_disease,
            risk_level=final_risk,
            limit=3
        )
        doctor_recommendations = [
            DoctorRecommendation(
                id=d["id"],
                name=d["name"],
                specialization=d["specialization"],
                location=d["location"],
                contact=d["contact"],
                availability=d["availability"],
                consultation_fee=d["consultation_fee"],
                experience=d.get("experience")
            )
            for d in doctors
        ]
        
        # ========================================
        # Step 8: Save prediction to database
        # ========================================
        db_prediction = Prediction(
            user_id=current_user.id,
            symptoms_text=symptoms,
            predicted_disease=predicted_disease,
            confidence=round(confidence, 2),
            risk_level=final_risk,
            precautions_text=format_precautions_for_storage(precautions_data),
            advice_level=precautions_data["advice_level"]
        )
        db.add(db_prediction)
        db.commit()
        db.refresh(db_prediction)  # Get the prediction ID
        
        # ========================================
        # Step 9: Create notifications
        # ========================================
        create_prediction_notifications(
            user_id=current_user.id,
            disease=predicted_disease,
            risk_level=final_risk,
            is_recurring=is_recurring
        )
        
        # ========================================
        # Step 10: Auto-save prediction to EHR
        # ========================================
        ehr_data = create_prediction_ehr_record(
            user_id=current_user.id,
            prediction_id=db_prediction.id,
            disease=predicted_disease,
            risk_level=final_risk,
            confidence=round(confidence, 2),
            precautions_text=format_precautions_for_storage(precautions_data),
            symptoms=symptoms
        )
        
        ehr_record = EHRRecord(**ehr_data)
        db.add(ehr_record)
        db.commit()
        
        # Create EHR notification
        create_ehr_prediction_notification(
            user_id=current_user.id,
            disease=predicted_disease
        )
        
        # ========================================
        # Step 11: Return response with everything
        # ========================================
        return PredictionResponse(
            disease=predicted_disease,
            risk=final_risk,
            confidence=round(confidence, 2),
            message=message,
            advice_level=precautions_data["advice_level"],
            precautions=precautions_data["precautions"],
            dos=precautions_data["dos"],
            donts=precautions_data["donts"],
            consult_when=precautions_data["consult_when"],
            disclaimer=precautions_data["disclaimer"],
            recommended_doctors=doctor_recommendations
        )
        
    except Exception as e:
        # Log error for debugging
        print(f"Prediction error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(e)}"
        )


# ============================================
# Prediction History Endpoint
# ============================================

@app.get("/predictions/me", response_model=List[PredictionHistoryItem])
def get_my_predictions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get current user's prediction history.
    Returns list of past predictions sorted by date (newest first).
    Includes doctor recommendations regenerated for each prediction.
    """
    predictions = db.query(Prediction).filter(
        Prediction.user_id == current_user.id
    ).order_by(Prediction.created_at.desc()).all()
    
    result = []
    for p in predictions:
        # Regenerate doctor recommendations based on stored disease and risk
        doctors = get_recommended_doctors(
            disease=p.predicted_disease,
            risk_level=p.risk_level,
            limit=3
        )
        doctor_recommendations = [
            DoctorRecommendation(
                id=d["id"],
                name=d["name"],
                specialization=d["specialization"],
                location=d["location"],
                contact=d["contact"],
                availability=d["availability"],
                consultation_fee=d["consultation_fee"],
                experience=d.get("experience")
            )
            for d in doctors
        ]
        
        result.append(PredictionHistoryItem(
            id=p.id,
            symptoms_text=p.symptoms_text,
            predicted_disease=p.predicted_disease,
            confidence=p.confidence,
            risk_level=p.risk_level,
            advice_level=p.advice_level,
            precautions_text=p.precautions_text,
            created_at=p.created_at.isoformat() + "Z",
            recommended_doctors=doctor_recommendations
        ))
    
    return result


# ============================================
# Notification Endpoints
# ============================================

@app.get("/notifications", response_model=NotificationResponse)
def get_notifications(
    unread_only: bool = False,
    current_user: User = Depends(get_current_user)
):
    """
    Get current user's notifications.
    Returns list of notifications with unread count.
    
    Query params:
        unread_only: If true, return only unread notifications
    """
    notifications = get_user_notifications(
        user_id=current_user.id,
        unread_only=unread_only,
        limit=50
    )
    
    return NotificationResponse(
        notifications=[
            NotificationItem(
                id=n["id"],
                type=n["type"],
                icon=n["icon"],
                title=n["title"],
                message=n["message"],
                read=n["read"],
                created_at=n["created_at"]
            )
            for n in notifications
        ],
        unread_count=get_unread_count(current_user.id)
    )


@app.post("/notifications/{notification_id}/read")
def mark_notification_as_read(
    notification_id: int,
    current_user: User = Depends(get_current_user)
):
    """Mark a specific notification as read."""
    success = mark_notification_read(current_user.id, notification_id)
    if not success:
        raise HTTPException(status_code=404, detail="Notification not found")
    return {"status": "success", "message": "Notification marked as read"}


@app.post("/notifications/read-all")
def mark_all_notifications_read(
    current_user: User = Depends(get_current_user)
):
    """Mark all notifications as read for the current user."""
    count = mark_all_read(current_user.id)
    return {"status": "success", "marked_read": count}


@app.delete("/notifications/{notification_id}")
def delete_notification_endpoint(
    notification_id: int,
    current_user: User = Depends(get_current_user)
):
    """Delete a specific notification."""
    success = delete_notification(current_user.id, notification_id)
    if not success:
        raise HTTPException(status_code=404, detail="Notification not found")
    return {"status": "success", "message": "Notification deleted"}


# ============================================
# Doctor Recommendation Endpoints (Public)
# ============================================

@app.get("/doctors", response_model=List[DoctorRecommendation])
def list_all_doctors():
    """
    Get list of all available doctors.
    Public endpoint - no authentication required.
    """
    doctors = get_all_doctors()
    return [
        DoctorRecommendation(
            id=d["id"],
            name=d["name"],
            specialization=d["specialization"],
            location=d["location"],
            contact=d["contact"],
            availability=d["availability"],
            consultation_fee=d["consultation_fee"],
            experience=d.get("experience")
        )
        for d in doctors
    ]


@app.get("/doctors/{doctor_id}", response_model=DoctorRecommendation)
def get_doctor(doctor_id: int):
    """
    Get a specific doctor by ID.
    Public endpoint - no authentication required.
    """
    doctor = get_doctor_by_id(doctor_id)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    
    return DoctorRecommendation(
        id=doctor["id"],
        name=doctor["name"],
        specialization=doctor["specialization"],
        location=doctor["location"],
        contact=doctor["contact"],
        availability=doctor["availability"],
        consultation_fee=doctor["consultation_fee"],
        experience=doctor.get("experience")
    )


# ============================================
# Prescription Endpoints
# ============================================

@app.post("/doctor/prescriptions", response_model=PrescriptionResponse)
def create_prescription(
    prescription_data: PrescriptionCreate,
    current_doctor: Doctor = Depends(get_current_doctor),
    db: Session = Depends(get_db)
):
    """
    Doctor creates a new prescription for a patient.
    Deactivates any existing active prescription.
    """
    # 1. Find patient
    patient = get_user_by_email(db, prescription_data.patient_email)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
        
    # 2. Deactivate existing active prescriptions
    existing_active = db.query(Prescription).filter(
        Prescription.user_id == patient.id,
        Prescription.is_active == True
    ).all()
    
    for p in existing_active:
        p.is_active = False
    
    # 3. Create new prescription
    import json
    new_prescription = Prescription(
        user_id=patient.id,
        doctor_id=current_doctor.id,
        notes=prescription_data.notes,
        total_days=prescription_data.total_days,
        completed_days="[]",  # Empty list initially
        is_active=True
    )
    
    db.add(new_prescription)
    db.commit()
    db.refresh(new_prescription)
    
    # 3.5. Auto-create EHR Record
    # ==========================
    ehr_record = EHRRecord(
        user_id=patient.id,
        title=f"Prescription - {datetime.utcnow().strftime('%d %b %Y')}",
        category="doctor_prescription",
        description=f"Prescribed by Dr. {current_doctor.name}. Duration: {prescription_data.total_days} days.",
        text_content=prescription_data.notes,
        doctor_id=current_doctor.id,
        record_date=datetime.utcnow(),
        created_at=datetime.utcnow(),
        is_archived=False
    )
    db.add(ehr_record)
    db.commit()
    
    # 4. Create notification for patient
    create_prescription_notification(patient.id, current_doctor.name)
    
    return PrescriptionResponse(
        id=new_prescription.id,
        doctor_name=current_doctor.name,
        notes=new_prescription.notes,
        total_days=new_prescription.total_days,
        completed_days=[],
        progress_percentage=0,
        is_active=True,
        created_at=new_prescription.created_at.isoformat() + "Z"
    )

@app.get("/prescriptions/active", response_model=PrescriptionResponse)
def get_active_prescription(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get the current active prescription for the logged-in patient.
    """
    prescription = db.query(Prescription).filter(
        Prescription.user_id == current_user.id,
        Prescription.is_active == True
    ).order_by(Prescription.created_at.desc()).first()
    
    if not prescription:
        raise HTTPException(status_code=404, detail="No active prescription found")
        
    import json
    completed_days_list = json.loads(prescription.completed_days)
    
    # Calculate progress
    progress = 0
    if prescription.total_days > 0:
        progress = int((len(completed_days_list) / prescription.total_days) * 100)
    
    return PrescriptionResponse(
        id=prescription.id,
        doctor_name=prescription.doctor.name,
        notes=prescription.notes,
        total_days=prescription.total_days,
        completed_days=completed_days_list,
        progress_percentage=progress,
        is_active=True,
        created_at=prescription.created_at.isoformat() + "Z"
    )

@app.post("/prescriptions/{id}/progress")
def update_prescription_progress(
    id: int,
    progress_data: PrescriptionProgressUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update the ticked days for a prescription.
    """
    prescription = db.query(Prescription).filter(
        Prescription.id == id,
        Prescription.user_id == current_user.id
    ).first()
    
    if not prescription:
        raise HTTPException(status_code=404, detail="Prescription not found")
        
    if not prescription.is_active:
        raise HTTPException(status_code=400, detail="Cannot update inactive prescription")
        
    # Serialize completed days to JSON
    import json
    # Ensure specific validation if needed (e.g., indices < total_days)
    valid_days = [d for d in progress_data.completed_days if 0 <= d < prescription.total_days]
    
    prescription.completed_days = json.dumps(valid_days)
    db.commit()
    
    return {"status": "success", "message": "Progress updated"}



# ============================================
# Doctor Portal Endpoints
# ============================================

@app.post("/doctor/login", response_model=DoctorTokenResponse)
def doctor_login(credentials: DoctorLogin, db: Session = Depends(get_db)):
    """
    Login endpoint for doctors.
    Doctors use pre-seeded credentials (not self-registered).
    """
    doctor = authenticate_doctor(db, credentials.email, credentials.password)
    
    if not doctor:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )
    
    # Generate JWT token with doctor type
    access_token = create_doctor_access_token(data={"sub": doctor.id})
    
    return DoctorTokenResponse(
        access_token=access_token,
        doctor=DoctorResponse.model_validate(doctor)
    )


@app.get("/doctor/me", response_model=DoctorResponse)
def get_doctor_profile(current_doctor: Doctor = Depends(get_current_doctor)):
    """Get current doctor's profile."""
    return DoctorResponse.model_validate(current_doctor)


@app.get("/doctor/lookup/{patient_email}", response_model=PatientLookupResponse)
def lookup_patient(
    patient_email: str,
    current_doctor: Doctor = Depends(get_current_doctor),
    db: Session = Depends(get_db)
):
    """
    Look up a patient by their email (user ID).
    Doctor must manually enter the patient's email - no browsing allowed.
    """
    patient = db.query(User).filter(User.email == patient_email).first()
    
    if not patient:
        return PatientLookupResponse(
            found=False,
            message=f"No patient found with email: {patient_email}"
        )
    
    return PatientLookupResponse(
        found=True,
        patient_id=patient.id,
        patient_name=patient.name,
        patient_email=patient.email,
        message=f"Patient found: {patient.name}"
    )


@app.post("/doctor/upload/text", response_model=DoctorUploadResponse)
def doctor_upload_text_record(
    record_data: DoctorUploadCreate,
    current_doctor: Doctor = Depends(get_current_doctor),
    db: Session = Depends(get_db)
):
    """
    Doctor uploads a text-based record (prescription, notes) for a patient.
    Patient is identified by their email.
    """
    # Find patient
    patient = db.query(User).filter(User.email == record_data.patient_email).first()
    
    if not patient:
        raise HTTPException(
            status_code=404,
            detail=f"Patient not found with email: {record_data.patient_email}"
        )
    
    # Validate category
    valid_categories = ["doctor_prescription", "doctor_report", "doctor_note", "prescription", "lab_report", "op_note"]
    if record_data.category not in valid_categories:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid category. Valid: {', '.join(valid_categories)}"
        )
    
    # Build text content from doctor's input
    text_parts = []
    
    if record_data.diagnosis:
        text_parts.append(f"DIAGNOSIS:\n{record_data.diagnosis}")
    
    if record_data.prescription:
        text_parts.append(f"PRESCRIPTION:\n{record_data.prescription}")
    
    if record_data.notes:
        text_parts.append(f"DOCTOR'S NOTES:\n{record_data.notes}")
    
    if record_data.text_content:
        text_parts.append(record_data.text_content)
    
    text_content = "\n\n".join(text_parts) if text_parts else None
    
    # Add doctor signature
    if text_content:
        text_content += f"\n\n---\nRecorded by: {current_doctor.name}\nSpecialization: {current_doctor.specialization}\nDate: {datetime.utcnow().strftime('%Y-%m-%d %H:%M')} UTC"
    
    # Parse record date if provided
    record_date = None
    if record_data.record_date:
        try:
            record_date = datetime.fromisoformat(record_data.record_date.replace('Z', '+00:00'))
        except ValueError:
            record_date = datetime.utcnow()
    else:
        record_date = datetime.utcnow()
    
    # Create EHR record
    ehr_record = EHRRecord(
        user_id=patient.id,
        title=record_data.title,
        category=record_data.category,
        description=record_data.description,
        text_content=text_content,
        record_date=record_date,
        doctor_id=current_doctor.id
    )
    
    db.add(ehr_record)
    db.commit()
    db.refresh(ehr_record)
    
    # Create notification for patient
    create_doctor_record_notification(
        user_id=patient.id,
        doctor_name=current_doctor.name,
        category=record_data.category,
        title=record_data.title
    )
    
    return DoctorUploadResponse(
        success=True,
        message=f"Record successfully added to {patient.name}'s EHR",
        record_id=ehr_record.id,
        patient_name=patient.name
    )


@app.post("/doctor/upload/file", response_model=DoctorUploadResponse)
async def doctor_upload_file_record(
    patient_email: str = Form(...),
    file: UploadFile = File(...),
    title: str = Form(...),
    category: str = Form(...),
    description: Optional[str] = Form(None),
    record_date: Optional[str] = Form(None),
    current_doctor: Doctor = Depends(get_current_doctor),
    db: Session = Depends(get_db)
):
    """
    Doctor uploads a file (report, scan, prescription image) for a patient.
    """
    # Find patient
    patient = db.query(User).filter(User.email == patient_email).first()
    
    if not patient:
        raise HTTPException(
            status_code=404,
            detail=f"Patient not found with email: {patient_email}"
        )
    
    # Validate category
    valid_categories = ["doctor_prescription", "doctor_report", "lab_report", "scan_image"]
    if category not in valid_categories:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid category for file upload. Valid: {', '.join(valid_categories)}"
        )
    
    # Validate file type
    is_valid, msg = validate_file_type(file.content_type)
    if not is_valid:
        raise HTTPException(status_code=400, detail=msg)
    
    # Read file content
    content = await file.read()
    
    # Validate file size
    is_valid, msg = validate_file_size(len(content))
    if not is_valid:
        raise HTTPException(status_code=400, detail=msg)
    
    # Generate unique filename and save to patient's folder
    unique_filename = generate_unique_filename(file.filename, file.content_type)
    file_path = get_file_path(patient.id, unique_filename)
    
    with open(file_path, "wb") as f:
        f.write(content)
    
    # Parse record date
    parsed_record_date = None
    if record_date:
        try:
            parsed_record_date = datetime.fromisoformat(record_date.replace('Z', '+00:00'))
        except ValueError:
            parsed_record_date = datetime.utcnow()
    else:
        parsed_record_date = datetime.utcnow()
    
    # Build description with doctor info
    full_description = description or ""
    full_description += f"\n\nUploaded by: {current_doctor.name} ({current_doctor.specialization})"
    
    # Create EHR record
    ehr_record = EHRRecord(
        user_id=patient.id,
        title=title,
        category=category,
        description=full_description.strip(),
        file_name=file.filename,
        file_type=file.content_type,
        file_path=unique_filename,
        file_size=len(content),
        record_date=parsed_record_date,
        doctor_id=current_doctor.id
    )
    
    db.add(ehr_record)
    db.commit()
    db.refresh(ehr_record)
    
    # Create notification for patient
    create_doctor_record_notification(
        user_id=patient.id,
        doctor_name=current_doctor.name,
        category=category,
        title=title
    )
    
    return DoctorUploadResponse(
        success=True,
        message=f"File successfully uploaded to {patient.name}'s EHR",
        record_id=ehr_record.id,
        patient_name=patient.name
    )


# ============================================
# Update Register to Create Welcome Notification
# ============================================
# Note: We modified the register endpoint above to create welcome notification


# ============================================
# EHR (Electronic Health Records) Endpoints
# ============================================

@app.get("/ehr", response_model=EHRListResponse)
def get_ehr_records(
    category: Optional[str] = None,
    include_archived: bool = False,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get user's EHR records.
    
    Query params:
        category: Filter by category (prescription/lab_report/scan_image/op_note/prediction)
        include_archived: Include archived records (default: false)
    """
    query = db.query(EHRRecord).filter(EHRRecord.user_id == current_user.id)
    
    if not include_archived:
        query = query.filter(EHRRecord.is_archived == False)
    
    if category:
        query = query.filter(EHRRecord.category == category)
    
    records = query.order_by(EHRRecord.created_at.desc()).all()
    
    # Format records with doctor names
    formatted_records = []
    for r in records:
        doctor_name = None
        if r.doctor_id:
            doctor = db.query(Doctor).filter(Doctor.id == r.doctor_id).first()
            if doctor:
                doctor_name = doctor.name
        formatted_records.append(format_ehr_record(r, doctor_name))
    
    return EHRListResponse(
        records=formatted_records,
        total_count=len(records),
        statistics=get_ehr_statistics(records)
    )


@app.get("/ehr/{record_id}", response_model=EHRRecordResponse)
def get_ehr_record(
    record_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific EHR record by ID."""
    record = db.query(EHRRecord).filter(
        EHRRecord.id == record_id,
        EHRRecord.user_id == current_user.id
    ).first()
    
    if not record:
        raise HTTPException(status_code=404, detail="EHR record not found")
    
    # Get doctor name if uploaded by doctor
    doctor_name = None
    if record.doctor_id:
        doctor = db.query(Doctor).filter(Doctor.id == record.doctor_id).first()
        if doctor:
            doctor_name = doctor.name
    
    return format_ehr_record(record, doctor_name)


@app.post("/ehr/text", response_model=EHRRecordResponse)
def create_text_ehr_record(
    record_data: EHRRecordCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a text-based EHR record (OP notes, doctor notes, etc.).
    For file uploads, use POST /ehr/upload instead.
    """
    # Validate category
    valid_categories = [c.value for c in EHRCategory]
    if record_data.category not in valid_categories:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid category. Valid categories: {', '.join(valid_categories)}"
        )
    
    # Parse record date if provided
    record_date = None
    if record_data.record_date:
        try:
            record_date = datetime.fromisoformat(record_data.record_date.replace('Z', '+00:00'))
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid date format. Use ISO format.")
    
    # Create EHR record
    ehr_record = EHRRecord(
        user_id=current_user.id,
        title=record_data.title,
        category=record_data.category,
        description=record_data.description,
        text_content=record_data.text_content,
        record_date=record_date
    )
    
    db.add(ehr_record)
    db.commit()
    db.refresh(ehr_record)
    
    # Create notification
    create_ehr_upload_notification(
        user_id=current_user.id,
        title=record_data.title,
        category=record_data.category
    )
    
    return format_ehr_record(ehr_record)


@app.post("/ehr/upload", response_model=EHRRecordResponse)
async def upload_ehr_file(
    file: UploadFile = File(...),
    title: str = Form(...),
    category: str = Form(...),
    description: Optional[str] = Form(None),
    record_date: Optional[str] = Form(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Upload a file to EHR (prescriptions, lab reports, scans).
    
    Supported file types: PDF, Word documents, images (JPEG, PNG, GIF, WebP)
    Maximum file size: 10 MB
    """
    # Validate category
    valid_categories = [c.value for c in EHRCategory if c != EHRCategory.PREDICTION]
    if category not in valid_categories:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid category for upload. Valid: {', '.join(valid_categories)}"
        )
    
    # Validate file type
    is_valid, msg = validate_file_type(file.content_type)
    if not is_valid:
        raise HTTPException(status_code=400, detail=msg)
    
    # Read file content
    content = await file.read()
    
    # Validate file size
    is_valid, msg = validate_file_size(len(content))
    if not is_valid:
        raise HTTPException(status_code=400, detail=msg)
    
    # Generate unique filename and save
    unique_filename = generate_unique_filename(file.filename, file.content_type)
    file_path = get_file_path(current_user.id, unique_filename)
    
    with open(file_path, "wb") as f:
        f.write(content)
    
    # Parse record date if provided
    parsed_record_date = None
    if record_date:
        try:
            parsed_record_date = datetime.fromisoformat(record_date.replace('Z', '+00:00'))
        except ValueError:
            pass  # Ignore invalid dates for file uploads
    
    # Create EHR record
    ehr_record = EHRRecord(
        user_id=current_user.id,
        title=title,
        category=category,
        description=description,
        file_name=file.filename,
        file_type=file.content_type,
        file_path=unique_filename,  # Store only filename, not full path
        file_size=len(content),
        record_date=parsed_record_date
    )
    
    db.add(ehr_record)
    db.commit()
    db.refresh(ehr_record)
    
    # Create notification
    create_ehr_upload_notification(
        user_id=current_user.id,
        title=title,
        category=category
    )
    
    return format_ehr_record(ehr_record)


@app.get("/ehr/{record_id}/download")
def download_ehr_file(
    record_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Download an EHR record file."""
    record = db.query(EHRRecord).filter(
        EHRRecord.id == record_id,
        EHRRecord.user_id == current_user.id
    ).first()
    
    if not record:
        raise HTTPException(status_code=404, detail="EHR record not found")
    
    if not record.file_path:
        raise HTTPException(status_code=400, detail="This record has no file attached")
    
    file_path = get_file_path(current_user.id, record.file_path)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found on server")
    
    return FileResponse(
        path=file_path,
        filename=record.file_name or record.file_path,
        media_type=record.file_type
    )


@app.put("/ehr/{record_id}", response_model=EHRRecordResponse)
def update_ehr_record(
    record_id: int,
    record_data: EHRRecordCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update an EHR record (title, description, notes)."""
    record = db.query(EHRRecord).filter(
        EHRRecord.id == record_id,
        EHRRecord.user_id == current_user.id
    ).first()
    
    if not record:
        raise HTTPException(status_code=404, detail="EHR record not found")
    
    # Update fields
    record.title = record_data.title
    record.description = record_data.description
    
    if record_data.text_content is not None:
        record.text_content = record_data.text_content
    
    if record_data.record_date:
        try:
            record.record_date = datetime.fromisoformat(record_data.record_date.replace('Z', '+00:00'))
        except ValueError:
            pass
    
    db.commit()
    db.refresh(record)
    
    return format_ehr_record(record)


@app.delete("/ehr/{record_id}")
def delete_ehr_record(
    record_id: int,
    permanent: bool = False,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete an EHR record.
    
    By default, records are archived (soft delete).
    Use permanent=true to permanently delete.
    """
    record = db.query(EHRRecord).filter(
        EHRRecord.id == record_id,
        EHRRecord.user_id == current_user.id
    ).first()
    
    if not record:
        raise HTTPException(status_code=404, detail="EHR record not found")
    
    if permanent:
        # Delete file if exists
        if record.file_path:
            delete_file(current_user.id, record.file_path)
        
        db.delete(record)
        db.commit()
        return {"status": "success", "message": "EHR record permanently deleted"}
    else:
        # Soft delete (archive)
        record.is_archived = True
        db.commit()
        return {"status": "success", "message": "EHR record archived"}


@app.post("/ehr/{record_id}/restore")
def restore_ehr_record(
    record_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Restore an archived EHR record."""
    record = db.query(EHRRecord).filter(
        EHRRecord.id == record_id,
        EHRRecord.user_id == current_user.id
    ).first()
    
    if not record:
        raise HTTPException(status_code=404, detail="EHR record not found")
    
    record.is_archived = False
    db.commit()
    
    return {"status": "success", "message": "EHR record restored"}


@app.get("/ehr/categories/list")
def get_ehr_categories():
    """Get list of available EHR categories."""
    return [
        {
            "value": cat.value,
            "name": CATEGORY_NAMES.get(cat, cat.value),
            "icon": CATEGORY_ICONS.get(cat, "📄")
        }
        for cat in EHRCategory
    ]


# ============================================
# Run Server (for development)
# ============================================
if __name__ == "__main__":
    import uvicorn
    
    print("\n" + "=" * 50)
    print("Starting Predict Care API Server")
    print("=" * 50)
    print("\nServer running at: http://localhost:8000")
    print("API Docs at: http://localhost:8000/docs")
    print("\nPress Ctrl+C to stop the server")
    print("=" * 50 + "\n")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True  # Auto-reload on code changes
    )
