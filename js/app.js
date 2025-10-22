'use strict';

// WebCrawler Commander 應用入口
// 負責初始化所有模組和服務

import { UIComponents } from './components/ui-components.js';
import { ResourceMonitor } from './utils/monitoring.js';
import { DashboardService } from './services/dashboard-service.js';

class WebCrawlerApp {
  constructor() {
    this.ui = null;
    this.monitor = null;
    this.api = null;
  }

  // 初始化應用
  init() {
    this.initFeatherIcons();
    this.initUI();
    this.initAPI();
    this.initMonitoring();
    this.initEventListeners();
    this.loadInitialData();
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

  // 初始化 API 服務
  initAPI() {
    this.api = new DashboardService();
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

  // 載入初始數據
  async loadInitialData() {
    try {
      await this.loadSystemStats();
      await this.loadCrawlers();
      await this.loadDataPreview();
    } catch (error) {
      console.error('Error loading initial data:', error);
    }
  }

  // 載入系統統計數據
  async loadSystemStats() {
    try {
      const stats = await this.api.getSystemStats();
      this.updateSystemStats(stats);
    } catch (error) {
      console.error('Error loading system stats:', error);
    }
  }

  // 載入爬蟲列表
  async loadCrawlers() {
    try {
      const crawlers = await this.api.getCrawlers();
      this.updateCrawlerList(crawlers);
    } catch (error) {
      console.error('Error loading crawlers:', error);
    }
  }

  // 載入數據預覽
  async loadDataPreview() {
    try {
      const data = await this.api.getDataPreview();
      this.updateDataPreview(data);
    } catch (error) {
      console.error('Error loading data preview:', error);
    }
  }

  // 更新系統統計顯示
  updateSystemStats(stats) {
    // 更新活躍爬蟲數
    const activeCrawlersEl = document.querySelector('.grid.grid-cols-1.md\\:grid-cols-2.lg\\:grid-cols-5 > div:nth-child(1) h3');
    if (activeCrawlersEl) {
      activeCrawlersEl.textContent = stats.active_crawlers;
    }

    // 更新今日任務數
    const todayTasksEl = document.querySelector('.grid.grid-cols-1.md\\:grid-cols-2.lg\\:grid-cols-5 > div:nth-child(2) h3');
    if (todayTasksEl) {
      todayTasksEl.textContent = stats.today_tasks;
    }

    // 更新抓取數據
    const scrapedDataEl = document.querySelector('.grid.grid-cols-1.md\\:grid-cols-2.lg\\:grid-cols-5 > div:nth-child(3) h3');
    if (scrapedDataEl) {
      const formattedData = stats.scraped_data >= 1000 ? (stats.scraped_data / 1000).toFixed(1) + 'K' : stats.scraped_data;
      scrapedDataEl.textContent = formattedData;
    }

    // 更新錯誤報告
    const errorReportsEl = document.querySelector('.grid.grid-cols-1.md\\:grid-cols-2.lg\\:grid-cols-5 > div:nth-child(4) h3');
    if (errorReportsEl) {
      errorReportsEl.textContent = stats.error_reports;
    }

    // 更新CPU使用率
    const cpuUsageEl = document.querySelector('.grid.grid-cols-1.md\\:grid-cols-2.lg\\:grid-cols-5 > div:nth-child(5) h3');
    if (cpuUsageEl) {
      cpuUsageEl.textContent = Math.round(stats.cpu_usage) + '%';
    }

    // 更新CPU進度條
    const cpuProgressEl = document.querySelector('.grid.grid-cols-1.md\\:grid-cols-2.lg\\:grid-cols-5 > div:nth-child(5) .bg-purple-600');
    if (cpuProgressEl) {
      cpuProgressEl.style.width = Math.round(stats.cpu_usage) + '%';
    }
  }

  // 更新爬蟲列表
  updateCrawlerList(crawlers) {
    const crawlerListEl = document.querySelector('.divide-y.divide-gray-200');
    if (!crawlerListEl) return;

    const crawlersHtml = crawlers.map(crawler => `
      <div class="p-6 hover:bg-gray-50 transition cursor-pointer">
        <div class="flex justify-between items-start">
          <div class="flex items-start space-x-4">
            <div class="p-3 bg-indigo-100 rounded-lg text-indigo-600">
              <i data-feather="globe" class="w-6 h-6"></i>
            </div>
            <div>
              <h4 class="text-lg font-medium text-gray-900">${crawler.name}</h4>
              <p class="text-gray-600">${crawler.type}</p>
              <div class="mt-2 flex flex-wrap gap-2">
                <span class="px-2 py-1 bg-green-100 text-green-800 text-xs rounded-full">${crawler.status}</span>
                <span class="px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded-full">${crawler.type}</span>
                <span class="px-2 py-1 bg-purple-100 text-purple-800 text-xs rounded-full">${crawler.schedule}</span>
              </div>
            </div>
          </div>
          <div class="flex space-x-3">
            <button class="text-indigo-600 hover:text-indigo-800 transition">
              <i data-feather="eye" class="w-5 h-5"></i>
            </button>
            <button class="text-gray-500 hover:text-gray-700 transition">
              <i data-feather="edit" class="w-5 h-5"></i>
            </button>
            <button class="text-gray-500 hover:text-gray-700 transition">
              <i data-feather="trash" class="w-5 h-5"></i>
            </button>
          </div>
        </div>
      </div>
    `).join('');

    crawlerListEl.innerHTML = crawlersHtml;

    // 重新初始化圖標
    if (typeof feather !== 'undefined') {
      feather.replace();
    }
  }

  // 更新數據預覽
  updateDataPreview(data) {
    const previewContainer = document.querySelector('.p-4.h-full.overflow-y-auto');
    if (!previewContainer) return;

    const productsHtml = data.products.map(product => `
      <div class="bg-white rounded-lg shadow-sm p-4 mb-4">
        <div class="flex items-start space-x-4">
          <img src="${product.image}" alt="${product.name}" class="w-16 h-16 object-cover rounded">
          <div class="flex-1">
            <h5 class="font-medium">${product.name}</h5>
            <p class="text-gray-600 text-sm">${product.platform}</p>
            <div class="mt-2 flex justify-between items-center">
              <span class="text-red-500 font-bold">${product.price.toLocaleString()}元</span>
              <span class="text-green-600 text-sm">${product.sales}</span>
            </div>
          </div>
        </div>
      </div>
    `).join('');

    previewContainer.innerHTML = productsHtml;
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
