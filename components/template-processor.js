/**
 * Template Processor - 模板处理器
 * 用于处理HTML模板的变量替换和组件化
 */

class TemplateProcessor {
    constructor() {
        this.templates = new Map();
    }

    /**
     * 注册模板
     * @param {string} name - 模板名称
     * @param {string} template - 模板HTML字符串
     */
    registerTemplate(name, template) {
        this.templates.set(name, template);
    }

    /**
     * 渲染模板
     * @param {string} name - 模板名称
     * @param {object} data - 模板数据
     * @returns {string} 渲染后的HTML
     */
    render(name, data = {}) {
        let template = this.templates.get(name);
        if (!template) {
            console.error(`Template "${name}" not found`);
            return '';
        }

        // 替换变量
        template = this.replaceVariables(template, data);

        return template;
    }

    /**
     * 替换模板变量
     * @param {string} template - 模板字符串
     * @param {object} data - 数据对象
     * @returns {string} 替换后的字符串
     */
    replaceVariables(template, data) {
        return template.replace(/\{\{\s*(\w+)\s*\}\}/g, (match, key) => {
            return data[key] !== undefined ? data[key] : '';
        });
    }

    /**
     * 从URL异步加载模板
     * @param {string} name - 模板名称
     * @param {string} url - 模板文件URL
     */
    async loadTemplate(name, url) {
        try {
            const response = await fetch(url);
            const template = await response.text();
            this.registerTemplate(name, template);
        } catch (error) {
            console.error(`Failed to load template "${name}" from ${url}:`, error);
        }
    }

    /**
     * 批量加载组件
     */
    async loadComponents() {
        const components = [
            { name: 'base', url: 'components/base.html' },
            { name: 'page-header', url: 'components/page-header.html' },
            { name: 'card', url: 'components/card.html' },
            { name: 'modal', url: 'components/modal.html' }
        ];

        for (const component of components) {
            await this.loadTemplate(component.name, component.url);
        }
    }

    /**
     * 渲染页面
     * @param {string} pageTemplate - 页面模板名
     * @param {object} pageData - 页面数据
     * @param {HTMLElement} container - 容器元素（默认为document.body）
     */
    renderPage(pageTemplate, pageData = {}, container = document.body) {
        const html = this.render(pageTemplate, pageData);
        container.innerHTML = html;

        // 重新初始化Feather图标
        if (typeof feather !== 'undefined') {
            feather.replace();
        }
    }
}

// 全局实例化
window.templateProcessor = new TemplateProcessor();

// DOM ready后加载组件
document.addEventListener('DOMContentLoaded', async () => {
    await window.templateProcessor.loadComponents();
});
