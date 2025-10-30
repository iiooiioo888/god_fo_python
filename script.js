// Shared JavaScript across all pages
document.addEventListener('DOMContentLoaded', function() {
    initRouter();
    initAuthSystem();

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

// Authentication System
function initAuthSystem() {
    // Check if user is logged in (secure session-based approach)
    const sessionToken = localStorage.getItem('sessionToken');
    let currentUser = null;

    if (sessionToken) {
        try {
            // Check if session is still valid (in real app, validate with server)
            const sessionData = JSON.parse(localStorage.getItem('sessionData') || '{}');
            if (sessionData.expiry && new Date() < new Date(sessionData.expiry)) {
                currentUser = sessionData.user;
            } else {
                // Session expired, clear data
                localStorage.removeItem('sessionToken');
                localStorage.removeItem('sessionData');
            }
        } catch (error) {
            console.warn('Session data corrupted, clearing:', error);
            localStorage.removeItem('sessionToken');
            localStorage.removeItem('sessionData');
        }
    }

    updateNavAuthState(currentUser);

    // Create auth modal
    createAuthModal();
}

function createAuthModal() {
    const modalHTML = `
        <div id="auth-modal" class="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 hidden">
            <div class="min-h-screen flex items-center justify-center px-4">
                <div class="bg-gray-800 rounded-xl border border-gray-700 w-full max-w-sm sm:max-w-md">
                    <div class="flex justify-between items-center p-6 border-b border-gray-700">
                        <h3 class="text-xl font-semibold" id="auth-title">登录镜界</h3>
                        <button onclick="closeAuthModal()" class="text-gray-400 hover:text-white">
                            <i data-feather="x" class="w-5 h-5"></i>
                        </button>
                    </div>
                    <div class="p-6">
                        <!-- Tabs -->
                        <div class="flex mb-6">
                            <button onclick="switchAuthTab('login')" id="login-tab" class="flex-1 py-2 px-4 text-center border-b-2 border-blue-500 text-blue-400 font-medium">登录</button>
                            <button onclick="switchAuthTab('register')" id="register-tab" class="flex-1 py-2 px-4 text-center border-b-2 border-transparent text-gray-400 hover:text-white transition-colors">注册</button>
                        </div>

                        <!-- Login Form -->
                        <div id="login-form" class="space-y-4">
                            <div>
                                <label class="block text-sm font-medium text-gray-300 mb-2">邮箱或用户名</label>
                                <input type="text" id="login-email" class="w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-white" placeholder="请输入邮箱或用户名">
                            </div>
                            <div>
                                <label class="block text-sm font-medium text-gray-300 mb-2">密码</label>
                                <input type="password" id="login-password" class="w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-white" placeholder="请输入密码">
                            </div>
                            <div class="flex items-center justify-between text-sm">
                                <label class="flex items-center">
                                    <input type="checkbox" class="w-4 h-4 bg-gray-700 border border-gray-600 rounded focus:ring-2 focus:ring-blue-500">
                                    <span class="ml-2 text-gray-300">记住我</span>
                                </label>
                                <a href="#" class="text-blue-400 hover:text-blue-300">忘记密码？</a>
                            </div>
                            <button onclick="login()" class="w-full bg-blue-600 hover:bg-blue-700 px-4 py-3 rounded-lg font-medium transition-colors">
                                登录
                            </button>
                        </div>

                        <!-- Register Form -->
                        <div id="register-form" class="space-y-4 hidden">
                            <div>
                                <label class="block text-sm font-medium text-gray-300 mb-2">用户名</label>
                                <input type="text" id="register-username" class="w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-white" placeholder="请输入用户名">
                            </div>
                            <div>
                                <label class="block text-sm font-medium text-gray-300 mb-2">邮箱</label>
                                <input type="email" id="register-email" class="w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-white" placeholder="请输入邮箱">
                            </div>
                            <div>
                                <label class="block text-sm font-medium text-gray-300 mb-2">密码</label>
                                <input type="password" id="register-password" class="w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-white" placeholder="请输入密码（至少6位）">
                            </div>
                            <div>
                                <label class="block text-sm font-medium text-gray-300 mb-2">确认密码</label>
                                <input type="password" id="register-confirm-password" class="w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-white" placeholder="请再次输入密码">
                            </div>
                            <div class="flex items-center">
                                <input type="checkbox" id="agree-terms" class="w-4 h-4 bg-gray-700 border border-gray-600 rounded focus:ring-2 focus:ring-blue-500">
                                <label for="agree-terms" class="ml-2 text-sm text-gray-300">
                                    我同意 <a href="#" class="text-blue-400 hover:text-blue-300">用户协议</a> 和 <a href="#" class="text-blue-400 hover:text-blue-300">隐私政策</a>
                                </label>
                            </div>
                            <button onclick="register()" class="w-full bg-green-600 hover:bg-green-700 px-4 py-3 rounded-lg font-medium transition-colors">
                                注册账户
                            </button>
                        </div>

                        <!-- Social Login -->
                        <div class="mt-6">
                            <div class="relative">
                                <div class="absolute inset-0 flex items-center">
                                    <div class="w-full border-t border-gray-600"></div>
                                </div>
                                <div class="relative flex justify-center text-sm">
                                    <span class="px-2 bg-gray-800 text-gray-400">或</span>
                                </div>
                            </div>

                            <div class="mt-6 grid grid-cols-2 gap-3">
                                <button onclick="socialLogin('github')" class="flex justify-center items-center px-4 py-3 bg-gray-700 hover:bg-gray-600 rounded-lg transition-colors">
                                    <i data-feather="github" class="w-4 h-4 mr-2"></i>
                                    GitHub
                                </button>
                                <button onclick="socialLogin('google')" class="flex justify-center items-center px-4 py-3 bg-gray-700 hover:bg-gray-600 rounded-lg transition-colors">
                                    <svg class="w-4 h-4 mr-2" viewBox="0 0 24 24">
                                        <path fill="currentColor" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
                                        <path fill="currentColor" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
                                        <path fill="currentColor" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
                                        <path fill="currentColor" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
                                    </svg>
                                    Google
                                </button>
                            </div>
                        </div>

                        <!-- Error Message -->
                        <div id="auth-error" class="mt-4 p-3 bg-red-900/30 border border-red-500/50 rounded-lg hidden">
                            <div class="flex items-center">
                                <i data-feather="alert-circle" class="text-red-400 w-4 h-4 mr-2"></i>
                                <span class="text-red-400 text-sm" id="auth-error-text"></span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;

    document.body.insertAdjacentHTML('beforeend', modalHTML);
}

// Functions for auth system
function openAuthModal(mode) {
    document.getElementById('auth-modal').classList.remove('hidden');
    document.getElementById('auth-error').classList.add('hidden');
    switchAuthTab(mode);
    // Prevent body scroll
    document.body.style.overflow = 'hidden';
}

function closeAuthModal() {
    document.getElementById('auth-modal').classList.add('hidden');
    document.body.style.overflow = 'auto';
    // Reset forms
    document.getElementById('login-email').value = '';
    document.getElementById('login-password').value = '';
    document.getElementById('register-username').value = '';
    document.getElementById('register-email').value = '';
    document.getElementById('register-password').value = '';
    document.getElementById('register-confirm-password').value = '';
    document.getElementById('agree-terms').checked = false;
}

function switchAuthTab(mode) {
    const loginTab = document.getElementById('login-tab');
    const registerTab = document.getElementById('register-tab');
    const loginForm = document.getElementById('login-form');
    const registerForm = document.getElementById('register-form');
    const authTitle = document.getElementById('auth-title');

    if (mode === 'login') {
        loginTab.classList.remove('border-transparent', 'text-gray-400');
        loginTab.classList.add('border-blue-500', 'text-blue-400');
        registerTab.classList.remove('border-blue-500', 'text-blue-400');
        registerTab.classList.add('border-transparent', 'text-gray-400');
        loginForm.classList.remove('hidden');
        registerForm.classList.add('hidden');
        authTitle.textContent = '登录镜界';
    } else {
        registerTab.classList.remove('border-transparent', 'text-gray-400');
        registerTab.classList.add('border-blue-500', 'text-blue-400');
        loginTab.classList.remove('border-blue-500', 'text-blue-400');
        loginTab.classList.add('border-transparent', 'text-gray-400');
        registerForm.classList.remove('hidden');
        loginForm.classList.add('hidden');
        authTitle.textContent = '注册账户';
    }
}

function login() {
    const email = document.getElementById('login-email').value;
    const password = document.getElementById('login-password').value;

    if (!email || !password) {
        showAuthError('请填写所有必填字段');
        return;
    }

    // Simple login simulation (in real app, this would be hashed password validation)
    const users = JSON.parse(localStorage.getItem('registeredUsers')) || [];

    const user = users.find(u => (u.email === email || u.username === email) && u.password === password);

    if (user) {
        // Login successful - Create secure session
        const sessionToken = generateSessionToken();
        const sessionExpiry = new Date(Date.now() + 24 * 60 * 60 * 1000); // 24 hours
        const sessionData = {
            user: {
                username: user.username,
                email: user.email,
                avatar: user.avatar
            },
            expiry: sessionExpiry.toISOString()
        };

        localStorage.setItem('sessionToken', sessionToken);
        localStorage.setItem('sessionData', JSON.stringify(sessionData));
        // Remove old insecure currentUser data
        localStorage.removeItem('currentUser');

        updateNavAuthState(sessionData.user);
        closeAuthModal();
        showToast('登录成功！', 'success');
    } else {
        showAuthError('用户名或密码错误');
    }
}

// Generate a cryptographically secure session token
function generateSessionToken() {
    const array = new Uint8Array(32);
    crypto.getRandomValues(array);
    return Array.from(array, byte => byte.toString(16).padStart(2, '0')).join('');
}

function register() {
    const username = document.getElementById('register-username').value.trim();
    const email = document.getElementById('register-email').value.trim();
    const password = document.getElementById('register-password').value;
    const confirmPassword = document.getElementById('register-confirm-password').value;
    const agreeTerms = document.getElementById('agree-terms').checked;

    // Enhanced validation
    if (!username || !email || !password) {
        showAuthError('请填写所有必填字段');
        return;
    }

    if (username.length < 3 || username.length > 30) {
        showAuthError('用户名长度应在3-30个字符之间');
        return;
    }

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
        showAuthError('请输入有效的邮箱地址');
        return;
    }

    if (password.length < 6) {
        showAuthError('密码至少需要6个字符');
        return;
    }

    if (password !== confirmPassword) {
        showAuthError('两次输入的密码不匹配');
        return;
    }

    if (!agreeTerms) {
        showAuthError('请同意用户协议和隐私政策');
        return;
    }

    // Check if user already exists
    const users = JSON.parse(localStorage.getItem('registeredUsers')) || [];
    if (users.find(u => u.email === email)) {
        showAuthError('此邮箱已被注册');
        return;
    }

    if (users.find(u => u.username === username)) {
        showAuthError('此用户名已被使用');
        return;
    }

    // Register user
    const newUser = {
        username: username,
        email: email,
        password: password, // Note: In production, password should be hashed with bcrypt or similar
        avatar: `data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='%233b82f6'><circle cx='12' cy='8' r='4'/><path d='M12 14c-6.1 0-8 4-8 4v2h16v-2s-1.9-4-8-4z'/></svg>`,
        registeredAt: new Date().toISOString()
    };

    users.push(newUser);
    localStorage.setItem('registeredUsers', JSON.stringify(users));

    // Auto login with secure session
    const sessionToken = generateSessionToken();
    const sessionExpiry = new Date(Date.now() + 7 * 24 * 60 * 60 * 1000); // 7 days for new users
    const sessionData = {
        user: {
            username: newUser.username,
            email: newUser.email,
            avatar: newUser.avatar
        },
        expiry: sessionExpiry.toISOString()
    };

    localStorage.setItem('sessionToken', sessionToken);
    localStorage.setItem('sessionData', JSON.stringify(sessionData));
    // Remove any old insecure currentUser data
    localStorage.removeItem('currentUser');

    updateNavAuthState(sessionData.user);
    closeAuthModal();
    showToast('注册成功，欢迎加入镜界！', 'success');
}

function socialLogin(provider) {
    showToast(`${provider} 登录功能正在开发中...`, 'info');
}

function logout() {
    // Secure session cleanup
    localStorage.removeItem('sessionToken');
    localStorage.removeItem('sessionData');
    // Also remove any old insecure currentUser data
    localStorage.removeItem('currentUser');

    updateNavAuthState(null);
    toggleUserMenu(); // Close dropdown
    showToast('已退出登录', 'info');
}

function updateNavAuthState(user) {
    const authButtons = document.getElementById('auth-buttons');
    const userMenu = document.getElementById('user-menu');

    if (user) {
        // Show user menu
        authButtons.style.display = 'none';
        userMenu.style.display = 'block';
        // Update avatar if needed
    } else {
        // Show auth buttons
        authButtons.style.display = 'flex';
        userMenu.style.display = 'none';
    }
}

function toggleUserMenu() {
    const dropdown = document.getElementById('user-dropdown');
    dropdown.classList.toggle('show');
}

function showAuthError(message) {
    const errorDiv = document.getElementById('auth-error');
    const errorText = document.getElementById('auth-error-text');
    errorText.textContent = message;
    errorDiv.classList.remove('hidden');
}

// Close auth modal when clicking outside
document.addEventListener('click', function(e) {
    if (e.target.id === 'auth-modal') {
        closeAuthModal();
    }
});

// Close user menu when clicking outside
document.addEventListener('click', function(e) {
    const userMenu = document.getElementById('user-menu');
    const userDropdown = document.getElementById('user-dropdown');
    const userAvatar = document.querySelector('.user-avatar');

    if (userMenu && !userMenu.contains(e.target)) {
        userDropdown.classList.remove('show');
    }
});

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

// Optimized Resource Loading
class ResourceOptimizer {
    constructor() {
        this.loadedScripts = new Set();
        this.loadedStyles = new Set();
        this.preloadedUrls = new Set();
    }

    loadScript(url, options = {}) {
        return new Promise((resolve, reject) => {
            if (this.loadedScripts.has(url)) {
                resolve();
                return;
            }

            const script = document.createElement('script');
            script.src = url;
            script.onload = () => {
                this.loadedScripts.add(url);
                resolve();
            };
            script.onerror = reject;

            // Add performance optimizations
            if (options.async !== false) script.async = true;
            if (options.defer) script.defer = true;
            if (options.integrity) script.integrity = options.integrity;
            if (options.crossOrigin) script.crossOrigin = options.crossOrigin;

            document.head.appendChild(script);
        });
    }

    loadStyle(href, options = {}) {
        return new Promise((resolve, reject) => {
            if (this.loadedStyles.has(href)) {
                resolve();
                return;
            }

            const link = document.createElement('link');
            link.rel = 'stylesheet';
            link.href = href;
            link.onload = () => {
                this.loadedStyles.add(href);
                resolve();
            };
            link.onerror = reject;

            // Add performance optimizations
            if (options.integrity) link.integrity = options.integrity;
            if (options.crossOrigin) link.crossOrigin = options.crossOrigin;

            document.head.appendChild(link);
        });
    }

    preload(url, as, options = {}) {
        if (this.preloadedUrls.has(url)) return;

        const link = document.createElement('link');
        link.rel = 'preload';
        link.href = url;
        link.as = as;

        if (options.crossOrigin) link.crossOrigin = options.crossOrigin;

        document.head.appendChild(link);
        this.preloadedUrls.add(url);
    }

    prefetch(url) {
        if (this.preloadedUrls.has(url)) return;

        const link = document.createElement('link');
        link.rel = 'prefetch';
        link.href = url;

        document.head.appendChild(link);
        this.preloadedUrls.add(url);
    }
}

// Global resource optimizer instance
const resourceOptimizer = new ResourceOptimizer();

// Optimized Router System
function initRouter() {
    // Route mapping
    const routes = {
        '/': 'index.html',
        '/mirrors.html': 'mirrors.html',
        '/tools.html': 'tools.html',
        '/community.html': 'community.html',
        '/profile.html': 'profile.html',
        '/workflow.html': 'workflow.html',
        '/notifications': 'notifications.html'
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

    // Preload routes on idle (with fallback for older browsers)
    const preloadRoutes = () => {
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
    };

    // Use requestIdleCallback if available, otherwise fallback to setTimeout
    if ('requestIdleCallback' in window) {
        requestIdleCallback(preloadRoutes);
    } else {
        // Fallback for browsers without requestIdleCallback
        setTimeout(preloadRoutes, 1000);
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
