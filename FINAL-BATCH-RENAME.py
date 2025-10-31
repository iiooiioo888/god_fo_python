#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
鏡界平台最終批量重命名腳本
完成 Ch6-Ch9 的文件重命名 (36 個文件)
"""

import os
import sys
from pathlib import Path

# 設置編碼
sys.stdout.reconfigure(encoding='utf-8')

# 章節配置
CHAPTERS_CONFIG = {
    6: ['模块概述', '详细功能清单', '技术架构', '核心组件详细实现', '数据模型详细定义', 'API详细规范', '性能优化策略', '安全考虑', '与其他模块的交互'],
    7: ['模块概述', '详细功能清单', '技术架构', '核心组件详细实现', '数据模型详细定义', 'API详细规范', '性能优化策略', '安全考虑', '与其他模块的交互'],
    8: ['模块概述', '详细功能清单', '技术架构', '核心组件详细实现', '数据模型详细定义', 'API详细规范', '性能优化策略', '安全考虑', '与其他模块的交互'],
    9: ['模块概述', '详细功能清单', '技术架构', '核心组件详细实现', '数据模型详细定义', 'API详细规范', '性能优化策略']
}

def rename_chapter_files(ch_num):
    """為指定章節重命名所有文件"""
    base_path = Path(r'E:\Jerry_python\腳本平台\doc\鏡界') / f'ch{ch_num}'
    
    if not base_path.exists():
        print(f"❌ 目錄不存在: {base_path}")
        return 0
    
    titles = CHAPTERS_CONFIG.get(ch_num, [])
    count = 0
    
    for idx, title in enumerate(titles, 1):
        old_file = base_path / f'ch{ch_num}-{idx}.md'
        new_file = base_path / f'ch{ch_num}-{idx}-{title}.md'
        
        if old_file.exists() and not new_file.exists():
            try:
                # 讀取舊文件
                with open(old_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 更新所有內部鏈接
                for i in range(1, 10):
                    if i <= len(titles):
                        old_link = f'ch{ch_num}-{i}.md'
                        new_link = f'ch{ch_num}-{i}-{titles[i-1]}.md'
                        content = content.replace(old_link, new_link)
                
                # 寫入新文件
                with open(new_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                print(f"  ✅ ch{ch_num}-{idx}-{title}.md")
                count += 1
                
            except Exception as e:
                print(f"  ❌ 錯誤: {old_file.name} - {str(e)}")
    
    return count

def main():
    print("=" * 60)
    print("鏡界平台最終批量重命名")
    print("=" * 60)
    
    total = 0
    
    for ch in [6, 7, 8, 9]:
        print(f"\n🔄 處理 Ch{ch}...")
        count = rename_chapter_files(ch)
        total += count
        expected = len(CHAPTERS_CONFIG.get(ch, []))
        print(f"  完成: {count}/{expected} 個文件")
    
    print("\n" + "=" * 60)
    print(f"✅ 總計完成: {total}/36 個文件")
    print("=" * 60)

if __name__ == '__main__':
    main()
