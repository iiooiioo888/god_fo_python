'use strict';

// WebCrawler Commander 應用入口
// 負責初始化所有模組和服務

import { UIComponents } from './components/ui-components.js';
import { ResourceMonitor } from './utils/monitoring.js';

class WebCrawlerApp {
  constructor() {
    this.ui = null;
    this.monitor = null;
  }

  // 初始化應用
  init() {
    this.initFeatherIcons();
    this.initUI();
    this.initMonitoring();
    this.initEventListeners();
  }

  // 初始化 Feather Icons
  initFeatherIcons() {
    if (typeof feather !== 'undefined') {
      feather.replace();
    }
  }

  // 初始化 UI 組件
  initUI() {
    this.ui = new UIComponents();
  }

  // 初始化資源監控
  initMonitoring() {
    this.monitor = new ResourceMonitor();
    this.monitor.start();
  }

  // 初始化事件監聽器
  initEventListeners() {
    // 可以添加全局事件監聽器
  }

  // 清理資源
  destroy() {
    if (this.monitor) {
      this.monitor.stop();
    }
  }
}

// 創建應用實例
const app = new WebCrawlerApp();

// 頁面載入完成後啟動應用
document.addEventListener('DOMContentLoaded', function() {
  app.init();
});

// 頁面卸載時清理資源
window.addEventListener('beforeunload', function() {
  app.destroy();
});

// 導出應用實例供其他模組使用
export default app;
