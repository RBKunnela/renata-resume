// ========================================
// Portfolio Website JavaScript
// Renata Baldissara-Kunnela
// ========================================

// ===== LANGUAGE SYSTEM =====
const translations = {
    en: {
        typedPhrases: [
            'LLM & Agent Systems',
            'AI Quality Engineering',
            'RAG & Fine-tuning',
            'Guardrails & Evaluation',
            'Production AI Builder'
        ]
    },
    fi: {
        typedPhrases: [
            'LLM & Agenttijärjestelmät',
            'AI Quality Engineering',
            'RAG & Hienosäätö',
            'Guardrails & Evaluointi',
            'Tuotanto-AI-rakentaja'
        ]
    }
};

let currentLang = 'en';

function setLang(lang) {
    currentLang = lang;

    // Update button states
    document.querySelectorAll('.lang-btn').forEach(btn => btn.classList.remove('active'));
    const activeBtn = document.getElementById(`btn-${lang}`);
    if (activeBtn) activeBtn.classList.add('active');

    // Update all data-en / data-fi elements
    document.querySelectorAll('[data-en]').forEach(el => {
        const text = el.getAttribute(`data-${lang}`);
        if (text !== null) {
            el.innerHTML = text;
        }
    });

    // Update nav links
    document.querySelectorAll('.nav-link[data-en]').forEach(el => {
        const text = el.getAttribute(`data-${lang}`);
        if (text !== null) el.textContent = text;
    });

    // Update HTML lang attribute
    document.documentElement.lang = lang === 'fi' ? 'fi' : 'en';

    // Update meta description
    const metaDesc = document.querySelector('meta[name="description"]');
    if (metaDesc) {
        metaDesc.setAttribute('content', lang === 'fi'
            ? 'AI Developer ja AI Quality Engineering -osaaja — LLM, Agenttijärjestelmät, RAG ja Testiautomaatio. Portfolio tuotantotason AI-projekteista.'
            : 'AI Developer and AI Quality Engineering specialist — LLM, Agent Systems, RAG, and Test Automation. Portfolio of production AI projects.'
        );
    }

    // Save preference
    localStorage.setItem('portfolio-lang', lang);

    // Update URL hash
    history.replaceState(null, null, `#${lang}`);

    // Restart typed animation with new phrases
    if (typedInstance) {
        typedInstance.restart(translations[lang].typedPhrases);
    }
}

// ===== TYPED TEXT ANIMATION =====
class TypedText {
    constructor(elementId, phrases, options = {}) {
        this.el = document.getElementById(elementId);
        this.phrases = phrases;
        this.typeSpeed = options.typeSpeed || 60;
        this.deleteSpeed = options.deleteSpeed || 35;
        this.pauseAfterType = options.pauseAfterType || 2000;
        this.pauseAfterDelete = options.pauseAfterDelete || 500;
        this.phraseIndex = 0;
        this.charIndex = 0;
        this.isDeleting = false;
        this.timer = null;
        if (this.el) this.tick();
    }

    tick() {
        const phrase = this.phrases[this.phraseIndex];
        const current = phrase.substring(0, this.charIndex);
        if (this.el) this.el.textContent = current;

        let delay = this.isDeleting ? this.deleteSpeed : this.typeSpeed;

        if (!this.isDeleting && this.charIndex === phrase.length) {
            delay = this.pauseAfterType;
            this.isDeleting = true;
        } else if (this.isDeleting && this.charIndex === 0) {
            this.isDeleting = false;
            this.phraseIndex = (this.phraseIndex + 1) % this.phrases.length;
            delay = this.pauseAfterDelete;
        }

        this.charIndex += this.isDeleting ? -1 : 1;
        this.timer = setTimeout(() => this.tick(), delay);
    }

    restart(newPhrases) {
        if (this.timer) clearTimeout(this.timer);
        this.phrases = newPhrases;
        this.phraseIndex = 0;
        this.charIndex = 0;
        this.isDeleting = false;
        this.tick();
    }
}

let typedInstance = null;

// ===== THEME SYSTEM =====
function initTheme() {
    const saved = localStorage.getItem('portfolio-theme');
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    const theme = saved || (prefersDark ? 'dark' : 'light');
    applyTheme(theme);
}

function applyTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('portfolio-theme', theme);
    const icon = document.getElementById('themeIcon');
    if (icon) {
        icon.className = theme === 'dark' ? 'fas fa-sun' : 'fas fa-moon';
    }
}

function toggleTheme() {
    const current = document.documentElement.getAttribute('data-theme');
    applyTheme(current === 'dark' ? 'light' : 'dark');
}

// ===== NAVBAR =====
function initNavbar() {
    const navbar = document.getElementById('navbar');
    const hamburger = document.getElementById('navHamburger');
    const navLinks = document.getElementById('navLinks');

    // Scroll effect
    window.addEventListener('scroll', () => {
        if (window.scrollY > 20) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
        updateActiveNavLink();
    }, { passive: true });

    // Hamburger menu
    if (hamburger) {
        hamburger.addEventListener('click', () => {
            navLinks.classList.toggle('open');
        });
    }

    // Close menu on link click
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', () => {
            navLinks.classList.remove('open');
        });
    });
}

function updateActiveNavLink() {
    const sections = document.querySelectorAll('section[id], .section-block[id]');
    let current = '';

    sections.forEach(section => {
        const sectionTop = section.offsetTop - 100;
        if (window.scrollY >= sectionTop) {
            current = section.getAttribute('id');
        }
    });

    document.querySelectorAll('.nav-link').forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href') === `#${current}`) {
            link.classList.add('active');
        }
    });
}

// ===== SCROLL ANIMATIONS =====
function initScrollAnimations() {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                observer.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '0px 0px -40px 0px'
    });

    // Add fade-in class to animatable elements
    const animatables = document.querySelectorAll(
        '.expertise-card, .project-card, .timeline-item, .edu-card, ' +
        '.skill-category, .cert-card, .contact-item, .cta-card, .stat-item'
    );

    animatables.forEach((el, i) => {
        el.classList.add('fade-in');
        el.style.transitionDelay = `${(i % 6) * 0.07}s`;
        observer.observe(el);
    });

    // Also observe section headers
    document.querySelectorAll('.section-header, .about-text, .projects-category-label').forEach(el => {
        el.classList.add('fade-in');
        observer.observe(el);
    });
}

// ===== SMOOTH SCROLL =====
function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            // Allow lang hash changes to pass through
            if (href === '#en' || href === '#fi') return;

            e.preventDefault();
            const target = document.querySelector(href);
            if (target) {
                target.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        });
    });
}

// ===== PRINT / EXPORT =====
function exportToPDF() {
    window.print();
}

// ===== COPY EMAIL =====
function copyEmail() {
    navigator.clipboard.writeText('renatbk.linkedin@gmail.com').then(() => {
        showToast('Email copied to clipboard!');
    });
}

// ===== TOAST NOTIFICATION =====
function showToast(message) {
    const existing = document.querySelector('.toast');
    if (existing) existing.remove();

    const toast = document.createElement('div');
    toast.className = 'toast';
    toast.textContent = message;
    toast.style.cssText = `
        position: fixed;
        bottom: 24px;
        right: 24px;
        background: var(--bg-card);
        border: 1px solid var(--border);
        color: var(--text);
        padding: 12px 20px;
        border-radius: 8px;
        font-size: 0.9rem;
        font-weight: 500;
        box-shadow: var(--shadow);
        z-index: 9999;
        animation: slideIn 0.3s ease;
    `;
    document.body.appendChild(toast);
    setTimeout(() => toast.remove(), 3000);
}

// ===== CONTACT FORM MODAL =====
function openContactModal(e) {
    if (e) e.preventDefault();
    const modal = document.getElementById('contactModal');
    if (!modal) return;
    modal.removeAttribute('hidden');
    document.body.style.overflow = 'hidden';
    // Update placeholders for current language
    modal.querySelectorAll('[data-placeholder-en]').forEach(el => {
        const ph = el.getAttribute(`data-placeholder-${currentLang}`);
        if (ph) el.placeholder = ph;
    });
    // Focus first input
    setTimeout(() => {
        const first = modal.querySelector('input:not([type=hidden]):not([type=checkbox])');
        if (first) first.focus();
    }, 100);
}

function closeContactModal() {
    const modal = document.getElementById('contactModal');
    if (!modal) return;
    modal.setAttribute('hidden', '');
    document.body.style.overflow = '';
    // Reset form state
    const form = document.getElementById('contactForm');
    if (form) {
        form.reset();
        form.querySelectorAll('.has-error').forEach(el => el.classList.remove('has-error'));
        form.querySelectorAll('.invalid').forEach(el => el.classList.remove('invalid'));
    }
    const success = document.getElementById('formSuccess');
    const error = document.getElementById('formError');
    if (success) success.setAttribute('hidden', '');
    if (error) error.setAttribute('hidden', '');
    const btn = document.getElementById('submitBtn');
    if (btn) { btn.disabled = false; btn.innerHTML = '<i class="fas fa-paper-plane"></i> <span>Send Message</span>'; }
}

function initContactForm() {
    const modal = document.getElementById('contactModal');
    const form  = document.getElementById('contactForm');
    if (!modal || !form) return;

    // Close on overlay click
    modal.addEventListener('click', (e) => {
        if (e.target === modal) closeContactModal();
    });

    // Close on Escape key
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && !modal.hasAttribute('hidden')) closeContactModal();
    });

    // Form submit
    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        // Validate
        let valid = true;
        const nameField  = document.getElementById('contactName');
        const emailField = document.getElementById('contactEmail');
        const msgField   = document.getElementById('contactMessage');

        [nameField, emailField, msgField].forEach(field => {
            const group = field.closest('.form-group');
            if (!field.value.trim() || (field.type === 'email' && !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(field.value))) {
                group.classList.add('has-error');
                field.classList.add('invalid');
                valid = false;
            } else {
                group.classList.remove('has-error');
                field.classList.remove('invalid');
            }
        });

        if (!valid) return;

        // Show loading state
        const btn = document.getElementById('submitBtn');
        const origHTML = btn.innerHTML;
        btn.disabled = true;
        btn.innerHTML = '<span class="btn-spinner"></span> Sending…';

        const success = document.getElementById('formSuccess');
        const errorEl = document.getElementById('formError');
        success.setAttribute('hidden', '');
        errorEl.setAttribute('hidden', '');

        // Submit to Web3Forms
        try {
            const data = new FormData(form);
            const res  = await fetch('https://api.web3forms.com/submit', {
                method: 'POST',
                body: data
            });
            const json = await res.json();

            if (json.success) {
                success.removeAttribute('hidden');
                form.reset();
                btn.disabled = false;
                btn.innerHTML = origHTML;
                // Auto-close after 3s
                setTimeout(() => closeContactModal(), 3000);
            } else {
                throw new Error(json.message || 'Submission failed');
            }
        } catch (err) {
            console.error('Contact form error:', err);
            errorEl.removeAttribute('hidden');
            btn.disabled = false;
            btn.innerHTML = origHTML;
        }
    });
}

// ===== PRINT HANDLER =====
window.addEventListener('beforeprint', () => {
    // Make all sections visible for printing
    document.querySelectorAll('.fade-in').forEach(el => {
        el.classList.add('visible');
    });
});

// ===== KEYBOARD SHORTCUTS =====
document.addEventListener('keydown', (e) => {
    if (e.altKey) {
        if (e.key === '1' || e.key === 'e') { e.preventDefault(); setLang('en'); }
        if (e.key === '2' || e.key === 'f') { e.preventDefault(); setLang('fi'); }
        if (e.key === 't') { e.preventDefault(); toggleTheme(); }
    }
});

// ===== INIT =====
document.addEventListener('DOMContentLoaded', () => {
    // Theme
    initTheme();

    // Theme toggle button
    const themeToggle = document.getElementById('themeToggle');
    if (themeToggle) themeToggle.addEventListener('click', toggleTheme);

    // Language: check URL hash or localStorage
    const hash = window.location.hash.substring(1);
    const savedLang = localStorage.getItem('portfolio-lang');
    const lang = (hash === 'en' || hash === 'fi') ? hash : (savedLang || 'en');
    setLang(lang);

    // Typed text
    typedInstance = new TypedText('typed-text', translations[lang].typedPhrases);

    // Navbar
    initNavbar();

    // Scroll animations
    initScrollAnimations();

    // Smooth scroll
    initSmoothScroll();

    // Handle browser back/forward
    window.addEventListener('popstate', () => {
        const h = window.location.hash.substring(1);
        if (h === 'en' || h === 'fi') setLang(h);
    });

    // Contact form modal
    initContactForm();

    console.log('Portfolio loaded — Renata Baldissara-Kunnela');
});
