'use strict';

// 資源監控工具模組
// 處理系統資源監控和動態數據更新

export class ResourceMonitor {
  constructor() {
    this.updateInterval = 3000; // 3秒更新一次
    this.intervalId = null;
  }

  // 開始監控
  start() {
    this.updateStats();
    this.intervalId = setInterval(() => this.updateStats(), this.updateInterval);
  }

  // 停止監控
  stop() {
    if (this.intervalId) {
      clearInterval(this.intervalId);
      this.intervalId = null;
    }
  }

  // 更新資源統計
  updateStats() {
    this.updateCPUStats();
    this.updateMemoryStats();
    this.updateNetworkStats();
    this.updateDiskStats();
  }

  // 更新 CPU 統計
  updateCPUStats() {
    const cpuElements = document.querySelectorAll('[style*="width: 64%"]');
    cpuElements.forEach(el => {
      const cpuPercent = this.getRandomValue(50, 80);
      el.style.width = `${cpuPercent}%`;

      const label = el.closest('.border').querySelector('span.text-sm.font-medium');
      if (label) {
        label.textContent = `${cpuPercent.toFixed(0)}%`;
      }
    });
  }

  // 更新記憶體統計
  updateMemoryStats() {
    const memoryElements = document.querySelectorAll('[style*="width: 40%"]');
    memoryElements.forEach(el => {
      const memoryPercent = this.getRandomValue(25, 50);
      el.style.width = `${memoryPercent}%`;

      const label = el.closest('.border').querySelector('span.text-sm.font-medium');
      if (label) {
        const memoryGB = (8 * memoryPercent / 100).toFixed(1);
        label.textContent = `${memoryGB}/8 GB`;
      }
    });
  }

  // 更新網路統計
  updateNetworkStats() {
    const networkElements = document.querySelectorAll('[style*="width: 75%"]');
    networkElements.forEach(el => {
      const networkPercent = this.getRandomValue(60, 90);
      el.style.width = `${networkPercent}%`;

      const label = el.closest('.border').querySelector('span.text-sm.font-medium');
      if (label) {
        const networkMB = (2 * networkPercent / 100).toFixed(1);
        label.textContent = `${networkMB} MB/s`;
      }
    });
  }

  // 更新磁碟統計
  updateDiskStats() {
    const diskElements = document.querySelectorAll('[style*="width: 24%"]');
    diskElements.forEach(el => {
      const diskPercent = this.getRandomValue(20, 30);
      el.style.width = `${diskPercent}%`;

      const label = el.closest('.border').querySelector('span.text-sm.font-medium');
      if (label) {
        const diskGB = (500 * diskPercent / 100).toFixed(0);
        label.textContent = `${diskGB}/500 GB`;
      }
    });
  }

  // 生成隨機值 (介於 min 和 max 之間)
  getRandomValue(min, max) {
    return Math.min(max, Math.max(min, min + Math.random() * (max - min) - (max - min) / 2));
  }

  // 更新統計卡片顯示
  updateStatCards() {
    // 可以根據需要添加更多的統計卡片更新邏輯
  }
}
