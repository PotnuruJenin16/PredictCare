/**
 * Notifications Module
 * ====================
 * Handles in-app notification display and management.
 * Works with the backend notification API.
 */

// ==========================================
// DOM Elements
// ==========================================
let notificationBadge = null;
let notificationPanel = null;
let notificationList = null;
let notificationBtn = null;
let markAllReadBtn = null;

// ==========================================
// State
// ==========================================
let notificationsPanelOpen = false;

// ==========================================
// Initialize Notifications
// ==========================================
function initNotifications() {
    notificationBadge = document.getElementById("notification-badge");
    notificationPanel = document.getElementById("notification-panel");
    notificationList = document.getElementById("notification-list");
    notificationBtn = document.getElementById("notifications-btn");
    markAllReadBtn = document.getElementById("mark-all-read");
    
    if (notificationBtn) {
        notificationBtn.addEventListener("click", toggleNotificationPanel);
    }
    
    if (markAllReadBtn) {
        markAllReadBtn.addEventListener("click", markAllNotificationsRead);
    }
    
    // Close panel when clicking outside
    document.addEventListener("click", function(e) {
        if (notificationsPanelOpen && 
            notificationPanel && 
            !notificationPanel.contains(e.target) &&
            notificationBtn &&
            !notificationBtn.contains(e.target)) {
            closeNotificationPanel();
        }
    });
    
    // Load notifications if logged in
    if (isLoggedIn()) {
        loadNotifications();
        // Poll for new notifications every 30 seconds
        setInterval(loadNotifications, 30000);
    }
}

// ==========================================
// API Functions
// ==========================================

/**
 * Load notifications from the server
 */
async function loadNotifications() {
    if (!isLoggedIn()) return;
    
    try {
        const response = await authenticatedFetch(`${API_URL}/notifications`);
        
        if (!response.ok) {
            console.error("Failed to load notifications");
            return;
        }
        
        const data = await response.json();
        
        // Update badge
        updateNotificationBadge(data.unread_count);
        
        // Update list if panel is open
        if (notificationsPanelOpen) {
            renderNotifications(data.notifications);
        }
        
    } catch (error) {
        console.error("Error loading notifications:", error);
    }
}

/**
 * Mark a single notification as read
 */
async function markNotificationRead(notificationId) {
    try {
        const response = await authenticatedFetch(
            `${API_URL}/notifications/${notificationId}/read`,
            { method: "POST" }
        );
        
        if (response.ok) {
            // Reload notifications to update UI
            loadNotifications();
        }
    } catch (error) {
        console.error("Error marking notification as read:", error);
    }
}

/**
 * Mark all notifications as read
 */
async function markAllNotificationsRead(e) {
    if (e) e.preventDefault();
    
    try {
        const response = await authenticatedFetch(
            `${API_URL}/notifications/read-all`,
            { method: "POST" }
        );
        
        if (response.ok) {
            loadNotifications();
        }
    } catch (error) {
        console.error("Error marking all notifications as read:", error);
    }
}

/**
 * Delete a notification
 */
async function deleteNotification(notificationId) {
    try {
        const response = await authenticatedFetch(
            `${API_URL}/notifications/${notificationId}`,
            { method: "DELETE" }
        );
        
        if (response.ok) {
            loadNotifications();
        }
    } catch (error) {
        console.error("Error deleting notification:", error);
    }
}

// ==========================================
// UI Functions
// ==========================================

/**
 * Toggle notification panel visibility
 */
function toggleNotificationPanel(e) {
    if (e) e.preventDefault();
    
    if (notificationsPanelOpen) {
        closeNotificationPanel();
    } else {
        openNotificationPanel();
    }
}

/**
 * Open notification panel
 */
async function openNotificationPanel() {
    if (!notificationPanel) return;
    
    // Load fresh notifications
    await loadNotificationsForPanel();
    
    notificationPanel.classList.remove("hidden");
    notificationsPanelOpen = true;
}

/**
 * Close notification panel
 */
function closeNotificationPanel() {
    if (!notificationPanel) return;
    
    notificationPanel.classList.add("hidden");
    notificationsPanelOpen = false;
}

/**
 * Load and render notifications in panel
 */
async function loadNotificationsForPanel() {
    if (!isLoggedIn()) return;
    
    try {
        const response = await authenticatedFetch(`${API_URL}/notifications`);
        
        if (!response.ok) return;
        
        const data = await response.json();
        renderNotifications(data.notifications);
        updateNotificationBadge(data.unread_count);
        
    } catch (error) {
        console.error("Error loading notifications for panel:", error);
    }
}

/**
 * Update the notification badge count
 */
function updateNotificationBadge(count) {
    if (!notificationBadge) return;
    
    if (count > 0) {
        notificationBadge.textContent = count > 99 ? "99+" : count;
        notificationBadge.classList.remove("hidden");
    } else {
        notificationBadge.classList.add("hidden");
    }
}

/**
 * Render notifications in the panel
 */
function renderNotifications(notifications) {
    if (!notificationList) return;
    
    if (notifications.length === 0) {
        notificationList.innerHTML = `
            <div class="notification-empty">
                <p>📭 No notifications yet</p>
            </div>
        `;
        return;
    }
    
    notificationList.innerHTML = notifications.map(n => `
        <div class="notification-item ${n.read ? 'read' : 'unread'}" data-id="${n.id}">
            <div class="notification-icon">${n.icon}</div>
            <div class="notification-content">
                <div class="notification-title">${escapeHtml(n.title)}</div>
                <div class="notification-message">${escapeHtml(n.message)}</div>
                <div class="notification-time">${formatTimeAgo(n.created_at)}</div>
            </div>
            <div class="notification-actions">
                ${!n.read ? `<button class="btn-icon" onclick="markNotificationRead(${n.id})" title="Mark as read">✓</button>` : ''}
                <button class="btn-icon" onclick="deleteNotification(${n.id})" title="Delete">×</button>
            </div>
        </div>
    `).join("");
}

/**
 * Format time ago (e.g., "5 minutes ago")
 */
function formatTimeAgo(isoString) {
    const date = new Date(isoString);
    const now = new Date();
    const seconds = Math.floor((now - date) / 1000);
    
    if (seconds < 60) return "Just now";
    if (seconds < 3600) return `${Math.floor(seconds / 60)} min ago`;
    if (seconds < 86400) return `${Math.floor(seconds / 3600)} hours ago`;
    if (seconds < 604800) return `${Math.floor(seconds / 86400)} days ago`;
    
    return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
}

/**
 * Escape HTML to prevent XSS
 */
function escapeHtml(text) {
    if (!text) return "";
    const div = document.createElement("div");
    div.textContent = text;
    return div.innerHTML;
}

// ==========================================
// Initialize on page load
// ==========================================
document.addEventListener("DOMContentLoaded", function() {
    // Only initialize if we're on a page with notifications
    if (document.getElementById("notification-badge")) {
        initNotifications();
    }
});
