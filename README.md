# 🏥 Predict Care - Intelligent Health Assistant

A comprehensive Machine Learning-based health assistant system that analyzes user-entered symptoms to predict potential diseases with risk assessment, precautionary advice, doctor recommendations, and personal health record management.

**BTech Final Year Project - Academic Demo**

---

## 📋 Table of Contents

1. [Problem Statement](#problem-statement)
2. [Key Features](#key-features)
3. [Why Machine Learning?](#why-machine-learning)
4. [System Architecture](#system-architecture)
5. [Dataset Creation](#dataset-creation)
6. [ML Algorithm Choice](#ml-algorithm-choice)
7. [Project Structure](#project-structure)
8. [Installation & Setup](#installation--setup)
9. [How to Run](#how-to-run)
10. [API Documentation](#api-documentation)
11. [Limitations](#limitations)
12. [Future Scope](#future-scope)

---

## 🎯 Problem Statement

Early disease detection is crucial for effective treatment. However:
- Many people delay doctor visits due to uncertainty about symptoms
- Initial symptom assessment can help prioritize healthcare visits
- There's a need for accessible preliminary health guidance

**Solution**: A web-based system that uses ML to analyze symptoms and provide:
- Predicted disease based on symptoms
- Risk level assessment (LOW/MEDIUM/HIGH)
- Confidence score for the prediction
- Precautionary advice and recommendations
- Doctor recommendations by specialization
- Personal Electronic Health Records (EHR)
- Real-time notifications

> ⚠️ **Disclaimer**: This is an academic demo. Not for actual medical diagnosis.

---

## ✨ Key Features

### 1. User Authentication
- Secure registration and login with JWT tokens
- Password hashing with bcrypt
- Session management

### 2. Disease Prediction
- ML-powered symptom analysis
- 50 diseases across multiple categories
- Confidence score with risk level assessment
- Natural language symptom input

### 3. Precautionary Advice
- Disease-specific precautions and recommendations
- Lifestyle modification suggestions
- Warning signs to watch for

### 4. Doctor Recommendations
- 64 doctors from Visakhapatnam across 11 specializations
- Filtered by predicted disease category
- Contact information and experience details
- Direct links to hospital locations

### 5. Electronic Health Records (EHR)
- Add and manage personal health records
- Track blood type, allergies, conditions
- View prediction history
- Secure user-specific data

### 7. Health Progress Tracking
- Track active prescriptions assigned by doctors
- Daily checklist for medication adherence
- Visual progress monitoring
- Integration with EHR for permanent records

### 8. In-App Notifications
- Health tips and reminders
- Prediction alerts
- Session notifications

---

## 🤖 Why Machine Learning?

Traditional rule-based systems have limitations:

| Aspect | Rule-Based | Machine Learning |
|--------|-----------|------------------|
| Symptom Patterns | Fixed rules | Learns from data |
| New Diseases | Manual updates | Retraining possible |
| Uncertainty | Binary yes/no | Probability scores |
| Scalability | Hard to maintain | Easy to scale |

**ML Advantages for this problem:**
1. **Pattern Recognition**: Identifies symptom-disease correlations
2. **Probabilistic Output**: Provides confidence scores
3. **Text Processing**: Handles natural language symptom input
4. **Multi-class Classification**: Predicts among 50 diseases

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        FRONTEND                                  │
│                   (HTML + CSS + JS)                             │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │  Pages: index, login, register, predictions, ehr, doctors │  │
│  │  Scripts: script.js, auth.js, notifications.js, ehr.js    │  │
│  │  Styling: style.css (CSS Variables, Responsive Design)    │  │
│  └───────────────────────────────────────────────────────────┘  │
└─────────────────────────────┬───────────────────────────────────┘
                              │ REST API (JSON)
                              │ JWT Authentication
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                        BACKEND                                   │
│                   (Python FastAPI)                              │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                     main.py                              │    │
│  │  Endpoints:                                              │    │
│  │  • POST /register, /login (Authentication)               │    │
│  │  • POST /predict (Disease Prediction)                    │    │
│  │  • GET /predictions/me (Prediction History)              │    │
│  │  • GET /doctors?specialty= (Doctor Recommendations)      │    │
│  │  • GET/POST /ehr (Electronic Health Records)             │    │
│  │  • GET /notifications (In-app Notifications)             │    │
│  └─────────────────────────────────────────────────────────┘    │
│                              │                                   │
│         ┌────────────────────┼────────────────────┐             │
│         ▼                    ▼                    ▼             │
│  ┌─────────────┐    ┌─────────────┐    ┌────────────────┐       │
│  │   model/    │    │   SQLite    │    │   Modules      │       │
│  │ ML Models   │    │  Database   │    │ auth, doctors  │       │
│  │ (joblib)    │    │   (users,   │    │ ehr, notifs    │       │
│  │             │    │ predictions)│    │ precautions    │       │
│  └─────────────┘    └─────────────┘    └────────────────┘       │
└─────────────────────────────────────────────────────────────────┘
```

**Data Flow:**
```
User Input → Authentication → Preprocessing → TF-IDF → RandomForest → 
  ↓
Prediction + Precautions + Doctor Recommendations → Save to DB → Response
```

---

## 📊 Dataset Creation

### Approach
Since real medical datasets require ethical approvals, we generated **synthetic data**:

### Dataset Specifications
- **50 common diseases** covering multiple categories
- **6-10 symptoms per disease** (medically relevant)
- **1000 total samples** (20 per disease)
- **3 risk levels**: LOW, MEDIUM, HIGH

### Disease Categories
| Category | Example Diseases |
|----------|-----------------|
| Respiratory | Common Cold, Flu, Pneumonia, Asthma |
| Digestive | Gastroenteritis, GERD, Peptic Ulcer |
| Cardiovascular | Hypertension, Heart Disease, Anemia |
| Neurological | Migraine, Vertigo, Epilepsy |
| Infectious | Malaria, Dengue, Typhoid, Chickenpox |
| Skin | Eczema, Psoriasis, Fungal Infection |
| Endocrine | Diabetes, Hyperthyroidism |
| Mental Health | Depression, Anxiety, Insomnia |

### Sample Data
```csv
symptoms,disease,risk_level
"fever, headache, body aches, chills",Influenza (Flu),MEDIUM
"itchy skin, red patches, dry skin",Eczema,LOW
"chest pain, shortness of breath",Heart Disease,HIGH
```

---

## 🧠 ML Algorithm Choice

### Text Vectorization: TF-IDF

**Why TF-IDF?**
- Converts text to numerical features
- Weighs important words higher
- Handles variable-length input
- Simple and interpretable

**Configuration:**
```python
TfidfVectorizer(
    max_features=500,      # Vocabulary limit
    ngram_range=(1, 2),    # Words and word pairs
    stop_words='english'   # Remove common words
)
```

### Classifier: RandomForest

**Why RandomForest?**

| Feature | Benefit |
|---------|---------|
| Ensemble method | More robust predictions |
| Handles multi-class | 50 disease classes |
| Probability output | Confidence scores |
| No feature scaling needed | Works with TF-IDF directly |
| Resistant to overfitting | Multiple trees vote |

**Configuration:**
```python
RandomForestClassifier(
    n_estimators=100,    # 100 decision trees
    max_depth=20,        # Prevent overfitting
    random_state=42      # Reproducibility
)
```

### Risk Level Logic

```
Confidence >= 70%  →  Use disease's base risk level
Confidence 40-70%  →  MEDIUM (uncertain prediction)
Confidence < 40%   →  HIGH (consult doctor)
```

---

## 📁 Project Structure

```
HealthAssistant/
├── backend/
│   ├── main.py                # FastAPI server with all endpoints
│   ├── database.py            # SQLAlchemy models and DB setup
│   ├── auth.py                # JWT authentication utilities
│   ├── doctors.py             # Doctor database (64 Visakhapatnam doctors)
│   ├── precautions.py         # Disease precautions mapping
│   ├── notifications.py       # Notification system
│   ├── ehr.py                 # EHR management
│   ├── dataset_generator.py   # Creates synthetic dataset
│   ├── train_model.py         # Trains ML model
│   ├── dataset.csv            # Generated dataset
│   ├── requirements.txt       # Python dependencies
│   └── model/
│       ├── disease_classifier.joblib
│       ├── tfidf_vectorizer.joblib
│       └── risk_mapping.joblib
├── frontend/
│   ├── index.html             # Main prediction page
│   ├── login.html             # User login
│   ├── register.html          # User registration
│   ├── predictions.html       # Prediction history
│   ├── ehr.html               # Electronic Health Records
│   ├── doctors.html           # Doctor directory
│   ├── style.css              # All styling
│   ├── script.js              # Main page logic
│   ├── auth.js                # Authentication handling
│   ├── notifications.js       # Notification display
│   └── ehr.js                 # EHR functionality
└── README.md                  # This file
```

---

## ⚙️ Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Step 1: Install Python Dependencies

```bash
cd backend
pip install -r requirements.txt
```

Or install manually:
```bash
pip install fastapi uvicorn scikit-learn pandas numpy joblib python-jose[cryptography] passlib[bcrypt] sqlalchemy
```

### Step 2: Generate Dataset (if needed)

```bash
python dataset_generator.py
```

### Step 3: Train the Model (if needed)

```bash
python train_model.py
```

---

## 🚀 How to Run

### Terminal 1: Start Backend Server

```bash
cd backend
uvicorn main:app --reload --port 8000
```

Server runs at: `http://localhost:8000`

### Terminal 2: Start Frontend

Option A - Using Python's HTTP server:
```bash
cd frontend
python -m http.server 3000
```

Option B - Simply open `frontend/index.html` in browser

### Access the Application

- Frontend: `http://localhost:3000` or open `index.html`
- API Docs: `http://localhost:8000/docs`

---

## 📡 API Documentation

### Authentication

#### POST /register
Register a new user.

**Request:**
```json
{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "secure_password"
}
```

**Response:**
```json
{
    "message": "User registered successfully"
}
```

#### POST /login
Login and receive JWT token.

**Request:**
```json
{
    "username": "john_doe",
    "password": "secure_password"
}
```

**Response:**
```json
{
    "access_token": "eyJhbGciOiJIUzI1...",
    "token_type": "bearer"
}
```

### Disease Prediction

#### POST /predict
Predict disease from symptoms (requires authentication).

**Headers:**
```
Authorization: Bearer <token>
```

**Request:**
```json
{
    "symptoms": "fever headache body aches fatigue"
}
```

**Response:**
```json
{
    "disease": "Influenza (Flu)",
    "risk": "MEDIUM",
    "confidence": 0.72,
    "message": "",
    "precautions": ["Rest and stay hydrated", "..."],
    "recommended_doctors": [
        {
            "name": "Dr. K. Ramesh",
            "specialty": "General Medicine",
            "hospital": "King George Hospital",
            "phone": "0891-2564891",
            "experience": "15 years"
        }
    ]
}
```

#### GET /predictions/me
Get user's prediction history.

**Response:**
```json
[
    {
        "id": 1,
        "symptoms": "fever headache",
        "disease": "Influenza (Flu)",
        "risk": "MEDIUM",
        "confidence": 0.72,
        "created_at": "2024-01-15T10:30:00"
    }
]
```

### Doctors

#### GET /doctors
Get all doctors or filter by specialty.

**Query Parameters:**
- `specialty` (optional): Filter by specialization

**Response:**
```json
[
    {
        "name": "Dr. K. Ramesh",
        "specialty": "General Medicine",
        "hospital": "King George Hospital",
        "address": "Maharanipeta, Visakhapatnam",
        "phone": "0891-2564891",
        "experience": "15 years",
        "maps_link": "https://maps.google.com/..."
    }
]
```

### Electronic Health Records

#### GET /ehr
Get user's EHR record.

#### POST /ehr
Create or update EHR record.

**Request:**
```json
{
    "blood_type": "O+",
    "allergies": "Penicillin",
    "chronic_conditions": "None",
    "emergency_contact": "9876543210"
}
```

### Other Endpoints

#### GET /health
Check API status.

#### GET /notifications
Get user notifications.

#### POST /notifications/mark-read
Mark all notifications as read.
```

---

## ⚠️ Limitations

1. **Synthetic Data**: Dataset is generated, not from real medical records
2. **Limited Diseases**: Only 50 diseases covered
3. **Symptom Overlap**: Many diseases share similar symptoms
4. **No Medical History**: Doesn't consider patient history, age, gender
5. **Text Dependency**: Relies on symptom description quality
6. **No Image Analysis**: Cannot process medical images
7. **Single Language**: English only

---

## 🔮 Future Scope

1. **Real Dataset Integration**: Partner with hospitals for real data
2. **Deep Learning**: Use BERT/transformers for better text understanding
3. **Multi-modal Input**: Add support for medical images
4. **Patient History**: Include demographics and medical history
5. **Multi-language Support**: Support regional languages
6. **Mobile App**: Develop Android/iOS application
7. **Doctor Integration**: Connect with telemedicine platforms
8. **Explainable AI**: Show which symptoms led to prediction

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| Frontend | HTML5, CSS3, JavaScript (Vanilla) |
| Backend | Python 3.x, FastAPI |
| Database | SQLite with SQLAlchemy ORM |
| Authentication | JWT (python-jose), bcrypt |
| ML Library | scikit-learn (RandomForest, TF-IDF) |
| Data Processing | pandas, numpy |
| Model Serialization | joblib |
| API Communication | Fetch API, REST |

---

## 👨‍💻 Author

**BTech Final Year Project - Predict Care**  
Intelligent Disease Prediction using Machine Learning

---

## 📝 License

This project is for academic/educational purposes only.

---

## 🙏 Acknowledgments

- scikit-learn documentation
- FastAPI documentation
- Medical symptom references for dataset creation
- Visakhapatnam hospitals and doctors directory
