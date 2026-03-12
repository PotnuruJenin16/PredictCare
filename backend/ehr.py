"""
Electronic Health Records (EHR) Module
======================================
Manages user's medical documents and health records.

EHR in This Project:
- A digital repository of user's health-related records
- Includes uploaded documents (prescriptions, reports, scans)
- Includes text-based records (OP notes, doctor notes)
- Includes system-generated prediction records
- Each record belongs to exactly one authenticated user

Security Approach (Academic Demo):
- User authentication via JWT tokens
- Records are isolated per user (no cross-user access)
- Files stored locally in uploads folder
- No encryption (demo purposes) - in production, use encryption at rest

Note: This is an academic demonstration, NOT a certified EHR system.
"""

import os
import uuid
import shutil
from datetime import datetime
from typing import List, Optional, Tuple
from enum import Enum

# ============================================
# Constants
# ============================================

# Upload directory (relative to backend folder)
UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "uploads")

# Maximum file size (10 MB for demo)
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB in bytes

# Allowed file types for upload
ALLOWED_FILE_TYPES = {
    # Documents
    "application/pdf": ".pdf",
    "application/msword": ".doc",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": ".docx",
    # Images
    "image/jpeg": ".jpg",
    "image/png": ".png",
    "image/gif": ".gif",
    "image/webp": ".webp",
    # Text
    "text/plain": ".txt",
}

# Reverse mapping for display
FILE_TYPE_NAMES = {
    "application/pdf": "PDF Document",
    "application/msword": "Word Document",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": "Word Document",
    "image/jpeg": "JPEG Image",
    "image/png": "PNG Image",
    "image/gif": "GIF Image",
    "image/webp": "WebP Image",
    "text/plain": "Text File",
}


class EHRCategory(str, Enum):
    """Categories of EHR records."""
    PRESCRIPTION = "prescription"
    LAB_REPORT = "lab_report"
    SCAN_IMAGE = "scan_image"
    OP_NOTE = "op_note"
    PREDICTION = "prediction"
    # Doctor-uploaded categories
    DOCTOR_PRESCRIPTION = "doctor_prescription"
    DOCTOR_REPORT = "doctor_report"
    DOCTOR_NOTE = "doctor_note"


# Human-readable category names
CATEGORY_NAMES = {
    EHRCategory.PRESCRIPTION: "Prescription",
    EHRCategory.LAB_REPORT: "Lab Report",
    EHRCategory.SCAN_IMAGE: "Scan / X-Ray",
    EHRCategory.OP_NOTE: "OP Note / Doctor Note",
    EHRCategory.PREDICTION: "Prediction Record",
    EHRCategory.DOCTOR_PRESCRIPTION: "Doctor's Prescription",
    EHRCategory.DOCTOR_REPORT: "Doctor's Report",
    EHRCategory.DOCTOR_NOTE: "Doctor's Notes",
}

# Category icons for UI
CATEGORY_ICONS = {
    EHRCategory.PRESCRIPTION: "💊",
    EHRCategory.LAB_REPORT: "🔬",
    EHRCategory.SCAN_IMAGE: "🩻",
    EHRCategory.OP_NOTE: "📝",
    EHRCategory.PREDICTION: "🔍",
    EHRCategory.DOCTOR_PRESCRIPTION: "👨‍⚕️💊",
    EHRCategory.DOCTOR_REPORT: "👨‍⚕️📋",
    EHRCategory.DOCTOR_NOTE: "👨‍⚕️📝",
}


# ============================================
# Utility Functions
# ============================================

def ensure_upload_dir():
    """Ensure the upload directory exists."""
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)


def get_user_upload_dir(user_id: int) -> str:
    """
    Get the upload directory for a specific user.
    Creates a separate folder per user for data isolation.
    """
    user_dir = os.path.join(UPLOAD_DIR, f"user_{user_id}")
    if not os.path.exists(user_dir):
        os.makedirs(user_dir)
    return user_dir


def generate_unique_filename(original_name: str, file_type: str) -> str:
    """
    Generate a unique filename to prevent conflicts.
    Format: {uuid}_{timestamp}_{sanitized_original_name}
    """
    # Get file extension
    ext = ALLOWED_FILE_TYPES.get(file_type, ".bin")
    
    # Sanitize original filename (remove path, keep only name)
    safe_name = os.path.basename(original_name)
    # Remove extension if present
    safe_name = os.path.splitext(safe_name)[0]
    # Remove any unsafe characters
    safe_name = "".join(c for c in safe_name if c.isalnum() or c in "._- ")[:50]
    
    # Generate unique filename
    unique_id = uuid.uuid4().hex[:8]
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    
    return f"{unique_id}_{timestamp}_{safe_name}{ext}"


def validate_file_type(content_type: str) -> Tuple[bool, str]:
    """
    Validate if the file type is allowed.
    Returns (is_valid, message).
    """
    if content_type not in ALLOWED_FILE_TYPES:
        allowed = ", ".join(FILE_TYPE_NAMES.values())
        return False, f"File type not allowed. Allowed types: {allowed}"
    return True, "Valid"


def validate_file_size(size: int) -> Tuple[bool, str]:
    """
    Validate if the file size is within limits.
    Returns (is_valid, message).
    """
    if size > MAX_FILE_SIZE:
        max_mb = MAX_FILE_SIZE / (1024 * 1024)
        return False, f"File too large. Maximum size: {max_mb:.0f} MB"
    return True, "Valid"


def get_file_path(user_id: int, filename: str) -> str:
    """Get the full file path for a user's file."""
    return os.path.join(get_user_upload_dir(user_id), filename)


def delete_file(user_id: int, filename: str) -> bool:
    """
    Delete a file from storage.
    Returns True if deleted, False if file didn't exist.
    """
    file_path = get_file_path(user_id, filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        return True
    return False


def format_file_size(size_bytes: int) -> str:
    """Format file size in human-readable format."""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    else:
        return f"{size_bytes / (1024 * 1024):.1f} MB"


# ============================================
# EHR Record Formatting
# ============================================

def format_ehr_record(record, doctor_name: str = None) -> dict:
    """
    Format an EHR record for API response.
    
    Args:
        record: EHRRecord database object
        doctor_name: Name of the doctor who uploaded (if applicable)
        
    Returns:
        Dictionary with formatted record data
    """
    # Determine if this was uploaded by a doctor
    uploaded_by_doctor = record.doctor_id is not None
    
    return {
        "id": record.id,
        "title": record.title,
        "category": record.category,
        "category_name": CATEGORY_NAMES.get(record.category, record.category),
        "category_icon": CATEGORY_ICONS.get(record.category, "📄"),
        "description": record.description,
        "file_name": record.file_name,
        "file_type": record.file_type,
        "file_type_name": FILE_TYPE_NAMES.get(record.file_type, "Unknown"),
        "file_size": record.file_size,
        "file_size_formatted": format_file_size(record.file_size) if record.file_size else None,
        "has_file": record.file_path is not None,
        "text_content": record.text_content,
        "prediction_id": record.prediction_id,
        "record_date": record.record_date.isoformat() if record.record_date else None,
        "created_at": record.created_at.isoformat() + "Z",
        "is_archived": record.is_archived,
        # Doctor upload information
        "uploaded_by_doctor": uploaded_by_doctor,
        "doctor_id": record.doctor_id,
        "doctor_name": doctor_name
    }


def create_prediction_ehr_record(
    user_id: int,
    prediction_id: int,
    disease: str,
    risk_level: str,
    confidence: float,
    precautions_text: str,
    symptoms: str
) -> dict:
    """
    Create EHR record data for a new prediction.
    This is called after a prediction to auto-add to EHR.
    
    Args:
        user_id: User's ID
        prediction_id: Prediction ID
        disease: Predicted disease
        risk_level: Risk level (LOW/MEDIUM/HIGH)
        confidence: Confidence score
        precautions_text: Generated precautions
        symptoms: User's symptoms text
        
    Returns:
        Dictionary with EHR record data (to be saved)
    """
    # Build text content summary
    text_content = f"""PREDICTION RECORD
================
Date: {datetime.utcnow().strftime("%Y-%m-%d %H:%M")} UTC

SYMPTOMS REPORTED:
{symptoms}

PREDICTION RESULTS:
- Predicted Condition: {disease}
- Risk Level: {risk_level}
- Confidence: {int(confidence * 100)}%

PRECAUTIONARY ADVICE:
{precautions_text if precautions_text else 'No specific advice generated.'}

---
⚠️ DISCLAIMER: This is an automated prediction from the Predict Care system.
This is NOT a medical diagnosis. Please consult a healthcare professional
for proper medical advice.
"""
    
    return {
        "user_id": user_id,
        "title": f"Prediction: {disease}",
        "category": EHRCategory.PREDICTION.value,
        "description": f"System-generated prediction record. Risk: {risk_level}, Confidence: {int(confidence * 100)}%",
        "text_content": text_content,
        "prediction_id": prediction_id,
        "record_date": datetime.utcnow()
    }


# ============================================
# Statistics and Summary
# ============================================

def get_ehr_statistics(records: List) -> dict:
    """
    Generate statistics from user's EHR records.
    
    Args:
        records: List of EHRRecord objects
        
    Returns:
        Dictionary with statistics
    """
    stats = {
        "total_records": len(records),
        "by_category": {},
        "total_file_size": 0,
        "file_count": 0,
        "text_record_count": 0,
        "oldest_record": None,
        "newest_record": None
    }
    
    for record in records:
        # Count by category
        cat = record.category
        if cat not in stats["by_category"]:
            stats["by_category"][cat] = 0
        stats["by_category"][cat] += 1
        
        # File statistics
        if record.file_path:
            stats["file_count"] += 1
            if record.file_size:
                stats["total_file_size"] += record.file_size
        
        if record.text_content:
            stats["text_record_count"] += 1
        
        # Date range
        if stats["oldest_record"] is None or record.created_at < stats["oldest_record"]:
            stats["oldest_record"] = record.created_at
        if stats["newest_record"] is None or record.created_at > stats["newest_record"]:
            stats["newest_record"] = record.created_at
    
    # Format for response
    stats["total_file_size_formatted"] = format_file_size(stats["total_file_size"])
    if stats["oldest_record"]:
        stats["oldest_record"] = stats["oldest_record"].isoformat() + "Z"
    if stats["newest_record"]:
        stats["newest_record"] = stats["newest_record"].isoformat() + "Z"
    
    return stats


# ============================================
# Initialization
# ============================================

# Ensure upload directory exists on module load
ensure_upload_dir()
