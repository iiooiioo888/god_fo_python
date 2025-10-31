#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""重命名 ch9 文件以解決編號衝突問題"""

import os
from pathlib import Path

# 定義重命名映射
renames = {
    "ch9-1-部署架构.md": "ch9-11-部署架構.md",
    "ch9-2-部署流程.md": "ch9-12-部署流程.md",
    "ch9-3-监控与告警.md": "ch9-13-監控與告警.md",
    "ch9-4-持续集成与持续部署.md": "ch9-14-持續整合與持續部署.md",
    "ch9-5-安全与合规.md": "ch9-15-安全與合規.md",
    "ch9-6-性能测试方案.md": "ch9-16-效能測試方案.md",
    "ch9-7-灾难恢复计划.md": "ch9-17-災難恢復計畫.md",
}

# 統一其他文件為繁體
other_renames = {
    "ch9-1-模块概述.md": "ch9-1-模組概述.md",
    "ch9-2-详细功能清单.md": "ch9-2-詳細功能清單.md",
    "ch9-3-技术架构.md": "ch9-3-技術架構.md",
    "ch9-4-核心组件详细实现.md": "ch9-4-核心組件詳細實現.md",
    "ch9-5-数据模型详细定义.md": "ch9-5-數據模型詳細定義.md",
    "ch9-6-API详细规范.md": "ch9-6-API詳細規範.md",
    "ch9-7-性能优化策略.md": "ch9-7-效能優化策略.md",
    "ch9-8-安全考虑.md": "ch9-8-安全考慮.md",
    "ch9-9-与其他模块的交互.md": "ch9-9-與其他模組的交互.md",
}

def main():
    ch9_dir = Path(r"E:\Jerry_python\腳本平台\doc\鏡界\ch9")
    
    print("開始重命名 ch9 文件...")
    print("=" * 60)
    
    # 第一階段：重命名部署相關文件
    print("\n階段一：解決編號衝突")
    for old_name, new_name in renames.items():
        old_path = ch9_dir / old_name
        new_path = ch9_dir / new_name
        
        if old_path.exists():
            try:
                old_path.rename(new_path)
                print(f"✓ {old_name} -> {new_name}")
            except Exception as e:
                print(f"✗ 重命名失敗: {old_name} -> {e}")
        else:
            print(f"⚠ 文件不存在: {old_name}")
    
    # 第二階段：統一命名為繁體
    print("\n階段二：統一繁體命名")
    for old_name, new_name in other_renames.items():
        old_path = ch9_dir / old_name
        new_path = ch9_dir / new_name
        
        if old_path.exists():
            try:
                old_path.rename(new_path)
                print(f"✓ {old_name} -> {new_name}")
            except Exception as e:
                print(f"✗ 重命名失敗: {old_name} -> {e}")
        else:
            print(f"⚠ 文件不存在: {old_name}")
    
    print("\n" + "=" * 60)
    print("重命名完成！")
    
    # 列出當前所有文件
    print("\n當前 ch9 目錄的所有 .md 文件：")
    for f in sorted(ch9_dir.glob("*.md")):
        print(f"  - {f.name}")

if __name__ == "__main__":
    main()

