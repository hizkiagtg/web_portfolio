// Main JavaScript for Portfolio Website

document.addEventListener('DOMContentLoaded', function() {
    // Initialize theme
    initializeTheme();
    
    // Initialize smooth scrolling
    initializeSmoothScrolling();
    
    // Initialize navigation highlighting
    initializeNavHighlight();
    
    // Initialize progress bar animations
    initializeProgressBars();
    
    // Add CSRF token to all AJAX requests
    setupCSRFToken();
});

// Theme Management
function initializeTheme() {
    const themeToggle = document.getElementById('theme-toggle');
    const themeIcon = document.getElementById('theme-icon');
    const htmlElement = document.documentElement;
    
    // Get saved theme or default to light
    const savedTheme = localStorage.getItem('theme') || 'light';
    setTheme(savedTheme);
    
    if (themeToggle) {
        themeToggle.addEventListener('click', function() {
            const currentTheme = htmlElement.getAttribute('data-bs-theme');
            const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
            setTheme(newTheme);
            localStorage.setItem('theme', newTheme);
        });
    }
    
    function setTheme(theme) {
        htmlElement.setAttribute('data-bs-theme', theme);
        if (themeIcon) {
            themeIcon.className = theme === 'dark' ? 'bi bi-sun-fill' : 'bi bi-moon-fill';
        }
    }
}

// Smooth Scrolling for Navigation Links
function initializeSmoothScrolling() {
    const navLinks = document.querySelectorAll('a[href^="#"]');
    
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href').substring(1);
            const targetElement = document.getElementById(targetId);
            
            if (targetElement) {
                const offsetTop = targetElement.offsetTop - 80; // Account for fixed navbar
                
                window.scrollTo({
                    top: offsetTop,
                    behavior: 'smooth'
                });
                
                // Close mobile menu if open
                const navbarCollapse = document.getElementById('navbarNav');
                if (navbarCollapse && navbarCollapse.classList.contains('show')) {
                    const bsCollapse = new bootstrap.Collapse(navbarCollapse);
                    bsCollapse.hide();
                }
            }
        });
    });
}

// Navigation Highlighting
function initializeNavHighlight() {
    const sections = document.querySelectorAll('section[id]');
    const navLinks = document.querySelectorAll('.navbar-nav .nav-link[href^="#"]');
    
    function highlightNavigation() {
        let current = '';
        
        sections.forEach(section => {
            const sectionTop = section.offsetTop - 100;
            const sectionHeight = section.offsetHeight;
            
            if (window.scrollY >= sectionTop && window.scrollY < sectionTop + sectionHeight) {
                current = section.getAttribute('id');
            }
        });
        
        navLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href') === `#${current}`) {
                link.classList.add('active');
            }
        });
    }
    
    // Throttle scroll events
    let ticking = false;
    window.addEventListener('scroll', function() {
        if (!ticking) {
            requestAnimationFrame(function() {
                highlightNavigation();
                ticking = false;
            });
            ticking = true;
        }
    });
}

// Progress Bar Animations
function initializeProgressBars() {
    const progressBars = document.querySelectorAll('.progress-bar');
    
    const observerOptions = {
        threshold: 0.5,
        rootMargin: '0px 0px -100px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const progressBar = entry.target;
                const width = progressBar.style.width;
                progressBar.style.width = '0%';
                
                setTimeout(() => {
                    progressBar.style.width = width;
                }, 100);
                
                observer.unobserve(progressBar);
            }
        });
    }, observerOptions);
    
    progressBars.forEach(bar => {
        observer.observe(bar);
    });
}

// CSRF Token Setup
function setupCSRFToken() {
    // Get CSRF token from cookie
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
    
    // Add CSRF token to meta tag if it doesn't exist
    if (!document.querySelector('meta[name="csrf-token"]')) {
        const csrfToken = getCookie('csrftoken');
        if (csrfToken) {
            const meta = document.createElement('meta');
            meta.name = 'csrf-token';
            meta.content = csrfToken;
            document.getElementsByTagName('head')[0].appendChild(meta);
        }
    }
}

// Utility Functions
function showAlert(message, type = 'info', duration = 5000) {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    alertDiv.style.cssText = 'top: 100px; right: 20px; z-index: 1060; max-width: 400px;';
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(alertDiv);
    
    // Auto remove after duration
    setTimeout(() => {
        if (alertDiv.parentNode) {
            alertDiv.remove();
        }
    }, duration);
}

// Loading State Management
function setLoadingState(button, isLoading) {
    if (isLoading) {
        button.dataset.originalText = button.innerHTML;
        button.innerHTML = '<i class="bi bi-hourglass-split me-2"></i>Loading...';
        button.disabled = true;
    } else {
        button.innerHTML = button.dataset.originalText || button.innerHTML;
        button.disabled = false;
    }
}

// Form Validation Helpers
function validateEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

function validateForm(formData) {
    const errors = [];
    
    if (!formData.name || formData.name.length < 2) {
        errors.push('Name must be at least 2 characters long');
    }
    
    if (!formData.email || !validateEmail(formData.email)) {
        errors.push('Please provide a valid email address');
    }
    
    if (!formData.subject || formData.subject.length < 5) {
        errors.push('Subject must be at least 5 characters long');
    }
    
    if (!formData.message || formData.message.length < 10) {
        errors.push('Message must be at least 10 characters long');
    }
    
    return errors;
}

// API Helper Functions
async function makeAPIRequest(url, options = {}) {
    const defaultOptions = {
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('meta[name="csrf-token"]')?.content || ''
        }
    };
    
    const mergedOptions = {
        ...defaultOptions,
        ...options,
        headers: {
            ...defaultOptions.headers,
            ...options.headers
        }
    };
    
    try {
        const response = await fetch(url, mergedOptions);
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || `HTTP error! status: ${response.status}`);
        }
        
        return data;
    } catch (error) {
        console.error('API Request failed:', error);
        throw error;
    }
}

// Intersection Observer for Animations
function createAnimationObserver() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in-up');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);
    
    // Observe elements with animation class
    document.querySelectorAll('[data-aos]').forEach(el => {
        observer.observe(el);
    });
}

// Initialize animations on load
window.addEventListener('load', function() {
    // Initialize custom animations if AOS is not available
    if (typeof AOS === 'undefined') {
        createAnimationObserver();
    }
});

// Lazy Loading for Images
function initializeLazyLoading() {
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver(function(entries) {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.classList.remove('lazy');
                    imageObserver.unobserve(img);
                }
            });
        });
        
        document.querySelectorAll('img[data-src]').forEach(img => {
            imageObserver.observe(img);
        });
    }
}

// Performance Monitoring
function logPerformance() {
    if ('performance' in window) {
        window.addEventListener('load', function() {
            setTimeout(function() {
                const perfData = performance.getEntriesByType('navigation')[0];
                const loadTime = perfData.loadEventEnd - perfData.loadEventStart;
                console.log(`Page loaded in ${loadTime}ms`);
            }, 0);
        });
    }
}

// Initialize performance monitoring in development
if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
    logPerformance();
}

// Export utility functions for use in other scripts
window.PortfolioUtils = {
    showAlert,
    setLoadingState,
    validateEmail,
    validateForm,
    makeAPIRequest
};