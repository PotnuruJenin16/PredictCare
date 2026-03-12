/**
 * Health Progress JavaScript
 * ==========================
 * Handles fetching active prescription and updating progress.
 */

// ==========================================
// Initialization
// ==========================================

document.addEventListener("DOMContentLoaded", function () {
    // Require authentication
    requireAuth();

    // Set user name
    const user = getUser();
    if (user) {
        document.getElementById("user-name").textContent = user.name;
    }

    // Logout handler
    document.getElementById("logout-btn").addEventListener("click", function (e) {
        e.preventDefault();
        logout();
    });

    // Load prescription data
    loadActivePrescription();
});

// ==========================================
// State
// ==========================================
let currentPrescription = null;

// ==========================================
// Core Functions
// ==========================================

async function loadActivePrescription() {
    const loadingEl = document.getElementById("loading");
    const activeSection = document.getElementById("active-prescription");
    const emptyState = document.getElementById("empty-state");

    loadingEl.classList.remove("hidden");
    activeSection.classList.add("hidden");
    emptyState.classList.add("hidden");

    try {
        const response = await authenticatedFetch(`${API_URL}/prescriptions/active`);

        if (response.status === 404) {
            // No active prescription
            loadingEl.classList.add("hidden");
            emptyState.classList.remove("hidden");
            return;
        }

        if (!response.ok) {
            throw new Error("Failed to load prescription");
        }

        const data = await response.json();
        currentPrescription = data;

        renderPrescription(data);

        loadingEl.classList.add("hidden");
        activeSection.classList.remove("hidden");

    } catch (error) {
        console.error(error);
        loadingEl.classList.add("hidden");
        showError("Could not load health progress. Please try again.");
    }
}

function renderPrescription(data) {
    document.getElementById("doctor-name-display").textContent = `Dr. ${data.doctor_name}`;
    document.getElementById("prescription-notes").textContent = data.notes;

    updateProgressUI(data.progress_percentage);
    renderDaysGrid(data.total_days, data.completed_days);
}

function updateProgressUI(percentage) {
    const bar = document.getElementById("progress-bar");
    const percentText = document.getElementById("progress-percent");

    bar.style.width = `${percentage}%`;
    percentText.textContent = `${percentage}%`;

    // Color coding
    // Color coding
    if (percentage >= 80) {
        bar.style.background = "var(--success-gradient)"; // Green gradient
    } else if (percentage >= 40) {
        bar.style.background = "var(--primary-gradient)"; // Blue/Purple gradient
    } else {
        bar.style.background = "var(--warning-color)"; // Orange
    }
}

function renderDaysGrid(totalDays, completedDays) {
    const grid = document.getElementById("days-grid");
    grid.innerHTML = "";

    const completedSet = new Set(completedDays);

    for (let i = 0; i < totalDays; i++) {
        const dayNum = i + 1;
        const isChecked = completedSet.has(i);

        const dayEl = document.createElement("div");
        dayEl.className = "day-check";
        dayEl.innerHTML = `
            <input type="checkbox" id="day-${i}" value="${i}" ${isChecked ? "checked" : ""}>
            <label for="day-${i}" class="check-label">
                <span class="day-number">Day ${dayNum}</span>
                <span class="check-icon">✓</span>
            </label>
        `;

        // Add change listener
        const checkbox = dayEl.querySelector("input");
        checkbox.addEventListener("change", () => handleCheckChange(i, checkbox.checked));

        grid.appendChild(dayEl);
    }
}

async function handleCheckChange(dayIndex, isChecked) {
    if (!currentPrescription) return;

    // Optimistic update
    const completedSet = new Set(currentPrescription.completed_days);
    if (isChecked) {
        completedSet.add(dayIndex);
    } else {
        completedSet.delete(dayIndex);
    }

    const newCompletedDays = Array.from(completedSet).sort((a, b) => a - b);
    currentPrescription.completed_days = newCompletedDays;

    // Recalculate progress
    const newProgress = Math.round((newCompletedDays.length / currentPrescription.total_days) * 100);
    updateProgressUI(newProgress);

    // Send to backend
    try {
        const response = await authenticatedFetch(
            `${API_URL}/prescriptions/${currentPrescription.id}/progress`,
            {
                method: "POST",
                body: JSON.stringify({ completed_days: newCompletedDays })
            }
        );

        if (!response.ok) {
            throw new Error("Failed to update progress");
        }
    } catch (error) {
        console.error(error);
        showError("Failed to save progress. Please check your connection.");
        // Revert UI if needed (omitted for simplicity in this demo)
    }
}

function showError(msg) {
    const errorEl = document.getElementById("error");
    const errorText = document.getElementById("error-text");
    errorText.textContent = msg;
    errorEl.classList.remove("hidden");
    setTimeout(() => errorEl.classList.add("hidden"), 3000);
}
