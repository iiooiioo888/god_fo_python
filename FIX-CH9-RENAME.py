#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

base_path = Path(r'E:\Jerry_python\腳本平台\doc\鏡界\ch9')

# Ch9 的正確標題
ch9_titles = [
    '部署架构',
    '部署流程', 
    '监控与告警',
    '持续集成与持续部署',
    '安全与合规',
    '性能测试方案',
    '灾难恢复计划'
]

# 錯誤的標題（腳本生成的）
wrong_titles = [
    '模块概述',
    '详细功能清单',
    '技术架构',
    '核心组件详细实现',
    '数据模型详细定义',
    'API详细规范',
    '性能优化策略'
]

for idx, (wrong, correct) in enumerate(zip(wrong_titles, ch9_titles), 1):
    old_file = base_path / f'ch9-{idx}-{wrong}.md'
    new_file = base_path / f'ch9-{idx}-{correct}.md'
    
    if old_file.exists() and not new_file.exists():
        # 讀取舊文件
        with open(old_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 更新所有內部鏈接
        for i in range(1, 8):
            if i <= len(ch9_titles):
                old_link = f'ch9-{i}-{wrong_titles[i-1]}.md'
                new_link = f'ch9-{i}-{ch9_titles[i-1]}.md'
                content = content.replace(old_link, new_link)
                # 也更新舊格式鏈接
                content = content.replace(f'ch9-{i}.md', new_link)
        
        # 寫入新文件
        with open(new_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ {old_file.name} → {new_file.name}")

print("\n完成 Ch9 文件重命名！")

