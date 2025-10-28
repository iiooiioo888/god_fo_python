# 项目组件化系统

这是一个现代化的HTML组件化系统，用于重构和组织前端代码。

## 📁 目录结构

```
components/
├── base.html              # 基础页面模板
├── page-header.html       # 页面头部组件
├── card.html              # 卡片组件库
├── modal.html             # 模态框组件
├── status-page.html       # 状态页面模板
├── template-processor.js  # 模板处理引擎
└── README.md             # 本文档
```

## 🚀 快速开始

### 1. 引入模板处理器

```html
<script src="components/template-processor.js"></script>
```

### 2. 使用基础模板

```javascript
// 渲染页面
const pageData = {
    PAGE_TITLE: '我的页面',
    PAGE_DESCRIPTION: '页面描述',
    PAGE_CONTENT: '<h1>Hello World</h1>',
    PAGE_ICON: '🚀'
};

templateProcessor.renderPage('base', pageData);
```

### 3. 使用组件

```javascript
// 渲染组件
const headerData = {
    PAGE_HEADER_TITLE: '标题',
    PAGE_HEADER_SUBTITLE: '副标题'
};

const headerHtml = templateProcessor.render('page-header', headerData);
document.querySelector('#main').innerHTML = headerHtml;
```

## 📋 可用组件

### 🏠 基础模板 (base.html)
```javascript
const data = {
    PAGE_TITLE: '页面标题',
    PAGE_DESCRIPTION: '页面描述',
    PAGE_KEYWORDS: '关键词',
    PAGE_ICON: '🔍',     // 页面图标
    PAGE_CONTENT: '<div>页面内容</div>',
    PAGE_SCRIPTS: '<script>//额外脚本</script>',
    PAGE_HEAD: '<meta name="custom" content="custom">'
};
```

### 📄 页面头部 (page-header.html)
```javascript
const data = {
    PAGE_HEADER_TITLE: '大标题',
    PAGE_HEADER_SUBTITLE: '副标题',
    PAGE_HEADER_EXTRA: '<div>额外内容</div>'
};
```

### 🃏 卡片组件 (card.html)
```javascript
// 基本卡片
const data = {
    CARD_CONTENT: '<div>卡片内容</div>',
    CARD_HOVER_COLOR: 'blue',  // 可选: blue, green, red, purple
    CARD_CLASSES: 'custom-class' // 可选
};

// 数据源卡片
const data = {
    MIRROR_NAME: '数据源名称',
    MIRROR_STATUS: '🟢 清晰',
    MIRROR_DESCRIPTION: '描述',
    MIRROR_TAGS: '<span>标签1</span><span>标签2</span>',
    MIRROR_DOWNLOADS: '1234',
    MIRROR_RATING: '4.5',
    MIRROR_DATE: '2023-10-15',
    MIRROR_STATUS_COLOR: 'green',
    MIRROR_BTN_TEXT: '查看详情'
};
```

### 🔲 模态框 (modal.html)
```javascript
const data = {
    MODAL_ID: 'my-modal',
    MODAL_TITLE: '模态框标题',
    MODAL_SIZE: 'lg',        // lg, xl, 2xl
    MODAL_CONTENT: '<p>模态框内容</p>',
    MODAL_CLOSE_HANDLER: 'closeModal()',
    MODAL_VISIBILITY_CLASS: 'hidden' // 或空字符串
};
```

## 🎨 模板变量语法

使用 `{{ VARIABLE_NAME }}` 语法定义变量：

```html
<h1>{{ PAGE_TITLE }}</h1>
<p>{{ PAGE_DESCRIPTION }}</p>
<div class="{{ COMPONENT_CLASS }}">{{ COMPONENT_CONTENT }}</div>
```

## ⚙️ 高级功能

### 异步模板加载
```javascript
await templateProcessor.loadComponents();  // 自动加载所有组件
// 或
await templateProcessor.loadTemplate('custom', 'components/custom.html');
```

### 模板继承
```javascript
// 可以组合使用多个组件
const pageHtml = `
    ${templateProcessor.render('page-header', headerData)}
    ${templateProcessor.render('card', cardData)}
    ${templateProcessor.render('modal', modalData)}
`;
```

### 自定义组件
1. 创建新的HTML文件
2. 使用 `{{ VARIABLE_NAME }}` 定义变量
3. 在templateProcessor中注册:
```javascript
templateProcessor.registerTemplate('my-component', componentHtml);
```

## 🎯 使用示例

### 创建完整页面
```javascript
// 页面数据
const pageData = {
    PAGE_TITLE: '镜库 - 数据源仓库',
    PAGE_DESCRIPTION: '收藏各类图片、视频数据源',
    PAGE_ICON: '🔍',
    PAGE_CONTENT: `
        ${templateProcessor.render('page-header', {
            PAGE_HEADER_TITLE: '镜库',
            PAGE_HEADER_SUBTITLE: '数据源仓库'
        })}
        <section>
            ${templateProcessor.render('card', {
                CARD_CONTENT: '<h3>数据源列表</h3><p>显示所有可用数据源</p>',
                CARD_HOVER_COLOR: 'blue'
            })}
        </section>
    `
};

// 渲染页面
templateProcessor.renderPage('base', pageData);
```

## 📝 注意事项

1. **性能优化**: 模板在客户端处理，避免服务器端渲染开销
2. **SEO友好**: meta标签和结构化内容仍然可以正确索引
3. **可维护性**: 组件复用减少代码重复，易于修改和扩展
4. **兼容性**: 现代浏览器支持，在不支持ES6的环境中需要转换

## 🔧 开发指南

### 添加新组件
1. 创建组件HTML文件
2. 定义变量语法
3. 在template-processor.js中注册
4. 更新文档

### 最佳实践
- 使用语义化HTML
- 保持组件独立性
- 变量命名清晰明了
- 注释完整组件用途
