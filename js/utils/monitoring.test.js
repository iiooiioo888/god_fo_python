'use strict';

// 資源監控模組的測試

import { ResourceMonitor } from './monitoring.js';

describe('ResourceMonitor', () => {
  let monitor;

  beforeEach(() => {
    // 設置測試用的DOM結構
    document.body.innerHTML = `
      <div class="border">
        <span class="text-sm font-medium">64%</span>
        <div style="width: 64%"></div>
      </div>
      <div class="border">
        <span class="text-sm font-medium">3.2/8 GB</span>
        <div style="width: 40%"></div>
      </div>
    `;

    monitor = new ResourceMonitor();
    jest.useFakeTimers();
  });

  afterEach(() => {
    jest.clearAllTimers();
  });

  test('應該可以創建實例', () => {
    expect(monitor).toBeInstanceOf(ResourceMonitor);
    expect(monitor.updateInterval).toBe(3000);
    expect(monitor.intervalId).toBeNull();
  });

  test('should start monitoring', () => {
    monitor.start();
    expect(monitor.intervalId).not.toBeNull();

    // 模擬一個更新週期
    jest.advanceTimersByTime(3000);
    expect(monitor.updateStats).toHaveBeenCalledTimes(1);
  });

  test('should stop monitoring', () => {
    monitor.start();
    expect(monitor.intervalId).not.toBeNull();

    monitor.stop();
    expect(monitor.intervalId).toBeNull();
  });

  test('should update CPU stats', () => {
    monitor.updateCPUStats();

    const elements = document.querySelectorAll('[style*="width: 64%"]');
    expect(elements.length).toBeGreaterThan(0);

    elements.forEach(el => {
      const width = parseFloat(el.style.width);
      expect(width).toBeGreaterThanOrEqual(50);
      expect(width).toBeLessThanOrEqual(80);
    });
  });

  test('should update memory stats', () => {
    monitor.updateMemoryStats();

    const elements = document.querySelectorAll('[style*="width: 40%"]');
    expect(elements.length).toBeGreaterThan(0);

    elements.forEach(el => {
      const width = parseFloat(el.style.width);
      expect(width).toBeGreaterThanOrEqual(25);
      expect(width).toBeLessThanOrEqual(50);
    });
  });

  test('should generate random values within bounds', () => {
    const value = monitor.getRandomValue(10, 20);
    expect(value).toBeGreaterThanOrEqual(10);
    expect(value).toBeLessThanOrEqual(20);
  });
});
