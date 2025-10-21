'use strict';

// UI 組件模組
// 處理導航選單、用戶下拉選單等 UI 組件行為

export class UIComponents {
  constructor() {
    this.init();
  }

  init() {
    this.initMobileMenu();
    this.initUserDropdown();
    this.initDropdowns();
  }

  // 行動端選單切換
  initMobileMenu() {
    const mobileMenuButton = document.getElementById('mobile-menu-button');
    const navMenu = document.getElementById('nav-menu');

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
  initUserDropdown() {
    const userAvatar = document.getElementById('user-avatar');
    const userDropdown = document.getElementById('user-dropdown');

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

  // 下拉選單功能
  initDropdowns() {
    const dropdownButtons = document.querySelectorAll('.dropdown-toggle');
    dropdownButtons.forEach(button => {
      button.addEventListener('click', function(e) {
        e.preventDefault();

        const dropdown = this.closest('.dropdown');
        if (!dropdown) return;

        const menu = dropdown.querySelector('.dropdown-menu');

        // 關閉其他下拉選單
        document.querySelectorAll('.dropdown-menu').forEach(m => {
          if (m !== menu) m.classList.add('hidden');
        });

        // 切換當前下拉選單
        menu.classList.toggle('hidden');
      });
    });

    // 點擊外部關閉所有下拉選單
    document.addEventListener('click', function(e) {
      if (!e.target.closest('.dropdown')) {
        document.querySelectorAll('.dropdown-menu').forEach(menu => {
          menu.classList.add('hidden');
        });
      }
    });
  }
}
