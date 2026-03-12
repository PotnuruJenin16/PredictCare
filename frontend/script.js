/**
 * Predict Care - Frontend JavaScript
 * ===================================
 * Handles user interaction and API communication.
 * Uses Fetch API for HTTP requests with JWT authentication.
 * 
 * Note: auth.js must be loaded before this file.
 * It provides: API_URL, requireAuth, getUser, logout, authenticatedFetch
 * 
 * Author: Predict Care
 */

// ==========================================
// Check Authentication on Page Load
// ==========================================
document.addEventListener("DOMContentLoaded", function() {
    // Require authentication
    requireAuth();
    
    // Set user name in header
    const user = getUser();
    if (user) {
        const userNameEl = document.getElementById("user-name");
        if (userNameEl) {
            userNameEl.textContent = user.name;
        }
    }
    
    // Add logout button handler
    const logoutBtn = document.getElementById("logout-btn");
    if (logoutBtn) {
        logoutBtn.addEventListener("click", function(e) {
            e.preventDefault();
            logout();
        });
    }
    
    // Check API health
    checkAPIHealth();
});

// ==========================================
// DOM Elements
// ==========================================
const symptomsInput = document.getElementById("symptoms-input");
const predictBtn = document.getElementById("predict-btn");
const loadingDiv = document.getElementById("loading");
const resultsSection = document.getElementById("results");
const errorSection = document.getElementById("error");

// Result elements
const diseaseNameEl = document.getElementById("disease-name");
const riskLevelEl = document.getElementById("risk-level");
const confidenceFillEl = document.getElementById("confidence-fill");
const confidenceTextEl = document.getElementById("confidence-text");
const messageBoxEl = document.getElementById("message-box");
const messageTextEl = document.getElementById("message-text");
const errorTextEl = document.getElementById("error-text");

// Precautions elements
const precautionsSectionEl = document.getElementById("precautions-section");
const adviceBadgeEl = document.getElementById("advice-badge");
const precautionsListEl = document.getElementById("precautions-list");
const dosListEl = document.getElementById("dos-list");
const dontsListEl = document.getElementById("donts-list");
const consultListEl = document.getElementById("consult-list");
const precautionsDisclaimerEl = document.getElementById("precautions-disclaimer");

// Doctors elements
const doctorsSectionEl = document.getElementById("doctors-section");
const doctorsListEl = document.getElementById("doctors-list");

// ==========================================
// Main Prediction Function
// ==========================================

/**
 * Main function called when user clicks "Analyze Symptoms"
 * 1. Validates input
 * 2. Sends POST request to /predict endpoint
 * 3. Displays results or error
 */
async function predictDisease() {
    // Get symptom text from textarea
    const symptoms = symptomsInput.value.trim();
    
    // ========================================
    // Input Validation
    // ========================================
    if (!symptoms) {
        showError("Please enter your symptoms before analyzing.");
        return;
    }
    
    if (symptoms.length < 3) {
        showError("Please enter more detailed symptoms.");
        return;
    }
    
    // ========================================
    // Show Loading State
    // ========================================
    showLoading(true);
    hideResults();
    hideError();
    
    try {
        // ========================================
        // API Request using Fetch with JWT
        // ========================================
        const response = await authenticatedFetch(`${API_URL}/predict`, {
            method: "POST",
            body: JSON.stringify({ symptoms: symptoms }),
        });
        
        // Check for HTTP errors
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || "Prediction failed");
        }
        
        // Parse JSON response
        const data = await response.json();
        
        // ========================================
        // Display Results
        // ========================================
        displayResults(data);
        
    } catch (error) {
        // ========================================
        // Handle Errors
        // ========================================
        console.error("Prediction error:", error);
        
        // Check if it's a network error (API not running)
        if (error.message === "Failed to fetch") {
            showError(
                "Cannot connect to the server. Please make sure the backend is running:\n" +
                "1. Open terminal in backend folder\n" +
                "2. Run: uvicorn main:app --reload --port 8000"
            );
        } else {
            showError(error.message || "An error occurred. Please try again.");
        }
    } finally {
        // Always hide loading spinner
        showLoading(false);
    }
}

// ==========================================
// Display Functions
// ==========================================

/**
 * Display prediction results on the page
 * @param {Object} data - Response from API
 */
function displayResults(data) {
    // Set disease name
    diseaseNameEl.textContent = data.disease;
    
    // Set risk level with appropriate styling
    riskLevelEl.textContent = data.risk;
    riskLevelEl.className = "value risk-badge"; // Reset classes
    
    // Add risk-specific class for styling
    switch (data.risk) {
        case "LOW":
            riskLevelEl.classList.add("risk-low");
            break;
        case "MEDIUM":
            riskLevelEl.classList.add("risk-medium");
            break;
        case "HIGH":
            riskLevelEl.classList.add("risk-high");
            break;
    }
    
    // Set confidence bar and text
    const confidencePercent = Math.round(data.confidence * 100);
    confidenceFillEl.style.width = `${confidencePercent}%`;
    confidenceTextEl.textContent = `${confidencePercent}%`;
    
    // Update confidence bar color based on level
    if (confidencePercent >= 70) {
        confidenceFillEl.style.background = "#10b981"; // Green
    } else if (confidencePercent >= 40) {
        confidenceFillEl.style.background = "#f59e0b"; // Orange
    } else {
        confidenceFillEl.style.background = "#ef4444"; // Red
    }
    
    // Show/hide warning message
    if (data.message && data.message.length > 0) {
        messageTextEl.textContent = data.message;
        messageBoxEl.classList.remove("hidden");
    } else {
        messageBoxEl.classList.add("hidden");
    }
    
    // ========================================
    // Display Precautionary Advice
    // ========================================
    if (data.precautions && data.precautions.length > 0) {
        displayPrecautions(data);
    }
    
    // ========================================
    // Display Doctor Recommendations
    // ========================================
    if (data.recommended_doctors && data.recommended_doctors.length > 0) {
        displayDoctors(data.recommended_doctors);
    }
    
    // Show results section
    resultsSection.classList.remove("hidden");
    
    // Smooth scroll to results
    resultsSection.scrollIntoView({ behavior: "smooth", block: "nearest" });
}

/**
 * Display precautionary advice section
 * @param {Object} data - Prediction response with precautions
 */
function displayPrecautions(data) {
    // Set advice level badge
    if (adviceBadgeEl) {
        adviceBadgeEl.textContent = data.advice_level.toUpperCase() + " URGENCY";
        adviceBadgeEl.className = "advice-badge";
        adviceBadgeEl.classList.add(`advice-${data.advice_level}`);
    }
    
    // Populate precautions list
    if (precautionsListEl && data.precautions) {
        precautionsListEl.innerHTML = data.precautions
            .map(p => `<li>${escapeHtml(p)}</li>`)
            .join("");
    }
    
    // Populate Do's list
    if (dosListEl && data.dos) {
        dosListEl.innerHTML = data.dos
            .map(d => `<li>${escapeHtml(d)}</li>`)
            .join("");
    }
    
    // Populate Don'ts list
    if (dontsListEl && data.donts) {
        dontsListEl.innerHTML = data.donts
            .map(d => `<li>${escapeHtml(d)}</li>`)
            .join("");
    }
    
    // Populate consult doctor list
    if (consultListEl && data.consult_when) {
        consultListEl.innerHTML = data.consult_when
            .map(c => `<li>${escapeHtml(c)}</li>`)
            .join("");
    }
    
    // Set disclaimer
    if (precautionsDisclaimerEl && data.disclaimer) {
        precautionsDisclaimerEl.textContent = data.disclaimer;
    }
    
    // Show precautions section
    if (precautionsSectionEl) {
        precautionsSectionEl.classList.remove("hidden");
    }
}

/**
 * Display doctor recommendations section
 * @param {Array} doctors - Array of recommended doctors
 */
function displayDoctors(doctors) {
    if (!doctorsListEl || !doctorsSectionEl) return;
    
    doctorsListEl.innerHTML = doctors.map(d => `
        <div class="doctor-card">
            <div class="doctor-header">
                <h4>${escapeHtml(d.name)}</h4>
                <span class="doctor-specialization">${escapeHtml(d.specialization)}</span>
            </div>
            <div class="doctor-details">
                <p class="doctor-info">
                    <span class="info-icon">📍</span>
                    ${escapeHtml(d.location)}
                </p>
                <p class="doctor-info">
                    <span class="info-icon">📞</span>
                    <a href="tel:${d.contact.replace(/\\s/g, '')}">${escapeHtml(d.contact)}</a>
                </p>
                <p class="doctor-info">
                    <span class="info-icon">🕐</span>
                    ${escapeHtml(d.availability)}
                </p>
                <p class="doctor-info">
                    <span class="info-icon">💰</span>
                    ${escapeHtml(d.consultation_fee)}
                </p>
                ${d.experience ? `
                <p class="doctor-info">
                    <span class="info-icon">⭐</span>
                    ${escapeHtml(d.experience)} experience
                </p>
                ` : ''}
            </div>
        </div>
    `).join("");
    
    doctorsSectionEl.classList.remove("hidden");
}

/**
 * Escape HTML to prevent XSS
 */
function escapeHtml(text) {
    const div = document.createElement("div");
    div.textContent = text;
    return div.innerHTML;
}

/**
 * Show error message
 * @param {string} message - Error message to display
 */
function showError(message) {
    errorTextEl.textContent = message;
    errorSection.classList.remove("hidden");
    
    // Scroll to error
    errorSection.scrollIntoView({ behavior: "smooth", block: "nearest" });
}

/**
 * Hide error section
 */
function hideError() {
    errorSection.classList.add("hidden");
}

/**
 * Hide results section
 */
function hideResults() {
    resultsSection.classList.add("hidden");
    // Also hide precautions section
    if (precautionsSectionEl) {
        precautionsSectionEl.classList.add("hidden");
    }
    // Also hide doctors section
    if (doctorsSectionEl) {
        doctorsSectionEl.classList.add("hidden");
    }
}

/**
 * Show/hide loading spinner
 * @param {boolean} show - Whether to show loading
 */
function showLoading(show) {
    if (show) {
        loadingDiv.classList.remove("hidden");
        predictBtn.disabled = true;
        predictBtn.textContent = "Analyzing...";
    } else {
        loadingDiv.classList.add("hidden");
        predictBtn.disabled = false;
        predictBtn.textContent = "🔍 Analyze Symptoms";
    }
}

// ==========================================
// Event Listeners
// ==========================================

// Button click event
if (predictBtn) {
    predictBtn.addEventListener("click", predictDisease);
}

// Allow pressing Enter to submit (with Ctrl or Cmd)
if (symptomsInput) {
    symptomsInput.addEventListener("keydown", function(event) {
        if ((event.ctrlKey || event.metaKey) && event.key === "Enter") {
            predictDisease();
        }
    });

    // Clear error when user starts typing
    symptomsInput.addEventListener("input", function() {
        hideError();
    });
}

// ==========================================
// Health Check on Page Load
// ==========================================

/**
 * Check if backend API is running when page loads
 */
async function checkAPIHealth() {
    try {
        const response = await fetch(`${API_URL}/health`);
        const data = await response.json();
        
        if (data.status === "error" || !data.model_loaded) {
            console.warn("⚠️ Model not loaded:", data.message);
        } else {
            console.log("✅ API is healthy and model is loaded");
        }
    } catch (error) {
        console.warn(
            "⚠️ Backend API not reachable. Make sure to start the server:\n" +
            "   cd backend && uvicorn main:app --reload --port 8000"
        );
    }
}

// ==========================================
// Location Section
// ==========================================

const LOCATION_STORAGE_KEY = "predictcare_user_location";

const locationBtn = document.getElementById("location-btn");
const locationStatus = document.getElementById("location-status");
const locationStatusIcon = document.getElementById("location-status-icon");
const locationStatusText = document.getElementById("location-status-text");
const locationDetails = document.getElementById("location-details");
const locationLat = document.getElementById("location-lat");
const locationLng = document.getElementById("location-lng");
const locationMapFrame = document.getElementById("location-map-frame");

/**
 * Set the location status UI
 */
function setLocationStatus(icon, text, statusClass) {
    if (!locationStatus) return;
    locationStatusIcon.textContent = icon;
    locationStatusText.textContent = text;
    locationStatus.className = "location-status" + (statusClass ? " " + statusClass : "");
}

/**
 * Display location data on the page (coords + map)
 */
function showLocationOnPage(lat, lng) {
    if (!locationDetails) return;
    locationLat.textContent = lat.toFixed(5);
    locationLng.textContent = lng.toFixed(5);
    // Use OpenStreetMap embed (no API key required)
    locationMapFrame.src =
        "https://www.openstreetmap.org/export/embed.html?bbox=" +
        (lng - 0.01) + "," + (lat - 0.01) + "," +
        (lng + 0.01) + "," + (lat + 0.01) +
        "&layer=mapnik&marker=" + lat + "," + lng;
    locationDetails.classList.remove("hidden");
}

/**
 * Save location to localStorage
 */
function saveLocation(lat, lng) {
    try {
        localStorage.setItem(LOCATION_STORAGE_KEY, JSON.stringify({ lat, lng, ts: Date.now() }));
    } catch (_) { /* ignore quota errors */ }
}

/**
 * Load saved location from localStorage
 */
function loadSavedLocation() {
    try {
        const raw = localStorage.getItem(LOCATION_STORAGE_KEY);
        if (raw) return JSON.parse(raw);
    } catch (_) { /* ignore */ }
    return null;
}

/**
 * Request the user's current geolocation
 */
function requestLocation() {
    if (!navigator.geolocation) {
        setLocationStatus("❌", "Geolocation is not supported by your browser.", "status-error");
        locationBtn.textContent = "📍 Not Supported";
        locationBtn.disabled = true;
        return;
    }

    setLocationStatus("⏳", "Requesting your location…", "status-loading");
    locationBtn.disabled = true;
    locationBtn.textContent = "Locating…";

    navigator.geolocation.getCurrentPosition(
        function onSuccess(position) {
            const lat = position.coords.latitude;
            const lng = position.coords.longitude;
            saveLocation(lat, lng);
            showLocationOnPage(lat, lng);
            setLocationStatus("✅", "Location updated successfully.", "status-success");
            locationBtn.textContent = "🔄 Refresh Location";
            locationBtn.disabled = false;
        },
        function onError(err) {
            let msg;
            switch (err.code) {
                case err.PERMISSION_DENIED:
                    msg = "Location access was denied. You can grant permission in your browser settings.";
                    break;
                case err.POSITION_UNAVAILABLE:
                    msg = "Location information is currently unavailable.";
                    break;
                case err.TIMEOUT:
                    msg = "The location request timed out. Please try again.";
                    break;
                default:
                    msg = "An unknown error occurred while fetching location.";
            }
            setLocationStatus("⚠️", msg, "status-error");
            locationBtn.textContent = "🔄 Try Again";
            locationBtn.disabled = false;
        },
        { enableHighAccuracy: true, timeout: 10000, maximumAge: 60000 }
    );
}

// Initialise location section on page load
(function initLocation() {
    if (!locationBtn) return;

    // If we have a saved location, show it immediately
    const saved = loadSavedLocation();
    if (saved && saved.lat != null && saved.lng != null) {
        showLocationOnPage(saved.lat, saved.lng);
        setLocationStatus("📌", "Showing your last known location. Refreshing…", "status-loading");
        locationBtn.textContent = "🔄 Refresh Location";
        // Silently attempt a live refresh
        requestLocation();
    }

    locationBtn.addEventListener("click", requestLocation);
})();
