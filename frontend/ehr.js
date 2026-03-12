/**
 * EHR (Electronic Health Records) Module - Frontend JavaScript
 * =============================================================
 * Handles EHR record management, file uploads, and display.
 * 
 * Features:
 * - List all EHR records with filtering
 * - Upload files (prescriptions, reports, scans)
 * - Add text-based notes (OP notes, doctor notes)
 * - View and download records
 * - Delete/archive records
 * 
 * Note: auth.js and notifications.js must be loaded before this file.
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
    
    // Initialize notifications
    if (typeof initNotifications === 'function') {
        initNotifications();
    }
    
    // Initialize EHR functionality
    initEHR();
});

// ==========================================
// State
// ==========================================
let allRecords = [];
let currentRecord = null;

// ==========================================
// DOM Elements
// ==========================================
const loadingEl = document.getElementById("loading");
const ehrSectionEl = document.getElementById("ehr-section");
const ehrListEl = document.getElementById("ehr-list");
const emptyStateEl = document.getElementById("empty-state");
const errorSectionEl = document.getElementById("error");
const errorTextEl = document.getElementById("error-text");
const statsSectionEl = document.getElementById("stats-section");

// Filter elements
const categoryFilterEl = document.getElementById("category-filter");
const showArchivedEl = document.getElementById("show-archived");

// Modal elements
const uploadModalEl = document.getElementById("upload-modal");
const viewModalEl = document.getElementById("view-modal");

// ==========================================
// Initialization
// ==========================================
function initEHR() {
    // Load records
    loadEHRRecords();
    
    // Setup event listeners
    setupEventListeners();
}

function setupEventListeners() {
    // Upload buttons
    document.getElementById("upload-btn")?.addEventListener("click", openUploadModal);
    document.getElementById("empty-upload-btn")?.addEventListener("click", openUploadModal);
    
    // Modal close buttons
    document.getElementById("close-modal")?.addEventListener("click", closeUploadModal);
    document.getElementById("close-view-modal")?.addEventListener("click", closeViewModal);
    
    // Close modals when clicking outside
    uploadModalEl?.addEventListener("click", (e) => {
        if (e.target === uploadModalEl) closeUploadModal();
    });
    viewModalEl?.addEventListener("click", (e) => {
        if (e.target === viewModalEl) closeViewModal();
    });
    
    // Tab switching
    document.querySelectorAll(".tab-btn").forEach(btn => {
        btn.addEventListener("click", () => switchTab(btn.dataset.tab));
    });
    
    // File input and drag/drop
    setupFileUpload();
    
    // Form submissions
    document.getElementById("file-upload-form")?.addEventListener("submit", handleFileUpload);
    document.getElementById("text-record-form")?.addEventListener("submit", handleTextRecord);
    
    // Filters
    categoryFilterEl?.addEventListener("change", filterRecords);
    showArchivedEl?.addEventListener("change", loadEHRRecords);
    
    // View modal actions
    document.getElementById("download-btn")?.addEventListener("click", downloadCurrentRecord);
    document.getElementById("delete-btn")?.addEventListener("click", deleteCurrentRecord);
}

// ==========================================
// API Functions
// ==========================================

async function loadEHRRecords() {
    showLoading(true);
    hideError();
    
    try {
        const includeArchived = showArchivedEl?.checked || false;
        const url = `${API_URL}/ehr?include_archived=${includeArchived}`;
        
        const response = await authenticatedFetch(url);
        
        if (!response.ok) {
            throw new Error("Failed to load health records");
        }
        
        const data = await response.json();
        allRecords = data.records;
        
        // Update statistics
        updateStatistics(data.statistics);
        
        // Apply current filter and render
        filterRecords();
        
    } catch (error) {
        console.error("Error loading EHR records:", error);
        showError(error.message || "Failed to load health records");
    } finally {
        showLoading(false);
    }
}

async function uploadFile(formData) {
    const response = await authenticatedFetch(`${API_URL}/ehr/upload`, {
        method: "POST",
        headers: {}, // Remove Content-Type to let browser set it with boundary
        body: formData
    });
    
    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || "Upload failed");
    }
    
    return await response.json();
}

async function createTextRecord(recordData) {
    const response = await authenticatedFetch(`${API_URL}/ehr/text`, {
        method: "POST",
        body: JSON.stringify(recordData)
    });
    
    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || "Failed to create record");
    }
    
    return await response.json();
}

async function deleteRecord(recordId, permanent = false) {
    const response = await authenticatedFetch(
        `${API_URL}/ehr/${recordId}?permanent=${permanent}`,
        { method: "DELETE" }
    );
    
    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || "Failed to delete record");
    }
    
    return await response.json();
}

// ==========================================
// UI Functions
// ==========================================

function updateStatistics(stats) {
    if (!stats) return;
    
    document.getElementById("total-records").textContent = stats.total_records || 0;
    document.getElementById("total-files").textContent = stats.file_count || 0;
    document.getElementById("total-size").textContent = stats.total_file_size_formatted || "0 KB";
    document.getElementById("prediction-count").textContent = 
        stats.by_category?.prediction || 0;
    
    statsSectionEl?.classList.remove("hidden");
}

function filterRecords() {
    const category = categoryFilterEl?.value || "all";
    
    let filtered = allRecords;
    
    if (category !== "all") {
        filtered = allRecords.filter(r => r.category === category);
    }
    
    renderRecords(filtered);
}

function renderRecords(records) {
    if (!ehrListEl) return;
    
    if (records.length === 0) {
        ehrSectionEl?.classList.add("hidden");
        emptyStateEl?.classList.remove("hidden");
        return;
    }
    
    emptyStateEl?.classList.add("hidden");
    ehrSectionEl?.classList.remove("hidden");
    
    ehrListEl.innerHTML = records.map(record => `
        <div class="ehr-record-card ${record.is_archived ? 'archived' : ''} ${record.uploaded_by_doctor ? 'doctor-uploaded' : ''}" data-id="${record.id}">
            <div class="ehr-record-icon">
                ${record.category_icon || '📄'}
            </div>
            <div class="ehr-record-info">
                <h4 class="ehr-record-title">${escapeHtml(record.title)}</h4>
                <div class="ehr-record-meta">
                    <span class="ehr-category-badge">${escapeHtml(record.category_name)}</span>
                    ${record.has_file ? `<span class="ehr-file-badge">📎 ${escapeHtml(record.file_type_name || 'File')}</span>` : ''}
                    ${record.is_archived ? '<span class="ehr-archived-badge">Archived</span>' : ''}
                    ${record.uploaded_by_doctor ? `<span class="ehr-doctor-badge">👨‍⚕️ From Doctor</span>` : ''}
                </div>
                ${record.uploaded_by_doctor && record.doctor_name ? `
                    <div class="ehr-doctor-info">
                        <span class="doctor-icon">👨‍⚕️</span>
                        Uploaded by: <strong>${escapeHtml(record.doctor_name)}</strong>
                    </div>
                ` : ''}
                <div class="ehr-record-date">
                    ${record.record_date ? `Record: ${formatDate(record.record_date)} • ` : ''}
                    Added: ${formatDate(record.created_at)}
                </div>
                ${record.description ? `<p class="ehr-record-desc">${escapeHtml(record.description)}</p>` : ''}
            </div>
            <div class="ehr-record-actions">
                <button class="btn-icon" onclick="viewRecord(${record.id})" title="View">👁️</button>
                ${record.has_file ? `<button class="btn-icon" onclick="downloadRecord(${record.id})" title="Download">📥</button>` : ''}
            </div>
        </div>
    `).join("");
}

function showLoading(show) {
    if (show) {
        loadingEl?.classList.remove("hidden");
        ehrSectionEl?.classList.add("hidden");
        emptyStateEl?.classList.add("hidden");
    } else {
        loadingEl?.classList.add("hidden");
    }
}

function showError(message) {
    if (errorTextEl) errorTextEl.textContent = message;
    errorSectionEl?.classList.remove("hidden");
}

function hideError() {
    errorSectionEl?.classList.add("hidden");
}

// ==========================================
// Modal Functions
// ==========================================

function openUploadModal() {
    uploadModalEl?.classList.remove("hidden");
    resetForms();
}

function closeUploadModal() {
    uploadModalEl?.classList.add("hidden");
    resetForms();
}

function openViewModal(record) {
    currentRecord = record;
    
    const titleEl = document.getElementById("view-modal-title");
    const bodyEl = document.getElementById("view-modal-body");
    const downloadBtn = document.getElementById("download-btn");
    
    if (titleEl) {
        titleEl.textContent = `${record.category_icon} ${record.title}`;
    }
    
    // Show/hide download button
    if (downloadBtn) {
        if (record.has_file) {
            downloadBtn.classList.remove("hidden");
        } else {
            downloadBtn.classList.add("hidden");
        }
    }
    
    // Build modal content
    if (bodyEl) {
        bodyEl.innerHTML = `
            <div class="view-record-details">
                <div class="detail-row">
                    <span class="detail-label">Category:</span>
                    <span class="detail-value">${escapeHtml(record.category_name)}</span>
                </div>
                ${record.record_date ? `
                <div class="detail-row">
                    <span class="detail-label">Record Date:</span>
                    <span class="detail-value">${formatDate(record.record_date)}</span>
                </div>
                ` : ''}
                <div class="detail-row">
                    <span class="detail-label">Added:</span>
                    <span class="detail-value">${formatDate(record.created_at)}</span>
                </div>
                ${record.has_file ? `
                <div class="detail-row">
                    <span class="detail-label">File:</span>
                    <span class="detail-value">${escapeHtml(record.file_name)} (${record.file_size_formatted})</span>
                </div>
                ` : ''}
                ${record.description ? `
                <div class="detail-row">
                    <span class="detail-label">Description:</span>
                    <span class="detail-value">${escapeHtml(record.description)}</span>
                </div>
                ` : ''}
            </div>
            
            ${record.text_content ? `
            <div class="view-record-content">
                <h4>Content:</h4>
                <pre class="record-text-content">${escapeHtml(record.text_content)}</pre>
            </div>
            ` : ''}
            
            ${record.has_file && isImageFile(record.file_type) ? `
            <div class="view-record-preview">
                <h4>Preview:</h4>
                <div id="image-preview-container">
                    <p class="loading-preview">Loading preview...</p>
                </div>
            </div>
            ` : ''}
            
            ${record.has_file && isPdfFile(record.file_type) ? `
            <div class="view-record-preview">
                <h4>Preview:</h4>
                <div id="pdf-preview-container">
                    <p class="loading-preview">Loading preview...</p>
                </div>
            </div>
            ` : ''}
        `;
        
        // Load image preview with authentication
        if (record.has_file && isImageFile(record.file_type)) {
            loadImagePreview(record.id);
        }
        
        // Load PDF preview with authentication
        if (record.has_file && isPdfFile(record.file_type)) {
            loadPdfPreview(record.id);
        }
    }
    
    viewModalEl?.classList.remove("hidden");
}

function closeViewModal() {
    viewModalEl?.classList.add("hidden");
    currentRecord = null;
}

function switchTab(tabName) {
    // Update tab buttons
    document.querySelectorAll(".tab-btn").forEach(btn => {
        btn.classList.toggle("active", btn.dataset.tab === tabName);
    });
    
    // Update tab content
    document.querySelectorAll(".tab-content").forEach(content => {
        content.classList.toggle("active", content.id === `${tabName}-tab`);
        content.classList.toggle("hidden", content.id !== `${tabName}-tab`);
    });
}

function resetForms() {
    document.getElementById("file-upload-form")?.reset();
    document.getElementById("text-record-form")?.reset();
    
    // Reset file selection display
    const dropZone = document.getElementById("file-drop-zone");
    if (dropZone) {
        dropZone.querySelector(".file-upload-prompt")?.classList.remove("hidden");
        dropZone.querySelector(".file-selected")?.classList.add("hidden");
    }
    
    // Reset to first tab
    switchTab("file");
}

// ==========================================
// File Upload Handling
// ==========================================

let selectedFile = null;

function setupFileUpload() {
    const fileInput = document.getElementById("file-input");
    const dropZone = document.getElementById("file-drop-zone");
    const removeBtn = document.getElementById("remove-file");
    
    if (!fileInput || !dropZone) return;
    
    // Click to select file
    dropZone.addEventListener("click", () => fileInput.click());
    
    // File selected via input
    fileInput.addEventListener("change", (e) => {
        if (e.target.files.length > 0) {
            handleFileSelection(e.target.files[0]);
        }
    });
    
    // Drag and drop
    dropZone.addEventListener("dragover", (e) => {
        e.preventDefault();
        dropZone.classList.add("drag-over");
    });
    
    dropZone.addEventListener("dragleave", () => {
        dropZone.classList.remove("drag-over");
    });
    
    dropZone.addEventListener("drop", (e) => {
        e.preventDefault();
        dropZone.classList.remove("drag-over");
        
        if (e.dataTransfer.files.length > 0) {
            handleFileSelection(e.dataTransfer.files[0]);
        }
    });
    
    // Remove file
    removeBtn?.addEventListener("click", (e) => {
        e.stopPropagation();
        clearFileSelection();
    });
}

function handleFileSelection(file) {
    // Validate file size (10 MB)
    if (file.size > 10 * 1024 * 1024) {
        alert("File too large. Maximum size is 10 MB.");
        return;
    }
    
    selectedFile = file;
    
    const dropZone = document.getElementById("file-drop-zone");
    const fileNameEl = document.getElementById("selected-file-name");
    
    if (dropZone && fileNameEl) {
        dropZone.querySelector(".file-upload-prompt")?.classList.add("hidden");
        dropZone.querySelector(".file-selected")?.classList.remove("hidden");
        fileNameEl.textContent = file.name;
    }
}

function clearFileSelection() {
    selectedFile = null;
    
    const fileInput = document.getElementById("file-input");
    const dropZone = document.getElementById("file-drop-zone");
    
    if (fileInput) fileInput.value = "";
    
    if (dropZone) {
        dropZone.querySelector(".file-upload-prompt")?.classList.remove("hidden");
        dropZone.querySelector(".file-selected")?.classList.add("hidden");
    }
}

// ==========================================
// Form Handlers
// ==========================================

async function handleFileUpload(e) {
    e.preventDefault();
    
    if (!selectedFile) {
        alert("Please select a file to upload.");
        return;
    }
    
    const title = document.getElementById("file-title").value.trim();
    const category = document.getElementById("file-category").value;
    const description = document.getElementById("file-description").value.trim();
    const recordDate = document.getElementById("file-date").value;
    
    if (!title || !category) {
        alert("Please fill in all required fields.");
        return;
    }
    
    const submitBtn = document.getElementById("file-submit-btn");
    if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.textContent = "Uploading...";
    }
    
    try {
        const formData = new FormData();
        formData.append("file", selectedFile);
        formData.append("title", title);
        formData.append("category", category);
        if (description) formData.append("description", description);
        if (recordDate) formData.append("record_date", recordDate);
        
        // Custom fetch for file upload (no JSON content-type)
        const token = getToken();
        const response = await fetch(`${API_URL}/ehr/upload`, {
            method: "POST",
            headers: {
                "Authorization": `Bearer ${token}`
            },
            body: formData
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || "Upload failed");
        }
        
        // Success
        closeUploadModal();
        loadEHRRecords();
        
    } catch (error) {
        alert("Upload failed: " + error.message);
    } finally {
        if (submitBtn) {
            submitBtn.disabled = false;
            submitBtn.textContent = "📤 Upload Record";
        }
    }
}

async function handleTextRecord(e) {
    e.preventDefault();
    
    const title = document.getElementById("text-title").value.trim();
    const category = document.getElementById("text-category").value;
    const textContent = document.getElementById("text-content").value.trim();
    const recordDate = document.getElementById("text-date").value;
    
    if (!title || !category || !textContent) {
        alert("Please fill in all required fields.");
        return;
    }
    
    const submitBtn = document.getElementById("text-submit-btn");
    if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.textContent = "Saving...";
    }
    
    try {
        await createTextRecord({
            title,
            category,
            text_content: textContent,
            record_date: recordDate || null
        });
        
        // Success
        closeUploadModal();
        loadEHRRecords();
        
    } catch (error) {
        alert("Failed to save record: " + error.message);
    } finally {
        if (submitBtn) {
            submitBtn.disabled = false;
            submitBtn.textContent = "💾 Save Record";
        }
    }
}

// ==========================================
// Record Actions
// ==========================================

function viewRecord(recordId) {
    const record = allRecords.find(r => r.id === recordId);
    if (record) {
        openViewModal(record);
    }
}

async function downloadRecord(recordId) {
    // Fetch file with authentication and trigger download
    try {
        const response = await authenticatedFetch(`${API_URL}/ehr/${recordId}/download`);
        
        if (!response.ok) {
            throw new Error("Download failed");
        }
        
        const blob = await response.blob();
        const record = allRecords.find(r => r.id === recordId);
        const filename = record?.file_name || "download";
        
        // Create download link
        const url = URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    } catch (error) {
        alert("Failed to download file: " + error.message);
    }
}

function downloadCurrentRecord() {
    if (currentRecord?.id) {
        downloadRecord(currentRecord.id);
    }
}

async function loadImagePreview(recordId) {
    const container = document.getElementById("image-preview-container");
    if (!container) return;
    
    try {
        const response = await authenticatedFetch(`${API_URL}/ehr/${recordId}/download`);
        
        if (!response.ok) {
            throw new Error("Failed to load preview");
        }
        
        const blob = await response.blob();
        const url = URL.createObjectURL(blob);
        
        container.innerHTML = `<img src="${url}" alt="Preview" class="file-preview-image" style="max-width: 100%; max-height: 400px; border-radius: 8px;">`;
    } catch (error) {
        container.innerHTML = `<p class="preview-error">Preview not available</p>`;
    }
}

async function loadPdfPreview(recordId) {
    const container = document.getElementById("pdf-preview-container");
    if (!container) return;
    
    try {
        const response = await authenticatedFetch(`${API_URL}/ehr/${recordId}/download`);
        
        if (!response.ok) {
            throw new Error("Failed to load preview");
        }
        
        const blob = await response.blob();
        const url = URL.createObjectURL(blob);
        
        container.innerHTML = `<iframe src="${url}" class="pdf-preview-frame" style="width: 100%; height: 500px; border: 1px solid #ddd; border-radius: 8px;"></iframe>`;
    } catch (error) {
        container.innerHTML = `<p class="preview-error">PDF preview not available. Click Download to view.</p>`;
    }
}

async function deleteCurrentRecord() {
    if (!currentRecord) return;
    
    const confirmMsg = currentRecord.is_archived
        ? "Permanently delete this record? This cannot be undone."
        : "Archive this record? You can restore it later.";
    
    if (!confirm(confirmMsg)) return;
    
    try {
        await deleteRecord(currentRecord.id, currentRecord.is_archived);
        closeViewModal();
        loadEHRRecords();
    } catch (error) {
        alert("Failed to delete record: " + error.message);
    }
}

// ==========================================
// Utility Functions
// ==========================================

function formatDate(dateStr) {
    if (!dateStr) return "N/A";
    
    const date = new Date(dateStr);
    return date.toLocaleDateString("en-IN", {
        year: "numeric",
        month: "short",
        day: "numeric"
    });
}

function escapeHtml(text) {
    if (!text) return "";
    const div = document.createElement("div");
    div.textContent = text;
    return div.innerHTML;
}

function isImageFile(mimeType) {
    return mimeType && mimeType.startsWith("image/");
}

function isPdfFile(mimeType) {
    return mimeType && mimeType === "application/pdf";
}
