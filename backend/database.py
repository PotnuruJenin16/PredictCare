"""
Database Configuration and Models
=================================
SQLAlchemy ORM setup with SQLite database.
Contains User, Doctor, Prediction, and EHR models.
"""

from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# ============================================
# Database Configuration
# ============================================
DATABASE_URL = "sqlite:///./health_assistant.db"

engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False}  # Required for SQLite
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# ============================================
# User Model (Patient)
# ============================================
class User(Base):
    """User model for patient authentication."""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship to predictions
    predictions = relationship("Prediction", back_populates="user")
    # Relationship to EHR records
    ehr_records = relationship("EHRRecord", back_populates="user")
    # Relationship to prescriptions
    prescriptions = relationship("Prescription", back_populates="user")


# ============================================
# Doctor Model (Pre-seeded accounts)
# ============================================
class Doctor(Base):
    """Doctor model for doctor authentication. Doctors are pre-seeded, not self-registered."""
    __tablename__ = "doctors"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    specialization = Column(String(100), nullable=False)
    license_number = Column(String(50), nullable=True)  # Medical license
    hospital = Column(String(200), nullable=True)
    contact = Column(String(50), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    # Relationship to medical records uploaded by this doctor
    uploaded_records = relationship("EHRRecord", back_populates="uploaded_by_doctor")


# ============================================
# Prediction Model
# ============================================
class Prediction(Base):
    """Prediction model to store user's disease predictions."""
    __tablename__ = "predictions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    symptoms_text = Column(Text, nullable=False)
    predicted_disease = Column(String(200), nullable=False)
    confidence = Column(Float, nullable=False)
    risk_level = Column(String(20), nullable=False)
    precautions_text = Column(Text, nullable=True)  # Stored precautions summary
    advice_level = Column(String(20), nullable=True)  # low/medium/high urgency
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship to user
    user = relationship("User", back_populates="predictions")


# ============================================
# EHR Record Model (Electronic Health Record)
# ============================================
class EHRRecord(Base):
    """
    Electronic Health Record model.
    Stores user's medical documents and health records.
    
    Categories:
    - prescription: Medical prescriptions from doctors
    - lab_report: Laboratory test reports
    - scan_image: Scanned medical images (X-rays, etc.)
    - op_note: Outpatient notes or doctor notes
    - prediction: System-generated prediction records
    - doctor_prescription: Prescription uploaded by doctor
    - doctor_report: Report uploaded by doctor
    
    Records can be uploaded by:
    - Patient themselves (doctor_id = NULL)
    - A doctor on behalf of patient (doctor_id = doctor's ID)
    """
    __tablename__ = "ehr_records"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Record metadata
    title = Column(String(200), nullable=False)  # User-provided title
    category = Column(String(50), nullable=False)  # prescription/lab_report/scan_image/op_note/prediction
    description = Column(Text, nullable=True)  # Optional description or notes
    
    # File information (for uploaded documents)
    file_name = Column(String(255), nullable=True)  # Original file name
    file_type = Column(String(50), nullable=True)  # MIME type (application/pdf, image/jpeg, etc.)
    file_path = Column(String(500), nullable=True)  # Storage path (relative to uploads folder)
    file_size = Column(Integer, nullable=True)  # File size in bytes
    
    # For text-based records (OP notes, prediction summaries)
    text_content = Column(Text, nullable=True)
    
    # Link to prediction (if this is a prediction record)
    prediction_id = Column(Integer, ForeignKey("predictions.id"), nullable=True)
    
    # Doctor who uploaded this record (NULL if patient uploaded)
    doctor_id = Column(Integer, ForeignKey("doctors.id"), nullable=True)
    
    # Record metadata
    record_date = Column(DateTime, nullable=True)  # Date of the medical record (not upload date)
    created_at = Column(DateTime, default=datetime.utcnow)  # When uploaded/created
    is_archived = Column(Boolean, default=False)  # Soft delete
    
    # Relationships
    user = relationship("User", back_populates="ehr_records")
    prediction = relationship("Prediction")
    uploaded_by_doctor = relationship("Doctor", back_populates="uploaded_records")


# ============================================
# Prescription Model (Health Progress)
# ============================================
class Prescription(Base):
    """
    Prescription model for Health Progress tracking.
    Only one active prescription allowed per user.
    """
    __tablename__ = "prescriptions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    doctor_id = Column(Integer, ForeignKey("doctors.id"), nullable=False)
    
    notes = Column(Text, nullable=False)  # Prescription details
    total_days = Column(Integer, nullable=False)  # Total duration in days
    
    # Store completed days as JSON string (e.g., "[0, 1, 4]")
    # Using simple indices (0 to total_days-1)
    completed_days = Column(Text, default="[]")
    
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="prescriptions")
    doctor = relationship("Doctor")


# ============================================
# Database Initialization
# ============================================
def init_db():
    """Create all tables in the database."""
    Base.metadata.create_all(bind=engine)


def get_db():
    """
    Database session dependency.
    Use this in FastAPI endpoints to get a database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
