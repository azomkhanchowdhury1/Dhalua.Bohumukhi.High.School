/* START: ABOUT_US_JS */
document.addEventListener('DOMContentLoaded', function() {
    // Scroll Animation using Intersection Observer
    const animatedElements = document.querySelectorAll('.hidden');

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('show');
                observer.unobserve(entry.target); // Only animate once
            }
        });
    }, {
        threshold: 0.15, // Trigger when 15% of the element is visible
        rootMargin: "0px 0px -50px 0px"
    });

    animatedElements.forEach(el => {
        observer.observe(el);
    });
});
/* END: ABOUT_US_JS */
