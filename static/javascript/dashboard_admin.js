// START: DASHBOARD_ADMIN_JS
document.addEventListener('DOMContentLoaded', () => {
    // Set current date
    const dateSpan = document.getElementById('dateText');
    if (dateSpan) {
        const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
        dateSpan.innerText = new Date().toLocaleDateString('en-US', options);
    }

    // Animation for cards
    const cards = document.querySelectorAll('.stat-card, .module-card');
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
// END: DASHBOARD_ADMIN_JS
