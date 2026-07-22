// START: ACADEMICS_JS_FILE

document.addEventListener("DOMContentLoaded", function() {
    
    // ---- Scroll Animation using IntersectionObserver (CSS class toggle, fixed) ----
    const observerOptions = {
        root: null,
        rootMargin: '0px 0px -60px 0px',
        threshold: 0.1
    };

    const observer = new IntersectionObserver((entries, obs) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                obs.unobserve(entry.target);
            }
        });
    }, observerOptions);

    document.querySelectorAll('.animate-in, .animate-zoom').forEach(el => {
        observer.observe(el);
    });

    // ---- Syllabus Modal ----
    const syllabusDataEl = document.getElementById('syllabusData');
    let syllabusData = {};
    if (syllabusDataEl) {
        try { syllabusData = JSON.parse(syllabusDataEl.textContent); } catch(e) {}
    }

    const groupIcons = {
        science: { icon: 'fa-flask', color: '#4a90e2', label: 'Science Group Syllabus' },
        commerce: { icon: 'fa-calculator', color: '#50e3c2', label: 'Commerce Group Syllabus' },
        humanities: { icon: 'fa-palette', color: '#ec4899', label: 'Humanities Group Syllabus' }
    };

    window.openSyllabusModal = function(group) {
        const modal = document.getElementById('syllabusModal');
        const title = document.getElementById('syllabusModalTitle');
        const body = document.getElementById('syllabusModalBody');
        const items = syllabusData[group] || [];
        const meta = groupIcons[group] || { icon: 'fa-book-open', color: '#fff', label: 'Syllabus' };

        title.innerHTML = `<i class="fas ${meta.icon}" style="color:${meta.color};"></i> ${meta.label}`;

        if (items.length === 0) {
            body.innerHTML = `
                <div class="syllabus-empty-state">
                    <i class="fas fa-folder-open"></i>
                    <p>No syllabus files have been uploaded yet for this group.</p>
                    <small>Admin can add syllabuses via the Django Admin panel.</small>
                </div>`;
        } else {
            body.innerHTML = items.map(item => `
                <div class="syllabus-item">
                    <div class="syllabus-item-info">
                        <div class="subject-name">${item.subject}</div>
                        <div class="syllabus-title">${item.title}</div>
                        <div class="upload-date"><i class="far fa-calendar-alt"></i> Uploaded: ${item.uploaded}</div>
                    </div>
                    <a href="${item.file}" class="syllabus-download-btn" target="_blank" download>
                        <i class="fas fa-download"></i> Download
                    </a>
                </div>
            `).join('');
        }

        modal.classList.add('active');
        document.body.style.overflow = 'hidden';
    };

    window.closeSyllabusModal = function() {
        document.getElementById('syllabusModal').classList.remove('active');
        document.body.style.overflow = '';
    };

    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') closeSyllabusModal();
    });

    // ---- Class Routine Selector ----
    const routineDataEl = document.getElementById('routineData');
    let routineData = {};
    if (routineDataEl) {
        try { routineData = JSON.parse(routineDataEl.textContent); } catch(e) {}
    }

    window.showRoutineForClass = function(classId) {
        const display = document.getElementById('routineDisplay');
        const empty = document.getElementById('routineEmpty');
        const classNameEl = document.getElementById('routineClassName');
        const fileContainer = document.getElementById('routineFileContainer');
        const downloadBtn = document.getElementById('routineDownloadBtn');

        if (!classId) {
            display.style.display = 'none';
            return;
        }

        const cls = routineData[classId];

        // Show the display panel regardless
        if (empty) empty.style.display = 'none';
        display.style.display = 'block';

        // Class name from routineData or from option text as fallback
        const selectedOption = document.querySelector(`#classSelect option[value="${classId}"]`);
        const className = (cls && cls.name) ? cls.name : (selectedOption ? selectedOption.textContent : 'Class');
        classNameEl.innerHTML = `<i class="fas fa-graduation-cap" style="color:#4a90e2;"></i> ${className} — Class Routine`;

        if (cls && cls.routines && cls.routines.length > 0) {
            // Show first file in download button
            downloadBtn.href = cls.routines[0].file;
            downloadBtn.style.display = 'inline-flex';

            fileContainer.innerHTML = cls.routines.map(r => {
                const ext = r.file.split('.').pop().toLowerCase();
                const isImage = ['jpg', 'jpeg', 'png', 'gif', 'webp'].includes(ext);
                const isPdf = ext === 'pdf';
                const fileIcon = isPdf ? 'fa-file-pdf' : isImage ? 'fa-file-image' : 'fa-file-alt';
                const iconColor = isPdf ? '#ef4444' : isImage ? '#8b5cf6' : '#4a90e2';

                return `
                    <div class="routine-file-item">
                        <div class="routine-file-info">
                            <i class="fas ${fileIcon}" style="color:${iconColor};"></i>
                            <div>
                                <div class="file-name">${r.title}</div>
                                <div class="file-date"><i class="far fa-calendar-alt"></i> ${r.uploaded}</div>
                            </div>
                        </div>
                        <a href="${r.file}" class="btn-download" download target="_blank">
                            <i class="fas fa-download"></i> Download
                        </a>
                    </div>
                    ${isImage ? `<div style="margin-top:12px; border-radius:10px; overflow:hidden;"><img src="${r.file}" style="width:100%; max-height:500px; object-fit:contain; border-radius:10px; background:#000;" alt="${r.title}"></div>` : ''}
                `;
            }).join('');
        } else {
            // No routines uploaded yet for this class
            downloadBtn.style.display = 'none';
            fileContainer.innerHTML = `
                <div class="routine-empty" style="display:block;">
                    <i class="fas fa-calendar-times"></i>
                    <p>রুটিন এখনো আপলোড করা হয়নি। / No routine uploaded yet for this class.</p>
                    <small style="color:#4a90e2;">Admin can upload routines from the Admin Panel → Academics → Class Routines.</small>
                </div>`;
        }
    };

});

// END: ACADEMICS_JS_FILE
