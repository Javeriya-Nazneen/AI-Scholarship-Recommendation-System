// AI-Scholar Main JavaScript
// Author: AI-Scholar Team

// Header search function - MUST BE GLOBAL for onclick attribute
function searchScholarships() {
    const searchInput = document.getElementById('headerScholarshipSearch');
    if (!searchInput) {
        console.error('Search input not found!');
        return;
    }
    
    const searchQuery = searchInput.value.trim();
    
    console.log('Search triggered with query:', searchQuery);
    
    // Redirect to scholarships page with search query
    if (searchQuery) {
        window.location.href = `/scholarships/?search=${encodeURIComponent(searchQuery)}`;
    } else {
        window.location.href = '/scholarships/';
    }
}

document.addEventListener('DOMContentLoaded', function() {
    console.log('AI-Scholar initialized!');
    
    // Initialize features
    initializeAnimations();
    initializeNavigation();
    initializeNotifications();
    initializeHeaderSearch();
});

// Initialize header search functionality
function initializeHeaderSearch() {
    const searchInput = document.getElementById('headerScholarshipSearch');
    if (searchInput) {
        console.log('Header search initialized');
        
        // Search on Enter key
        searchInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                searchScholarships();
            }
        });
    } else {
        console.warn('Header search input not found');
    }
}

// Smooth scroll for anchor links
function initializeNavigation() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// Intersection Observer for fade-in animations
function initializeAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Observe all cards
    document.querySelectorAll('.card').forEach(card => {
        observer.observe(card);
    });
}

// Notification system
function initializeNotifications() {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.animation = 'fadeOut 0.5s';
            setTimeout(() => alert.remove(), 500);
        }, 5000);
    });
}

// Show notification
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} fade-in`;
    notification.textContent = message;
    notification.style.cssText = `
        position: fixed;
        top: 100px;
        right: 20px;
        z-index: 9999;
        min-width: 300px;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: var(--shadow-lg);
        background: white;
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'fadeOut 0.5s';
        setTimeout(() => notification.remove(), 500);
    }, 5000);
}

// Form validation
function validateForm(formId) {
    const form = document.getElementById(formId);
    if (!form) return false;
    
    const inputs = form.querySelectorAll('input[required], select[required], textarea[required]');
    let isValid = true;
    
    inputs.forEach(input => {
        if (!input.value.trim()) {
            isValid = false;
            input.style.borderColor = 'var(--danger)';
            
            setTimeout(() => {
                input.style.borderColor = '';
            }, 3000);
        }
    });
    
    if (!isValid) {
        showNotification('Please fill in all required fields', 'danger');
    }
    
    return isValid;
}

// AJAX helper function
async function fetchAPI(url, method = 'GET', data = null) {
    const options = {
        method: method,
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        }
    };
    
    if (data && method !== 'GET') {
        options.body = JSON.stringify(data);
    }
    
    try {
        const response = await fetch(url, options);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        console.error('API Error:', error);
        showNotification('An error occurred. Please try again.', 'danger');
        throw error;
    }
}

// Get CSRF token
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

// Loading spinner
function showLoading(element) {
    const spinner = document.createElement('div');
    spinner.className = 'loading-spinner';
    spinner.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Loading...';
    spinner.style.cssText = `
        text-align: center;
        padding: 2rem;
        color: var(--primary-color);
        font-size: 1.2rem;
    `;
    element.appendChild(spinner);
    return spinner;
}

function hideLoading(spinner) {
    if (spinner && spinner.parentElement) {
        spinner.remove();
    }
}

// Copy to clipboard
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        showNotification('Copied to clipboard!', 'success');
    }).catch(err => {
        console.error('Failed to copy:', err);
        showNotification('Failed to copy', 'danger');
    });
}

// Format date
function formatDate(dateString) {
    const options = { year: 'numeric', month: 'long', day: 'numeric' };
    return new Date(dateString).toLocaleDateString('en-US', options);
}

// Format currency in Indian Rupees
function formatCurrency(amount) {
    if (amount >= 10000000) { // 1 Crore
        return `₹${(amount/10000000).toFixed(2)} Cr`;
    } else if (amount >= 100000) { // 1 Lakh
        return `₹${(amount/100000).toFixed(2)} L`;
    } else {
        return new Intl.NumberFormat('en-IN', {
            style: 'currency',
            currency: 'INR',
            maximumFractionDigits: 0
        }).format(amount);
    }
}

// Debounce function
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// ========================================
// FLOATING CHATBOT FUNCTIONALITY
// ========================================

document.addEventListener('DOMContentLoaded', function() {
    initializeChatbot();
});

function initializeChatbot() {
    const chatbotToggle = document.getElementById('chatbot-toggle');
    const chatbotWindow = document.getElementById('chatbot-window');
    const chatbotClose = document.getElementById('chatbot-close');
    
    if (!chatbotToggle || !chatbotWindow || !chatbotClose) {
        console.log('Chatbot elements not found');
        return;
    }
    
    let hasShownWelcome = false;
    
    // Toggle chatbot
    chatbotToggle.addEventListener('click', function() {
        chatbotWindow.classList.toggle('active');
        if (chatbotWindow.classList.contains('active')) {
            document.getElementById('chatbot-input').focus();
            
            // Show welcome message on first open
            if (!hasShownWelcome) {
                setTimeout(() => {
                    const welcomeMessage = "👋 Hello! I'm your AI Scholarship Assistant. I can help you with:\n\n• Finding eligible scholarships\n• Checking deadlines\n• Application tips and advice\n• Required documents\n• Your profile and applications\n\nWhat would you like to know?";
                    addChatMessage(welcomeMessage, 'bot');
                    hasShownWelcome = true;
                }, 500);
            }
        }
    });
    
    // Close chatbot
    chatbotClose.addEventListener('click', function() {
        chatbotWindow.classList.remove('active');
    });
    
    // Close on outside click
    document.addEventListener('click', function(e) {
        if (!chatbotToggle.contains(e.target) && 
            !chatbotWindow.contains(e.target)) {
            chatbotWindow.classList.remove('active');
        }
    });
}

// Send chatbot message
function sendChatbotMessage() {
    const input = document.getElementById('chatbot-input');
    const message = input.value.trim();
    
    if (!message) return;
    
    // Add user message
    addChatMessage(message, 'user');
    input.value = '';
    
    // Show typing indicator
    const typingIndicator = addTypingIndicator();
    
    // Send to API
    fetch('/api/chatbot/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({ message: message })
    })
    .then(response => response.json())
    .then(data => {
        // Remove typing indicator
        typingIndicator.remove();
        
        // Add bot response
        addChatMessage(data.response, 'bot');
    })
    .catch(error => {
        console.error('Chatbot error:', error);
        typingIndicator.remove();
        addChatMessage('Sorry, I encountered an error. Please try again.', 'bot');
    });
}

// Add message to chat
function addChatMessage(message, sender) {
    const messagesContainer = document.getElementById('chatbot-messages');
    
    const messageDiv = document.createElement('div');
    messageDiv.className = `chatbot-message ${sender}-message`;
    messageDiv.style.animation = 'slideUp 0.3s ease-out';
    
    const avatar = document.createElement('div');
    avatar.className = 'message-avatar';
    avatar.innerHTML = sender === 'bot' 
        ? '<i class="fas fa-robot"></i>' 
        : '<i class="fas fa-user"></i>';
    
    const content = document.createElement('div');
    content.className = 'message-content';
    
    // Format message (convert markdown-like syntax)
    const formattedMessage = formatChatMessage(message);
    content.innerHTML = formattedMessage;
    
    if (sender === 'user') {
        messageDiv.appendChild(content);
        messageDiv.appendChild(avatar);
    } else {
        messageDiv.appendChild(avatar);
        messageDiv.appendChild(content);
    }
    
    messagesContainer.appendChild(messageDiv);
    
    // Smooth scroll with animation
    setTimeout(() => {
        messagesContainer.scrollTo({
            top: messagesContainer.scrollHeight,
            behavior: 'smooth'
        });
    }, 100);
}

// Format chat message (convert markdown-like syntax to HTML)
function formatChatMessage(message) {
    // Convert **bold** to <strong>
    message = message.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
    
    // Convert *italic* to <em>
    message = message.replace(/\*([^*]+)\*/g, '<em>$1</em>');
    
    // Convert `code` to <code>
    message = message.replace(/`([^`]+)`/g, '<code>$1</code>');
    
    // Convert links [text](url) to <a>
    message = message.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank">$1</a>');
    
    // Convert line breaks to <br>
    message = message.replace(/\n/g, '<br>');
    
    // Convert bullet points
    message = message.replace(/^• (.+)$/gm, '<li>$1</li>');
    message = message.replace(/(<li>.*<\/li>)/s, '<ul>$1</ul>');
    
    return message;
}

// Add typing indicator
function addTypingIndicator() {
    const messagesContainer = document.getElementById('chatbot-messages');
    
    const messageDiv = document.createElement('div');
    messageDiv.className = 'chatbot-message bot-message typing-indicator';
    
    const avatar = document.createElement('div');
    avatar.className = 'message-avatar';
    avatar.innerHTML = '<i class="fas fa-robot"></i>';
    
    const content = document.createElement('div');
    content.className = 'message-content';
    content.innerHTML = '<p><i class="fas fa-ellipsis-h fa-pulse"></i> Thinking...</p>';
    
    messageDiv.appendChild(avatar);
    messageDiv.appendChild(content);
    messagesContainer.appendChild(messageDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
    
    return messageDiv;
}

// Handle Enter key
function handleChatbotKeyPress(event) {
    if (event.key === 'Enter') {
        sendChatbotMessage();
    }
}

// Send quick reply
function sendQuickReply(message) {
    document.getElementById('chatbot-input').value = message;
    sendChatbotMessage();
}

// Mobile Menu Toggle
function toggleMobileMenu() {
    const navMenu = document.querySelector('.nav-menu');
    if (navMenu) {
        navMenu.classList.toggle('active');
    }
}

// Export functions for use in other scripts
window.AIScholar = {
    showNotification,
    validateForm,
    fetchAPI,
    showLoading,
    hideLoading,
    copyToClipboard,
    formatDate,
    formatCurrency,
    debounce,
    getCookie
};
