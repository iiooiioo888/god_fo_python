# 批量文件重命名自動化方案

**目標**：快速為 Ch2-Ch9 的 72 個子文件添加小章節標題  
**完成時間**：預計 30-60 分鐘（使用自動化方法）

---

## 📋 任務概況

### 工作量統計
- **總文件數**：72 個（8 章 × 9 個文件）
- **操作類型**：
  - 文件重命名：72 個
  - 內部鏈接更新：360+ 個
  - 索引更新：8 個

### 進度追蹤

| 章節 | 原始狀態 | 目標狀態 | 進度 | 狀態 |
|------|---------|---------|------|------|
| ✅ Ch1 | ch1-X.md | ch1-X-標題.md | 9/9 | ✅ 完成 |
| 🔄 Ch2 | ch2-X.md | ch2-X-標題.md | 1/9 | 進行中 |
| ⏳ Ch3 | ch3-X.md | ch3-X-標題.md | 0/9 | 待進行 |
| ⏳ Ch4 | ch4-X.md | ch4-X-標題.md | 0/9 | 待進行 |
| ⏳ Ch5 | ch5-X.md | ch5-X-標題.md | 0/9 | 待進行 |
| ⏳ Ch6 | ch6-X.md | ch6-X-標題.md | 0/9 | 待進行 |
| ⏳ Ch7 | ch7-X.md | ch7-X-標題.md | 0/9 | 待進行 |
| ⏳ Ch8 | ch8-X.md | ch8-X-標題.md | 0/9 | 待進行 |
| ⏳ Ch9 | ch9-X.md | ch9-X-標題.md | 0/7 | 待進行 |

**總進度**：1/72 (1%)

---

## 🔧 執行方案

### 方案 A：自動化腳本（推薦）

由於工作量巨大，建議使用 Python 腳本自動化完成：

```python
#!/usr/bin/env python3
import os
import re
from pathlib import Path

# 配置章節映射
chapters_config = {
    2: {
        'name': '網站指紋分析引擎',
        'titles': [
            '模組概述', '詳細功能清單', '技術架構',
            '核心組件詳細實現', '資料模型詳細定義', 'API詳細規範',
            '效能優化策略', '安全考慮', '與其他模組的交互'
        ]
    },
    3: {
        'name': '資料源健康监测系統',
        'titles': [
            '模組概述', '詳細功能清單', '技術架構',
            '核心組件詳細實現', '資料模型詳細定義', 'API詳細規範',
            '效能優化策略', '安全考慮', '與其他模組的交互'
        ]
    },
    # ... 其他章節配置 ...
}

def rename_chapter_files(chapter_num):
    """為指定章節的所有文件重命名並更新鏈接"""
    config = chapters_config[chapter_num]
    base_path = Path(f'ch{chapter_num}')
    
    print(f"\n🔄 處理 Ch{chapter_num}：{config['name']}")
    
    for idx, title in enumerate(config['titles'], 1):
        old_file = base_path / f'ch{chapter_num}-{idx}.md'
        new_file = base_path / f'ch{chapter_num}-{idx}-{title}.md'
        
        if old_file.exists():
            # 讀取文件內容
            with open(old_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 批量更新所有鏈接
            for i in range(1, 10):
                old_link = f'ch{chapter_num}-{i}.md'
                new_link = f'ch{chapter_num}-{i}-{config["titles"][i-1]}.md'
                content = content.replace(old_link, new_link)
            
            # 寫入新文件
            with open(new_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"  ✅ {old_file.name} → {new_file.name}")

# 主程序
if __name__ == '__main__':
    for ch in range(2, 10):
        if ch in chapters_config:
            rename_chapter_files(ch)
    
    print("\n✅ 所有文件已重命名！")
```

### 方案 B：批量手動操作指南

如果偏好手動操作，按以下步驟進行：

1. **Ch2**：9 個文件
   - 打開每個 ch2-X.md
   - 複製內容到新文件 ch2-X-標題.md
   - 使用查找替換更新所有鏈接

2. **重複上述步驟**直到 Ch9

3. **驗證**：檢查所有鏈接是否正常工作

---

## ✨ 實施步驟

### 步驟 1：準備（已完成）
- ✅ 建立完整的映射表
- ✅ Ch1 已完全完成（9/9）
- ✅ Ch2 已開始（1/9）

### 步驟 2：執行（進行中）
- 🔄 繼續完成 Ch2 其餘 8 個文件
- ⏳ 按順序完成 Ch3-Ch9

### 步驟 3：驗證（待進行）
- ⏳ 測試所有鏈接
- ⏳ 更新索引文件
- ⏳ 最終檢查

---

## 📊 預期成果

### 完成後的結構
```
文件結構將從：
ch2/
├── ch2-1.md
├── ch2-2.md
├── ch2-3.md
... (9 個簡單名稱)

變為：
ch2/
├── ch2-1-模組概述.md
├── ch2-2-詳細功能清單.md
├── ch2-3-技術架構.md
... (9 個描述性名稱)
```

### 優勢
- 📚 **可讀性提升**：清晰看到每個文件的內容
- 🔗 **鏈接完整**：所有跨文件鏈接正確
- 📖 **組織性改善**：整個文檔結構更清晰
- 🎯 **用戶友好**：更容易找到需要的章節

---

## 🚀 快速完成計劃

### 立即行動
```
時間分配：
- Ch2：15 分鐘（1/9 已完成）
- Ch3：12 分鐘（0/9）
- Ch4：12 分鐘（0/9）
- Ch5：12 分鐘（0/9）
- Ch6：12 分鐘（0/9）
- Ch7：12 分鐘（0/9）
- Ch8：12 分鐘（0/9）
- Ch9：10 分鐘（0/7）

總計：85 分鐘內完成所有 72 個文件重命名
```

### 推薦執行方式

**最快方法**（推薦）：
1. 使用上述 Python 腳本自動化
2. 3-5 分鐘內完成所有 72 個文件
3. 驗證無誤即可

**次快方法**：
1. 逐章使用編輯器批量替換
2. 20-30 分鐘完成
3. 需要手動檢查

---

## 💾 腳本配置（完整版）

針對 Ch3-Ch9，標題配置如下：

```python
chapters_config = {
    3: {'name': '資料源健康监测系統', 'titles': [...]},
    4: {'name': '資料處理工作流引擎', 'titles': [...]},
    5: {'name': '自動化媒體處理管道', 'titles': [...]},
    6: {'name': 'AI輔助開发系統', 'titles': [...]},
    7: {'name': '資料合規與安全中心', 'titles': [...]},
    8: {'name': '分布式爬蟲集群管理系統', 'titles': [...]},
    9: {'name': '系統整合與部署', 'titles': [...]},
}
```

---

## 📝 檢查清單

完成後，確保：
- [ ] 所有 72 個新文件已建立
- [ ] 所有舊文件鏈接已更新
- [ ] 索引文件已更新
- [ ] 所有鏈接都能正常工作
- [ ] 沒有損壞的鏈接

---

## 🎯 最終目標

**完全完成**所有 9 章 × 9 個文件的重命名工作，使整個文檔系統：
- ✨ 組織清晰
- 📚 易於導航
- 🔗 鏈接完整
- 📖 專業呈現

**預計總耗時**：2 小時內完成所有工作
