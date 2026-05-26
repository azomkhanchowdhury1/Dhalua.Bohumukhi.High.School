// START: CONTACT_JS_FILE

document.addEventListener("DOMContentLoaded", function() {
    
    // Intersection Observer for scroll animations
    const observerOptions = {
        root: null,
        rootMargin: '0px',
        threshold: 0.15
    };

    const observer = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                // Resume the paused CSS animation
                entry.target.style.animationPlayState = 'running';
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Initial state: pause animations
    const animatedElements = document.querySelectorAll('.animate-zoom, .animate-slide-up, .animate-slide-right, .animate-slide-left');
    animatedElements.forEach(el => {
        el.style.animationPlayState = 'paused';
        observer.observe(el);
    });

    // Form Submission Feedback
    const contactForm = document.getElementById('contactForm');
    if (contactForm) {
        contactForm.addEventListener('submit', function() {
            const submitBtn = contactForm.querySelector('.btn-primary');
            const btnText = submitBtn.querySelector('span');
            const btnIcon = submitBtn.querySelector('i');
            
            // Show loading state
            submitBtn.disabled = true;
            btnText.innerText = 'Sending...';
            btnIcon.className = 'fas fa-spinner fa-spin';
            
            // Note: The actual submission is handled by Django POST.
            // This just provides immediate visual feedback before the page reloads.
        });
    }

});

// END: CONTACT_JS_FILE
