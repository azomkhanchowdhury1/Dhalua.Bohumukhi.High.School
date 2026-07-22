// START: ONLINE_CLASSES_JS
document.addEventListener('DOMContentLoaded', () => {
    // Animate cards on load
    const cards = document.querySelectorAll('.oc-card, .oc-banner, .oc-info-banner');
    cards.forEach((card, i) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(24px)';
        setTimeout(() => {
            card.style.transition = 'opacity 0.55s ease, transform 0.55s ease';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, 80 + i * 70);
    });

    // Teacher: Toggle schedule form
    const toggleBtn  = document.getElementById('toggleScheduleForm');
    const cancelBtn  = document.getElementById('cancelForm');
    const form       = document.getElementById('scheduleForm');

    if (toggleBtn && form) {
        toggleBtn.addEventListener('click', (e) => {
            e.preventDefault();
            form.classList.toggle('open');
            form.scrollIntoView({ behavior: 'smooth', block: 'start' });
        });
    }
    if (cancelBtn && form) {
        cancelBtn.addEventListener('click', () => {
            form.classList.remove('open');
        });
    }
});
// END: ONLINE_CLASSES_JS
