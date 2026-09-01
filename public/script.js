/**
 * =============================================================================
 * LPU Student Registration Finder - Frontend Logic
 * =============================================================================
 * Connects to Flask REST API with Google Sheets integration:
 * GET /api/student?query=<student_name>
 * Displays single or multiple verified student cards matching the reference design.
 */

const CONFIG = {
    API_BASE_URL: window.location.origin.startsWith('http')
        ? `${window.location.origin}/api/student`
        : 'http://127.0.0.1:5000/api/student'
};

// DOM References
const elements = {
    searchForm: document.getElementById('searchForm'),
    searchInput: document.getElementById('searchInput'),
    clearBtn: document.getElementById('clearBtn'),
    searchBtn: document.getElementById('searchBtn'),
    validationMessage: document.getElementById('validationMessage'),
    hintChips: document.querySelectorAll('.hint-chip'),

    // State sections
    loadingState: document.getElementById('loadingState'),
    notFoundState: document.getElementById('notFoundState'),
    notFoundQueryText: document.getElementById('notFoundQueryText'),
    errorState: document.getElementById('errorState'),
    errorMessageText: document.getElementById('errorMessageText'),
    retryBtn: document.getElementById('retryBtn'),

    // Results container
    resultsSection: document.getElementById('resultsSection'),
    resultsCountPill: document.getElementById('resultsCountPill'),
    studentsCardsList: document.getElementById('studentsCardsList'),
    newSearchTopBtn: document.getElementById('newSearchTopBtn')
};

// UI State Controller
function setActiveState(stateName) {
    if (elements.loadingState) elements.loadingState.classList.add('hidden');
    if (elements.notFoundState) elements.notFoundState.classList.add('hidden');
    if (elements.errorState) elements.errorState.classList.add('hidden');
    if (elements.resultsSection) elements.resultsSection.classList.add('hidden');

    switch (stateName) {
        case 'initial':
            // Reset states
            break;
        case 'loading':
            if (elements.loadingState) {
                elements.loadingState.classList.remove('hidden');
                elements.loadingState.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
            }
            break;
        case 'results':
            if (elements.resultsSection) {
                elements.resultsSection.classList.remove('hidden');
                elements.resultsSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
            }
            break;
        case 'not-found':
            if (elements.notFoundState) {
                elements.notFoundState.classList.remove('hidden');
                elements.notFoundState.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
            }
            break;
        case 'error':
            if (elements.errorState) {
                elements.errorState.classList.remove('hidden');
                elements.errorState.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
            }
            break;
    }
}

function showValidationError(show = true, message = "Please enter a student name.") {
    const textSpan = elements.validationMessage ? elements.validationMessage.querySelector('span') : null;
    if (textSpan) textSpan.textContent = message;

    if (elements.validationMessage) {
        if (show) {
            elements.validationMessage.classList.add('active');
            elements.searchInput.focus();
        } else {
            elements.validationMessage.classList.remove('active');
        }
    }
}

function escapeHtml(str) {
    if (!str) return "";
    return String(str)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

/**
 * Copies registration number to clipboard with visual feedback
 */
async function copyToClipboard(text, buttonElement) {
    if (!text || text === "N/A" || text === "-") return;

    const copyTextSpan = buttonElement.querySelector('.copy-btn-text') || buttonElement;

    try {
        if (navigator.clipboard && window.isSecureContext) {
            await navigator.clipboard.writeText(text);
        } else {
            // Fallback for non-https or older environments
            const tempTextArea = document.createElement('textarea');
            tempTextArea.value = text;
            tempTextArea.style.position = 'fixed';
            tempTextArea.style.left = '-999999px';
            document.body.appendChild(tempTextArea);
            tempTextArea.select();
            document.execCommand('copy');
            document.body.removeChild(tempTextArea);
        }

        // Visual feedback
        buttonElement.classList.add('copied');
        if (copyTextSpan) copyTextSpan.textContent = "Copied!";

        setTimeout(() => {
            buttonElement.classList.remove('copied');
            if (copyTextSpan) copyTextSpan.textContent = "Copy Number";
        }, 2000);

    } catch (err) {
        console.error("Clipboard copy failed:", err);
    }
}

/**
 * Creates and appends student cards matching reference design
 */
function renderStudentsList(students, query) {
    elements.studentsCardsList.innerHTML = "";

    const total = students.length;
    if (elements.resultsCountPill) {
        elements.resultsCountPill.textContent = total === 1 ? "1 Result" : `${total} Results`;
    }

    students.forEach((student) => {
        const name = student.name || "Unknown Student";
        const regNo = student.registration_no || "N/A";

        const card = document.createElement('article');
        card.className = "student-record-card";
        card.setAttribute('aria-label', `Student Record - ${name}`);

        card.innerHTML = `
            <div class="card-left-group">
                <div class="student-avatar-box" aria-hidden="true">
                    <svg class="avatar-silhouette" viewBox="0 0 24 24" fill="currentColor">
                        <path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/>
                    </svg>
                </div>
                <div class="student-info-col">
                    <div class="verified-record-pill">
                        <span class="pill-text">VERIFIED STUDENT RECORD</span>
                        <svg class="check-icon" viewBox="0 0 24 24" fill="currentColor">
                            <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
                        </svg>
                    </div>
                    <h3 class="student-fullname">${escapeHtml(name)}</h3>
                    <div class="reg-number-line">
                        <span class="reg-label">Registration Number</span>
                        <span class="reg-value">${escapeHtml(regNo)}</span>
                    </div>
                </div>
            </div>
            <div class="card-right-group">
                <button type="button" class="copy-number-btn" title="Copy Registration Number" data-reg="${escapeHtml(regNo)}">
                    <svg class="copy-btn-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
                        <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
                    </svg>
                    <span class="copy-btn-text">Copy Number</span>
                </button>
            </div>
        `;

        // Attach copy event
        const copyBtn = card.querySelector('.copy-number-btn');
        if (copyBtn) {
            copyBtn.addEventListener('click', () => {
                copyToClipboard(regNo, copyBtn);
            });
        }

        elements.studentsCardsList.appendChild(card);
    });

    setActiveState('results');
}

/**
 * Fetch data from Flask Backend API
 */
async function searchStudent(queryText) {
    const trimmedQuery = queryText.trim();

    if (!trimmedQuery) {
        showValidationError(true, "Please enter a student name.");
        return;
    }
    showValidationError(false);

    setActiveState('loading');

    try {
        const url = `${CONFIG.API_BASE_URL}?query=${encodeURIComponent(trimmedQuery)}`;
        const response = await fetch(url, {
            method: 'GET',
            headers: {
                'Accept': 'application/json'
            }
        });

        // 400 Bad Request
        if (response.status === 400) {
            showValidationError(true, "Please provide a valid student name.");
            setActiveState('initial');
            return;
        }

        // 404 Not Found
        if (response.status === 404) {
            if (elements.notFoundQueryText) elements.notFoundQueryText.textContent = trimmedQuery;
            setActiveState('not-found');
            return;
        }

        // 500 Server or Sheets Error
        if (response.status === 500) {
            const errData = await response.json().catch(() => ({}));
            const msg = errData.message || "Internal server error occurred while querying Google Sheets.";
            if (elements.errorMessageText) elements.errorMessageText.textContent = msg;
            setActiveState('error');
            return;
        }

        // 200 OK
        if (response.ok) {
            const data = await response.json();

            let studentsList = [];
            if (Array.isArray(data.students) && data.students.length > 0) {
                studentsList = data.students;
            } else if (data.student && data.student.name) {
                studentsList = [data.student];
            }

            if (studentsList.length > 0) {
                renderStudentsList(studentsList, trimmedQuery);
            } else {
                if (elements.notFoundQueryText) elements.notFoundQueryText.textContent = trimmedQuery;
                setActiveState('not-found');
            }
        } else {
            throw new Error(`Server responded with status: ${response.status}`);
        }

    } catch (error) {
        console.error("Search request error:", error);
        if (elements.errorMessageText) {
            elements.errorMessageText.textContent = "Unable to connect to Flask API server. Make sure `python app.py` is running on port 5000.";
        }
        setActiveState('error');
    }
}

// Clear button visibility toggle
function toggleClearBtn() {
    if (!elements.clearBtn) return;
    if (elements.searchInput.value.trim().length > 0) {
        elements.clearBtn.style.display = 'block';
    } else {
        elements.clearBtn.style.display = 'none';
    }
}

// Event Listeners
function initEventListeners() {
    // Search Form Submit
    if (elements.searchForm) {
        elements.searchForm.addEventListener('submit', (e) => {
            e.preventDefault();
            searchStudent(elements.searchInput.value);
        });
    }

    // Input events
    if (elements.searchInput) {
        elements.searchInput.addEventListener('input', () => {
            toggleClearBtn();
            if (elements.validationMessage && elements.validationMessage.classList.contains('active')) {
                showValidationError(false);
            }
        });

        elements.searchInput.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                elements.searchInput.value = '';
                toggleClearBtn();
                showValidationError(false);
            }
        });
    }

    // Clear input button
    if (elements.clearBtn) {
        elements.clearBtn.addEventListener('click', () => {
            elements.searchInput.value = '';
            toggleClearBtn();
            showValidationError(false);
            elements.searchInput.focus();
        });
    }

    // Quick Search Hints
    if (elements.hintChips) {
        elements.hintChips.forEach((chip) => {
            chip.addEventListener('click', () => {
                const query = chip.getAttribute('data-query');
                if (query && elements.searchInput) {
                    elements.searchInput.value = query;
                    toggleClearBtn();
                    searchStudent(query);
                }
            });
        });
    }

    // Retry Button on error
    if (elements.retryBtn) {
        elements.retryBtn.addEventListener('click', () => {
            if (elements.searchInput && elements.searchInput.value.trim()) {
                searchStudent(elements.searchInput.value);
            } else {
                setActiveState('initial');
            }
        });
    }

    // "New Search" link button
    if (elements.newSearchTopBtn) {
        elements.newSearchTopBtn.addEventListener('click', () => {
            if (elements.searchInput) {
                elements.searchInput.value = '';
                toggleClearBtn();
                elements.searchInput.focus();
            }
            elements.searchForm.scrollIntoView({ behavior: 'smooth', block: 'center' });
        });
    }
}

// Initialize on DOM Ready
document.addEventListener('DOMContentLoaded', () => {
    initEventListeners();
    toggleClearBtn();
    setActiveState('initial');
});
