# 微博USID爬蟲使用說明

## 概述

這個腳本專門用於爬取 weibo.cn 的用戶信息，只收集女性用戶的數據並輸出為CSV格式。

## 功能特點

- ✅ 支持10位數字UID範圍掃描
- ✅ 支持使用登錄cookie獲取關注列表
- ✅ 自動識別用戶性別，只收錄女性用戶
- ✅ 收集用戶名、最近發佈時間、相冊相片數量
- ✅ CSV格式輸出，支持中文
- ✅ 異步處理，多線程並發
- ✅ 智能重試和錯誤處理
- ✅ Cookie支持處理反爬蟲

## 系統需求

- Python 3.8+
- 已安裝的依賴：
  - httpx
  - beautifulsoup4
  - lxml

## 安裝依賴

```bash
pip install httpx beautifulsoup4 lxml
```

## 使用方法

### 1. 範圍掃描模式 (掃描指定UID範圍)

```python
import asyncio
from scripts.weibo_crawler_example import example_range_scan

# 運行範圍掃描示例
asyncio.run(example_range_scan())
```

### 2. 關注列表示例 (使用登錄cookie)

```python
import asyncio
from scripts.weibo_crawler_example import example_following_list

# 運行關注列表示例 (需要設置cookie)
asyncio.run(example_following_list())
```

### 3. 自定義配置

```python
import asyncio
from services.weibo_usid_crawler import create_weibo_config, get_weibo_crawler, DataSource

# 創建配置
config = create_weibo_config(
    data_source=DataSource.RANGE_SCAN,  # 或 DataSource.FOLLOWING_LIST
    uid_range_start=1669879400,         # 起始UID
    uid_range_end=1669879500,           # 結束UID
    max_concurrent=3,                   # 並發數量
    request_delay=2.0,                  # 請求間隔(秒)
    cookie="your_weibo_cookie_here",    # 微博cookie
    csv_output_path="data/my_results.csv"  # 輸出路徑
)

# 運行爬蟲
crawler = get_weibo_crawler()
results = await crawler.crawl_female_users(config)

print(f"找到 {len(results)} 個女性用戶")

# 關閉資源
await crawler.close()
```

## 配置說明

### 數據來源選擇

1. **RANGE_SCAN (範圍掃描)**
   - 自動生成連續的10位數字UID
   - 適用於大規模掃描
   - 配置參數：`uid_range_start`, `uid_range_end`

2. **FOLLOWING_LIST (關注列表)**
   - 使用您的微博登錄cookie獲取關注用戶
   - 適用於精準收集
   - 配置參數：`cookie`

### 重要參數

| 參數 | 說明 | 默認值 |
|------|------|--------|
| `max_concurrent` | 最大並發請求數量 | 5 |
| `request_delay` | 請求間隔(秒)，反爬蟲 | 1.0 |
| `timeout` | 單個請求超時(秒) | 15.0 |
| `retry_attempts` | 重試次數 | 3 |
| `cookie` | 微博登錄cookie | "" |

## Cookie獲取方法

1. 打開瀏覽器訪問 https://weibo.cn
2. 使用微博賬號登錄
3. 打開開發者工具 (F12)
4. 切換到 Network 標籤
5. 訪問任意微博頁面
6. 在請求頭中找到 Cookie 字段
7. 複製完整cookie字符串

## 輸出格式

CSV文件包含以下字段：

```csv
uid,username,gender,last_post_time,photos_count,crawled_at
1669879400,张三,女,2023-01-15T14:30:00,25,2023-01-20T10:00:00
```

### 字段說明

- `uid`: 用戶ID (數字)
- `username`: 用戶名 (字符串)
- `gender`: 性別，目前只包含 "女"
- `last_post_time`: 最近發佈時間 (ISO格式日期時間)
- `photos_count`: 相冊相片數量 (數字)
- `crawled_at`: 數據收集時間 (ISO格式日期時間)

## 運行示例腳本

### 命令行運行

```bash
# 範圍掃描模式
python scripts/weibo_crawler_example.py range

# 關注列表模式
python scripts/weibo_crawler_example.py following

# 交互式配置
python scripts/weibo_crawler_example.py
```

### Python代碼調用

```python
import asyncio
from scripts.weibo_crawler_example import example_range_scan

# 直接運行
asyncio.run(example_range_scan())
```

## 注意事項

### 反爬蟲措施

1. ⚠️ **請求間隔**: 不要設置過小的請求間隔，可能導致賬號被封
2. ⚠️ **IP限制**: 大規模爬取可能觸發IP限制
3. ⚠️ **Cookie時效**: 定期更新微博cookie
4. ⚠️ **用戶協議**: 請遵守微博使用協議

### 性能優化

1. **並發數量**: 建議 2-5 個並發請求
2. **請求間隔**: 建議 1-3 秒
3. **範圍大小**: 單次運行不超過10萬個UID

### 錯誤處理

腳本會自動處理常見錯誤：
- 網路連接失敗
- 頁面加載失敗
- 用戶不存在
- 權限不足

所有錯誤都會記錄到日誌中，並且不會中斷整個爬取進程。

## 故障排除

### 常見問題

**Q: ImportError: No module named 'beautifulsoup4'**
A: 安裝依賴 `pip install beautifulsoup4 lxml`

**Q: 沒有找到任何女性用戶**
A: 檢查UID範圍是否正確，或者該範圍內用戶很少

**Q: Cookie無效**
A: 重新獲取微博cookie，確保包含有效的登錄信息

**Q: 請求被拒絕**
A: 增加請求間隔，或者更換cookie

**Q: 輸出文件為空**
A: 檢查日誌，看是否有錯誤信息

## 日誌查看

腳本會生成詳細的日誌信息，包括：
- 處理進度
- 錯誤信息
- 統計數據

日誌文件位置：`backend/logs/webcrawler.log`

## 擴展開發

### 添加新功能

1. 在 `WeibolusIDCrawler` 類中添加新方法
2. 更新配置類 `WeibouserConfig` 以支持新參數
3. 修改數據提取邏輯

### 自定義數據提取

```python
# 在 _extract_gender_from_html 方法中修改性別識別邏輯
def _extract_gender_from_html(self, html_content: str) -> Gender:
    # 自定義性別識別邏輯
    pass
```

## 作者

Cline (基於Jerry開發工作室框架)

## 版本

v1.0.0
