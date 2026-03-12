/**
 * Authentication Helper Functions
 * ================================
 * Shared authentication utilities for all pages.
 * Handles JWT token storage and authenticated API requests.
 */

// ==========================================
// Configuration
// ==========================================
const API_URL = "http://localhost:8000";
const TOKEN_KEY = "health_assistant_token";
const USER_KEY = "health_assistant_user";

// ==========================================
// Token Management
// ==========================================

/**
 * Save authentication data to localStorage
 */
function saveAuthData(token, user) {
    localStorage.setItem(TOKEN_KEY, token);
    localStorage.setItem(USER_KEY, JSON.stringify(user));
}

/**
 * Get JWT token from localStorage
 */
function getToken() {
    return localStorage.getItem(TOKEN_KEY);
}

/**
 * Get user data from localStorage
 */
function getUser() {
    const userData = localStorage.getItem(USER_KEY);
    return userData ? JSON.parse(userData) : null;
}

/**
 * Check if user is logged in
 */
function isLoggedIn() {
    return getToken() !== null;
}

/**
 * Clear authentication data and redirect to home
 */
function logout() {
    localStorage.removeItem(TOKEN_KEY);
    localStorage.removeItem(USER_KEY);
    window.location.href = 'home.html';
}

/**
 * Require authentication - redirect to login if not authenticated
 */
function requireAuth() {
    if (!isLoggedIn()) {
        window.location.href = 'login.html';
    }
}

// ==========================================
// Authenticated Fetch
// ==========================================

/**
 * Make an authenticated API request with JWT token
 * @param {string} url - API endpoint URL
 * @param {object} options - Fetch options (method, body, etc.)
 * @returns {Promise<Response>} - Fetch response
 */
async function authenticatedFetch(url, options = {}) {
    const token = getToken();
    
    if (!token) {
        // Redirect to login if no token
        window.location.href = 'login.html';
        throw new Error('Not authenticated');
    }
    
    // Add Authorization header
    const headers = {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
        ...options.headers,
    };
    
    const response = await fetch(url, {
        ...options,
        headers,
    });
    
    // If unauthorized, clear token and redirect to login
    if (response.status === 401) {
        logout();
        throw new Error('Session expired. Please login again.');
    }
    
    return response;
}
