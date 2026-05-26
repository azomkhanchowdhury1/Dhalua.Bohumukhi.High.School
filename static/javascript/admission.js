// START: ADMISSION_JS_FILE

document.addEventListener("DOMContentLoaded", function() {
    
    // Smooth scrolling for "Apply Now" button
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            if (targetId !== '#') {
                document.querySelector(targetId).scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });

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
    const animatedElements = document.querySelectorAll('.animate-zoom, .animate-fade-up, .animate-slide-up, .animate-slide-right, .animate-slide-left');
    animatedElements.forEach(el => {
        el.style.animationPlayState = 'paused';
        observer.observe(el);
    });

    // Handle Form Submission visually
    const form = document.getElementById('admissionForm');
    if (form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault(); // Prevent actual submission for UI demo
            
            // Get submit button
            const submitBtn = form.querySelector('.btn-submit');
            const originalText = submitBtn.innerHTML;
            
            // Loading state
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Submitting...';
            submitBtn.disabled = true;
            
            // Simulate API call
            setTimeout(() => {
                submitBtn.innerHTML = '<i class="fas fa-check"></i> Application Submitted!';
                submitBtn.style.background = 'linear-gradient(90deg, #50e3c2, #28a745)';
                
                // Reset form
                form.reset();
                
                // Revert button after 3 seconds
                setTimeout(() => {
                    submitBtn.innerHTML = originalText;
                    submitBtn.style.background = '';
                    submitBtn.disabled = false;
                }, 3000);
            }, 1500);
        });
    }

});

// END: ADMISSION_JS_FILE
