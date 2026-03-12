"""
Doctor Recommendation Module
============================
Rule-based doctor recommendation system.
Matches predicted diseases with specialist doctors.

All doctors are based in Visakhapatnam, Andhra Pradesh.
This is a predefined list for academic demo purposes.
NO external API calls - all data is hardcoded.
"""

from typing import List, Optional

# ============================================
# Doctor Database (Visakhapatnam Doctors)
# ============================================
# Each doctor has: name, specialization, domain expertise, hospital, city, contact, experience

DOCTORS_DATABASE = [
    # ==========================================
    # General Physicians (Influenza / Fever / Viral infections)
    # ==========================================
    {
        "id": 1,
        "name": "Dr. Anitha Kolukula",
        "specialization": "General Physician",
        "expertise": ["Influenza (Flu)", "Fever", "Viral Infections", "Common Cold"],
        "location": "Apollo Hospitals Health City, Visakhapatnam",
        "contact": "Not Available",
        "availability": "Mon-Sat: 9AM-5PM",
        "consultation_fee": "₹500",
        "experience": "15 years"
    },
    {
        "id": 2,
        "name": "Dr. G. V. Hari Krishna",
        "specialization": "General Physician",
        "expertise": ["Influenza (Flu)", "Fever", "Viral Infections", "Common Cold"],
        "location": "Prasad Clinic, Visakhapatnam",
        "contact": "Not Available",
        "availability": "Mon-Sat: 9AM-6PM",
        "consultation_fee": "₹400",
        "experience": "16 years"
    },
    {
        "id": 3,
        "name": "Dr. U H P Kshipani",
        "specialization": "General Physician",
        "expertise": ["Influenza (Flu)", "Fever", "Viral Infections", "Common Cold"],
        "location": "Apollo Clinic Seethammapeta, Visakhapatnam",
        "contact": "040-44442424",
        "availability": "Mon-Sat: 10AM-6PM",
        "consultation_fee": "₹500",
        "experience": "10 years"
    },
    {
        "id": 4,
        "name": "Dr. G Sarveswara Rao",
        "specialization": "General Physician",
        "expertise": ["Influenza (Flu)", "Fever", "Viral Infections", "Common Cold"],
        "location": "Apollo Clinic, Visakhapatnam",
        "contact": "Not Available",
        "availability": "Mon-Sat: 9AM-5PM",
        "consultation_fee": "₹500",
        "experience": "15 years"
    },
    {
        "id": 5,
        "name": "Dr. Ravi Kumar Gurugubelli",
        "specialization": "General Physician",
        "expertise": ["Influenza (Flu)", "Fever", "Viral Infections", "Common Cold"],
        "location": "Medicover Hospitals, Visakhapatnam",
        "contact": "Not Available",
        "availability": "Mon-Sat: 9AM-6PM",
        "consultation_fee": "₹600",
        "experience": "23 years"
    },
    {
        "id": 6,
        "name": "Dr. K Vamsi Krishna",
        "specialization": "General Physician",
        "expertise": ["Influenza (Flu)", "Fever", "Viral Infections", "Common Cold"],
        "location": "Seven Hills Hospital, Visakhapatnam",
        "contact": "Not Available",
        "availability": "Mon-Sat: 10AM-5PM",
        "consultation_fee": "₹450",
        "experience": "11 years"
    },
    {
        "id": 7,
        "name": "Dr. Thriveni Reddy",
        "specialization": "General Physician",
        "expertise": ["Influenza (Flu)", "Fever", "Viral Infections", "Common Cold"],
        "location": "Private Clinic, Visakhapatnam",
        "contact": "Not Available",
        "availability": "Mon-Sat: 9AM-6PM",
        "consultation_fee": "₹400",
        "experience": "22 years"
    },
    {
        "id": 8,
        "name": "Dr. C H Madhuri",
        "specialization": "General Physician",
        "expertise": ["Influenza (Flu)", "Fever", "Viral Infections", "Common Cold"],
        "location": "Private Clinic, Visakhapatnam",
        "contact": "Not Available",
        "availability": "Mon-Sat: 9AM-5PM",
        "consultation_fee": "₹350",
        "experience": "30 years"
    },
    {
        "id": 9,
        "name": "Dr. Sai Sekhar P",
        "specialization": "General Physician",
        "expertise": ["Influenza (Flu)", "Fever", "Viral Infections", "Common Cold"],
        "location": "Private Clinic Muralinagar, Visakhapatnam",
        "contact": "Not Available",
        "availability": "Mon-Sat: 10AM-6PM",
        "consultation_fee": "₹350",
        "experience": "9 years"
    },

    # ==========================================
    # Endocrinologists / Diabetologists (Diabetes)
    # ==========================================
    {
        "id": 10,
        "name": "Dr. A. Mythili",
        "specialization": "Endocrinologist",
        "expertise": ["Diabetes Symptoms", "Diabetes", "Hormonal Issues", "Thyroid"],
        "location": "Neuro and Endocrine Clinic, Visakhapatnam",
        "contact": "Not Available",
        "availability": "Mon-Sat: 10AM-5PM",
        "consultation_fee": "₹600",
        "experience": "20 years"
    },
    {
        "id": 11,
        "name": "Dr. K. Dileep Kumar",
        "specialization": "Diabetologist",
        "expertise": ["Diabetes Symptoms", "Diabetes", "Metabolic Disorders"],
        "location": "Visakha Diabetes & Endocrine Centre, Visakhapatnam",
        "contact": "Not Available",
        "availability": "Mon-Sat: 9AM-6PM",
        "consultation_fee": "₹700",
        "experience": "44 years"
    },
    {
        "id": 12,
        "name": "Dr. P Venu Madhavi",
        "specialization": "Endocrinologist",
        "expertise": ["Diabetes Symptoms", "Diabetes", "Hormonal Issues", "Thyroid"],
        "location": "CARE Hospitals, Visakhapatnam",
        "contact": "040-68106529",
        "availability": "Mon-Sat: 10AM-5PM",
        "consultation_fee": "₹650",
        "experience": "12 years"
    },
    {
        "id": 13,
        "name": "Dr. Ramya Varada",
        "specialization": "Endocrinologist",
        "expertise": ["Diabetes Symptoms", "Diabetes", "Hormonal Issues", "Thyroid"],
        "location": "Apollo Health City, Visakhapatnam",
        "contact": "Not Available",
        "availability": "Mon-Sat: 9AM-5PM",
        "consultation_fee": "₹700",
        "experience": "18 years"
    },
    {
        "id": 14,
        "name": "Dr. K.A.V. Subrahmanyam",
        "specialization": "Endocrinologist",
        "expertise": ["Diabetes Symptoms", "Diabetes", "Hormonal Issues", "Thyroid"],
        "location": "Visakha Diabetes & Endocrine Centre, Visakhapatnam",
        "contact": "Not Available",
        "availability": "Mon-Sat: 9AM-6PM",
        "consultation_fee": "₹800",
        "experience": "39 years"
    },
    {
        "id": 15,
        "name": "Dr. Jayanthy Ramesh",
        "specialization": "Endocrinologist",
        "expertise": ["Diabetes Symptoms", "Diabetes", "Hormonal Issues", "Thyroid"],
        "location": "Sai's Institute of Endocrinology, Visakhapatnam",
        "contact": "Not Available",
        "availability": "Mon-Sat: 10AM-5PM",
        "consultation_fee": "₹650",
        "experience": "27 years"
    },
    {
        "id": 16,
        "name": "Dr. B. Vivekananda",
        "specialization": "Endocrinologist",
        "expertise": ["Diabetes Symptoms", "Diabetes", "Hormonal Issues", "Thyroid"],
        "location": "Visakha Diabetes & Endocrine Centre, Visakhapatnam",
        "contact": "Not Available",
        "availability": "Mon-Sat: 9AM-5PM",
        "consultation_fee": "₹600",
        "experience": "16 years"
    },
    {
        "id": 17,
        "name": "Dr. Deepthi Florence",
        "specialization": "Endocrinologist",
        "expertise": ["Diabetes Symptoms", "Diabetes", "Hormonal Issues", "Thyroid"],
        "location": "Queen's NRI Hospital, Visakhapatnam",
        "contact": "Not Available",
        "availability": "Mon-Sat: 10AM-6PM",
        "consultation_fee": "₹550",
        "experience": "8 years"
    },

    # ==========================================
    # Cardiologists (Heart-related diseases)
    # ==========================================
    {
        "id": 18,
        "name": "Dr. Nanda Kishore Panigrahi",
        "specialization": "Cardiologist",
        "expertise": ["Hypertension Symptoms", "Heart Health", "Blood Pressure", "Chest Pain"],
        "location": "Apollo Health City, Visakhapatnam",
        "contact": "Not Available",
        "availability": "Mon-Sat: 9AM-5PM",
        "consultation_fee": "₹800",
        "experience": "25 years"
    },
    {
        "id": 19,
        "name": "Dr. Ganesh Kasinadhuni",
        "specialization": "Interventional Cardiologist",
        "expertise": ["Hypertension Symptoms", "Heart Health", "Blood Pressure", "Chest Pain", "Cardiac Interventions"],
        "location": "KIMS Hospital, Visakhapatnam",
        "contact": "8872804321",
        "availability": "Mon-Sat: 10AM-5PM",
        "consultation_fee": "₹750",
        "experience": "10 years"
    },
    {
        "id": 20,
        "name": "Dr. A Suresh",
        "specialization": "Cardiologist",
        "expertise": ["Hypertension Symptoms", "Heart Health", "Blood Pressure", "Chest Pain"],
        "location": "Medicover Hospitals, Visakhapatnam",
        "contact": "Not Available",
        "availability": "Mon-Sat: 9AM-6PM",
        "consultation_fee": "₹800",
        "experience": "25 years"
    },
    {
        "id": 21,
        "name": "Dr. P Siva Satya Subramanyam",
        "specialization": "Cardiologist",
        "expertise": ["Hypertension Symptoms", "Heart Health", "Blood Pressure", "Chest Pain"],
        "location": "Private Clinic, Visakhapatnam",
        "contact": "Not Available",
        "availability": "Mon-Sat: 10AM-5PM",
        "consultation_fee": "₹700",
        "experience": "19 years"
    },
    {
        "id": 22,
        "name": "Dr. Narasimha Raju Challapalli",
        "specialization": "Cardiologist",
        "expertise": ["Hypertension Symptoms", "Heart Health", "Blood Pressure", "Chest Pain"],
        "location": "Private Clinic, Visakhapatnam",
        "contact": "Not Available",
        "availability": "Mon-Sat: 9AM-5PM",
        "consultation_fee": "₹700",
        "experience": "20 years"
    },
    {
        "id": 23,
        "name": "Dr. K P Ranganayakulu",
        "specialization": "Cardiologist",
        "expertise": ["Hypertension Symptoms", "Heart Health", "Blood Pressure", "Chest Pain"],
        "location": "Private Clinic, Visakhapatnam",
        "contact": "Not Available",
        "availability": "Mon-Sat: 9AM-6PM",
        "consultation_fee": "₹750",
        "experience": "22 years"
    },
    {
        "id": 24,
        "name": "Dr. Hemanta Kumar Behera",
        "specialization": "Cardiologist",
        "expertise": ["Hypertension Symptoms", "Heart Health", "Blood Pressure", "Chest Pain"],
        "location": "Medicover Hospitals, Visakhapatnam",
        "contact": "Not Available",
        "availability": "Mon-Sat: 9AM-5PM",
        "consultation_fee": "₹850",
        "experience": "30 years"
    },
    {
        "id": 25,
        "name": "Dr. Dibya Kumar Baruah",
        "specialization": "Cardiologist",
        "expertise": ["Hypertension Symptoms", "Heart Health", "Blood Pressure", "Chest Pain"],
        "location": "Apollo Hospitals, Visakhapatnam",
        "contact": "Not Available",
        "availability": "Mon-Sat: 10AM-5PM",
        "consultation_fee": "₹800",
        "experience": "18 years"
    },
    {
        "id": 26,
        "name": "Dr. Shashanka Chunduri",
        "specialization": "Cardiologist",
        "expertise": ["Hypertension Symptoms", "Heart Health", "Blood Pressure", "Chest Pain"],
        "location": "Apollo Hospitals, Visakhapatnam",
        "contact": "Not Available",
        "availability": "Mon-Sat: 9AM-5PM",
        "consultation_fee": "₹700",
        "experience": "12 years"
    },

    # ==========================================
    # Pulmonologists (Respiratory diseases - Asthma / Bronchitis)
    # ==========================================
    {
        "id": 27,
        "name": "Dr. Sateesh Chandra Alavala",
        "specialization": "Pulmonologist",
        "expertise": ["Asthma Attack", "Respiratory Issues", "Bronchitis", "Breathing Problems"],
        "location": "Vizag Chest Institute, Visakhapatnam",
        "contact": "9519595789",
        "availability": "Mon-Sat: 10AM-5PM",
        "consultation_fee": "₹600",
        "experience": "12 years"
    },
    {
        "id": 28,
        "name": "Dr. K. Venkateswara Rao",
        "specialization": "Pulmonologist",
        "expertise": ["Asthma Attack", "Respiratory Issues", "Bronchitis", "Breathing Problems"],
        "location": "Apollo Health City, Visakhapatnam",
        "contact": "Not Available",
        "availability": "Mon-Sat: 9AM-5PM",
        "consultation_fee": "₹750",
        "experience": "30 years"
    },
    {
        "id": 29,
        "name": "Dr. Sushmitha",
        "specialization": "Pulmonologist",
        "expertise": ["Asthma Attack", "Respiratory Issues", "Bronchitis", "Breathing Problems"],
        "location": "Vizag Chest Institute, Visakhapatnam",
        "contact": "Not Available",
        "availability": "Mon-Sat: 10AM-6PM",
        "consultation_fee": "₹500",
        "experience": "8 years"
    },
    {
        "id": 30,
        "name": "Dr. M. Phanindranath Reddy",
        "specialization": "Pulmonologist",
        "expertise": ["Asthma Attack", "Respiratory Issues", "Bronchitis", "Breathing Problems"],
        "location": "Pinnacle Hospitals, Visakhapatnam",
        "contact": "Not Available",
        "availability": "Mon-Sat: 9AM-5PM",
        "consultation_fee": "₹600",
        "experience": "13 years"
    },
    {
        "id": 31,
        "name": "Dr. Konathala Sureendra",
        "specialization": "Pulmonologist",
        "expertise": ["Asthma Attack", "Respiratory Issues", "Bronchitis", "Breathing Problems"],
        "location": "KIMS Hospitals, Visakhapatnam",
        "contact": "Not Available",
        "availability": "Mon-Sat: 10AM-5PM",
        "consultation_fee": "₹650",
        "experience": "15 years"
    },
    {
        "id": 32,
        "name": "Dr. Venkatesh Vulli",
        "specialization": "Pulmonologist",
        "expertise": ["Asthma Attack", "Respiratory Issues", "Bronchitis", "Breathing Problems"],
        "location": "Apoorva Hospital, Visakhapatnam",
        "contact": "Not Available",
        "availability": "Mon-Sat: 9AM-6PM",
        "consultation_fee": "₹450",
        "experience": "5 years"
    },
    {
        "id": 33,
        "name": "Dr. Gayatri Devi",
        "specialization": "Pulmonologist",
        "expertise": ["Asthma Attack", "Respiratory Issues", "Bronchitis", "Breathing Problems"],
        "location": "Apollo Clinic, Visakhapatnam",
        "contact": "Not Available",
        "availability": "Mon-Sat: 10AM-5PM",
        "consultation_fee": "₹550",
        "experience": "12 years"
    },
    {
        "id": 34,
        "name": "Dr. Sunil Kumar R",
        "specialization": "Pulmonologist",
        "expertise": ["Asthma Attack", "Respiratory Issues", "Bronchitis", "Breathing Problems"],
        "location": "Private Clinic, Visakhapatnam",
        "contact": "Not Available",
        "availability": "Mon-Sat: 9AM-5PM",
        "consultation_fee": "₹600",
        "experience": "25 years"
    },

    # ==========================================
    # Neurologists (Neurological disorders)
    # ==========================================
    {
        "id": 35,
        "name": "Dr. G. Kishore Babu",
        "specialization": "Neurologist",
        "expertise": ["Migraine", "Headaches", "Neurological Disorders", "Anxiety Disorder"],
        "location": "CARE Hospitals Ramnagar, Visakhapatnam",
        "contact": "040-68106529",
        "availability": "Mon-Sat: 10AM-5PM",
        "consultation_fee": "₹700",
        "experience": "20 years"
    },
    {
        "id": 36,
        "name": "Dr. K. Venkateswarlu",
        "specialization": "Neurologist",
        "expertise": ["Migraine", "Headaches", "Neurological Disorders", "Anxiety Disorder"],
        "location": "Medicover Hospitals, Visakhapatnam",
        "contact": "Not Available",
        "availability": "Mon-Sat: 9AM-5PM",
        "consultation_fee": "₹850",
        "experience": "35 years"
    },
    {
        "id": 37,
        "name": "Dr. Sailesh Modi",
        "specialization": "Neurologist",
        "expertise": ["Migraine", "Headaches", "Neurological Disorders", "Anxiety Disorder"],
        "location": "KIMS Hospitals, Visakhapatnam",
        "contact": "Not Available",
        "availability": "Mon-Sat: 10AM-6PM",
        "consultation_fee": "₹650",
        "experience": "12 years"
    },
    {
        "id": 38,
        "name": "Dr. Rajesh Venkat Indala",
        "specialization": "Neurologist",
        "expertise": ["Migraine", "Headaches", "Neurological Disorders", "Anxiety Disorder"],
        "location": "Apollo Health City, Visakhapatnam",
        "contact": "Not Available",
        "availability": "Mon-Sat: 9AM-5PM",
        "consultation_fee": "₹700",
        "experience": "10 years"
    },
    {
        "id": 39,
        "name": "Dr. T Suresh",
        "specialization": "Neurologist",
        "expertise": ["Migraine", "Headaches", "Neurological Disorders", "Anxiety Disorder"],
        "location": "Medicover Hospitals, Visakhapatnam",
        "contact": "Not Available",
        "availability": "Mon-Sat: 10AM-5PM",
        "consultation_fee": "₹650",
        "experience": "14 years"
    },
    {
        "id": 40,
        "name": "Dr. Sibasankar Dalai",
        "specialization": "Neurologist",
        "expertise": ["Migraine", "Headaches", "Neurological Disorders", "Anxiety Disorder"],
        "location": "Medicover Hospitals, Visakhapatnam",
        "contact": "Not Available",
        "availability": "Mon-Sat: 9AM-6PM",
        "consultation_fee": "₹650",
        "experience": "14 years"
    },
    {
        "id": 41,
        "name": "Dr. R. V. Narayana",
        "specialization": "Neurologist",
        "expertise": ["Migraine", "Headaches", "Neurological Disorders", "Anxiety Disorder"],
        "location": "Seven Hills Hospitals, Visakhapatnam",
        "contact": "Not Available",
        "availability": "Mon-Sat: 10AM-5PM",
        "consultation_fee": "₹700",
        "experience": "18 years"
    },

    # ==========================================
    # Dermatologists (Skin diseases)
    # ==========================================
    {
        "id": 42,
        "name": "Dr. Sasi Kiran Attili",
        "specialization": "Dermatologist",
        "expertise": ["Skin Infection", "Skin Allergies", "Skin Diseases", "Rashes", "Allergies"],
        "location": "Visakha Institute of Skin & Allergy, Visakhapatnam",
        "contact": "Not Available",
        "availability": "Mon-Sat: 10AM-6PM",
        "consultation_fee": "₹600",
        "experience": "22 years"
    },
    {
        "id": 43,
        "name": "Dr. Tankala Rajkamal",
        "specialization": "Dermatologist",
        "expertise": ["Skin Infection", "Skin Allergies", "Skin Diseases", "Rashes", "Allergies"],
        "location": "CARE Hospitals, Visakhapatnam",
        "contact": "Not Available",
        "availability": "Mon-Sat: 9AM-5PM",
        "consultation_fee": "₹700",
        "experience": "28 years"
    },
    {
        "id": 44,
        "name": "Dr. Gopi Chand Dadithota",
        "specialization": "Dermatologist",
        "expertise": ["Skin Infection", "Skin Allergies", "Skin Diseases", "Rashes", "Allergies"],
        "location": "Apollo Clinic, Visakhapatnam",
        "contact": "Not Available",
        "availability": "Mon-Sat: 10AM-5PM",
        "consultation_fee": "₹650",
        "experience": "25 years"
    },
    {
        "id": 45,
        "name": "Dr. Swetha Penmetsa",
        "specialization": "Dermatologist",
        "expertise": ["Skin Infection", "Skin Allergies", "Skin Diseases", "Rashes", "Allergies"],
        "location": "Apollo Health City, Visakhapatnam",
        "contact": "Not Available",
        "availability": "Mon-Sat: 9AM-5PM",
        "consultation_fee": "₹600",
        "experience": "12 years"
    },
    {
        "id": 46,
        "name": "Dr. K.V.T. Gopal",
        "specialization": "Dermatologist",
        "expertise": ["Skin Infection", "Skin Allergies", "Skin Diseases", "Rashes", "Allergies"],
        "location": "Skin Care Clinic MVP, Visakhapatnam",
        "contact": "Not Available",
        "availability": "Mon-Sat: 10AM-6PM",
        "consultation_fee": "₹550",
        "experience": "24 years"
    },
    {
        "id": 47,
        "name": "Dr. Sravanthi Alluri",
        "specialization": "Dermatologist",
        "expertise": ["Skin Infection", "Skin Allergies", "Skin Diseases", "Rashes", "Allergies"],
        "location": "Novaskin Clinic, Visakhapatnam",
        "contact": "Not Available",
        "availability": "Mon-Sat: 10AM-5PM",
        "consultation_fee": "₹500",
        "experience": "13 years"
    },
    {
        "id": 48,
        "name": "Dr. R Siri Sandhya Lakshmi",
        "specialization": "Dermatologist",
        "expertise": ["Skin Infection", "Skin Allergies", "Skin Diseases", "Rashes", "Allergies"],
        "location": "Oliva Skin and Hair Clinic, Visakhapatnam",
        "contact": "Not Available",
        "availability": "Mon-Sat: 11AM-7PM",
        "consultation_fee": "₹500",
        "experience": "9 years"
    },

    # ==========================================
    # Gastroenterologists (Gastrointestinal disorders)
    # ==========================================
    {
        "id": 49,
        "name": "Dr. G. Satyanarayana",
        "specialization": "Gastroenterologist",
        "expertise": ["Food Poisoning", "Gastroenteritis", "Digestive Issues", "Stomach Problems"],
        "location": "CARE Hospitals, Visakhapatnam",
        "contact": "040-68106529",
        "availability": "Mon-Sat: 10AM-5PM",
        "consultation_fee": "₹650",
        "experience": "16 years"
    },
    {
        "id": 50,
        "name": "Dr. Baipalli Ramesh",
        "specialization": "Surgical Gastroenterologist",
        "expertise": ["Food Poisoning", "Gastroenteritis", "Digestive Issues", "Stomach Problems", "GI Surgery"],
        "location": "Laparoscopic Center, Visakhapatnam",
        "contact": "9701108209",
        "availability": "Mon-Sat: 9AM-6PM",
        "consultation_fee": "₹700",
        "experience": "15 years"
    },
    {
        "id": 51,
        "name": "Dr. A. V. Siva Prasad",
        "specialization": "Gastroenterologist",
        "expertise": ["Food Poisoning", "Gastroenteritis", "Digestive Issues", "Stomach Problems"],
        "location": "Institute of Gastroenterology, Visakhapatnam",
        "contact": "Not Available",
        "availability": "Mon-Sat: 9AM-5PM",
        "consultation_fee": "₹900",
        "experience": "44 years"
    },
    {
        "id": 52,
        "name": "Dr. Y. Radha Krishna",
        "specialization": "Gastroenterologist",
        "expertise": ["Food Poisoning", "Gastroenteritis", "Digestive Issues", "Stomach Problems", "Liver Diseases"],
        "location": "Radha Krishna Liver & Gastro Center, Visakhapatnam",
        "contact": "Not Available",
        "availability": "Mon-Sat: 10AM-5PM",
        "consultation_fee": "₹700",
        "experience": "23 years"
    },
    {
        "id": 53,
        "name": "Dr. Reddy Sreenivasa Rao",
        "specialization": "Gastroenterologist",
        "expertise": ["Food Poisoning", "Gastroenteritis", "Digestive Issues", "Stomach Problems"],
        "location": "Sri Srinivasa Gastro Centre, Visakhapatnam",
        "contact": "Not Available",
        "availability": "Mon-Sat: 9AM-6PM",
        "consultation_fee": "₹650",
        "experience": "20 years"
    },
    {
        "id": 54,
        "name": "Dr. Mohammed Akbar",
        "specialization": "Gastroenterologist",
        "expertise": ["Food Poisoning", "Gastroenteritis", "Digestive Issues", "Stomach Problems"],
        "location": "Life Medical Center, Visakhapatnam",
        "contact": "Not Available",
        "availability": "Mon-Sat: 10AM-5PM",
        "consultation_fee": "₹600",
        "experience": "24 years"
    },
    {
        "id": 55,
        "name": "Dr. Viswanath N",
        "specialization": "Gastroenterologist",
        "expertise": ["Food Poisoning", "Gastroenteritis", "Digestive Issues", "Stomach Problems"],
        "location": "Seven Hills Hospitals, Visakhapatnam",
        "contact": "Not Available",
        "availability": "Mon-Sat: 9AM-5PM",
        "consultation_fee": "₹600",
        "experience": "15 years"
    },

    # ==========================================
    # Orthopedists (Orthopedic conditions)
    # ==========================================
    {
        "id": 56,
        "name": "Dr. Sridhar Gangavarapu",
        "specialization": "Orthopedist",
        "expertise": ["Joint Pain", "Bone Disorders", "Arthritis", "Fractures", "Orthopedic Conditions"],
        "location": "Medicover Hospitals, Visakhapatnam",
        "contact": "Not Available",
        "availability": "Mon-Sat: 10AM-5PM",
        "consultation_fee": "₹700",
        "experience": "22 years"
    },
    {
        "id": 57,
        "name": "Dr. Pratap Reddy A",
        "specialization": "Orthopedist",
        "expertise": ["Joint Pain", "Bone Disorders", "Arthritis", "Fractures", "Orthopedic Conditions"],
        "location": "Medicover Hospitals, Visakhapatnam",
        "contact": "Not Available",
        "availability": "Mon-Sat: 9AM-6PM",
        "consultation_fee": "₹800",
        "experience": "33 years"
    },
    {
        "id": 58,
        "name": "Dr. Abdul D Khan",
        "specialization": "Orthopedist",
        "expertise": ["Joint Pain", "Bone Disorders", "Arthritis", "Fractures", "Orthopedic Conditions"],
        "location": "Apollo Health City, Visakhapatnam",
        "contact": "Not Available",
        "availability": "Mon-Sat: 9AM-5PM",
        "consultation_fee": "₹750",
        "experience": "27 years"
    },
    {
        "id": 59,
        "name": "Dr. Naveen Palla",
        "specialization": "Orthopedist",
        "expertise": ["Joint Pain", "Bone Disorders", "Arthritis", "Fractures", "Orthopedic Conditions"],
        "location": "Apollo Health City, Visakhapatnam",
        "contact": "Not Available",
        "availability": "Mon-Sat: 10AM-5PM",
        "consultation_fee": "₹700",
        "experience": "22 years"
    },
    {
        "id": 60,
        "name": "Dr. Sasibhushana Rao S",
        "specialization": "Orthopedist",
        "expertise": ["Joint Pain", "Bone Disorders", "Arthritis", "Fractures", "Orthopedic Conditions"],
        "location": "Apollo Health City, Visakhapatnam",
        "contact": "Not Available",
        "availability": "Mon-Sat: 9AM-5PM",
        "consultation_fee": "₹700",
        "experience": "22 years"
    },
    {
        "id": 61,
        "name": "Dr. B V R N Varma",
        "specialization": "Orthopedist",
        "expertise": ["Joint Pain", "Bone Disorders", "Arthritis", "Fractures", "Orthopedic Conditions"],
        "location": "Rekon Centre, Visakhapatnam",
        "contact": "Not Available",
        "availability": "Mon-Sat: 10AM-6PM",
        "consultation_fee": "₹750",
        "experience": "27 years"
    },
    {
        "id": 62,
        "name": "Dr. P S B Hussain",
        "specialization": "Orthopedist",
        "expertise": ["Joint Pain", "Bone Disorders", "Arthritis", "Fractures", "Orthopedic Conditions", "Trauma"],
        "location": "Hussain Ortho And Trauma Care, Visakhapatnam",
        "contact": "Not Available",
        "availability": "Mon-Sat: 9AM-5PM",
        "consultation_fee": "₹650",
        "experience": "19 years"
    },
    {
        "id": 63,
        "name": "Dr. Gudla Siva Prasad",
        "specialization": "Orthopedist",
        "expertise": ["Joint Pain", "Bone Disorders", "Arthritis", "Fractures", "Orthopedic Conditions"],
        "location": "Apollo Health City, Visakhapatnam",
        "contact": "Not Available",
        "availability": "Mon-Sat: 10AM-5PM",
        "consultation_fee": "₹700",
        "experience": "20 years"
    },
    {
        "id": 64,
        "name": "Dr. Srinivsa Rao",
        "specialization": "Orthopedist",
        "expertise": ["Joint Pain", "Bone Disorders", "Arthritis", "Fractures", "Orthopedic Conditions"],
        "location": "Janani Hospital, Visakhapatnam",
        "contact": "Not Available",
        "availability": "Mon-Sat: 9AM-6PM",
        "consultation_fee": "₹650",
        "experience": "26 years"
    }
]

# ============================================
# Disease to Specialization Mapping
# ============================================
# Maps predicted diseases to relevant medical specializations

DISEASE_SPECIALIZATION_MAP = {
    "Common Cold": ["General Physician", "Pulmonologist"],
    "Influenza (Flu)": ["General Physician", "Pulmonologist"],
    "Allergies": ["Dermatologist", "General Physician", "Pulmonologist"],
    "Migraine": ["Neurologist", "General Physician"],
    "Food Poisoning": ["Gastroenterologist", "Surgical Gastroenterologist", "General Physician"],
    "Gastroenteritis": ["Gastroenterologist", "Surgical Gastroenterologist", "General Physician"],
    "Hypertension Symptoms": ["Cardiologist", "Interventional Cardiologist", "General Physician"],
    "Diabetes Symptoms": ["Endocrinologist", "Diabetologist", "General Physician"],
    "Anxiety Disorder": ["Neurologist", "General Physician"],
    "Asthma Attack": ["Pulmonologist", "General Physician"],
    "Skin Infection": ["Dermatologist", "General Physician"],
    "Urinary Tract Infection": ["General Physician"],
    "Joint Pain": ["Orthopedist", "General Physician"],
    "Arthritis": ["Orthopedist", "General Physician"]
}


# ============================================
# Recommendation Functions
# ============================================

def get_recommended_doctors(
    disease: str,
    risk_level: str,
    limit: int = 3
) -> List[dict]:
    """
    Get recommended doctors based on predicted disease and risk level.
    
    Args:
        disease: The predicted disease name
        risk_level: Risk level (LOW/MEDIUM/HIGH)
        limit: Maximum number of doctors to recommend
        
    Returns:
        List of recommended doctor dictionaries
    """
    recommendations = []
    
    # Get relevant specializations for this disease
    specializations = DISEASE_SPECIALIZATION_MAP.get(
        disease, 
        ["General Physician"]  # Default to GP if disease not mapped
    )
    
    # For HIGH risk, prioritize specialists over GPs
    if risk_level == "HIGH":
        # Put specialists first
        specializations = [s for s in specializations if s != "General Physician"]
        if not specializations:
            specializations = ["General Physician"]
    
    # Find matching doctors
    for doctor in DOCTORS_DATABASE:
        # Check if doctor's specialization matches
        if doctor["specialization"] in specializations:
            # Check if doctor has expertise for this disease
            expertise_match = any(
                disease.lower() in exp.lower() or exp.lower() in disease.lower()
                for exp in doctor["expertise"]
            )
            
            recommendation = {
                "id": doctor["id"],
                "name": doctor["name"],
                "specialization": doctor["specialization"],
                "location": doctor["location"],
                "contact": doctor["contact"],
                "availability": doctor["availability"],
                "consultation_fee": doctor["consultation_fee"],
                "experience": doctor.get("experience", "N/A"),
                "expertise_match": expertise_match,
                "relevance_score": _calculate_relevance(
                    doctor, disease, risk_level, expertise_match
                )
            }
            recommendations.append(recommendation)
    
    # Sort by relevance score (higher is better)
    recommendations.sort(key=lambda x: x["relevance_score"], reverse=True)
    
    # Return top N recommendations
    return recommendations[:limit]


def _calculate_relevance(
    doctor: dict,
    disease: str,
    risk_level: str,
    expertise_match: bool
) -> int:
    """
    Calculate relevance score for doctor recommendation.
    Higher score = more relevant.
    """
    score = 0
    
    # Expertise match bonus
    if expertise_match:
        score += 50
    
    # Specialist bonus for high risk
    if risk_level == "HIGH" and doctor["specialization"] != "General Physician":
        score += 30
    
    # Direct disease mention in expertise
    for exp in doctor["expertise"]:
        if disease.lower() == exp.lower():
            score += 40
            break
    
    # General physician baseline (good for low risk)
    if doctor["specialization"] == "General Physician" and risk_level == "LOW":
        score += 20
    
    # Experience bonus (more experience = higher score)
    experience = doctor.get("experience", "0 years")
    try:
        years = int(experience.split()[0])
        score += min(years, 30)  # Cap at 30 points for experience
    except:
        pass
    
    return score


def get_doctor_by_id(doctor_id: int) -> Optional[dict]:
    """
    Get a specific doctor by their ID.
    
    Args:
        doctor_id: The doctor's unique ID
        
    Returns:
        Doctor dictionary or None if not found
    """
    for doctor in DOCTORS_DATABASE:
        if doctor["id"] == doctor_id:
            return doctor
    return None


def get_all_doctors() -> List[dict]:
    """
    Get all doctors in the database.
    Useful for displaying a full directory.
    
    Returns:
        List of all doctor dictionaries
    """
    return DOCTORS_DATABASE.copy()


def get_doctors_by_specialization(specialization: str) -> List[dict]:
    """
    Get all doctors with a specific specialization.
    
    Args:
        specialization: The specialization to filter by
        
    Returns:
        List of matching doctors
    """
    return [
        doctor for doctor in DOCTORS_DATABASE
        if doctor["specialization"].lower() == specialization.lower()
    ]


# ============================================
# Response Schema Helper
# ============================================

def format_doctor_recommendation(doctor: dict, include_score: bool = False) -> dict:
    """
    Format doctor data for API response.
    Removes internal fields like expertise list.
    """
    result = {
        "id": doctor["id"],
        "name": doctor["name"],
        "specialization": doctor["specialization"],
        "location": doctor["location"],
        "contact": doctor["contact"],
        "availability": doctor["availability"],
        "consultation_fee": doctor["consultation_fee"],
        "experience": doctor.get("experience", "N/A")
    }
    
    if include_score and "relevance_score" in doctor:
        result["relevance_score"] = doctor["relevance_score"]
    
    return result

