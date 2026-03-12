/**
 * Doctor Dashboard JavaScript
 * ===========================
 * Handles doctor portal functionality:
 * - Patient lookup
 * - Record upload (prescriptions, reports, notes)
 * - File uploads
 */

// ==========================================
// Configuration
// ==========================================
const API_URL = "http://localhost:8000";
const DOCTOR_TOKEN_KEY = "predict_care_doctor_token";
const DOCTOR_DATA_KEY = "predict_care_doctor_data";

// Current patient being worked on
let currentPatient = null;

// ==========================================
// Authentication Functions
// ==========================================

function getDoctorToken() {
    return localStorage.getItem(DOCTOR_TOKEN_KEY);
}

function getDoctorData() {
    const data = localStorage.getItem(DOCTOR_DATA_KEY);
    return data ? JSON.parse(data) : null;
}

function isDoctorLoggedIn() {
    return getDoctorToken() !== null;
}

function doctorLogout() {
    localStorage.removeItem(DOCTOR_TOKEN_KEY);
    localStorage.removeItem(DOCTOR_DATA_KEY);
    window.location.href = 'home.html';
}

function requireDoctorAuth() {
    if (!isDoctorLoggedIn()) {
        window.location.href = 'doctor-login.html';
    }
}

async function authenticatedDoctorFetch(url, options = {}) {
    const token = getDoctorToken();
    
    if (!token) {
        window.location.href = 'doctor-login.html';
        throw new Error('Not authenticated');
    }
    
    const headers = {
        'Authorization': `Bearer ${token}`,
        ...options.headers,
    };
    
    // Only add Content-Type for non-FormData requests
    if (!(options.body instanceof FormData)) {
        headers['Content-Type'] = 'application/json';
    }
    
    const response = await fetch(url, {
        ...options,
        headers,
    });
    
    if (response.status === 401 || response.status === 403) {
        doctorLogout();
        throw new Error('Session expired. Please login again.');
    }
    
    return response;
}

// ==========================================
// Initialization
// ==========================================

document.addEventListener("DOMContentLoaded", function() {
    // Require authentication
    requireDoctorAuth();
    
    // Set doctor info in header
    const doctor = getDoctorData();
    if (doctor) {
        document.getElementById("doctor-name").textContent = doctor.name;
        document.getElementById("doctor-specialization").textContent = doctor.specialization;
        document.getElementById("doctor-hospital").textContent = doctor.hospital || "Predict Care";
    }
    
    // Setup logout
    document.getElementById("logout-btn").addEventListener("click", function(e) {
        e.preventDefault();
        doctorLogout();
    });
    
    // Setup patient lookup
    setupPatientLookup();
    
    // Setup tabs
    setupTabs();
    
    // Setup forms
    setupForms();
    
    // Setup file upload
    setupFileUpload();
});

// ==========================================
// Patient Lookup
// ==========================================

function setupPatientLookup() {
    const lookupBtn = document.getElementById("lookup-btn");
    const patientEmailInput = document.getElementById("patient-email");
    
    lookupBtn.addEventListener("click", lookupPatient);
    
    patientEmailInput.addEventListener("keypress", function(e) {
        if (e.key === "Enter") {
            lookupPatient();
        }
    });
}

async function lookupPatient() {
    const email = document.getElementById("patient-email").value.trim();
    
    if (!email) {
        showLookupError("Please enter a patient email");
        return;
    }
    
    const lookupBtn = document.getElementById("lookup-btn");
    lookupBtn.disabled = true;
    lookupBtn.textContent = "Looking up...";
    
    try {
        const response = await authenticatedDoctorFetch(
            `${API_URL}/doctor/lookup/${encodeURIComponent(email)}`
        );
        
        const data = await response.json();
        
        if (data.found) {
            showPatientFound(data);
        } else {
            showLookupError(data.message);
        }
        
    } catch (error) {
        showLookupError(error.message);
    } finally {
        lookupBtn.disabled = false;
        lookupBtn.textContent = "🔍 Look Up Patient";
    }
}

function showPatientFound(data) {
    currentPatient = {
        id: data.patient_id,
        name: data.patient_name,
        email: data.patient_email
    };
    
    // Show success
    document.getElementById("lookup-result").classList.remove("hidden");
    document.getElementById("lookup-success").classList.remove("hidden");
    document.getElementById("lookup-error").classList.add("hidden");
    
    document.getElementById("patient-name").textContent = data.patient_name;
    document.getElementById("patient-email-display").textContent = data.patient_email;
    
    // Show upload section
    document.getElementById("upload-section").classList.remove("hidden");
    document.getElementById("upload-for-patient").textContent = data.patient_name;
    
    // Hide any previous success message
    document.getElementById("upload-success").classList.add("hidden");
    
    // Scroll to upload section
    document.getElementById("upload-section").scrollIntoView({ behavior: "smooth" });
}

function showLookupError(message) {
    currentPatient = null;
    
    document.getElementById("lookup-result").classList.remove("hidden");
    document.getElementById("lookup-success").classList.add("hidden");
    document.getElementById("lookup-error").classList.remove("hidden");
    document.getElementById("lookup-error-text").textContent = message;
    
    // Hide upload section
    document.getElementById("upload-section").classList.add("hidden");
}

// ==========================================
// Tab Navigation
// ==========================================

function setupTabs() {
    const tabBtns = document.querySelectorAll(".tab-btn");
    
    tabBtns.forEach(btn => {
        btn.addEventListener("click", function() {
            // Remove active from all tabs and tab contents
            tabBtns.forEach(b => b.classList.remove("active"));
            document.querySelectorAll(".tab-content").forEach(c => {
                c.classList.remove("active");
                c.classList.add("hidden");
            });
            
            // Activate clicked tab
            this.classList.add("active");
            const tabId = this.getAttribute("data-tab");
            const tabContent = document.getElementById(tabId);
            tabContent.classList.add("active");
            tabContent.classList.remove("hidden");
        });
    });
}

// ==========================================
// Form Handling
// ==========================================

function setupForms() {
    // Prescription form
    const rxForm = document.getElementById("assign-prescription-form");
    if (rxForm) {
        rxForm.addEventListener("submit", handleAssignPrescriptionSubmit);
    }
    
    // Legacy prescription form (if it existed) or just keep this structure clean
    // document.getElementById("prescription-form")?.addEventListener("submit", handlePrescriptionSubmit);
    
    // Report form
    document.getElementById("report-form").addEventListener("submit", handleReportSubmit);
    
    // Notes form
    document.getElementById("notes-form").addEventListener("submit", handleNotesSubmit);
    
    // Add another button
    document.getElementById("add-another-btn").addEventListener("click", function() {
        document.getElementById("upload-success").classList.add("hidden");
        document.getElementById("upload-section").classList.remove("hidden");
        resetForms();
    });
}

async function handleAssignPrescriptionSubmit(e) {
    e.preventDefault();
    
    if (!currentPatient) {
        showError("Please look up a patient first");
        return;
    }
    
    const days = document.getElementById("rx-days").value;
    const notes = document.getElementById("rx-notes").value.trim();
    
    const submitBtn = e.target.querySelector('button[type="submit"]');
    submitBtn.disabled = true;
    submitBtn.textContent = "Assigning...";
    
    try {
        const response = await authenticatedDoctorFetch(`${API_URL}/doctor/prescriptions`, {
            method: "POST",
            body: JSON.stringify({
                patient_email: currentPatient.email,
                notes: notes,
                total_days: parseInt(days)
            })
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.detail || "Assignment failed");
        }
        
        showUploadSuccess("Prescription assigned successfully! The patient has been notified.");
        
    } catch (error) {
        showError(error.message);
    } finally {
        submitBtn.disabled = false;
        submitBtn.textContent = "💊 Assign & Track Progress";
    }
}

async function handleReportSubmit(e) {
    e.preventDefault();
    
    if (!currentPatient) {
        showError("Please look up a patient first");
        return;
    }
    
    const title = document.getElementById("report-title").value.trim();
    const category = document.getElementById("report-category").value;
    const fileInput = document.getElementById("report-file");
    const description = document.getElementById("report-description").value.trim();
    
    if (!fileInput.files.length) {
        showError("Please select a file to upload");
        return;
    }
    
    const submitBtn = e.target.querySelector('button[type="submit"]');
    submitBtn.disabled = true;
    submitBtn.textContent = "Uploading...";
    
    try {
        const formData = new FormData();
        formData.append("patient_email", currentPatient.email);
        formData.append("file", fileInput.files[0]);
        formData.append("title", title);
        formData.append("category", category);
        if (description) {
            formData.append("description", description);
        }
        
        const response = await authenticatedDoctorFetch(`${API_URL}/doctor/upload/file`, {
            method: "POST",
            body: formData
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.detail || "Upload failed");
        }
        
        showUploadSuccess(data.message);
        
    } catch (error) {
        showError(error.message);
    } finally {
        submitBtn.disabled = false;
        submitBtn.textContent = "📤 Upload Report";
    }
}

async function handleNotesSubmit(e) {
    e.preventDefault();
    
    if (!currentPatient) {
        showError("Please look up a patient first");
        return;
    }
    
    const title = document.getElementById("notes-title").value.trim();
    const content = document.getElementById("notes-content").value.trim();
    
    const submitBtn = e.target.querySelector('button[type="submit"]');
    submitBtn.disabled = true;
    submitBtn.textContent = "Saving...";
    
    try {
        const response = await authenticatedDoctorFetch(`${API_URL}/doctor/upload/text`, {
            method: "POST",
            body: JSON.stringify({
                patient_email: currentPatient.email,
                title: title,
                category: "doctor_note",
                text_content: content
            })
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.detail || "Upload failed");
        }
        
        showUploadSuccess(data.message);
        
    } catch (error) {
        showError(error.message);
    } finally {
        submitBtn.disabled = false;
        submitBtn.textContent = "📤 Save Notes";
    }
}

function resetForms() {
    document.getElementById("assign-prescription-form").reset();
    document.getElementById("report-form").reset();
    document.getElementById("notes-form").reset();
    
    // Reset file selection display
    document.querySelector("#report-drop-zone .file-upload-prompt").classList.remove("hidden");
    document.querySelector("#report-drop-zone .file-selected").classList.add("hidden");
}

// ==========================================
// File Upload UI
// ==========================================

function setupFileUpload() {
    const dropZone = document.getElementById("report-drop-zone");
    const fileInput = document.getElementById("report-file");
    const removeBtn = document.getElementById("remove-report-file");
    
    // Click to select
    dropZone.addEventListener("click", function(e) {
        if (e.target.id !== "remove-report-file") {
            fileInput.click();
        }
    });
    
    // File selected
    fileInput.addEventListener("change", function() {
        if (this.files.length > 0) {
            showSelectedFile(this.files[0]);
        }
    });
    
    // Remove file
    removeBtn.addEventListener("click", function(e) {
        e.stopPropagation();
        fileInput.value = "";
        document.querySelector("#report-drop-zone .file-upload-prompt").classList.remove("hidden");
        document.querySelector("#report-drop-zone .file-selected").classList.add("hidden");
    });
    
    // Drag and drop
    dropZone.addEventListener("dragover", function(e) {
        e.preventDefault();
        this.classList.add("drag-over");
    });
    
    dropZone.addEventListener("dragleave", function() {
        this.classList.remove("drag-over");
    });
    
    dropZone.addEventListener("drop", function(e) {
        e.preventDefault();
        this.classList.remove("drag-over");
        
        if (e.dataTransfer.files.length > 0) {
            fileInput.files = e.dataTransfer.files;
            showSelectedFile(e.dataTransfer.files[0]);
        }
    });
}

function showSelectedFile(file) {
    document.getElementById("selected-report-name").textContent = file.name;
    document.querySelector("#report-drop-zone .file-upload-prompt").classList.add("hidden");
    document.querySelector("#report-drop-zone .file-selected").classList.remove("hidden");
}

// ==========================================
// UI Feedback
// ==========================================

function showUploadSuccess(message) {
    document.getElementById("upload-section").classList.add("hidden");
    document.getElementById("upload-success").classList.remove("hidden");
    document.getElementById("success-message").textContent = message;
    
    // Scroll to success message
    document.getElementById("upload-success").scrollIntoView({ behavior: "smooth" });
}

function showError(message) {
    const errorSection = document.getElementById("error");
    document.getElementById("error-text").textContent = message;
    errorSection.classList.remove("hidden");
    
    setTimeout(() => {
        errorSection.classList.add("hidden");
    }, 5000);
}
