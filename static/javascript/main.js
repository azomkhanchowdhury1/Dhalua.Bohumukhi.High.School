// START: GLOBAL_SCRIPTS
document.addEventListener('DOMContentLoaded', function() {
    // --- 1. Auto-dismiss flash messages after 1 second ---
    const messages = document.querySelectorAll('.messages-container .message, .message');
    messages.forEach(msg => {
        setTimeout(() => {
            msg.style.transition = 'opacity 0.6s cubic-bezier(0.4, 0, 0.2, 1), transform 0.6s cubic-bezier(0.4, 0, 0.2, 1)';
            msg.style.opacity = '0';
            msg.style.transform = 'translateY(-10px)';
            setTimeout(() => {
                msg.remove();
                const container = document.querySelector('.messages-container');
                if (container && container.querySelectorAll('.message').length === 0) {
                    container.remove();
                }
            }, 600);
        }, 1000);
    });

    // --- 2. Top Progress Bar Navigation Indicator ---
    (function() {
        const bar = document.getElementById('nav-progress-bar');
        if (!bar) return;

        let animFrame;
        let currentWidth = 0;

        function startProgress() {
            bar.style.transition = 'none';
            bar.style.width = '0%';
            bar.classList.add('active');
            bar.classList.remove('complete');
            currentWidth = 0;

            // Animate to ~85% quickly, then slow down (simulates waiting)
            function grow() {
                if (currentWidth < 70) {
                    currentWidth += 3;
                } else if (currentWidth < 85) {
                    currentWidth += 0.5;
                } else {
                    return; // stop at 85, wait for page load
                }
                bar.style.transition = 'none';
                bar.style.width = currentWidth + '%';
                animFrame = requestAnimationFrame(grow);
            }
            animFrame = requestAnimationFrame(grow);
        }

        function completeProgress() {
            cancelAnimationFrame(animFrame);
            bar.classList.add('complete');
            setTimeout(() => {
                bar.style.width = '0%';
                bar.classList.remove('active', 'complete');
            }, 650);
        }

        // Show bar on link clicks (internal navigation only)
        document.addEventListener('click', function(e) {
            const link = e.target.closest('a');
            if (!link) return;
            const href = link.getAttribute('href');
            const target = link.getAttribute('target');
            if (
                href &&
                !href.startsWith('#') &&
                !href.startsWith('javascript:') &&
                !href.startsWith('mailto:') &&
                !href.startsWith('tel:') &&
                target !== '_blank' &&
                !link.hasAttribute('download')
            ) {
                startProgress();
            }
        });

        // Show bar on form submit
        document.addEventListener('submit', function(e) {
            if (!e.target.classList.contains('no-loader')) {
                startProgress();
            }
        });

        // Complete bar when new page is loaded
        window.addEventListener('pageshow', completeProgress);
        completeProgress(); // complete on current page load too
    })();

    // --- 3. Hamburger Menu toggle logic ---
    const menuToggle = document.getElementById('mobileMenuToggle');
    const navRight = document.getElementById('navRightSection');
    if (menuToggle && navRight) {
        menuToggle.addEventListener('click', function(e) {
            e.stopPropagation();
            navRight.classList.toggle('active');
            const icon = menuToggle.querySelector('i');
            if (icon) {
                icon.classList.toggle('fa-bars');
                icon.classList.toggle('fa-times');
            }
        });
        
        // Close mobile menu when clicking outside
        document.addEventListener('click', function(e) {
            if (!navRight.contains(e.target) && !menuToggle.contains(e.target)) {
                navRight.classList.remove('active');
                const icon = menuToggle.querySelector('i');
                if (icon) {
                    icon.classList.add('fa-bars');
                    icon.classList.remove('fa-times');
                }
            }
        });
    }
});
// END: GLOBAL_SCRIPTS
