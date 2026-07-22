// START: GALLERY_JS_FILE

// Gallery Modal: Open full-size image or video
function openModal(url, category) {
    const modal = document.getElementById('galleryModal');
    const modalBody = document.getElementById('modalBody');
    modal.style.display = 'flex';

    if (category === 'image') {
        modalBody.innerHTML = `<img src="${url}" class="modal-content animated fadeIn">`;
    } else {
        modalBody.innerHTML = `
            <video controls autoplay class="modal-content animated fadeIn" style="max-height: 80vh;">
                <source src="${url}" type="video/mp4">
                Your browser does not support the video tag.
            </video>`;
    }

    document.body.style.overflow = 'hidden';
}

// Gallery Modal: Close
function closeModal() {
    const modal = document.getElementById('galleryModal');
    const modalBody = document.getElementById('modalBody');
    modal.style.display = 'none';
    modalBody.innerHTML = '';
    document.body.style.overflow = 'auto';
}

document.addEventListener('DOMContentLoaded', function () {
    // Close modal on escape key
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') closeModal();
    });

    // Close modal on clicking outside content
    const galleryModal = document.getElementById('galleryModal');
    if (galleryModal) {
        galleryModal.addEventListener('click', (e) => {
            if (e.target.id === 'galleryModal') closeModal();
        });
    }
});

// END: GALLERY_JS_FILE
