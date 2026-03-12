"""
Doctor Authentication Module
============================
JWT-based authentication for doctors.
Doctors are pre-seeded, not self-registered.
"""

from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session

from database import Doctor, get_db

# ============================================
# Configuration (same as patient auth)
# ============================================
SECRET_KEY = "your-secret-key-change-in-production-btechproject2024"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 hours

# ============================================
# Password Hashing
# ============================================
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ============================================
# JWT Bearer Scheme
# ============================================
security = HTTPBearer()


# ============================================
# Pydantic Schemas
# ============================================
class DoctorLogin(BaseModel):
    """Schema for doctor login."""
    email: EmailStr
    password: str


class DoctorResponse(BaseModel):
    """Schema for doctor response (without password)."""
    id: int
    name: str
    email: str
    specialization: str
    hospital: Optional[str] = None
    contact: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


class DoctorTokenResponse(BaseModel):
    """Schema for doctor JWT token response."""
    access_token: str
    token_type: str = "bearer"
    user_type: str = "doctor"
    doctor: DoctorResponse


# ============================================
# Helper Functions
# ============================================
def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    return pwd_context.verify(plain_password, hashed_password)


def create_doctor_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token for doctor.
    Includes 'type': 'doctor' to differentiate from patient tokens.
    """
    to_encode = data.copy()
    
    # Ensure sub is a string
    if "sub" in to_encode:
        to_encode["sub"] = str(to_encode["sub"])
    
    # Add doctor type marker
    to_encode["type"] = "doctor"
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_token(token: str) -> Optional[dict]:
    """Decode and validate a JWT token."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None


# ============================================
# Authentication Dependencies
# ============================================
def get_current_doctor(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> Doctor:
    """
    FastAPI dependency to get the current authenticated doctor.
    Verifies the token is a doctor token.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    token = credentials.credentials
    payload = decode_token(token)
    
    if payload is None:
        raise credentials_exception
    
    # Verify this is a doctor token
    if payload.get("type") != "doctor":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. Doctor credentials required."
        )
    
    doctor_id_str = payload.get("sub")
    if doctor_id_str is None:
        raise credentials_exception
    
    try:
        doctor_id = int(doctor_id_str)
    except (ValueError, TypeError):
        raise credentials_exception
    
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id, Doctor.is_active == True).first()
    if doctor is None:
        raise credentials_exception
    
    return doctor


# ============================================
# Doctor Operations
# ============================================
def get_doctor_by_email(db: Session, email: str) -> Optional[Doctor]:
    """Get a doctor by email address."""
    return db.query(Doctor).filter(Doctor.email == email).first()


def authenticate_doctor(db: Session, email: str, password: str) -> Optional[Doctor]:
    """
    Authenticate a doctor by email and password.
    Returns Doctor object if valid, None otherwise.
    """
    doctor = get_doctor_by_email(db, email)
    if not doctor:
        return None
    if not doctor.is_active:
        return None
    if not verify_password(password, doctor.password_hash):
        return None
    return doctor


def create_doctor(
    db: Session,
    name: str,
    email: str,
    password: str,
    specialization: str,
    hospital: str = None,
    contact: str = None,
    license_number: str = None
) -> Doctor:
    """
    Create a new doctor account (for seeding only).
    NOT exposed via API - doctors are pre-seeded.
    """
    hashed_password = hash_password(password)
    
    db_doctor = Doctor(
        name=name,
        email=email,
        password_hash=hashed_password,
        specialization=specialization,
        hospital=hospital,
        contact=contact,
        license_number=license_number
    )
    
    db.add(db_doctor)
    db.commit()
    db.refresh(db_doctor)
    
    return db_doctor
