#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
格式化 Ch7-Ch9 的所有文件，統一格式與 Ch1-Ch6 一致
"""
import sys
from pathlib import Path
import re

sys.stdout.reconfigure(encoding='utf-8')

# 章節配置
CHAPTERS = {
    7: {
        'title': '数据合规与安全中心',
        'subtitle': 'Data Compliance and Security Center',
        'files': [
            ('模块概述', '模块概述'),
            ('详细功能清单', '详细功能清单'),
            ('技术架构', '技术架构'),
            ('核心组件详细实现', '核心组件详细实现'),
            ('数据模型详细定义', '数据模型详细定义'),
            ('API详细规范', 'API详细规范'),
            ('性能优化策略', '性能优化策略'),
            ('安全考虑', '安全考虑'),
            ('与其他模块的交互', '与其他模块的交互'),
        ]
    },
    8: {
        'title': '分布式爬虫集群管理系统',
        'subtitle': 'Distributed Crawler Cluster Management System',
        'files': [
            ('模块概述', '模块概述'),
            ('详细功能清单', '详细功能清单'),
            ('技术架构', '技术架构'),
            ('核心组件详细实现', '核心组件详细实现'),
            ('数据模型详细定义', '数据模型详细定义'),
            ('API详细规范', 'API详细规范'),
            ('性能优化策略', '性能优化策略'),
            ('安全考虑', '安全考虑'),
            ('与其他模块的交互', '与其他模块的交互'),
        ]
    },
    9: {
        'title': '系统集成与部署',
        'subtitle': '',
        'files': [
            ('部署架构', '部署架构'),
            ('部署流程', '部署流程'),
            ('监控与告警', '监控与告警'),
            ('持续集成与持续部署', '持续集成与持续部署'),
            ('安全与合规', '安全与合规'),
            ('性能测试方案', '性能测试方案'),
            ('灾难恢复计划', '灾难恢复计划'),
        ]
    }
}

def format_file(ch_num, idx, title, base_path):
    """格式化單個文件"""
    file_path = base_path / f'ch{ch_num}' / f'ch{ch_num}-{idx}-{title}.md'
    
    if not file_path.exists():
        print(f"⚠️  文件不存在: {file_path.name}")
        return False
    
    # 讀取文件
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    config = CHAPTERS[ch_num]
    chapter_title = f"第{ch_num}章：{config['title']}"
    if config['subtitle']:
        chapter_title += f" ({config['subtitle']})"
    
    section_title = f"{ch_num}.{idx} {title}"
    
    # 檢查是否已經格式化
    if content.startswith(f"# {chapter_title}"):
        print(f"⏭️  已格式化: {file_path.name}")
        return True
    
    # 1. 添加章節標題
    if not content.startswith('#'):
        content = f"# {chapter_title}\n\n## {section_title}\n\n" + content
    else:
        # 替換現有的標題格式
        content = re.sub(r'^\*\*\[←.*?\*\*\n\n---\n\n### \d+\.\d+ .+?\n', 
                        f'# {chapter_title}\n\n## {section_title}\n\n**[← 返回第{ch_num}章首頁](ch{ch_num}-index.md)**\n\n---\n\n', 
                        content, count=1, flags=re.MULTILINE)
    
    # 2. 統一導航格式
    # 找出所有章節文件標題
    file_titles = [t for _, t in config['files']]
    
    # 更新導航表格
    for i in range(1, len(file_titles) + 1):
        if i == idx:
            # 當前章節
            current_pattern = rf'\|\s+\[?{ch_num}\.{idx}\]?.*?\|\s+\*\*{ch_num}\.{idx}\*\*.*?\|\s+\[?{ch_num}\.{idx\+1}\]?'
            current_replacement = f'| [{"前序" if idx > 1 else "-"}] | **{section_title}** | [{"後續" if idx < len(file_titles) else "-"}]'
        else:
            # 更新鏈接格式
            old_link = f'ch{ch_num}-{i}.md'
            new_link = f'ch{ch_num}-{i}-{file_titles[i-1]}.md'
            content = content.replace(old_link, new_link)
            
            # 更新簡短格式鏈接
            short_pattern = rf'\[{ch_num}\.{i}\]\(ch{ch_num}-{i}.md\)'
            replacement = f'[{ch_num}.{i} {file_titles[i-1]}](ch{ch_num}-{i}-{file_titles[i-1]}.md)'
            content = re.sub(short_pattern, replacement, content)
    
    # 3. 更新導航表格中的完整標題
    # 更新前序
    if idx > 1:
        prev_idx = idx - 1
        prev_title = file_titles[prev_idx - 1]
        prev_pattern = rf'\[{ch_num}\.{prev_idx}\]\(ch{ch_num}-{prev_idx}-{prev_title}\.md\)'
        prev_replacement = f'[{ch_num}.{prev_idx} {prev_title}](ch{ch_num}-{prev_idx}-{prev_title}.md)'
        content = re.sub(prev_pattern, prev_replacement, content)
        
        # 更新表格中的前序部分
        table_prev_pattern = rf'\|\s+\[{ch_num}\.{prev_idx}\]\(ch{ch_num}-{prev_idx}-{prev_title}\.md\)\s+\|\s+\*\*{ch_num}\.{idx}.*?\*\*'
        table_prev_replacement = f'| [{ch_num}.{prev_idx} {prev_title}](ch{ch_num}-{prev_idx}-{prev_title}.md) | **{section_title}**'
        content = re.sub(table_prev_pattern, table_prev_replacement, content)
    
    # 更新後續
    if idx < len(file_titles):
        next_idx = idx + 1
        next_title = file_titles[next_idx - 1]
        next_pattern = rf'\[{ch_num}\.{next_idx}\]\(ch{ch_num}-{next_idx}-{next_title}\.md\)'
        next_replacement = f'[{ch_num}.{next_idx} {next_title}](ch{ch_num}-{next_idx}-{next_title}.md)'
        content = re.sub(next_pattern, next_replacement, content)
        
        # 更新表格中的後續部分
        table_next_pattern = rf'\|\s+\*\*{ch_num}\.{idx}.*?\*\*\s+\|\s+\[{ch_num}\.{next_idx}\]\(ch{ch_num}-{next_idx}-{next_title}\.md\)'
        table_next_replacement = f'| **{section_title}** | [{ch_num}.{next_idx} {next_title}](ch{ch_num}-{next_idx}-{next_title}.md)'
        content = re.sub(table_next_pattern, table_next_replacement, content)
    
    # 4. 更新快速鏈接
    quick_links = []
    if idx > 1:
        prev_idx = idx - 1
        prev_title = file_titles[prev_idx - 1]
        quick_links.append(f"- [{ch_num}.{prev_idx} {prev_title}](ch{ch_num}-{prev_idx}-{prev_title}.md)")
    if idx < len(file_titles):
        next_idx = idx + 1
        next_title = file_titles[next_idx - 1]
        quick_links.append(f"- [{ch_num}.{next_idx} {next_title}](ch{ch_num}-{next_idx}-{next_title}.md)")
    quick_links.append(f"- [← 返回第{ch_num}章首頁](ch{ch_num}-index.md)")
    
    # 替換快速鏈接部分
    quick_link_pattern = r'\*\*快速链接：\*\*\n- \[← 返回.*?\]'
    quick_link_replacement = '**快速链接：**\n' + '\n'.join(quick_links)
    content = re.sub(quick_link_pattern, quick_link_replacement, content, flags=re.DOTALL)
    
    # 寫回文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ {file_path.name}")
    return True

def main():
    base_path = Path(r'E:\Jerry_python\腳本平台\doc\鏡界')
    
    for ch_num in [7, 8, 9]:
        config = CHAPTERS[ch_num]
        print(f"\n🔄 處理 Ch{ch_num}: {config['title']}")
        
        for idx, (_, title) in enumerate(config['files'], 1):
            format_file(ch_num, idx, title, base_path)
    
    print("\n✅ 完成！")

if __name__ == '__main__':
    main()

