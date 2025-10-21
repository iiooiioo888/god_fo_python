// WebCrawler Commander - 主腳本文件

// DOM 元素引用
const mobileMenuButton = document.getElementById('mobile-menu-button');
const navMenu = document.getElementById('nav-menu');
const userAvatar = document.getElementById('user-avatar');
const userDropdown = document.getElementById('user-dropdown');

// 初始化 Feather Icons
document.addEventListener('DOMContentLoaded', function() {
    if (typeof feather !== 'undefined') {
        feather.replace();
    }
});

// 資源監控數據模擬
function updateResourceStats() {
    // CPU 使用率
    const cpuElements = document.querySelectorAll('[style*="width: 64%"]');
    cpuElements.forEach(el => {
        const cpuPercent = Math.min(100, Math.max(0, 60 + Math.random() * 20 - 10));
        el.style.width = `${cpuPercent}%`;

        const label = el.closest('.border').querySelector('span.text-sm.font-medium');
        if (label) {
            label.textContent = `${cpuPercent.toFixed(0)}%`;
            // 更新 CPU 統計卡片的顯示
            const cpuCardValue = document.querySelector('h3[data-cpu-value]');
            if (cpuCardValue) cpuCardValue.textContent = `${Math.round(cpuPercent)}%`;
        }
    });

    // 記憶體使用
    const memoryElements = document.querySelectorAll('[style*="width: 40%"]');
    memoryElements.forEach(el => {
        const memoryPercent = Math.min(100, Math.max(0, 35 + Math.random() * 15 - 7.5));
        el.style.width = `${memoryPercent}%`;

        const label = el.closest('.border').querySelector('span.text-sm.font-medium');
        if (label) {
            const memoryGB = (8 * memoryPercent / 100).toFixed(1);
            label.textContent = `${memoryGB}/8 GB`;
        }
    });

    // 網路流量
    const networkElements = document.querySelectorAll('[style*="width: 75%"]');
    networkElements.forEach(el => {
        const networkPercent = Math.min(100, Math.max(0, 70 + Math.random() * 20 - 10));
        el.style.width = `${networkPercent}%`;

        const label = el.closest('.border').querySelector('span.text-sm.font-medium');
        if (label) {
            const networkMB = (2 * networkPercent / 100).toFixed(1);
            label.textContent = `${networkMB} MB/s`;
        }
    });

    // 繼續監控
    setTimeout(updateResourceStats, 3000);
}

// 行動端選單切換
function initMobileMenu() {
    if (mobileMenuButton && navMenu) {
        mobileMenuButton.addEventListener('click', function() {
            navMenu.classList.toggle('hidden');
            navMenu.classList.toggle('flex');
            navMenu.classList.toggle('flex-col');
            navMenu.classList.toggle('absolute');
            navMenu.classList.toggle('top-16');
            navMenu.classList.toggle('right-4');
            navMenu.classList.toggle('bg-white');
            navMenu.classList.toggle('p-4');
            navMenu.classList.toggle('rounded-lg');
            navMenu.classList.toggle('shadow-lg');
            navMenu.classList.toggle('space-y-4');
            navMenu.classList.toggle('space-x-0');
            navMenu.classList.toggle('text-gray-800');
        });
    }
}

// 用戶下拉選單
function initUserDropdown() {
    if (userAvatar && userDropdown) {
        userAvatar.addEventListener('click', function() {
            userDropdown.classList.toggle('hidden');
        });

        // 點擊外部關閉下拉選單
        document.addEventListener('click', function(e) {
            if (!userAvatar.contains(e.target) && !userDropdown.contains(e.target)) {
                userDropdown.classList.add('hidden');
            }
        });
    }
}

// 初始化所有功能
function init() {
    initMobileMenu();
    initUserDropdown();
    updateResourceStats();
}

// 頁面載入完成後初始化
document.addEventListener('DOMContentLoaded', init);
