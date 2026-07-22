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

    // 3. Welcome Title - simple display, no heavy animation
    // (letter-by-letter animation removed for performance)

});
/* END: HOME_JS */
