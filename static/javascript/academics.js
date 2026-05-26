// START: ACADEMICS_JS_FILE

document.addEventListener("DOMContentLoaded", function() {
    
    // Tab functionality for Class Routine
    window.openTab = function(evt, tabName) {
        // Get all elements with class="tab-content" and hide them
        var tabcontent = document.getElementsByClassName("tab-content");
        for (var i = 0; i < tabcontent.length; i++) {
            tabcontent[i].style.display = "none";
        }

        // Get all elements with class="tab-btn" and remove the class "active"
        var tablinks = document.getElementsByClassName("tab-btn");
        for (var i = 0; i < tablinks.length; i++) {
            tablinks[i].className = tablinks[i].className.replace(" active", "");
        }

        // Show the current tab, and add an "active" class to the button that opened the tab
        document.getElementById(tabName).style.display = "block";
        evt.currentTarget.className += " active";
        
        // Retrigger animations within the tab
        const animations = document.getElementById(tabName).querySelectorAll('.animate-zoom, .animate-fade-up, .animate-slide-up, .animate-slide-right, .animate-slide-left');
        animations.forEach(el => {
            el.style.animation = 'none';
            el.offsetHeight; /* trigger reflow */
            el.style.animation = null; 
        });
    };

    // Intersection Observer for scroll animations
    const observerOptions = {
        root: null,
        rootMargin: '0px',
        threshold: 0.1
    };

    const observer = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                // Add an 'in-view' class or just let the CSS animation run
                // Our CSS has forwards, so we can just re-trigger or rely on it
                // To make it run only when visible, we can set animation-play-state
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

});

// END: ACADEMICS_JS_FILE
