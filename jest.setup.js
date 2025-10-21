// Jest 測試環境設置
import 'regenerator-runtime/runtime';

// Mock 全局變數
global.feather = {
  replace: jest.fn(),
};

global.Chart = jest.fn();

// Mock fetch API
global.fetch = jest.fn();

// Mock 控制台警告以便測試時不會輸出
const originalWarn = console.warn;
console.warn = (...args) => {
  if (typeof args[0] === 'string' && args[0].includes('act()')) {
    return;
  }
  originalWarn.call(console, ...args);
};
