"""
Notification Module
===================
Web-based notification system for in-app alerts.
Stores notifications per user and provides API endpoints.

Notifications are triggered when:
- A new prediction is generated
- Risk level is HIGH
- New advice is available

This is a web-only system - no SMS, WhatsApp, or mobile push.
"""

from datetime import datetime
from typing import List, Optional
from enum import Enum


class NotificationType(str, Enum):
    """Types of notifications in the system."""
    PREDICTION = "prediction"       # New prediction made
    HIGH_RISK = "high_risk"         # High risk alert
    ADVICE = "advice"               # New advice available
    RECURRING = "recurring"         # Recurring condition detected
    WELCOME = "welcome"             # Welcome message for new users
    EHR_UPLOAD = "ehr_upload"       # New EHR record uploaded
    EHR_PREDICTION = "ehr_prediction"  # Prediction saved to EHR
    DOCTOR_RECORD = "doctor_record"    # Doctor uploaded a record
    PRESCRIPTION_ADDED = "prescription_added" # Doctor assigned a new prescription


# ============================================
# Notification Templates
# ============================================
# Pre-defined templates for different notification types

NOTIFICATION_TEMPLATES = {
    NotificationType.PREDICTION: {
        "icon": "🔍",
        "title": "Prediction Complete",
        "template": "Your symptom analysis is complete. Predicted condition: {disease}"
    },
    NotificationType.HIGH_RISK: {
        "icon": "⚠️",
        "title": "High Risk Alert",
        "template": "Your prediction indicates a HIGH risk level. Please consider consulting a doctor soon."
    },
    NotificationType.ADVICE: {
        "icon": "💡",
        "title": "Health Advice Available",
        "template": "Personalized health advice is ready for your recent prediction of {disease}."
    },
    NotificationType.RECURRING: {
        "icon": "📊",
        "title": "Recurring Condition",
        "template": "We noticed you've had similar symptoms ({disease}) multiple times. Consider a medical checkup."
    },
    NotificationType.WELCOME: {
        "icon": "👋",
        "title": "Welcome to Predict Care!",
        "template": "Welcome {name}! Start by entering your symptoms to get a health prediction."
    },
    NotificationType.EHR_UPLOAD: {
        "icon": "📁",
        "title": "EHR Record Added",
        "template": "Your {category} '{title}' has been added to your Electronic Health Records."
    },
    NotificationType.EHR_PREDICTION: {
        "icon": "📋",
        "title": "Prediction Saved to EHR",
        "template": "Your prediction for {disease} has been saved to your Electronic Health Records."
    },
    NotificationType.DOCTOR_RECORD: {
        "icon": "👨‍⚕️",
        "title": "New Medical Record from Doctor",
        "template": "Dr. {doctor_name} has added a new {category} to your health records: '{title}'"
    },
    NotificationType.PRESCRIPTION_ADDED: {
        "icon": "💊",
        "title": "New Prescription Assigned",
        "template": "Dr. {doctor_name} has assigned a new prescription. Check 'Health Progress' to track your adherence."
    }
}


# ============================================
# In-Memory Notification Store
# ============================================
# For academic demo, we store notifications in memory.
# In production, this would be in a database.

# Structure: {user_id: [notification1, notification2, ...]}
_notification_store: dict = {}
_notification_counter: int = 0


def _get_next_id() -> int:
    """Generate a unique notification ID."""
    global _notification_counter
    _notification_counter += 1
    return _notification_counter


# ============================================
# Notification Creation Functions
# ============================================

def create_notification(
    user_id: int,
    notification_type: NotificationType,
    context: dict = None
) -> dict:
    """
    Create a new notification for a user.
    
    Args:
        user_id: The user's ID
        notification_type: Type of notification
        context: Dictionary with template variables (e.g., disease name)
        
    Returns:
        The created notification dict
    """
    global _notification_store
    
    if context is None:
        context = {}
    
    template = NOTIFICATION_TEMPLATES[notification_type]
    
    # Format the message with context variables
    try:
        message = template["template"].format(**context)
    except KeyError:
        message = template["template"]
    
    notification = {
        "id": _get_next_id(),
        "user_id": user_id,
        "type": notification_type.value,
        "icon": template["icon"],
        "title": template["title"],
        "message": message,
        "read": False,
        "created_at": datetime.utcnow().isoformat() + "Z"
    }
    
    # Initialize user's notification list if not exists
    if user_id not in _notification_store:
        _notification_store[user_id] = []
    
    # Add to store (newest first)
    _notification_store[user_id].insert(0, notification)
    
    # Keep only last 50 notifications per user
    _notification_store[user_id] = _notification_store[user_id][:50]
    
    return notification


def create_prediction_notifications(
    user_id: int,
    disease: str,
    risk_level: str,
    is_recurring: bool = False
) -> List[dict]:
    """
    Create all relevant notifications for a new prediction.
    
    Args:
        user_id: The user's ID
        disease: Predicted disease name
        risk_level: Risk level (LOW/MEDIUM/HIGH)
        is_recurring: Whether this is a recurring condition
        
    Returns:
        List of created notifications
    """
    notifications = []
    
    # Always create prediction notification
    notif = create_notification(
        user_id,
        NotificationType.PREDICTION,
        {"disease": disease}
    )
    notifications.append(notif)
    
    # Create high risk notification if applicable
    if risk_level == "HIGH":
        notif = create_notification(
            user_id,
            NotificationType.HIGH_RISK,
            {"disease": disease}
        )
        notifications.append(notif)
    
    # Create advice notification
    notif = create_notification(
        user_id,
        NotificationType.ADVICE,
        {"disease": disease}
    )
    notifications.append(notif)
    
    # Create recurring notification if applicable
    if is_recurring:
        notif = create_notification(
            user_id,
            NotificationType.RECURRING,
            {"disease": disease}
        )
        notifications.append(notif)
    
    return notifications


def create_welcome_notification(user_id: int, user_name: str) -> dict:
    """
    Create a welcome notification for new users.
    
    Args:
        user_id: The new user's ID
        user_name: The user's name
        
    Returns:
        The welcome notification
    """
    return create_notification(
        user_id,
        NotificationType.WELCOME,
        {"name": user_name.split()[0]}  # First name only
    )


# ============================================
# Notification Retrieval Functions
# ============================================

def get_user_notifications(
    user_id: int,
    unread_only: bool = False,
    limit: int = 20
) -> List[dict]:
    """
    Get notifications for a user.
    
    Args:
        user_id: The user's ID
        unread_only: If True, return only unread notifications
        limit: Maximum number of notifications to return
        
    Returns:
        List of notifications (newest first)
    """
    global _notification_store
    
    notifications = _notification_store.get(user_id, [])
    
    if unread_only:
        notifications = [n for n in notifications if not n["read"]]
    
    return notifications[:limit]


def get_unread_count(user_id: int) -> int:
    """
    Get count of unread notifications for a user.
    
    Args:
        user_id: The user's ID
        
    Returns:
        Number of unread notifications
    """
    global _notification_store
    
    notifications = _notification_store.get(user_id, [])
    return sum(1 for n in notifications if not n["read"])


def mark_notification_read(user_id: int, notification_id: int) -> bool:
    """
    Mark a specific notification as read.
    
    Args:
        user_id: The user's ID
        notification_id: The notification ID
        
    Returns:
        True if notification was found and marked, False otherwise
    """
    global _notification_store
    
    notifications = _notification_store.get(user_id, [])
    
    for notif in notifications:
        if notif["id"] == notification_id:
            notif["read"] = True
            return True
    
    return False


def mark_all_read(user_id: int) -> int:
    """
    Mark all notifications as read for a user.
    
    Args:
        user_id: The user's ID
        
    Returns:
        Number of notifications marked as read
    """
    global _notification_store
    
    notifications = _notification_store.get(user_id, [])
    count = 0
    
    for notif in notifications:
        if not notif["read"]:
            notif["read"] = True
            count += 1
    
    return count


def delete_notification(user_id: int, notification_id: int) -> bool:
    """
    Delete a specific notification.
    
    Args:
        user_id: The user's ID
        notification_id: The notification ID
        
    Returns:
        True if notification was deleted, False otherwise
    """
    global _notification_store
    
    if user_id not in _notification_store:
        return False
    
    original_len = len(_notification_store[user_id])
    _notification_store[user_id] = [
        n for n in _notification_store[user_id]
        if n["id"] != notification_id
    ]
    
    return len(_notification_store[user_id]) < original_len


def clear_all_notifications(user_id: int) -> int:
    """
    Clear all notifications for a user.
    
    Args:
        user_id: The user's ID
        
    Returns:
        Number of notifications cleared
    """
    global _notification_store
    
    count = len(_notification_store.get(user_id, []))
    _notification_store[user_id] = []
    
    return count


# ============================================
# EHR Notification Functions
# ============================================

def create_ehr_upload_notification(
    user_id: int,
    title: str,
    category: str
) -> dict:
    """
    Create a notification for EHR record upload.
    
    Args:
        user_id: The user's ID
        title: Title of the uploaded record
        category: Category of the record
        
    Returns:
        The created notification
    """
    # Format category name for display
    category_names = {
        "prescription": "prescription",
        "lab_report": "lab report",
        "scan_image": "scan/image",
        "op_note": "OP note"
    }
    formatted_category = category_names.get(category, category)
    
    return create_notification(
        user_id,
        NotificationType.EHR_UPLOAD,
        {"title": title, "category": formatted_category}
    )


def create_ehr_prediction_notification(
    user_id: int,
    disease: str
) -> dict:
    """
    Create a notification when prediction is saved to EHR.
    
    Args:
        user_id: The user's ID
        disease: The predicted disease name
        
    Returns:
        The created notification
    """
    return create_notification(
        user_id,
        NotificationType.EHR_PREDICTION,
        {"disease": disease}
    )


def create_doctor_record_notification(
    user_id: int,
    doctor_name: str,
    category: str,
    title: str
) -> dict:
    """
    Create a notification when a doctor uploads a record for a patient.
    
    Args:
        user_id: The patient's user ID
        doctor_name: Name of the doctor who uploaded
        category: Category of the record (prescription, lab_report, etc.)
        title: Title of the uploaded record
        
    Returns:
        The created notification
    """
    # Format category name for display
    category_names = {
        "prescription": "prescription",
        "lab_report": "lab report",
        "scan_image": "scan/image",
        "op_note": "doctor's note",
        "doctor_prescription": "prescription",
        "doctor_report": "medical report"
    }
    formatted_category = category_names.get(category, category)
    
    return create_notification(
        user_id,
        NotificationType.DOCTOR_RECORD,
        {"doctor_name": doctor_name, "category": formatted_category, "title": title}
    )


    return create_notification(
        user_id,
        NotificationType.DOCTOR_RECORD,
        {"doctor_name": doctor_name, "category": formatted_category, "title": title}
    )


def create_prescription_notification(
    user_id: int,
    doctor_name: str
) -> dict:
    """
    Create a notification when a doctor assigns a new prescription.
    
    Args:
        user_id: The patient's user ID
        doctor_name: Name of the doctor who assigned prescription
        
    Returns:
        The created notification
    """
    return create_notification(
        user_id,
        NotificationType.PRESCRIPTION_ADDED,
        {"doctor_name": doctor_name}
    )
