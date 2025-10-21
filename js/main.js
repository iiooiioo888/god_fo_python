'use strict';

// WebCrawler Commander - 向後相容主腳本
// 載入新的模組化應用

// 檢查是否支持模組
if ('import' in document.createElement('script')) {
    // 使用ESM模組系統
    const script = document.createElement('script');
    script.type = 'module';
    script.src = '../../js/app.js';
    document.head.appendChild(script);
} else {
    // Fallback 提示用戶升級瀏覽器
    console.warn('您的瀏覽器不支持ES模組，請升級到現代瀏覽器以獲得最佳體驗。');
    console.info('WebCrawler Commander - 舊版兼容模式載入中...');

    // 載入舊版代碼 (如果需要的話)
    document.addEventListener('DOMContentLoaded', function() {
        console.log('WebCrawler Commander 已載入');
    });
}
