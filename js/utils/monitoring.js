'use strict';

// 資源監控工具模組
// 處理系統資源監控和動態數據更新

import { DashboardService } from '../services/dashboard-service.js';

export class ResourceMonitor {
  constructor() {
    this.updateInterval = 5000; // 5秒更新一次
    this.intervalId = null;
    this.api = new DashboardService();
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
  async updateStats() {
    try {
      const resourceStats = await this.api.getResourceStats();
      this.updateResourceDisplays(resourceStats);
    } catch (error) {
      console.error('Error updating resource stats:', error);
      // 如果API調用失敗，暫時停止更新
      this.stop();
    }
  }

  // 更新資源顯示
  updateResourceDisplays(stats) {
    this.updateCPUStats(stats.cpu);
    this.updateMemoryStats(stats.memory);
    this.updateNetworkStats(stats.network);
    this.updateDiskStats(stats.disk);
  }

  // 更新 CPU 統計
  updateCPUStats(cpuData) {
    const cpuPercent = Math.round(cpuData.usage);

    // 找到CPU區塊
    const resourceBlocks = document.querySelectorAll('.border.border-gray-200.rounded-lg.p-4');
    if (resourceBlocks.length >= 4) {
      const cpuBlock = resourceBlocks[0]; // CPU 是第一個

      // 更新進度條
      const cpuProgressEl = cpuBlock.querySelector('.bg-purple-600');
      if (cpuProgressEl) {
        cpuProgressEl.style.width = `${cpuPercent}%`;
      }

      // 更新標籤
      const cpuLabelEl = cpuBlock.querySelector('span.text-sm.font-medium');
      if (cpuLabelEl) {
        cpuLabelEl.textContent = `${cpuPercent}%`;
      }
    }
  }

  // 更新記憶體統計
  updateMemoryStats(memoryData) {
    const memoryPercent = Math.round(memoryData.usage);

    // 找到記憶體區塊
    const resourceBlocks = document.querySelectorAll('.border.border-gray-200.rounded-lg.p-4');
    if (resourceBlocks.length >= 4) {
      const memoryBlock = resourceBlocks[1]; // 記憶體是第二個

      // 更新進度條
      const memoryProgressEl = memoryBlock.querySelector('.bg-blue-600');
      if (memoryProgressEl) {
        memoryProgressEl.style.width = `${memoryPercent}%`;
      }

      // 更新標籤
      const memoryLabelEl = memoryBlock.querySelector('span.text-sm.font-medium');
      if (memoryLabelEl) {
        memoryLabelEl.textContent = memoryData.details;
      }
    }
  }

  // 更新網路統計
  updateNetworkStats(networkData) {
    const networkPercent = Math.round(networkData.usage);

    // 找到網路區塊
    const resourceBlocks = document.querySelectorAll('.border.border-gray-200.rounded-lg.p-4');
    if (resourceBlocks.length >= 4) {
      const networkBlock = resourceBlocks[2]; // 網路是第三個

      // 更新進度條
      const networkProgressEl = networkBlock.querySelector('.bg-yellow-600');
      if (networkProgressEl) {
        networkProgressEl.style.width = `${networkPercent}%`;
      }

      // 更新標籤
      const networkLabelEl = networkBlock.querySelector('span.text-sm.font-medium');
      if (networkLabelEl) {
        networkLabelEl.textContent = networkData.details;
      }
    }
  }

  // 更新磁碟統計
  updateDiskStats(diskData) {
    const diskPercent = Math.round(diskData.usage);

    // 找到磁碟區塊
    const resourceBlocks = document.querySelectorAll('.border.border-gray-200.rounded-lg.p-4');
    if (resourceBlocks.length >= 4) {
      const diskBlock = resourceBlocks[3]; // 磁碟是第四個

      // 更新進度條
      const diskProgressEl = diskBlock.querySelector('.bg-green-600');
      if (diskProgressEl) {
        diskProgressEl.style.width = `${diskPercent}%`;
      }

      // 更新標籤
      const diskLabelEl = diskBlock.querySelector('span.text-sm.font-medium');
      if (diskLabelEl) {
        diskLabelEl.textContent = diskData.details;
      }
    }
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
