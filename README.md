# WebCrawler Commander 爬爬总控台

一個現代化的 Web 爬蟲管理系統，提供完整的爬蟲任務管理和系統監控功能。

## 🌟 功能特性

- **儀表板管理** - 實時查看系統狀態和爬蟲運行情況
- **爬蟲管理** - 創建、編輯、刪除和管理爬蟲任務
- **任務監控** - 實時監控任務執行狀態和資源使用
- **數據預覽** - 查看爬取到的數據樣本
- **API 文檔** - 完整的 RESTful API 說明文件
- **通知中心** - 系統消息和重要事件通知
- **系統設定** - 全面的參數配置和管理功能
- **用戶認證** - 安全的登入和用戶管理系統

## 📁 專案結構

```
webcrawler-commander/
├── index.html           # 主頁面 - 儀表板
├── login.html           # 登入頁面
├── settings.html        # 系統設定頁面
├── api-docs.html        # API 文檔頁面
├── notifications.html   # 通知中心頁面
├── assets/              # 靜態資源文件
│   ├── images/          # 圖片資源
│   └── icons/           # 圖標資源
├── css/                 # 樣式表文件
│   └── styles.css       # 自定義 CSS 樣式
├── js/                  # JavaScript 文件
│   └── main.js          # 主腳本文件
└── config/              # 配置文件
    └── config.json      # 系統配置參數
```

## 🚀 快速開始

### 方法 1: 本地運行
```bash
# 高隆專案
git clone https://github.com/your-repo/webcrawler-commander.git
cd webcrawler-commander

# 使用 Web 伺服器運行（如 Python 的 http.server）
python -m http.server 8000

# 或使用 Node.js 的 http-server
npx http-server -p 8000

# 打開瀏覽器訪問 http://localhost:8000
```

### 方法 2: 開啟靜態文件
直接在瀏覽器中開啟 `index.html` 文件開始使用。

## 🔧 系統要求

- **瀏覽器** - Chrome 70+, Firefox 65+, Safari 12+, Edge 79+
- **解析度** - 支持響應式設計，適應桌面和移動設備
- **連接** - 需要網路連接到 CDN 資源 (Tailwind CSS, Feather Icons 等)

## 📋 使用指南

### 首次使用
1. 打開 `login.html` 進入登入頁面
2. 使用測試帳號登入：`admin` / `admin`
3. 進入主儀表板查看系統概況

### 功能模組

#### 🏠 儀表板
- 查看系統運行情況統計
- 監控資源使用情況
- 預覽爬取的數據樣本

#### 🕷️ 爬蟲管理
- **廠商創建** - 配置新的爬蟲任務
- **編輯設置** - 修改現有爬蟲參數
- **狀態監控** - 查看實時運行情況

#### ⚙️ 系統設定
- **通用設定** - 語言、時區配置
- **爬蟲參數** - 請求延遲、並發數量
- **監控設置** - 警報閾值配置
- **安全設定** - 用戶權限和管理

#### 📊 API 文檔
完整的 RESTful API 說明，包含：
- 認證方式說明
- 詳細的接口文檔
- 請求響應示例
- 錯誤代碼解釋

#### 🔔 通知中心
- **系統消息** - 重要的系統狀態通知
- **任務提醒** - 爬蟲任務完成提醒
- **錯誤提醒** - 異常情況及時通知
- **更新提醒** - 系統更新和維護通知

## 🔒 安全說明

- 所有敏感配置項應在生產環境中修改
- 默認登入密碼僅用於演示，請及時更換
- 請勿將 `config.json` 中的敏感信息提交到代碼倉庫

## 🎨 技術棧

- **前端框架** - HTML5, CSS3, JavaScript (ES6+)
- **UI 框架** - Tailwind CSS
- **圖標庫** - Feather Icons
- **邏輯結構** - RESTful API
- **響應式** - 移動端友好的設計
- **瀏覽器兼容** - 現代瀏覽器支援

## 📈 性能優化

- 使用 CDN 加載外部資源
- 響應式圖片和資源
- 模塊化 CSS 和 JavaScript
- 優化的資源監控算法
- 預載入關鍵資源

## 🔄 更新日誌

### v1.0.0 (2023-12-01)
- ✨ 首次發佈
- 🎯 完整的功能管理系統
- 🎨 現代化的用戶界面
- 📱 響應式設計支持
- 🔧 可配置的系統參數
- 📋 完善的 API 文檔

## 🤝 貢獻指南

歡迎提交 Issues 和 Pull Requests！

### 開發環境設置
```bash
# 安裝 Node.js 開發工具 (可選)
npm install -g http-server
npm install -g live-server

# 運行開發服務器
live-server --port=8000
```

### 代碼規範
- 使用語義化 HTML 結構
- 遵循 BEM CSS 命名規範
- 使用現代 JavaScript 特性
- 添加適當的注釋文檔

## 📄 許可證

本專案採用 MIT 許可證。詳見 [LICENSE](LICENSE) 文件。

## 🆘 支持與聯繫

- 📧 電子郵件: support@webcrawler-commander.com
- 🐛 問題反饋: [GitHub Issues](https://github.com/your-repo/webcrawler-commander/issues)
- 📚 文檔中心: [API 文檔](api-docs.html)

---

<div align="center">
  <p>製作團隊: Jerry 開發工作室</p>
  <p>© 2023 WebCrawler Commander. 保留所有權利。</p>
</div>
