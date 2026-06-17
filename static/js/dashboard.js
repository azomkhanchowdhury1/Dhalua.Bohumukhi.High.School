/* START: DASHBOARD_JS */
// ==================== CORE MODAL & TAB FUNCTIONS ====================

// Set current date & minimum dates on DOM load
document.addEventListener('DOMContentLoaded', () => {
    const dateSpan = document.getElementById('dateText');
    if (dateSpan) {
        const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
        dateSpan.innerText = new Date().toLocaleDateString('en-US', options);
    }
    // Set today's date as minimum for leave form and date inputs
    const today = new Date().toISOString().split('T')[0];
    document.querySelectorAll('input[type="date"]').forEach(inp => inp.min = today);
});

// Open Modal
function openModal(modalId) {
    document.querySelectorAll('.modal-overlay').forEach(el => el.classList.remove('active'));
    const modal = document.getElementById(modalId);
    if (modal) modal.classList.add('active');
}

// Close Modal
function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) modal.classList.remove('active');
}

// Close on outside click
window.onclick = function(event) {
    if (event.target.classList.contains('modal-overlay')) {
        event.target.classList.remove('active');
    }
}

// Tab Switcher (event-based - for onclick buttons)
function switchTab(event, panelId) {
    const modalContainer = event.currentTarget.closest('.modal-container');
    if (!modalContainer) return;
    modalContainer.querySelectorAll('.modal-tab-btn').forEach(btn => btn.classList.remove('active'));
    modalContainer.querySelectorAll('.tab-panel').forEach(panel => panel.style.display = 'none');
    event.currentTarget.classList.add('active');
    const panel = modalContainer.querySelector('#' + panelId);
    if (panel) panel.style.display = 'block';
}

// Tab Switcher (direct - for programmatic calls)
function switchTabDirect(panelId) {
    // Find the panel across all open modals
    setTimeout(() => {
        const panel = document.getElementById(panelId);
        if (!panel) return;
        const modalContainer = panel.closest('.modal-container');
        if (!modalContainer) return;
        modalContainer.querySelectorAll('.modal-tab-btn').forEach(btn => btn.classList.remove('active'));
        modalContainer.querySelectorAll('.tab-panel').forEach(p => p.style.display = 'none');
        // Activate matching tab button
        const tabId = 'tab-' + panelId;
        const tabBtn = modalContainer.querySelector('#' + tabId);
        if (tabBtn) tabBtn.classList.add('active');
        panel.style.display = 'block';
    }, 50);
}

// Tab switcher by ID
function switchTabById(panelId) {
    switchTabDirect(panelId);
}

// ==================== DUTY SCHEDULE ====================
function showDutyTab(tabId) {
    switchTabDirect(tabId);
}

// ==================== HOLIDAY CALENDAR FILTER ====================
function filterHoliday(type) {
    setTimeout(() => {
        const cards = document.querySelectorAll('.holiday-card');
        cards.forEach(card => {
            if (!type || card.dataset.type === type) {
                card.style.display = 'flex';
            } else {
                card.style.display = 'none';
            }
        });
    }, 60);
}

// ==================== DOCUMENT CENTER FILTER ====================
function filterDoc(type) {
    // filter logic handled by showing different tab panels
}

// ==================== EVENT DUTY FILTER ====================
function filterEvent(eventName) {
    const map = {
        'Annual Sports': 'evSports',
        'Cultural Program': 'evCultural',
        'Parents Meeting Duty': 'evParents'
    };
    if (map[eventName]) switchTabDirect(map[eventName]);
}

// ==================== PERFORMANCE FILTER ====================
function filterPerformance(type) {
    const map = {
        'Evaluation': 'perfEval',
        'Award': 'perfAward',
        'Warning': 'perfWarn'
    };
    if (map[type]) switchTabDirect(map[type]);
}

// ==================== DIRECT MESSAGING RELATIONSHIPS ====================
function setMessage(text) {
    const textarea = document.getElementById('msgTextarea');
    if (textarea) textarea.value = text;
}

// Automatically selects a DM recipient from a username and fills the message draft
function selectDMRecipient(username, defaultText) {
    // Switch to Compose tab
    switchTabDirect('msgCompose');
    
    // Find the select element
    const selectEl = document.querySelector('select[name="receiver_id"]');
    if (selectEl) {
        // Find option that matches username in parentheses, e.g. "(rahim)"
        let foundOption = false;
        for (let i = 0; i < selectEl.options.length; i++) {
            const opt = selectEl.options[i];
            if (opt.text.toLowerCase().includes('(' + username.toLowerCase() + ')') || opt.value === username) {
                selectEl.selectedIndex = i;
                foundOption = true;
                break;
            }
        }
        // If not found by username, look for a partial match
        if (!foundOption) {
            for (let i = 0; i < selectEl.options.length; i++) {
                const opt = selectEl.options[i];
                if (opt.text.toLowerCase().includes(username.toLowerCase())) {
                    selectEl.selectedIndex = i;
                    break;
                }
            }
        }
    }
    
    // Set message textarea
    setMessage(defaultText);
}

// ==================== TASK MANAGEMENT ====================
function markTaskDone(btn) {
    const taskCard = btn.closest('.task-card');
    if (!taskCard) return;
    taskCard.classList.add('task-completed');
    const badge = taskCard.querySelector('.status-badge');
    if (badge) {
        badge.className = 'status-badge status-approved';
        badge.textContent = 'COMPLETED';
    }
    btn.style.display = 'none';
}

// ==================== PROFILE - PASSWORD TOGGLE ====================
function togglePass(fieldId) {
    const field = document.getElementById(fieldId);
    if (!field) return;
    if (field.type === 'password') {
        field.type = 'text';
    } else {
        field.type = 'password';
    }
}

// ==================== SALARY - PRINT PAY SLIP ====================
function printPaySlip() {
    const slipContent = document.querySelector('.payslip-card');
    if (!slipContent) return;
    const printWin = window.open('', '_blank');
    printWin.document.write(`
        <html><head><title>Pay Slip</title>
        <style>
            body { font-family: Arial, sans-serif; padding: 30px; }
            table { width:100%; border-collapse:collapse; }
            td, th { padding:10px; border:1px solid #ccc; }
            h4 { color: #1a202c; }
        </style></head>
        <body>${slipContent.innerHTML}</body></html>
    `);
    printWin.document.close();
    printWin.print();
}

// ==================== LEAVE INFO BOX ====================
function updateLeaveInfo() {
    const selectEl = document.getElementById('leaveTypeSelect');
    if (!selectEl) return;
    const type = selectEl.value;
    const box = document.getElementById('leaveInfoBox');
    if (!box) return;
    
    const infos = {
        'Sick Leave': '<i class="fas fa-heartbeat"></i> Allowed: 14 days/year with medical certificate',
        'Casual Leave': '<i class="fas fa-sun"></i> Allowed: 10 days/year',
        'Emergency Leave': '<i class="fas fa-exclamation-triangle"></i> Up to 3 days. Approval required immediately.',
        'Annual Leave': '<i class="fas fa-calendar"></i> Allowed: 15 days/year. Apply 7 days in advance.',
        'Maternity Leave': '<i class="fas fa-baby"></i> 16 weeks paid leave. Documents required.'
    };
    box.innerHTML = infos[type] ? `<div class="leave-info-text">${infos[type]}</div>` : '';
}

// ==================== INVENTORY CHECKBOX SYNC ====================
function syncInventorySelect() {
    const checks = document.querySelectorAll('.inv-check:checked');
    const selected = Array.from(checks).map(c => c.value);
    // Update display input
    const displayInput = document.getElementById('inventoryDisplayInput');
    if (displayInput) displayInput.value = selected.join(', ') || '';
    // Sync hidden select
    const sel = document.getElementById('inventorySelect');
    if (sel) {
        Array.from(sel.options).forEach(opt => {
            opt.selected = selected.includes(opt.value);
        });
    }
    // Ensure at least 1 item is selected for form submit
    const submitBtn = document.getElementById('invSubmitBtn');
    if (submitBtn) {
        submitBtn.disabled = selected.length === 0;
    }
}

// Pre-select inventory item from module card click
function selectInventoryItem(item) {
    setTimeout(() => {
        const check = document.querySelector(`.inv-check[value="${item}"]`);
        if (check) { 
            check.checked = true; 
            syncInventorySelect(); 
        }
    }, 60);
}

// Keyboard close (Escape key)
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        document.querySelectorAll('.modal-overlay.active').forEach(m => m.classList.remove('active'));
    }
});
/* END: DASHBOARD_JS */
