// START: SUPPORT_JS_FILE

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

    const animatedElements = document.querySelectorAll('.animate-zoom, .animate-fade-up, .animate-slide-up, .animate-slide-left, .animate-slide-right');
    animatedElements.forEach(el => {
        el.style.animationPlayState = 'paused';
        observer.observe(el);
    });

    // Chat input enter key
    const chatInputEl = document.getElementById('chatInput');
    if (chatInputEl) {
        chatInputEl.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') sendChatMessage();
        });
    }

});

// ========== FAQ Accordion Toggle ==========
function toggleFAQ(element) {
    const item = element.parentElement;
    const isActive = item.classList.contains('active');
    document.querySelectorAll('.faq-item').forEach(faq => faq.classList.remove('active'));
    if (!isActive) item.classList.add('active');
}

// ========== Ticket Modal ==========
function openTicketModal() {
    document.getElementById('ticketModal').style.display = 'block';
}

function closeTicketModal() {
    document.getElementById('ticketModal').style.display = 'none';
}

// Close modal on outside click
window.onclick = function(event) {
    const modal = document.getElementById('ticketModal');
    if (event.target == modal) closeTicketModal();
};

// ========== Help Category Modals ==========
const categoryContent = {
    admission: {
        icon: '<i class="fas fa-user-plus" style="color:#6366f1;"></i>',
        title: 'Admission Help',
        content: `
            <div class="help-section">
                <h4><i class="fas fa-info-circle"></i> How to Apply Online</h4>
                <div class="modal-step-flow">
                    <div class="modal-step-card">
                        <div class="modal-step-num">01</div>
                        <div class="modal-step-text">Visit the <a href="/admission/" style="color:#818cf8; text-decoration: underline;">Admissions page</a>.</div>
                    </div>
                    <div class="modal-step-card">
                        <div class="modal-step-num">02</div>
                        <div class="modal-step-text">Fill in the <strong>Online Application Form</strong> (Name, Email, DOB, Class, Guardian's Mobile).</div>
                    </div>
                    <div class="modal-step-card">
                        <div class="modal-step-num">03</div>
                        <div class="modal-step-text">Click <strong>Submit Application</strong> and wait for Admin review.</div>
                    </div>
                    <div class="modal-step-card">
                        <div class="modal-step-num">04</div>
                        <div class="modal-step-text">Upon approval, your login <strong>credentials (username & password)</strong> will be sent to your email.</div>
                    </div>
                </div>
            </div>
            <div class="help-section">
                <h4><i class="fas fa-graduation-cap"></i> Eligibility Requirements</h4>
                <div class="modal-grid">
                    <div class="modal-info-card">
                        <i class="fas fa-certificate" style="color: var(--secondary);"></i>
                        <h5>Class 6 Admission</h5>
                        <p>Requires minimum <span class="modal-badge sec">GPA 4.00</span> in PEC exam.</p>
                    </div>
                    <div class="modal-info-card">
                        <i class="fas fa-atom" style="color: var(--primary);"></i>
                        <h5>Class 9 Science</h5>
                        <p>Requires minimum <span class="modal-badge">GPA 4.50</span> in JSC exam.</p>
                    </div>
                    <div class="modal-info-card">
                        <i class="fas fa-briefcase" style="color: var(--accent);"></i>
                        <h5>Class 9 Arts/Comm</h5>
                        <p>Requires minimum <span class="modal-badge acc">GPA 4.00</span> in JSC exam.</p>
                    </div>
                </div>
                <div class="help-note" style="margin-top: -10px; margin-bottom: 20px;">
                    <i class="fas fa-file-alt"></i> Required: Birth Certificate, 4 passport photos, and Transfer Certificate.
                </div>
            </div>
            <div class="help-section">
                <h4><i class="fas fa-money-bill-wave"></i> School Fee Structure</h4>
                <div class="modal-table-wrapper">
                    <table class="modal-table">
                        <thead>
                            <tr>
                                <th>Fee Category</th>
                                <th>Amount (BDT)</th>
                                <th>Billing Cycle</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>Admission Fee</td>
                                <td><strong>৳5,000</strong></td>
                                <td>One-time</td>
                            </tr>
                            <tr>
                                <td>Monthly Tuition</td>
                                <td><strong>৳1,200</strong></td>
                                <td>Monthly</td>
                            </tr>
                            <tr>
                                <td>Library & Lab Fee</td>
                                <td><strong>৳1,500</strong></td>
                                <td>Annually</td>
                            </tr>
                            <tr>
                                <td>Extracurriculars</td>
                                <td><strong>৳800</strong></td>
                                <td>Annually</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
            <div class="help-note">
                <i class="fas fa-phone"></i> For direct office queries, call: <strong>+880 1607-55120</strong> (Sun–Thu, 9AM–5PM)
            </div>
        `
    },
    academic: {
        icon: '<i class="fas fa-book-reader" style="color:#50e3c2;"></i>',
        title: 'Academic Support',
        content: `
            <div class="help-section">
                <h4><i class="fas fa-book"></i> Syllabus & Curriculum</h4>
                <div class="modal-grid">
                    <div class="modal-info-card">
                        <i class="fas fa-flask" style="color: var(--primary);"></i>
                        <h5>Science Group</h5>
                        <p>Physics, Chemistry, Biology, Higher Math. <span class="modal-badge">View in Academics</span></p>
                    </div>
                    <div class="modal-info-card">
                        <i class="fas fa-calculator" style="color: var(--secondary);"></i>
                        <h5>Commerce Group</h5>
                        <p>Accounting, Finance, Business. <span class="modal-badge sec">View in Academics</span></p>
                    </div>
                    <div class="modal-info-card">
                        <i class="fas fa-landmark" style="color: var(--accent);"></i>
                        <h5>Humanities Group</h5>
                        <p>History, Civics, Geography. <span class="modal-badge acc">View in Academics</span></p>
                    </div>
                </div>
                <div class="help-note" style="margin-top: -10px; margin-bottom: 20px;">
                    <i class="fas fa-download"></i> Go to the <a href="/academics/" style="color:#818cf8; text-decoration:underline;">Academics page</a> to download the full syllabus files.
                </div>
            </div>
            <div class="help-section">
                <h4><i class="fas fa-calendar-alt"></i> Class Routines</h4>
                <div class="modal-step-flow">
                    <div class="modal-step-card">
                        <div class="modal-step-num">01</div>
                        <div class="modal-step-text">Navigate to the <a href="/academics/" style="color:#818cf8; text-decoration: underline;">Academics page</a>.</div>
                    </div>
                    <div class="modal-step-card">
                        <div class="modal-step-num">02</div>
                        <div class="modal-step-text">Scroll down to the <strong>Class Routine</strong> section.</div>
                    </div>
                    <div class="modal-step-card">
                        <div class="modal-step-num">03</div>
                        <div class="modal-step-text">Select your Class (Class 6 - Class 10) from the dropdown.</div>
                    </div>
                    <div class="modal-step-card">
                        <div class="modal-step-num">04</div>
                        <div class="modal-step-text">Download the PDF version or view the routine schedule on screen.</div>
                    </div>
                </div>
            </div>
            <div class="help-section">
                <h4><i class="fas fa-chart-line"></i> Academic Grading System</h4>
                <div class="modal-table-wrapper">
                    <table class="modal-table">
                        <thead>
                            <tr>
                                <th>Marks Range</th>
                                <th>Letter Grade</th>
                                <th>Grade Point</th>
                                <th>Status</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>80% - 100%</td>
                                <td><span class="modal-badge sec">A+</span></td>
                                <td>5.00</td>
                                <td>Outstanding</td>
                            </tr>
                            <tr>
                                <td>70% - 79%</td>
                                <td><span class="modal-badge">A</span></td>
                                <td>4.00</td>
                                <td>Excellent</td>
                            </tr>
                            <tr>
                                <td>60% - 69%</td>
                                <td><span class="modal-badge">A-</span></td>
                                <td>3.50</td>
                                <td>Very Good</td>
                            </tr>
                            <tr>
                                <td>50% - 59%</td>
                                <td><span class="modal-badge acc">B</span></td>
                                <td>3.00</td>
                                <td>Good</td>
                            </tr>
                            <tr>
                                <td>33% - 49%</td>
                                <td><span class="modal-badge acc">C / D</span></td>
                                <td>2.00 / 1.00</td>
                                <td>Pass</td>
                            </tr>
                            <tr>
                                <td>0% - 32%</td>
                                <td><span class="modal-badge" style="background:rgba(239,68,68,0.15); color:#fca5a5; border-color:rgba(239,68,68,0.2);">F</span></td>
                                <td>0.00</td>
                                <td>Fail</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        `
    },
    account: {
        icon: '<i class="fas fa-key" style="color:#f59e0b;"></i>',
        title: 'Account &amp; Security',
        content: `
            <div class="help-section">
                <h4><i class="fas fa-lock-open"></i> Forgot Portal Password?</h4>
                <div class="modal-step-flow">
                    <div class="modal-step-card">
                        <div class="modal-step-num">01</div>
                        <div class="modal-step-text">Go to the <a href="/accounts/login/" style="color:#818cf8; text-decoration: underline;">Login page</a>.</div>
                    </div>
                    <div class="modal-step-card">
                        <div class="modal-step-num">02</div>
                        <div class="modal-step-text">Click the <strong>Forgot Password</strong> link under the form.</div>
                    </div>
                    <div class="modal-step-card">
                        <div class="modal-step-num">03</div>
                        <div class="modal-step-text">Enter your registered email address to receive a 6-digit OTP code.</div>
                    </div>
                    <div class="modal-step-card">
                        <div class="modal-step-num">04</div>
                        <div class="modal-step-text">Verify the OTP code on the verification page and set your new password.</div>
                    </div>
                </div>
                <div class="help-note">
                    <i class="fas fa-exclamation-triangle"></i> If you don't see the email, please check your <strong>Spam or Junk folder</strong>.
                </div>
            </div>
            <div class="help-section" style="margin-top:20px;">
                <h4><i class="fas fa-user-edit"></i> Profile Management</h4>
                <div class="modal-grid">
                    <div class="modal-info-card">
                        <i class="fas fa-image" style="color: var(--secondary);"></i>
                        <h5>Profile Image & Info</h5>
                        <p>Log in and navigate to Settings to upload your profile picture, gender, and blood group.</p>
                    </div>
                    <div class="modal-info-card">
                        <i class="fas fa-shield-alt" style="color: var(--primary);"></i>
                        <h5>Password Change</h5>
                        <p>Change your active session password anytime from the settings page securely.</p>
                    </div>
                </div>
            </div>
        `
    },
    technical: {
        icon: '<i class="fas fa-laptop-code" style="color:#ec4899;"></i>',
        title: 'Technical Issues',
        content: `
            <div class="help-section">
                <h4><i class="fas fa-tools"></i> Troubleshooting Common Issues</h4>
                <div class="modal-grid">
                    <div class="modal-info-card">
                        <i class="fas fa-sync" style="color: var(--primary);"></i>
                        <h5>Page not Loading</h5>
                        <p>Force refresh the browser tab using <kbd style="background:rgba(255,255,255,0.1); padding:2px 4px; border-radius:4px; font-size:11px;">Ctrl + F5</kbd> or clear cookies.</p>
                    </div>
                    <div class="modal-info-card">
                        <i class="fas fa-key" style="color: var(--secondary);"></i>
                        <h5>Incorrect Login</h5>
                        <p>Ensure Caps Lock is off and check that your username exactly matches the email credentials.</p>
                    </div>
                    <div class="modal-info-card">
                        <i class="fas fa-file-download" style="color: var(--accent);"></i>
                        <h5>Download Blocked</h5>
                        <p>Enable automatic PDF downloads or file saving permissions in browser settings.</p>
                    </div>
                </div>
            </div>
            <div class="help-section">
                <h4><i class="fas fa-globe"></i> Recommended Browsers</h4>
                <div class="modal-table-wrapper">
                    <table class="modal-table">
                        <thead>
                            <tr>
                                <th>Browser Name</th>
                                <th>Desktop Status</th>
                                <th>Mobile Status</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>Google Chrome</td>
                                <td><span class="modal-badge sec">Recommended</span></td>
                                <td><span class="modal-badge sec">Recommended</span></td>
                            </tr>
                            <tr>
                                <td>Mozilla Firefox</td>
                                <td><span class="modal-badge sec">Fully Compatible</span></td>
                                <td><span class="modal-badge sec">Fully Compatible</span></td>
                            </tr>
                            <tr>
                                <td>Safari</td>
                                <td><span class="modal-badge sec">Compatible (Mac)</span></td>
                                <td><span class="modal-badge sec">Recommended (iOS)</span></td>
                            </tr>
                            <tr>
                                <td>Microsoft Edge</td>
                                <td><span class="modal-badge sec">Compatible</span></td>
                                <td><span class="modal-badge sec">Compatible</span></td>
                            </tr>
                            <tr>
                                <td>Internet Explorer</td>
                                <td><span class="modal-badge" style="background:rgba(239,68,68,0.15); color:#fca5a5; border-color:rgba(239,68,68,0.2);">NOT Supported</span></td>
                                <td><span class="modal-badge" style="background:rgba(239,68,68,0.15); color:#fca5a5; border-color:rgba(239,68,68,0.2);">NOT Supported</span></td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
            <div class="help-note">
                <i class="fas fa-ticket-alt"></i> Still having issues? <button onclick="closeCategoryModal(); openTicketModal();" style="background:none; border:none; color:#818cf8; cursor:pointer; font-size:1rem; text-decoration:underline;">Submit a Support Ticket</button> or call <strong>+880 1607-55120</strong>.
            </div>
        `
    }
};

window.openCategoryModal = function(category) {
    const data = categoryContent[category];
    if (!data) return;

    document.getElementById('categoryModalIcon').innerHTML = data.icon;
    document.getElementById('categoryModalTitle').textContent = data.title.replace('&amp;', '&');
    document.getElementById('categoryModalBody').innerHTML = data.content;
    document.getElementById('categoryModal').classList.add('active');
    document.body.style.overflow = 'hidden';
};

window.closeCategoryModal = function() {
    document.getElementById('categoryModal').classList.remove('active');
    document.body.style.overflow = '';
};

document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        closeCategoryModal();
        closeTicketModal();
    }
});

// ========== Live Chat (AI Robot) ==========
function toggleChat() {
    const widget = document.getElementById('chatWidget');
    const floatBtn = document.getElementById('chatFloatBtn');
    widget.classList.toggle('active');
    if (widget.classList.contains('active')) {
        floatBtn.style.display = 'none';
        document.getElementById('chatInput').focus();
    } else {
        floatBtn.style.display = 'flex';
    }
}

function addBotTyping() {
    const chatBody = document.getElementById('chatBody');
    const typing = document.createElement('div');
    typing.className = 'chat-msg bot typing-indicator-msg';
    typing.id = 'typingIndicator';
    typing.innerHTML = `
        <div class="bot-msg-avatar"><i class="fas fa-robot"></i></div>
        <div class="bot-msg-bubble typing-bubble">
            <span></span><span></span><span></span>
        </div>
    `;
    chatBody.appendChild(typing);
    chatBody.scrollTop = chatBody.scrollHeight;
}

function removeTyping() {
    const typing = document.getElementById('typingIndicator');
    if (typing) typing.remove();
}

function sendChatMessage() {
    const input = document.getElementById('chatInput');
    const chatBody = document.getElementById('chatBody');
    const msg = input.value.trim();
    const sendBtn = document.getElementById('chatSendBtn');

    if (!msg) return;

    // User Message
    const userMsg = document.createElement('div');
    userMsg.className = 'chat-msg user';
    userMsg.innerHTML = `<div class="user-msg-bubble"><p>${escapeHtml(msg)}</p></div>`;
    chatBody.appendChild(userMsg);
    input.value = '';
    input.disabled = true;
    sendBtn.disabled = true;
    chatBody.scrollTop = chatBody.scrollHeight;

    // Typing indicator
    addBotTyping();

    // Fetch bot response
    fetch('/accounts/chatbot/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'X-CSRFToken': getCookie('csrftoken') },
        body: JSON.stringify({ message: msg })
    })
    .then(res => res.json())
    .then(data => {
        removeTyping();
        const botMsg = document.createElement('div');
        botMsg.className = 'chat-msg bot';
        const replyHtml = (data.reply || 'Sorry, I could not process your request.')
            .replace(/\n/g, '<br>')
            .replace(/•/g, '&bull;');
        botMsg.innerHTML = `
            <div class="bot-msg-avatar"><i class="fas fa-robot"></i></div>
            <div class="bot-msg-bubble"><p>${replyHtml}</p></div>
        `;
        chatBody.appendChild(botMsg);
        chatBody.scrollTop = chatBody.scrollHeight;
    })
    .catch(() => {
        removeTyping();
        const errMsg = document.createElement('div');
        errMsg.className = 'chat-msg bot';
        errMsg.innerHTML = `
            <div class="bot-msg-avatar"><i class="fas fa-robot"></i></div>
            <div class="bot-msg-bubble"><p>⚠️ Could not connect to the assistant. Please try again.</p></div>
        `;
        chatBody.appendChild(errMsg);
        chatBody.scrollTop = chatBody.scrollHeight;
    })
    .finally(() => {
        input.disabled = false;
        sendBtn.disabled = false;
        input.focus();
    });
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.appendChild(document.createTextNode(text));
    return div.innerHTML;
}

// ========== CSRF Cookie Helper ==========
function getCookie(name) {
    let val = null;
    if (document.cookie && document.cookie !== '') {
        document.cookie.split(';').forEach(c => {
            c = c.trim();
            if (c.startsWith(name + '=')) val = decodeURIComponent(c.slice(name.length + 1));
        });
    }
    return val;
}

// END: SUPPORT_JS_FILE
