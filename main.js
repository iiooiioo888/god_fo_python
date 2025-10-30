// Main application logic extracted from index.html inline scripts

class PageOptimizer {
    constructor() {
        this.init();
    }

    init() {
        this.setupLoadingStates();
        this.setupErrorHandling();
        this.setupLazyLoading();
        this.setupAccessibility();
        this.setupPerformanceMonitoring();
        this.initVantaGlobe();
    }

    setupLoadingStates() {
        // Create loading overlay
        const loadingOverlay = document.createElement('div');
        loadingOverlay.id = 'page-loading';
        loadingOverlay.className = 'fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center pointer-events-none opacity-0 transition-opacity duration-300';
        loadingOverlay.innerHTML = `
            <div class="bg-gray-800 rounded-xl p-8 flex items-center gap-4 shadow-2xl">
                <div class="animate-spin rounded-full h-8 w-8 border-2 border-blue-500 border-t-transparent"></div>
                <div class="text-white font-medium">加载中...</div>
            </div>
        `;
        document.body.appendChild(loadingOverlay);
    }

    setupErrorHandling() {
        // Global error handler
        window.addEventListener('error', (e) => {
            console.error('JavaScript error:', e.error);
            this.showErrorToast('页面出现错误，请刷新重试');
        });

        // Promise rejection handler
        window.addEventListener('unhandledrejection', (e) => {
            console.error('Promise rejection:', e.reason);
            this.showErrorToast('网络请求失败');
        });
    }

    setupLazyLoading() {
        // Intersection Observer for lazy loading
        const observerOptions = {
            root: null,
            rootMargin: '50px 0px',
            threshold: 0.1
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const element = entry.target;

                    // Add fade-in animation
                    element.classList.add('animate-fade-in');

                    // Lazy load images if any
                    const img = element.querySelector('img[data-src]');
                    if (img) {
                        img.src = img.dataset.src;
                        img.removeAttribute('data-src');
                    }

                    observer.unobserve(element);
                }
            });
        }, observerOptions);

        // Observe feature cards
        document.querySelectorAll('#features .bg-gray-800\\/50').forEach(card => {
            observer.observe(card);
        });
    }

    setupAccessibility() {
        // Skip to content link
        const skipLink = document.createElement('a');
        skipLink.href = '#main-content';
        skipLink.className = 'sr-only focus:not-sr-only focus:absolute focus:top-4 focus:left-4 bg-blue-600 text-white px-4 py-2 rounded z-50';
        skipLink.textContent = '跳到主要内容';
        document.body.insertBefore(skipLink, document.body.firstChild);

        // Add main content landmark
        const mainContent = document.querySelector('main');
        if (mainContent) {
            mainContent.id = 'main-content';
            mainContent.setAttribute('role', 'main');
        }

        // Improve heading hierarchy
        const headings = document.querySelectorAll('h1, h2, h3, h4, h5, h6');
        headings.forEach((heading, index) => {
            if (!heading.id) {
                heading.id = `heading-${index}`;
            }
        });

        // Add ARIA labels
        const buttons = document.querySelectorAll('button:not([aria-label]):not([aria-labelledby])');
        buttons.forEach(button => {
            const text = button.textContent.trim();
            if (text) {
                button.setAttribute('aria-label', text);
            }
        });
    }

    setupPerformanceMonitoring() {
        // Performance observer (with fallback)
        if ('PerformanceObserver' in window) {
            const observer = new PerformanceObserver((list) => {
                const entries = list.getEntries();
                entries.forEach((entry) => {
                    if (entry.duration > 100) {
                        console.warn('Long task detected:', entry);
                    }
                });
            });
            observer.observe({ entryTypes: ['longtask'] });
        }
    }

    initVantaGlobe() {
        // Lazy load Vanta.js
        const loadVanta = () => {
            if (window.VANTA) {
                this.createVantaGlobe();
            } else {
                // Load Three.js first
                if (!window.THREE) {
                    this.loadScript('https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js')
                        .then(() => this.loadScript('https://cdn.jsdelivr.net/npm/vanta@latest/dist/vanta.globe.min.js'))
                        .then(() => this.createVantaGlobe())
                        .catch((error) => {
                            console.warn('Failed to load Vanta.js:', error);
                            this.createFallbackHero();
                        });
                } else {
                    this.loadScript('https://cdn.jsdelivr.net/npm/vanta@latest/dist/vanta.globe.min.js')
                        .then(() => this.createVantaGlobe())
                        .catch((error) => {
                            console.warn('Failed to load Vanta.js:', error);
                            this.createFallbackHero();
                        });
                }
            }
        };

        loadVanta();
    }

    loadScript(src) {
        return new Promise((resolve, reject) => {
            const script = document.createElement('script');
            script.src = src;
            script.onload = resolve;
            script.onerror = reject;
            document.head.appendChild(script);
        });
    }

    createVantaGlobe() {
        const globeElement = document.getElementById('globe-background');
        if (!globeElement) return;

        try {
            window.vantaEffect = window.VANTA.GLOBE({
                el: globeElement,
                mouseControls: true,
                touchControls: true,
                gyroControls: false,
                minHeight: 200.00,
                minWidth: 200.00,
                scale: 1.00,
                scaleMobile: 1.00,
                color: 0x3b82f6,
                color2: 0x8b5cf6,
                backgroundColor: 0x000000
            });

            // Setup cleanup on page unload
            window.addEventListener('beforeunload', () => {
                if (window.vantaEffect) {
                    window.vantaEffect.destroy();
                }
            });

        } catch (error) {
            console.warn('Vanta.js initialization failed:', error);
            this.createFallbackHero();
        }
    }

    createFallbackHero() {
        const hero = document.getElementById('hero');
        if (!hero) return;

        // Create animated gradient background
        hero.style.background = `
            linear-gradient(45deg,
                #1a1a2e 0%,
                #16213e 50%,
                #0f172a 100%
            )
        `;
        hero.style.backgroundSize = '400% 400%';
        hero.style.animation = 'gradientShift 15s ease infinite';

        // Add fallback animation
        const style = document.createElement('style');
        style.textContent = `
            @keyframes gradientShift {
                0% { background-position: 0% 50%; }
                50% { background-position: 100% 50%; }
                100% { background-position: 0% 50%; }
            }
        `;
        document.head.appendChild(style);
    }

    showErrorToast(message) {
        // Use existing toast system if available, otherwise create simple alert
        if (window.showToast) {
            window.showToast(message, 'error');
        } else {
            alert(message);
        }
    }
}

// Initialize page optimizer
document.addEventListener('DOMContentLoaded', () => {
    new PageOptimizer();
});

// Smooth scroll for hero buttons
document.addEventListener('click', function(e) {
    const link = e.target.closest('a[href^="#"]');
    if (link) {
        e.preventDefault();
        const target = document.querySelector(link.getAttribute('href'));
        if (target) {
            const offset = 80; // Account for fixed navbar
            const top = target.offsetTop - offset;
            window.scrollTo({
                top: top,
                behavior: 'smooth'
            });
        }
    }
});

// Add scroll-triggered animations
const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, {
    threshold: 0.1,
    rootMargin: '-50px 0px'
});

// Set initial styles for animated elements
document.querySelectorAll('section > .container').forEach(section => {
    section.style.opacity = '0';
    section.style.transform = 'translateY(20px)';
    section.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    observer.observe(section);
});

// Add stats counter animation
function animateCounters() {
    const counters = document.querySelectorAll('.text-4xl.font-bold:not(.animated)');
    counters.forEach(counter => {
        const target = parseInt(counter.textContent.replace(/[^\d]/g, ''));
        if (isNaN(target)) return;

        counter.classList.add('animated');
        let current = 0;
        const increment = target / 50; // Animate over 50 frames
        const timer = setInterval(() => {
            current += increment;
            if (current >= target) {
                counter.textContent = target.toLocaleString() + (counter.textContent.match(/\D+$/) || [''])[0];
                clearInterval(timer);
            } else {
                counter.textContent = Math.floor(current).toLocaleString() + (counter.textContent.match(/\D+$/) || [''])[0];
            }
        }, 30);
    });
}

// Trigger counter animation when stats section is visible
const statsSection = document.querySelector('.py-20.bg-gray-900\\/50');
if (statsSection) {
    const statsObserver = new IntersectionObserver((entries) => {
        if (entries[0].isIntersecting) {
            animateCounters();
            statsObserver.unobserve(statsSection);
        }
    });
    statsObserver.observe(statsSection);
}

// Add keyboard navigation support
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        // Close any open modals (if any)
        const modals = document.querySelectorAll('[class*="modal"]');
        modals.forEach(modal => {
            modal.classList.add('hidden');
        });
    }

    if (e.key === 'Home') {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }

    if (e.key === 'End') {
        window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' });
    }
});
