// ============================================================
// TEACHER MESSAGES JS — student_messages.html
// School Management System
// ============================================================

// START: TEACHER_MESSAGES_JS

let activeStudentId = null;
let pollInterval = null;

function selectStudent(studentId, studentName, element) {
    activeStudentId = studentId;
    
    // Update active class in sidebar
    document.querySelectorAll('.student-item').forEach(item => item.classList.remove('active'));
    element.classList.add('active');

    // Toggle visibility
    const welcomeEl = document.getElementById('chatWelcome');
    const contentEl = document.getElementById('chatContent');
    
    if (welcomeEl) welcomeEl.style.display = 'none';
    if (contentEl) contentEl.style.display = 'flex';
    
    const nameEl = document.getElementById('activeStudentName');
    if (nameEl) nameEl.innerText = studentName;
    
    const bodyEl = document.getElementById('chatBody');
    if (bodyEl) bodyEl.innerHTML = '<div style="text-align:center; color:#64748b; margin-top:50px;">Loading conversation history...</div>';

    loadChatHistory();

    // Setup polling
    if (pollInterval) clearInterval(pollInterval);
    pollInterval = setInterval(loadChatHistory, 5000);

    // Handle Input Enter Key
    const inputEl = document.getElementById('chatInput');
    if (inputEl) {
        inputEl.removeEventListener('keypress', handleKeyPress);
        inputEl.addEventListener('keypress', handleKeyPress);
    }
}

function handleKeyPress(e) {
    if (e.key === 'Enter') {
        sendChatMessage();
    }
}

function loadChatHistory() {
    if (!activeStudentId) return;

    fetch(`/teachers/messages/chat/?student_id=${activeStudentId}`)
        .then(res => res.json())
        .then(data => {
            if (data.status === 'success') {
                const chatBody = document.getElementById('chatBody');
                if (!chatBody) return;
                
                const isAtBottom = chatBody.scrollHeight - chatBody.clientHeight <= chatBody.scrollTop + 50;

                chatBody.innerHTML = '';
                if (data.messages.length === 0) {
                    chatBody.innerHTML = '<div style="text-align:center; color:#64748b; margin-top:50px;">No messages yet. Send a message to start conversation!</div>';
                    return;
                }

                data.messages.forEach(msg => {
                    const isSentByMe = msg.sender_id === data.current_user_id;
                    const bubble = document.createElement('div');
                    bubble.className = `chat-bubble ${isSentByMe ? 'sent' : 'received'}`;
                    bubble.innerHTML = `
                        <div>${escapeHTML(msg.message)}</div>
                        <span class="chat-time">${msg.created_at}</span>
                    `;
                    chatBody.appendChild(bubble);
                });

                if (isAtBottom) {
                    chatBody.scrollTop = chatBody.scrollHeight;
                }
            }
        })
        .catch(err => console.error("Error loading chat history:", err));
}

function sendChatMessage() {
    const input = document.getElementById('chatInput');
    if (!input) return;
    
    const text = input.value.trim();
    if (!text || !activeStudentId) return;

    input.value = '';

    fetch('/teachers/messages/chat/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({
            student_id: activeStudentId,
            message: text
        })
    })
    .then(res => res.json())
    .then(data => {
        if (data.status === 'success') {
            loadChatHistory();
        }
    })
    .catch(err => console.error("Error sending message:", err));
}

function filterStudents() {
    const searchEl = document.getElementById('studentSearch');
    if (!searchEl) return;
    
    const q = searchEl.value.toLowerCase();
    const items = document.querySelectorAll('.student-item');
    items.forEach(item => {
        const nameEl = item.querySelector('h4');
        if (nameEl) {
            const name = nameEl.innerText.toLowerCase();
            item.style.display = name.includes(q) ? 'flex' : 'none';
        }
    });
}

function escapeHTML(str) {
    return str.replace(/[&<>'"]/g, 
        tag => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', "'": '&#39;', '"': '&quot;' }[tag] || tag)
    );
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// END: TEACHER_MESSAGES_JS
