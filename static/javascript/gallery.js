// START: GALLERY_JS_FILE

document.addEventListener("DOMContentLoaded", function() {
    
    // Intersection Observer for scroll animations
    const observerOptions = {
        root: null,
        rootMargin: '0px',
        threshold: 0.1
    };

    const observer = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.animationPlayState = 'running';
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    const animatedElements = document.querySelectorAll('.animate-zoom, .animate-fade-up, .animate-slide-up');
    animatedElements.forEach(el => {
        el.style.animationPlayState = 'paused';
        observer.observe(el);
    });

});

// Gallery Filtering
function filterGallery(category) {
    const items = document.querySelectorAll('.gallery-item');
    const buttons = document.querySelectorAll('.filter-btn');

    // Update buttons
    buttons.forEach(btn => {
        btn.classList.remove('active');
        if (btn.getAttribute('onclick').includes(category)) {
            btn.classList.add('active');
        }
    });

    // Filter items
    items.forEach(item => {
        item.style.display = 'none';
        if (category === 'all' || item.classList.contains(category)) {
            item.style.display = 'block';
            // Trigger animation again
            item.style.animation = 'none';
            item.offsetHeight; // reflow
            item.style.animation = null;
            item.style.animationPlayState = 'running';
        }
    });
}

// Lightbox Logic for Photos
function openLightbox(element) {
    const modal = document.getElementById("lightboxModal");
    const img = document.getElementById("lightboxImg");
    const captionText = document.getElementById("caption");
    const itemImg = element.querySelector('img');
    const itemCaption = element.querySelector('span').innerText;

    modal.style.display = "block";
    img.src = itemImg.src;
    captionText.innerHTML = itemCaption;
}

function closeLightbox() {
    document.getElementById("lightboxModal").style.display = "none";
}

// Video Modal Logic
function openVideoModal(videoSrc) {
    const modal = document.getElementById("videoModal");
    const video = document.getElementById("galleryVideo");
    
    modal.style.display = "block";
    video.querySelector('source').src = videoSrc;
    video.load();
    video.play();
}

function closeVideoModal() {
    const modal = document.getElementById("videoModal");
    const video = document.getElementById("galleryVideo");
    modal.style.display = "none";
    video.pause();
}

// Close modals on outside click
window.onclick = function(event) {
    const lightbox = document.getElementById("lightboxModal");
    const videoModal = document.getElementById("videoModal");
    if (event.target == lightbox) {
        closeLightbox();
    }
    if (event.target == videoModal) {
        closeVideoModal();
    }
};

// END: GALLERY_JS_FILE
