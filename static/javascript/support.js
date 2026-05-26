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

});

// FAQ Accordion Toggle
function toggleFAQ(element) {
    const item = element.parentElement;
    const isActive = item.classList.contains('active');

    // Close all other items
    document.querySelectorAll('.faq-item').forEach(faq => {
        faq.classList.remove('active');
    });

    // Toggle current item
    if (!isActive) {
        item.classList.add('active');
    }
}

// Ticket Modal Functions
function openTicketModal() {
    document.getElementById('ticketModal').style.display = 'block';
}

function closeTicketModal() {
    document.getElementById('ticketModal').style.display = 'none';
}

// Live Chat Functions
function toggleChat() {
    document.getElementById('chatWidget').classList.toggle('active');
}

function sendChatMessage() {
    const input = document.getElementById('chatInput');
    const chatBody = document.getElementById('chatBody');
    const msg = input.value.trim();

    if (msg) {
        // User Message
        const userMsg = document.createElement('div');
        userMsg.className = 'chat-msg user';
        userMsg.innerHTML = `<p>${msg}</p>`;
        chatBody.appendChild(userMsg);
        
        input.value = '';
        chatBody.scrollTop = chatBody.scrollHeight;

        // Bot Response (Simulated)
        setTimeout(() => {
            const botMsg = document.createElement('div');
            botMsg.className = 'chat-msg bot';
            botMsg.innerHTML = `<p>Thank you for your message. An agent will be with you shortly!</p>`;
            chatBody.appendChild(botMsg);
            chatBody.scrollTop = chatBody.scrollHeight;
        }, 1000);
    }
}

// Close modal on outside click
window.onclick = function(event) {
    const modal = document.getElementById('ticketModal');
    if (event.target == modal) {
        closeTicketModal();
    }
}

// Chat input enter key
document.getElementById('chatInput').addEventListener('keypress', function (e) {
    if (e.key === 'Enter') {
        sendChatMessage();
    }
});

// END: SUPPORT_JS_FILE
