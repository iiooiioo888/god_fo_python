#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
镜界平台文件重命名自动化脚本
快速完成 Ch3-Ch9 的所有文件重命名工作（62 個文件）
"""

import os
import re
from pathlib import Path

# 完整的章節配置
CHAPTERS_CONFIG = {
    3: {
        'name': '数据源健康监测系统',
        'titles': [
            '模块概述', '详细功能清单', '技术架构',
            '核心组件详细实现', '数据模型详细定义', 'API详细规范',
            '性能优化策略', '安全考虑', '与其他模块的交互'
        ]
    },
    4: {
        'name': '数据处理工作流引擎',
        'titles': [
            '模块概述', '详细功能清单', '技术架构',
            '核心组件详细实现', '数据模型详细定义', 'API详细规范',
            '性能优化策略', '安全考虑', '与其他模块的交互'
        ]
    },
    5: {
        'name': '自动化媒体处理管道',
        'titles': [
            '模块概述', '详细功能清单', '技术架构',
            '核心组件详细实现', '数据模型详细定义', 'API详细规范',
            '性能优化策略', '安全考虑', '与其他模块的交互'
        ]
    },
    6: {
        'name': 'AI辅助开发系统',
        'titles': [
            '模块概述', '详细功能清单', '技术架构',
            '核心组件详细实现', '数据模型详细定义', 'API详细规范',
            '性能优化策略', '安全考虑', '与其他模块的交互'
        ]
    },
    7: {
        'name': '数据合规与安全中心',
        'titles': [
            '模块概述', '详细功能清单', '技术架构',
            '核心组件详细实现', '数据模型详细定义', 'API详细规范',
            '性能优化策略', '安全考虑', '与其他模块的交互'
        ]
    },
    8: {
        'name': '分布式爬虫集群管理系统',
        'titles': [
            '模块概述', '详细功能清单', '技术架构',
            '核心组件详细实现', '数据模型详细定义', 'API详细规范',
            '性能优化策略', '安全考虑', '与其他模块的交互'
        ]
    },
    9: {
        'name': '系统集成与部署',
        'titles': [
            '模块概述', '详细功能清单', '技术架构',
            '核心组件详细实现', '数据模型详细定义', 'API详细规范',
            '性能优化策略'
        ]
    }
}

def rename_chapter_files(chapter_num, base_path='./doc/鏡界'):
    """為指定章節的所有文件重命名並更新鏈接"""
    if chapter_num not in CHAPTERS_CONFIG:
        print(f"❌ Ch{chapter_num} 配置不存在")
        return False
    
    config = CHAPTERS_CONFIG[chapter_num]
    chapter_dir = Path(base_path) / f'ch{chapter_num}'
    
    print(f"\n🔄 處理 Ch{chapter_num}：{config['name']}")
    
    if not chapter_dir.exists():
        print(f"  ❌ 目錄不存在：{chapter_dir}")
        return False
    
    count = 0
    for idx, title in enumerate(config['titles'], 1):
        old_file = chapter_dir / f'ch{chapter_num}-{idx}.md'
        new_file = chapter_dir / f'ch{chapter_num}-{idx}-{title}.md'
        
        if old_file.exists():
            try:
                # 讀取原始文件
                with open(old_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 批量更新所有鏈接
                for i in range(1, 10):
                    if i <= len(config['titles']):
                        old_link = f'ch{chapter_num}-{i}.md'
                        new_link = f'ch{chapter_num}-{i}-{config["titles"][i-1]}.md'
                        content = content.replace(old_link, new_link)
                
                # 寫入新文件
                with open(new_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                print(f"  ✅ {old_file.name} → {new_file.name}")
                count += 1
                
            except Exception as e:
                print(f"  ❌ 錯誤處理 {old_file.name}: {str(e)}")
        else:
            print(f"  ⚠️  文件不存在：{old_file.name}")
    
    print(f"  📊 Ch{chapter_num} 完成：{count}/{len(config['titles'])} 文件")
    return count == len(config['titles'])

def main():
    """主程序"""
    print("=" * 60)
    print("镜界平台文件重命名自动化脚本")
    print("=" * 60)
    
    # 處理 Ch3-Ch9
    completed = 0
    total = 0
    
    for ch in range(3, 10):
        if ch in CHAPTERS_CONFIG:
            total += len(CHAPTERS_CONFIG[ch]['titles'])
            if rename_chapter_files(ch):
                completed += len(CHAPTERS_CONFIG[ch]['titles'])
    
    print("\n" + "=" * 60)
    print(f"✅ 完成統計：{completed}/{total} 個文件")
    print("=" * 60)
    print("\n🎉 所有文件重命名完成！")

if __name__ == '__main__':
    main()
