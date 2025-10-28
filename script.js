// Shared JavaScript across all pages
document.addEventListener('DOMContentLoaded', function() {
    initRouter();

    // Smooth scrolling for anchor links
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

    // Navbar scroll effect
    const navbar = document.querySelector('custom-navbar');
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });

    // Intersection Observer for fade-in animations
    const fadeElements = document.querySelectorAll('.fade-in-element');
    if (fadeElements.length > 0) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('fade-in');
                }
            });
        }, { threshold: 0.1 });

        fadeElements.forEach(element => {
            observer.observe(element);
        });
    }
});

// Utility functions
function showToast(message, type = 'info') {
    // Create toast notification
    const toast = document.createElement('div');
    toast.className = `fixed bottom-4 right-4 px-6 py-4 rounded-lg shadow-lg z-50 transform transition-transform duration-300 ${
        type === 'success' ? 'bg-green-500' : 
        type === 'error' ? 'bg-red-500' : 
        type === 'warning' ? 'bg-yellow-500' : 'bg-blue-500'
    }`;
    toast.textContent = message;
    
    document.body.appendChild(toast);
    
    // Auto remove after 3 seconds
    setTimeout(() => {
        toast.classList.add('translate-x-full');
        setTimeout(() => {
            document.body.removeChild(toast);
        }, 300);
    }, 3000);
}

// Format large numbers
function formatNumber(num) {
    if (num >= 1000000) {
        return (num / 1000000).toFixed(1) + 'M';
    }
    if (num >= 1000) {
        return (num / 1000).toFixed(1) + 'K';
    }
    return num.toString();
}

// Debounce function for search inputs
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

// Optimized Router System
function initRouter() {
    // Route mapping
    const routes = {
        '/': 'index.html',
        '/mirrors.html': 'mirrors.html',
        '/tools.html': 'tools.html',
        '/community.html': 'community.html'
    };

    // Page content cache
    const pageCache = new Map();

    // Main content area - find the main content wrapper
    let mainContent = document.querySelector('main');
    if (!mainContent) {
        // Fallback: create a wrapper for the body content excluding navbar/footer
        const children = Array.from(document.body.children);
        mainContent = document.createElement('main');

        // Find content between navbar and footer
        let start = false;
        for (const child of children) {
            if (child.tagName === 'CUSTOM-NAVBAR') {
                start = true;
                continue;
            }
            if (child.tagName === 'CUSTOM-FOOTER') {
                break;
            }
            if (start && child !== mainContent) {
                if (!mainContent.contains(child)) {
                    mainContent.appendChild(child.cloneNode(true));
                    child.remove();
                }
            }
        }
        document.body.appendChild(mainContent);
    }

    // Loading overlay
    const loadingOverlay = document.createElement('div');
    loadingOverlay.className = 'fixed inset-0 bg-black/50 backdrop-blur-sm z-40 flex items-center justify-center opacity-0 pointer-events-none transition-opacity duration-300';
    loadingOverlay.innerHTML = `
        <div class="bg-gray-800 rounded-lg p-6 flex items-center space-x-3">
            <div class="animate-spin rounded-full h-6 w-6 border-2 border-blue-500 border-t-transparent"></div>
            <span class="text-white">載入中...</span>
        </div>
    `;
    document.body.appendChild(loadingOverlay);

    // Navigate function
    async function navigateTo(path, pushState = true) {
        // Show loading
        loadingOverlay.style.opacity = '1';
        loadingOverlay.style.pointerEvents = 'auto';

        try {
            const htmlFile = routes[path] || routes['/'];

            // Check cache first
            let content = pageCache.get(htmlFile);
            if (!content) {
                const response = await fetch(htmlFile);
                const html = await response.text();

            // Extract body content (everything between <body> and </body>)
            const bodyMatch = html.match(/<body[^>]*>(.*?)<\/body>/s);
            if (bodyMatch) {
                content = bodyMatch[1];
            } else {
                // Fallback: try to extract main content
                content = html;
            }

            // Clean content (remove navbar, footer, scripts that are already loaded)
            content = content.replace(/<custom-navbar[^>]*>[\s\S]*?<\/custom-navbar>/gi, '');
            content = content.replace(/<custom-footer[^>]*>[\s\S]*?<\/custom-footer>/gi, '');
            content = content.replace(/<script[^>]*src=["'](?:components\/(?:navbar|footer)\.js|script\.js)["'][^>]*><\/script>/gi, '');
            // Also remove inline scripts that might interfere
            content = content.replace(/<script[^>]*feather\.replace\(\)[^>]*<\/script>/gi, '');

                // Cache the content
                pageCache.set(htmlFile, content);
            }

            // Update the page
            const newContent = document.createElement('div');
            newContent.innerHTML = content;

            // Add fade classes for transition
            mainContent.style.opacity = '0';
            mainContent.style.transform = 'translateY(-20px)';

            setTimeout(() => {
                // Replace content
                mainContent.innerHTML = newContent.innerHTML;

                // Update page title
                const titleMatch = content.match(/<title[^>]*>(.*?)<\/title>/i);
                if (titleMatch && titleMatch[1]) {
                    document.title = titleMatch[1];
                }

                // Re-initialize Feather icons
                if (typeof feather !== 'undefined') {
                    feather.replace();
                }

                // Re-attach event listeners and initialize components
                initPageScripts();

                // Fade in
                mainContent.style.opacity = '1';
                mainContent.style.transform = 'translateY(0)';

                // Update URL
                if (pushState) {
                    history.pushState({ path }, '', path);
                }
            }, 150);

        } catch (error) {
            console.error('Navigation error:', error);
            showToast('頁面載入失敗', 'error');
        } finally {
            // Hide loading
            setTimeout(() => {
                loadingOverlay.style.opacity = '0';
                loadingOverlay.style.pointerEvents = 'none';
            }, 200);
        }
    }

    // Initialize page scripts (for dynamic content)
    function initPageScripts() {
        // Re-initialize Vanta.js if on homepage
        if (location.pathname === '/' && document.getElementById('globe-background')) {
            if (typeof VANTA !== 'undefined') {
                VANTA.GLOBE({
                    el: "#globe-background",
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
            }
        }

        // Re-attach fade-in animations
        const fadeElements = document.querySelectorAll('.fade-in-element');
        if (fadeElements.length > 0) {
            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        entry.target.classList.add('fade-in');
                    }
                });
            }, { threshold: 0.1 });

            fadeElements.forEach(element => {
                observer.observe(element);
            });
        }
    }

    // Intercept navigation clicks
    document.addEventListener('click', function(e) {
        const link = e.target.closest('a[href]');
        if (!link) return;

        const href = link.getAttribute('href');

        // Only handle internal routes
        if (routes[href]) {
            e.preventDefault();
            navigateTo(href);
        } else if (href.startsWith('#')) {
            // Handle anchor links
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

    // Handle browser back/forward buttons
    window.addEventListener('popstate', function(e) {
        if (e.state && e.state.path) {
            navigateTo(e.state.path, false);
        }
    });

    // Preload routes on idle
    if ('requestIdleCallback' in window) {
        requestIdleCallback(() => {
            Object.values(routes).forEach(file => {
                if (!pageCache.has(file) && file !== routes[location.pathname]) {
                    fetch(file).then(response => response.text()).then(html => {
                        // Extract and cache content (same as in navigateTo)
                        const bodyMatch = html.match(/<body[^>]*>(.*?)<\/body>/s);
                        if (bodyMatch) {
                            let content = bodyMatch[1];
                            content = content.replace(/<custom-navbar[^>]*>[\s\S]*?<\/custom-navbar>/gi, '');
                            content = content.replace(/<custom-footer[^>]*>[\s\S]*?<\/custom-footer>/gi, '');
                            content = content.replace(/<script[^>]*src=["'](?:components\/(?:navbar|footer)\.js|script\.js)["'][^>]*><\/script>/gi, '');
                            pageCache.set(file, content);
                        }
                    }).catch(() => {}); // Ignore preload failures
                }
            });
        });
    }

    // Add transition styles
    if (!document.getElementById('router-styles')) {
        const style = document.createElement('style');
        style.id = 'router-styles';
        style.textContent = `
            body > :not(custom-navbar):not(custom-footer) {
                transition: opacity 0.3s ease, transform 0.3s ease;
                opacity: 1;
                transform: translateY(0);
            }
            .fade-in-element {
                opacity: 0;
                transform: translateY(20px);
                transition: opacity 0.6s ease, transform 0.6s ease;
            }
            .fade-in-element.fade-in {
                opacity: 1;
                transform: translateY(0);
            }
        `;
        document.head.appendChild(style);
    }
}
