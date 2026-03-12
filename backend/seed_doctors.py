"""
Doctor Account Seeding Script
=============================
Seeds pre-defined doctor accounts into the database.
Run this script to create doctor accounts.

Usage: python seed_doctors.py
"""

import sys
import os

# Add the backend directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import init_db, get_db, Doctor
from doctor_auth import hash_password

# ============================================
# Pre-defined Doctor Accounts
# ============================================
# These are the doctors who can log in to the system.
# Patients visit these doctors in person, then doctors
# upload reports/prescriptions to the patient's EHR.

SEED_DOCTORS = [
    {
        "name": "Dr. Anitha Kolukula",
        "email": "anitha.kolukula@predictcare.com",
        "password": "doctor123",  # Change in production!
        "specialization": "General Physician",
        "hospital": "Apollo Hospitals Health City, Visakhapatnam",
        "contact": "040-44442424",
        "license_number": "AP-MED-12345"
    },
    {
        "name": "Dr. K. Dileep Kumar",
        "email": "dileep.kumar@predictcare.com",
        "password": "doctor123",
        "specialization": "Diabetologist & Endocrinologist",
        "hospital": "Visakha Diabetes & Endocrine Centre",
        "contact": "0891-2555555",
        "license_number": "AP-MED-23456"
    },
    {
        "name": "Dr. P. Venu Madhavi",
        "email": "venu.madhavi@predictcare.com",
        "password": "doctor123",
        "specialization": "Cardiologist",
        "hospital": "CARE Hospitals, Visakhapatnam",
        "contact": "040-68106529",
        "license_number": "AP-MED-34567"
    },
    {
        "name": "Dr. Ramesh Varma",
        "email": "ramesh.varma@predictcare.com",
        "password": "doctor123",
        "specialization": "Dermatologist",
        "hospital": "Seven Hills Hospital, Visakhapatnam",
        "contact": "0891-2777777",
        "license_number": "AP-MED-45678"
    },
    {
        "name": "Dr. Srinivas Rao",
        "email": "srinivas.rao@predictcare.com",
        "password": "doctor123",
        "specialization": "Pulmonologist",
        "hospital": "Medicover Hospitals, Visakhapatnam",
        "contact": "0891-6666666",
        "license_number": "AP-MED-56789"
    }
]


def seed_doctors():
    """Seed doctor accounts into the database."""
    # Initialize database tables
    init_db()
    
    # Get database session
    db = next(get_db())
    
    print("\n" + "=" * 50)
    print("Seeding Doctor Accounts")
    print("=" * 50)
    
    created_count = 0
    skipped_count = 0
    
    for doctor_data in SEED_DOCTORS:
        # Check if doctor already exists
        existing = db.query(Doctor).filter(Doctor.email == doctor_data["email"]).first()
        
        if existing:
            print(f"⏭️  Skipped (exists): {doctor_data['name']} ({doctor_data['email']})")
            skipped_count += 1
            continue
        
        # Create new doctor
        doctor = Doctor(
            name=doctor_data["name"],
            email=doctor_data["email"],
            password_hash=hash_password(doctor_data["password"]),
            specialization=doctor_data["specialization"],
            hospital=doctor_data.get("hospital"),
            contact=doctor_data.get("contact"),
            license_number=doctor_data.get("license_number"),
            is_active=True
        )
        
        db.add(doctor)
        print(f"✅ Created: {doctor_data['name']} ({doctor_data['email']})")
        created_count += 1
    
    db.commit()
    
    print("\n" + "-" * 50)
    print(f"Summary: {created_count} created, {skipped_count} skipped")
    print("-" * 50)
    
    # List all doctors
    print("\n📋 All Doctor Accounts:")
    print("-" * 50)
    all_doctors = db.query(Doctor).all()
    for doc in all_doctors:
        print(f"  • {doc.name}")
        print(f"    Email: {doc.email}")
        print(f"    Specialization: {doc.specialization}")
        print(f"    Password: doctor123")  # For demo purposes
        print()
    
    print("=" * 50)
    print("Doctor seeding complete!")
    print("=" * 50 + "\n")
    
    db.close()


if __name__ == "__main__":
    seed_doctors()
