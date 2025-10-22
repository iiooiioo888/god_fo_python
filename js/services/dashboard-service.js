'use strict';

// Dashboard API 服務模組
// 處理與後台API的數據通訊

export class DashboardService {
    constructor() {
        this.baseURL = 'http://localhost:8000';
        this.endpoints = {
            stats: '/api/dashboard/stats',
            resources: '/api/dashboard/resources',
            crawlers: '/api/dashboard/crawlers',
            dataPreview: '/api/dashboard/data-preview',
            systemStatus: '/api/dashboard/system-status'
        };
    }

    // 通用API請求方法
    async request(endpoint, options = {}) {
        const url = `${this.baseURL}${endpoint}`;
        const config = {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        };

        try {
            const response = await fetch(url, config);

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error(`API request failed: ${url}`, error);
            throw error;
        }
    }

    // 獲取系統統計數據
    async getSystemStats() {
        return await this.request(this.endpoints.stats);
    }

    // 獲取資源統計數據
    async getResourceStats() {
        return await this.request(this.endpoints.resources);
    }

    // 獲取爬蟲列表
    async getCrawlers() {
        return await this.request(this.endpoints.crawlers);
    }

    // 獲取數據預覽
    async getDataPreview() {
        return await this.request(this.endpoints.dataPreview);
    }

    // 獲取系統狀態
    async getSystemStatus() {
        return await this.request(this.endpoints.systemStatus);
    }
}
