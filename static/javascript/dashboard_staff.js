// ============================================================
// STAFF DASHBOARD JS — dashboard_staff.js
// School Management System
// ============================================================

// START: DASHBOARD_STAFF_JS

document.addEventListener('DOMContentLoaded', () => {

    // ── 1. Set current date display ──────────────────────────
    const dateSpan = document.getElementById('dateText');
    if (dateSpan) {
        const options = {
            weekday: 'long',
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        };
        dateSpan.innerText = new Date().toLocaleDateString('en-US', options);
    }

    // ── 2. Animate cards on page load ────────────────────────
    const cards = document.querySelectorAll('.stat-card, .module-card, .info-card');
    cards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        setTimeout(() => {
            card.style.transition = 'all 0.6s cubic-bezier(0.16, 1, 0.3, 1)';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, index * 100);
    });

});

// ── 3. Modal open/close ──────────────────────────────────────
function openModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.style.display = 'flex';
        document.body.style.overflow = 'hidden';
    }
}

function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.style.display = 'none';
        document.body.style.overflow = '';
    }
}

// Close modal when clicking the overlay background
document.addEventListener('click', (e) => {
    if (e.target.classList.contains('modal-overlay')) {
        e.target.style.display = 'none';
        document.body.style.overflow = '';
    }
});

// ── 4. Tab switching inside modals ───────────────────────────
function switchTab(event, tabId) {
    const modal = event.target.closest('.modal-container');
    if (!modal) return;

    // Deactivate all tab buttons and panels
    modal.querySelectorAll('.modal-tab-btn').forEach(btn => btn.classList.remove('active'));
    modal.querySelectorAll('.tab-panel').forEach(panel => {
        panel.style.display = 'none';
    });

    // Activate selected tab
    event.target.classList.add('active');
    const panel = document.getElementById(tabId);
    if (panel) panel.style.display = 'block';
}

// ── 5. Inventory checkbox → select sync ─────────────────────
function syncInventorySelect() {
    const checked = Array.from(document.querySelectorAll('.inv-check:checked'))
                         .map(cb => cb.value);
    const select  = document.getElementById('inventorySelect');
    const display = document.getElementById('inventoryDisplayInput');

    if (select) {
        Array.from(select.options).forEach(opt => {
            opt.selected = checked.includes(opt.value);
        });
    }
    if (display) {
        display.value = checked.length ? checked.join(', ') : '';
    }

    // Disable submit if nothing selected
    const submitBtn = document.getElementById('invSubmitBtn');
    if (submitBtn) {
        submitBtn.disabled = checked.length === 0;
    }
}

// ── 6. Duty filter table rows ────────────────────────────────
function filterDuties(type) {
    const rows = document.querySelectorAll('[data-duty-type]');
    rows.forEach(row => {
        row.style.display = (type === 'all' || row.dataset.dutyType === type)
            ? '' : 'none';
    });

    // Update active filter button
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.filter === type);
    });
}

// END: DASHBOARD_STAFF_JS
