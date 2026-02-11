// ========================================
// CV Website JavaScript - AI Optimized
// ========================================

// Language toggle functionality
function showCV(lang) {
    // Hide all CV content
    document.querySelectorAll('.cv-content').forEach(el => {
        el.classList.remove('active');
    });

    // Remove active class from all buttons
    document.querySelectorAll('.lang-btn').forEach(btn => {
        btn.classList.remove('active');
    });

    // Show selected CV content
    document.getElementById(`cv-${lang}`).classList.add('active');

    // Add active class to selected button
    document.getElementById(`btn-${lang}`).classList.add('active');

    // Save preference to localStorage
    localStorage.setItem('cv-lang-preference', lang);

    // Update URL hash without scrolling
    history.pushState(null, null, `#${lang}`);

    // Update meta description based on language
    updateMetaDescription(lang);
}

// Update meta description for SEO
function updateMetaDescription(lang) {
    const metaDesc = document.querySelector('meta[name="description"]');
    if (lang === 'fi') {
        metaDesc.setAttribute('content', 'AI Developer ja AI Quality Engineering -osaaja - LLM, Agenttijärjestelmät, RAG ja Testiautomaatio');
    } else {
        metaDesc.setAttribute('content', 'AI Developer and AI Quality Engineering specialist - LLM, Agent Systems, RAG, and Test Automation');
    }
}

// Initialize: check URL hash or localStorage
function init() {
    const hash = window.location.hash.substring(1);
    const saved = localStorage.getItem('cv-lang-preference');
    const lang = (hash === 'en' || hash === 'fi') ? hash : (saved || 'en');
    showCV(lang);
}

// Add smooth scroll behavior
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        const href = this.getAttribute('href');
        if (href !== '#en' && href !== '#fi') {
            e.preventDefault();
            const target = document.querySelector(href);
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        }
    });
});

// Add animation on scroll
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

// Observe sections for animation
document.addEventListener('DOMContentLoaded', () => {
    init();

    // Add initial animation state to sections
    document.querySelectorAll('.section').forEach(section => {
        section.style.opacity = '0';
        section.style.transform = 'translateY(20px)';
        section.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
        observer.observe(section);
    });

    // Handle browser back/forward buttons
    window.addEventListener('popstate', () => {
        const hash = window.location.hash.substring(1);
        if (hash === 'en' || hash === 'fi') {
            showCV(hash);
        }
    });
});

// Keyboard navigation for accessibility
document.addEventListener('keydown', (e) => {
    if (e.altKey) {
        if (e.key === '1' || e.key === 'e') {
            e.preventDefault();
            showCV('en');
        } else if (e.key === '2' || e.key === 'f') {
            e.preventDefault();
            showCV('fi');
        }
    }
});

// Print functionality - always show English when printing
window.addEventListener('beforeprint', () => {
    // Ensure English version is visible when printing
    document.querySelectorAll('.cv-content').forEach(el => {
        el.classList.remove('active');
    });
    document.getElementById('cv-en').classList.add('active');
});

// Add to calendar functionality (optional)
function addToCalendar() {
    const event = {
        title: 'Interview with Renata Baldissara-Kunnela',
        description: 'AI Developer & Quality Engineering Specialist',
        location: 'Video Call / Viitasaari, Finland',
        email: 'renatbk.linkedin@gmail.com'
    };
    // Calendar integration can be added here
    console.log('Calendar event:', event);
}

// Export functionality - save CV as PDF
function exportToPDF() {
    window.print();
}

// Copy email to clipboard
function copyEmail() {
    navigator.clipboard.writeText('renatbk.linkedin@gmail.com').then(() => {
        // Could add toast notification here
        console.log('Email copied to clipboard');
    });
}

// Track CV views (for analytics - optional)
function trackView() {
    const views = localStorage.getItem('cv-views') || 0;
    localStorage.setItem('cv-views', parseInt(views) + 1);
    console.log('CV views:', parseInt(views) + 1);
}

trackView();

// Service Worker registration for offline support (optional)
if ('serviceWorker' in navigator) {
    // Add service worker registration here if needed
    console.log('Service Worker support detected');
}

console.log('CV Website Loaded - AI Optimized Version');
