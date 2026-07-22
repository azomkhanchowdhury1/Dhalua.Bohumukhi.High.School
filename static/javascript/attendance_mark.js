// ============================================================
// ATTENDANCE MARK PAGE JS — teacher/attendance_mark.html
// School Management System
// ============================================================

// START: ATTENDANCE_MARK_JS

document.addEventListener('DOMContentLoaded', () => {

    // ── 1. Mark ALL students with one status ─────────────────
    document.querySelectorAll('.mark-all-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const status = btn.dataset.status; // 'Present' | 'Absent' | 'Late'
            document.querySelectorAll(`input[type="radio"][value="${status}"]`)
                    .forEach(radio => {
                        radio.checked = true;
                        // trigger visual update
                        radio.dispatchEvent(new Event('change'));
                    });
        });
    });

    // ── 2. Highlight selected row ────────────────────────────
    document.querySelectorAll('.attendance-table tbody tr').forEach(row => {
        const radios = row.querySelectorAll('input[type="radio"]');
        radios.forEach(radio => {
            radio.addEventListener('change', () => {
                row.classList.remove('row-present', 'row-absent', 'row-late');
                if (radio.checked) {
                    const map = { Present: 'row-present', Absent: 'row-absent', Late: 'row-late' };
                    row.classList.add(map[radio.value] || '');
                }
            });
        });

        // Set initial highlight for pre-checked (Present is default)
        const checkedRadio = row.querySelector('input[type="radio"]:checked');
        if (checkedRadio) {
            const map = { Present: 'row-present', Absent: 'row-absent', Late: 'row-late' };
            row.classList.add(map[checkedRadio.value] || '');
        }
    });

    // ── 3. Counter badge ─────────────────────────────────────
    function updateCounter() {
        const total    = document.querySelectorAll('.attendance-table tbody tr').length;
        const present  = document.querySelectorAll('input[value="Present"]:checked').length;
        const absent   = document.querySelectorAll('input[value="Absent"]:checked').length;
        const late     = document.querySelectorAll('input[value="Late"]:checked').length;

        const badge = document.getElementById('attendanceSummaryBadge');
        if (badge) {
            badge.innerHTML =
                `<span class="summary-pill summary-present"><i class="fas fa-check-circle"></i> ${present} Present</span>
                 <span class="summary-pill summary-absent"><i class="fas fa-times-circle"></i> ${absent} Absent</span>
                 <span class="summary-pill summary-late"><i class="fas fa-clock"></i> ${late} Late</span>
                 <span class="summary-pill summary-total"><i class="fas fa-users"></i> ${total} Total</span>`;
        }
    }

    // Listen for all radio changes to update counter
    document.querySelectorAll('input[type="radio"]').forEach(r => {
        r.addEventListener('change', updateCounter);
    });
    updateCounter(); // run once on load

    // ── 4. Confirm before submit if any student unmarked ─────
    const attendanceForm = document.getElementById('attendanceForm');
    if (attendanceForm) {
        attendanceForm.addEventListener('submit', (e) => {
            const subjectEl = attendanceForm.querySelector('[name="subject_id"]');
            const dateEl    = attendanceForm.querySelector('[name="date"]');
            const timeEl    = attendanceForm.querySelector('[name="time"]');

            if (subjectEl && !subjectEl.value) {
                e.preventDefault();
                alert('Please select a subject before saving attendance.');
                subjectEl.focus();
                return;
            }
            if (dateEl && !dateEl.value) {
                e.preventDefault();
                alert('Please select a date before saving attendance.');
                dateEl.focus();
                return;
            }
            if (timeEl && !timeEl.value) {
                e.preventDefault();
                alert('Please enter the class time before saving attendance.');
                timeEl.focus();
                return;
            }
        });
    }

});

// END: ATTENDANCE_MARK_JS
