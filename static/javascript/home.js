/* START: HOME_JS */
document.addEventListener('DOMContentLoaded', function() {
    // 1. Hero Slider Logic
    let slideIndex = 0;
    let slides = document.querySelectorAll('.slide');
    let dots = document.querySelectorAll('.dot');
    let sliderInterval;

    function showSlides(n) {
        if (n >= slides.length) { slideIndex = 0; }
        if (n < 0) { slideIndex = slides.length - 1; }
        
        slides.forEach(slide => slide.classList.remove('active'));
        dots.forEach(dot => dot.classList.remove('active'));
        
        slides[slideIndex].classList.add('active');
        dots[slideIndex].classList.add('active');
    }

    // Auto slide every 3 seconds
    function startSlider() {
        sliderInterval = setInterval(function() {
            slideIndex++;
            showSlides(slideIndex);
        }, 3000);
    }

    function stopSlider() {
        clearInterval(sliderInterval);
    }

    // Manual controls
    window.changeSlide = function(n) {
        stopSlider();
        slideIndex += n;
        showSlides(slideIndex);
        startSlider();
    };

    window.currentSlide = function(n) {
        stopSlider();
        slideIndex = n;
        showSlides(slideIndex);
        startSlider();
    };

    // Initialize
    if(slides.length > 0) {
        showSlides(slideIndex);
        startSlider();
    }

    // 2. Statistics Counter Animation logic
    const counters = document.querySelectorAll('.counter');
    const speed = 200; // The lower the slower

    const animateCounters = () => {
        counters.forEach(counter => {
            const updateCount = () => {
                const target = +counter.getAttribute('data-target');
                const count = +counter.innerText;
                const inc = target / speed;

                if (count < target) {
                    counter.innerText = Math.ceil(count + inc);
                    setTimeout(updateCount, 10);
                } else {
                    counter.innerText = target;
                }
            };
            updateCount();
        });
    };

    // Intersection Observer to trigger counter animation when scrolled into view
    const statsSection = document.querySelector('.stats-section');
    if(statsSection) {
        const observer = new IntersectionObserver((entries) => {
            if(entries[0].isIntersecting) {
                animateCounters();
                observer.disconnect();
            }
        });
        observer.observe(statsSection);
    }

    // 3. Welcome Title Animation Logic (Load, Hover, 15s Idle Cycle)
    const welcomeTitle = document.querySelector('.welcome-title');
    if (welcomeTitle) {
        const text = welcomeTitle.textContent.trim();
        welcomeTitle.innerHTML = ''; // Clear original text
        
        // Split text into words, then letters to prevent breaking layout on wrap
        const words = text.split(' ');
        words.forEach((wordText, wordIdx) => {
            const wordSpan = document.createElement('span');
            wordSpan.className = 'word';
            
            const letters = wordText.split('');
            letters.forEach((char) => {
                const charSpan = document.createElement('span');
                charSpan.className = 'letter';
                charSpan.textContent = char;
                wordSpan.appendChild(charSpan);
            });
            
            welcomeTitle.appendChild(wordSpan);
            
            // Add space between words (except the last one)
            if (wordIdx < words.length - 1) {
                const space = document.createTextNode(' ');
                welcomeTitle.appendChild(space);
            }
        });

        const letterSpans = welcomeTitle.querySelectorAll('.letter');
        let idleTimer = null;

        // Function to trigger/replay the letter-by-letter welcome animation
        const playWelcomeAnimation = () => {
            letterSpans.forEach((span, index) => {
                span.classList.remove('animate-letter');
                // Force reflow
                void span.offsetWidth;
                // Staggered delay for each letter (0.04s interval)
                span.style.animationDelay = `${index * 0.04}s`;
                span.classList.add('animate-letter');
            });
        };

        // Function to start the 15-second idle interval
        const startIdleTimer = () => {
            if (idleTimer) clearInterval(idleTimer);
            idleTimer = setInterval(() => {
                playWelcomeAnimation();
            }, 15000); // 15 seconds
        };

        // Function to stop the idle timer
        const stopIdleTimer = () => {
            if (idleTimer) {
                clearInterval(idleTimer);
                idleTimer = null;
            }
        };

        // Event listener for mouse enter (hover)
        welcomeTitle.addEventListener('mouseenter', () => {
            stopIdleTimer(); // Pause idle timer on hover to avoid overlapping animations
            playWelcomeAnimation();
        });

        // Event listener for mouse leave
        welcomeTitle.addEventListener('mouseleave', () => {
            startIdleTimer(); // Resume/restart idle timer when mouse leaves
        });

        // Initialize: Trigger animation immediately on load and start the idle timer
        playWelcomeAnimation();
        startIdleTimer();
    }
});
/* END: HOME_JS */
