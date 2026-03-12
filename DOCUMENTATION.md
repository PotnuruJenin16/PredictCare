# 🏥 Predict Care - Personal Digital Health Assistant

## BTech Final Year Project - Complete Documentation

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [System Architecture](#system-architecture)
3. [Data Flow](#data-flow)
4. [Core Features](#core-features)
5. [Technical Implementation](#technical-implementation)
6. [ML Model Explanation](#ml-model-explanation)
7. [Ethical Considerations & Disclaimers](#ethical-considerations--disclaimers)
8. [Installation & Setup](#installation--setup)
9. [API Documentation](#api-documentation)
10. [Project Structure](#project-structure)
11. [Viva Questions & Answers](#viva-questions--answers)

---

## 1. Project Overview

### What is Predict Care?

**Predict Care** is a personal digital health assistant that helps users understand their symptoms and provides:

- **Disease Predictions** based on natural language symptom input
- **Risk Assessment** (Low/Medium/High) based on prediction confidence
- **Personalized Precautionary Advice** tailored to the user
- **Doctor Recommendations** matching the predicted condition
- **Health History Tracking** for pattern awareness
- **In-App Notifications** for important health alerts

### Why This Project?

1. **Accessibility**: Many people are unsure whether their symptoms warrant a doctor visit
2. **Awareness**: Helps users understand potential health conditions
3. **Tracking**: Maintains history for recurring pattern identification
4. **Guidance**: Provides actionable do's and don'ts with professional consultation advice

### What This Project is NOT

- ❌ NOT a medical diagnosis system
- ❌ NOT a replacement for professional healthcare
- ❌ NOT intended for emergency situations
- ❌ NOT using real patient data

---

## 2. System Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           FRONTEND (HTML/CSS/JS)                         │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐    │
│  │  index.html  │ │ doctors.html │ │predictions   │ │   auth pages │    │
│  │  (Main App)  │ │ (Directory)  │ │   .html      │ │(login/register)│  │
│  └──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘    │
│                              │                                           │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │                    JavaScript Modules                             │   │
│  │  auth.js (JWT)  |  script.js (Logic)  |  notifications.js        │   │
│  └──────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────┬───────────────────────────────────────┘
                                  │ HTTP REST API (JSON)
                                  │ Authorization: Bearer <JWT>
                                  ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                        BACKEND (Python FastAPI)                          │
│                                                                          │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │                         main.py                                   │   │
│  │  • Authentication endpoints (/register, /login)                   │   │
│  │  • Prediction endpoint (/predict)                                 │   │
│  │  • History endpoint (/predictions/me)                             │   │
│  │  • Notification endpoints (/notifications/*)                      │   │
│  │  • Doctor endpoints (/doctors/*)                                  │   │
│  └──────────────────────────────────────────────────────────────────┘   │
│                              │                                           │
│  ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌────────────────────┐    │
│  │  auth.py   │ │precautions │ │ doctors.py │ │  notifications.py  │    │
│  │  (JWT)     │ │    .py     │ │ (Recommend)│ │   (In-App Alerts)  │    │
│  └────────────┘ └────────────┘ └────────────┘ └────────────────────┘    │
│                              │                                           │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │                    ML Model (model/)                              │   │
│  │  • disease_classifier.joblib (RandomForest)                       │   │
│  │  • tfidf_vectorizer.joblib (Text → Features)                      │   │
│  │  • risk_mapping.joblib (Disease → Risk Level)                     │   │
│  └──────────────────────────────────────────────────────────────────┘   │
│                              │                                           │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │                   Database (SQLite)                               │   │
│  │  • users table (id, name, email, password_hash, created_at)       │   │
│  │  • predictions table (id, user_id, symptoms, disease, risk, etc.) │   │
│  └──────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Data Flow

### User Makes a Prediction

```
User Input: "I have fever, headache, body aches, and fatigue"
                │
                ▼
┌─────────────────────────────────────┐
│ 1. PREPROCESSING                    │
│    • Convert to lowercase           │
│    • Remove extra whitespace        │
│    • Clean special characters       │
│    Input: "fever headache body      │
│            aches fatigue"           │
└─────────────────────────────────────┘
                │
                ▼
┌─────────────────────────────────────┐
│ 2. TF-IDF VECTORIZATION             │
│    • Convert text to numerical      │
│      feature vector                 │
│    • Uses vocabulary from training  │
│    Output: [0.3, 0.0, 0.5, ...]    │
└─────────────────────────────────────┘
                │
                ▼
┌─────────────────────────────────────┐
│ 3. RANDOM FOREST PREDICTION         │
│    • Passes features through        │
│      100 decision trees             │
│    • Each tree votes for a class    │
│    • Majority vote = prediction     │
│    • Confidence = vote percentage   │
│    Output: "Influenza (Flu)", 0.72  │
└─────────────────────────────────────┘
                │
                ▼
┌─────────────────────────────────────┐
│ 4. RISK CALCULATION                 │
│    • If confidence >= 70%:          │
│      use disease's base risk        │
│    • If confidence 40-70%:          │
│      MEDIUM (uncertain)             │
│    • If confidence < 40%:           │
│      HIGH (consult doctor)          │
│    Output: "MEDIUM"                 │
└─────────────────────────────────────┘
                │
                ▼
┌─────────────────────────────────────┐
│ 5. GENERATE ADVICE & DOCTORS        │
│    • Match disease to precautions   │
│    • Personalize based on history   │
│    • Match disease to specialists   │
│    • Create notifications           │
└─────────────────────────────────────┘
                │
                ▼
┌─────────────────────────────────────┐
│ 6. STORE & RESPOND                  │
│    • Save prediction to database    │
│    • Return complete response       │
└─────────────────────────────────────┘
```

---

## 4. Core Features

### 4.1 User Authentication

- **JWT-based authentication** for secure API access
- **Password hashing** using bcrypt
- **Session persistence** via localStorage
- **Protected routes** require valid token

### 4.2 Disease Prediction

- **Natural language input** - no medical jargon required
- **12 disease categories** supported
- **Confidence score** (0-100%) for transparency
- **Risk level** (LOW/MEDIUM/HIGH) assessment

### 4.3 Personalized Precautionary Advice

Generated based on:
- Predicted disease
- Confidence level
- Risk assessment
- User's prediction history (recurring conditions)

Includes:
- Key recommendations
- Do's and Don'ts
- When to consult a doctor
- Disclaimer

### 4.4 Doctor Recommendations

- **12 specialist doctors** in the database
- **Rule-based matching** to disease specializations
- **Relevance scoring** prioritizes best matches
- Contact information and consultation fees

### 4.5 Notifications

Triggered when:
- New prediction is made
- Risk level is HIGH
- Recurring condition detected
- User registers (welcome message)

### 4.6 Health History

- All predictions saved with timestamp
- View past symptoms, predictions, advice
- See recommended doctors for each prediction
- See recommended doctors for each prediction
- Track patterns over time

### 4.8 Health Progress Tracking

Allows patients to manage and track their active treatment plans:

- **Active Prescriptions**: View current prescriptions assigned by doctors
- **Daily Adherence**: interactive checklist to mark daily medication intake
- **Progress Visualization**: Visual progress bar showing completion percentage
- **Doctor's Notes**: View specific instructions and notes from the doctor
- **One-Active-Policy**: Focus on one active treatment plan at a time for better adherence

### 4.7 Electronic Health Records (EHR)

**What is EHR?**
Electronic Health Records (EHR) is a digital repository of a user's health-related documents and records. In Predict Care, EHR allows users to:

- **Upload Medical Documents**: Store prescriptions, lab reports, scan images
- **Add Text Notes**: Record doctor notes, OP summaries, observations
- **Auto-save Predictions**: System predictions are automatically saved to EHR
- **View Unified Timeline**: See all health records in chronological order
- **Download Records**: Access uploaded files anytime

**Why EHR is Important in Healthcare:**
1. **Centralized Access**: All medical records in one place
2. **Continuity of Care**: Track health history over time
3. **Patient Empowerment**: Users own and control their health data
4. **Better Decision Making**: Access to historical data helps in consultations
5. **Reduced Paperwork**: Digital storage eliminates physical document management

**EHR Categories in Predict Care:**
| Category | Icon | Description |
|----------|------|-------------|
| Prescription | 💊 | Doctor-prescribed medications (Auto-synced) |
| Lab Report | 🔬 | Laboratory test results |
| Scan/X-Ray | 🩻 | Medical imaging documents |
| OP Note | 📝 | Outpatient notes, doctor observations |
| Prediction | 🔍 | System-generated prediction records |

**Security & Privacy:**
- Records are isolated per user (user A cannot see user B's records)
- JWT authentication required for all EHR operations
- Files stored in user-specific directories
- Soft delete (archive) prevents accidental data loss

**Academic Note:**
This EHR implementation is for educational demonstration. A production EHR system would require:
- Healthcare compliance (HIPAA, GDPR)
- Encryption at rest and in transit
- Audit logging
- Professional certification

---

## 5. Technical Implementation

### Backend Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Framework | FastAPI | REST API with automatic docs |
| Database | SQLAlchemy + SQLite | Data persistence |
| Auth | python-jose + passlib | JWT tokens + bcrypt |
| ML | scikit-learn | Model training & inference |
| Serialization | joblib | Model persistence |

### Frontend Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Structure | HTML5 | Semantic markup |
| Styling | CSS3 | Responsive design |
| Logic | Vanilla JS | No framework overhead |
| Storage | localStorage | Token persistence |

### Key Files

```
backend/
├── main.py              # FastAPI application
├── auth.py              # JWT authentication
├── database.py          # SQLAlchemy models
├── precautions.py       # Advice generation
├── doctors.py           # Doctor recommendations
├── notifications.py     # Alert system
├── train_model.py       # Model training
└── model/               # Trained artifacts

frontend/
├── index.html           # Main prediction page
├── predictions.html     # Health history
├── doctors.html         # Doctor directory
├── login.html           # Authentication
├── register.html        # Registration
├── script.js            # Main logic
├── auth.js              # Auth utilities
├── notifications.js     # Notification UI
└── style.css            # All styles
```

---

## 6. ML Model Explanation

### Why TF-IDF + RandomForest?

**TF-IDF (Term Frequency - Inverse Document Frequency)**
- Converts text to numerical features
- Captures word importance in context
- Handles varying symptom descriptions
- No need for exact keyword matching

**RandomForest Classifier**
- Ensemble of 100 decision trees
- Handles multi-class classification (12 diseases)
- Provides probability scores (confidence)
- Robust to noisy data
- No need for feature scaling

### Why Predictions are Probabilistic

1. **Symptom Overlap**: Many diseases share similar symptoms
2. **Natural Language Variance**: "headache" vs "head pain"
3. **Missing Information**: User may not mention all symptoms
4. **Model Uncertainty**: Limited training data

**This is why we always recommend professional consultation.**

### Training Data

- Synthetic dataset generated for academic demo
- 12 disease categories
- ~100 samples per disease
- Varied symptom combinations

---

## 7. Ethical Considerations & Disclaimers

### Important Disclaimers

```
⚠️ CRITICAL DISCLAIMER

This system is an ACADEMIC DEMONSTRATION PROJECT.

1. NOT A MEDICAL DEVICE: This software has not been validated
   for clinical use and should NEVER be used for actual medical
   diagnosis or treatment decisions.

2. EDUCATIONAL PURPOSE ONLY: Results are intended to demonstrate
   machine learning concepts, not provide medical advice.

3. ALWAYS CONSULT PROFESSIONALS: For any health concerns, always
   consult a qualified healthcare provider.

4. NO LIABILITY: The creators accept no responsibility for any
   decisions made based on this system's outputs.

5. DATA PRIVACY: This demo uses a local database. In production,
   proper healthcare data regulations (HIPAA, etc.) would apply.
```

### Why These Disclaimers Matter

1. **ML Predictions are Probabilistic**: Not definitive diagnoses
2. **Training Data Limitations**: Synthetic data doesn't represent real-world complexity
3. **Medical Ethics**: Healthcare requires professional judgment
4. **Legal Requirements**: Healthcare software has strict regulations

---

## 8. Installation & Setup

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Modern web browser

### Step-by-Step Setup

```bash
# 1. Navigate to project directory
cd /path/to/HealthAssistant

# 2. Install Python dependencies
cd backend
pip install -r requirements.txt

# 3. Generate dataset (if not present)
python dataset_generator.py

# 4. Train the ML model
python train_model.py

# 5. Start the backend server
python main.py
# Server runs at http://localhost:8000

# 6. Open frontend in browser
# Open frontend/index.html in your browser
# Or use a simple HTTP server:
cd ../frontend
python -m http.server 3000
# Then visit http://localhost:3000
```

### Quick Start (After Setup)

```bash
cd backend && python main.py
```

Then open `frontend/login.html` in your browser.

---

## 9. API Documentation

### Authentication

#### POST /register
Register a new user account.

```json
Request:
{
    "name": "John Doe",
    "email": "john@example.com",
    "password": "securepass123"
}

Response:
{
    "access_token": "eyJ...",
    "token_type": "bearer",
    "user": {
        "id": 1,
        "name": "John Doe",
        "email": "john@example.com"
    }
}
```

#### POST /login
Authenticate existing user.

```json
Request:
{
    "email": "john@example.com",
    "password": "securepass123"
}

Response: (same as register)
```

### Predictions

#### POST /predict (Auth Required)
Analyze symptoms and get prediction.

```json
Request:
{
    "symptoms": "fever headache body aches fatigue"
}

Response:
{
    "disease": "Influenza (Flu)",
    "risk": "MEDIUM",
    "confidence": 0.72,
    "advice_level": "medium",
    "precautions": ["Rest and stay hydrated", ...],
    "dos": ["Monitor temperature", ...],
    "donts": ["Don't take antibiotics", ...],
    "consult_when": ["Difficulty breathing", ...],
    "disclaimer": "This is for educational purposes...",
    "recommended_doctors": [
        {
            "name": "Dr. Rajesh Kumar",
            "specialization": "General Physician",
            "contact": "+91 98765 43210"
        }
    ]
}
```

#### GET /predictions/me (Auth Required)
Get user's prediction history.

### Notifications

#### GET /notifications (Auth Required)
Get user's notifications.

#### POST /notifications/read-all (Auth Required)
Mark all notifications as read.

### Doctors

#### GET /doctors
Get all doctors (public endpoint).

#### GET /doctors/{id}
Get specific doctor details.

### EHR (Electronic Health Records)

#### GET /ehr (Auth Required)
Get user's EHR records.

```
Query Parameters:
- category: Filter by category (prescription/lab_report/scan_image/op_note/prediction)
- include_archived: Include archived records (default: false)

Response:
{
    "records": [
        {
            "id": 1,
            "title": "Blood Test Report",
            "category": "lab_report",
            "category_name": "Lab Report",
            "category_icon": "🔬",
            "has_file": true,
            "file_name": "blood_test.pdf",
            "created_at": "2026-01-28T10:30:00Z"
        }
    ],
    "total_count": 5,
    "statistics": {
        "total_records": 5,
        "file_count": 3,
        "total_file_size_formatted": "2.5 MB"
    }
}
```

#### POST /ehr/upload (Auth Required)
Upload a file to EHR.

```
Form Data:
- file: The file to upload (PDF, images, documents)
- title: Record title (required)
- category: prescription/lab_report/scan_image/op_note (required)
- description: Optional description
- record_date: Optional date of the record (ISO format)

Max file size: 10 MB
Supported types: PDF, Word, JPEG, PNG, GIF, WebP, TXT
```

#### POST /ehr/text (Auth Required)
Create a text-based EHR record (notes, summaries).

```json
Request:
{
    "title": "Dr. Sharma - Follow-up Notes",
    "category": "op_note",
    "text_content": "Patient shows improvement...",
    "record_date": "2026-01-28"
}
```

#### GET /ehr/{id}/download (Auth Required)
Download an EHR file.

#### DELETE /ehr/{id} (Auth Required)
Delete/archive an EHR record.

```
Query Parameters:
- permanent: true for permanent deletion, false for archive (default: false)
```

---

## 10. Project Structure

```
HealthAssistant/
│
├── backend/
│   ├── main.py              # FastAPI application entry point
│   ├── auth.py              # JWT authentication module
│   ├── database.py          # SQLAlchemy models & config
│   ├── precautions.py       # Precautionary advice generation
│   ├── doctors.py           # Doctor recommendation engine
│   ├── notifications.py     # In-app notification system
│   ├── ehr.py               # EHR management module
│   ├── train_model.py       # ML model training script
│   ├── dataset_generator.py # Synthetic data generator
│   ├── dataset.csv          # Training dataset
│   ├── requirements.txt     # Python dependencies
│   ├── uploads/             # User uploaded EHR files
│   │   └── user_{id}/       # Per-user file storage
│   └── model/
│       ├── disease_classifier.joblib
│       ├── tfidf_vectorizer.joblib
│       └── risk_mapping.joblib
│
├── frontend/
│   ├── index.html           # Main prediction interface
│   ├── predictions.html     # Health history page
│   ├── ehr.html             # EHR management page
│   ├── doctors.html         # Doctor directory page
│   ├── login.html           # Login page
│   ├── register.html        # Registration page
│   ├── script.js            # Main frontend logic
│   ├── auth.js              # Authentication utilities
│   ├── notifications.js     # Notification UI handlers
│   ├── ehr.js               # EHR UI handlers
│   └── style.css            # All stylesheets
│
├── README.md                # Original README
└── DOCUMENTATION.md         # This file
```

---

## 11. Viva Questions & Answers

### Q1: What is the purpose of this project?
**A:** Predict Care is a personal digital health assistant that helps users understand potential health conditions based on their symptoms. It provides disease predictions, risk assessment, precautionary advice, and doctor recommendations. It's an educational tool, NOT a medical diagnosis system.

### Q2: Why did you choose TF-IDF for text processing?
**A:** TF-IDF is ideal because:
1. Converts natural language to numerical features
2. Captures word importance (rare symptoms carry more weight)
3. Handles varying user descriptions
4. Works well with small datasets
5. No need for neural networks or large models

### Q3: Why RandomForest over other algorithms?
**A:** RandomForest was chosen because:
1. Handles multi-class classification (12 diseases)
2. Provides probability scores for confidence
3. Robust to overfitting with small datasets
4. No feature scaling needed
5. Interpretable results

### Q4: How does the risk level calculation work?
**A:** Risk is calculated using both disease severity and prediction confidence:
- Confidence ≥ 70%: Use disease's inherent risk level
- Confidence 40-70%: MEDIUM (uncertain, recommend caution)
- Confidence < 40%: HIGH (uncertain, recommend doctor visit)

This ensures that even low-risk diseases with uncertain predictions prompt medical consultation.

### Q5: How are doctor recommendations generated?
**A:** Using a rule-based matching system:
1. Each disease maps to relevant medical specializations
2. Doctors are filtered by matching specialization
3. Relevance score calculated based on expertise match
4. Higher risk = prioritize specialists over GPs
5. Top 3 most relevant doctors returned

### Q6: How does the notification system work?
**A:** Notifications are stored in memory (for demo) and triggered by:
1. New prediction → "Analysis complete" notification
2. HIGH risk → Alert notification
3. Recurring condition → Pattern warning
4. New user → Welcome notification

In production, this would use a database and push notifications.

### Q7: How is user authentication handled?
**A:** Using JWT (JSON Web Tokens):
1. User registers/logs in with email/password
2. Password hashed with bcrypt before storage
3. Server generates JWT with user ID
4. Client stores token in localStorage
5. All protected API calls include token in header
6. Server validates token on each request

### Q8: What are the ethical considerations?
**A:**
1. Clear disclaimers that it's not medical advice
2. Always recommend professional consultation
3. Transparency about confidence levels
4. No claim of diagnosis or treatment
5. Educational purpose clearly stated

### Q9: How could this be improved for production?
**A:**
1. Use real, validated medical datasets
2. Get medical professional review
3. Implement proper healthcare compliance (HIPAA)
4. Add more sophisticated NLP (medical NER)
5. Include more diseases and specialists
6. Add proper push notifications
7. Mobile app development
8. Integration with healthcare systems

### Q10: What is the accuracy of the model?
**A:** On the synthetic test dataset, the model achieves ~85-90% accuracy. However, this is with synthetic data. Real-world accuracy would require:
1. Real medical datasets
2. Clinical validation
3. Professional medical review
4. Continuous monitoring and retraining

### Q11: What is EHR and why is it important?
**A:** EHR (Electronic Health Records) is a digital repository of health-related records. In Predict Care, EHR stores:
- Uploaded prescriptions and lab reports
- Scanned medical images
- Doctor notes and OP summaries
- System-generated prediction records

**Importance:**
1. Centralized access to all medical history
2. Supports continuity of care
3. Patient controls their own data
4. Creates unified health timeline
5. Reduces paperwork and improves accessibility

### Q12: How does EHR access control work?
**A:** Access control is user-based:
1. All EHR operations require JWT authentication
2. Each record has a `user_id` foreign key
3. API queries filter by `current_user.id`
4. Files stored in user-specific directories (`uploads/user_{id}/`)
5. No endpoint allows cross-user data access

### Q13: How are predictions saved to EHR?
**A:** When a user makes a prediction:
1. Prediction is saved to `predictions` table
2. System automatically creates an EHR record
3. EHR record links to prediction via `prediction_id`
4. Record contains symptoms, results, and advice
5. Notification sent to user about EHR addition

This creates a comprehensive health timeline without user intervention.

### Q14: What file types does EHR support?
**A:** Supported file types:
- Documents: PDF, Word (.doc, .docx), Text files
- Images: JPEG, PNG, GIF, WebP
- Maximum size: 10 MB per file

Files are validated for type and size before storage.

### Q15: How would you make EHR production-ready?
**A:** Production requirements:
1. **Compliance**: HIPAA (US), GDPR (EU) healthcare regulations
2. **Security**: Encryption at rest and in transit
3. **Audit Logging**: Track all access and modifications
4. **Backup & Recovery**: Regular backups, disaster recovery
5. **Access Control**: Role-based (patient, doctor, admin)
6. **Interoperability**: HL7 FHIR standards for data exchange
7. **Certification**: Get healthcare software certification

---

## Conclusion

Predict Care demonstrates how machine learning can be applied to healthcare scenarios while emphasizing the critical importance of professional medical consultation. The project showcases:

- Full-stack web development
- Machine learning integration
- User authentication systems
- API design principles
- Ethical AI considerations

**Remember: This is an academic demonstration. Always consult healthcare professionals for medical concerns.**

---

*BTech Final Year Project - Predict Care*
*Personal Digital Health Assistant*
