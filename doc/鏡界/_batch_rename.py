#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""批量重命名並統一繁體中文命名"""

import os
import shutil
from pathlib import Path

def rename_files():
    base_dir = Path(r"E:\Jerry_python\腳本平台\doc\鏡界")
    
    # Ch9 部署相關文件重命名映射 (編號 14-17，這些已經部分處理，現在處理剩下的)
    ch9_deployment_renames = {
        "ch9/ch9-4-持续集成与持续部署.md": "ch9/ch9-14-持續整合與持續部署.md",
        "ch9/ch9-5-安全与合规.md": "ch9/ch9-15-安全與合規.md",
        "ch9/ch9-6-性能测试方案.md": "ch9/ch9-16-效能測試方案.md",
        "ch9/ch9-7-灾难恢复计划.md": "ch9/ch9-17-災難恢復計畫.md",
    }
    
    # 統一其他章節為繁體
    unified_renames = {
        # Ch1
        "ch1/ch1-2-詳細功能清单.md": "ch1/ch1-2-詳細功能清單.md",
        "ch1/ch1-3-技术架构.md": "ch1/ch1-3-技術架構.md",
        "ch1/ch1-7-性能优化策略.md": "ch1/ch1-7-效能優化策略.md",
        "ch1/ch1-8-安全考虑.md": "ch1/ch1-8-安全考慮.md",
        "ch1/ch1-9-与其他模块的交互.md": "ch1/ch1-9-與其他模組的交互.md",
        "ch1/ch1-10-最佳实践指南.md": "ch1/ch1-10-最佳實踐指南.md",
        
        # Ch2
        "ch2/ch2-1-模块概述.md": "ch2/ch2-1-模組概述.md",
        "ch2/ch2-2-详细功能清单.md": "ch2/ch2-2-詳細功能清單.md",
        "ch2/ch2-3-技术架构.md": "ch2/ch2-3-技術架構.md",
        "ch2/ch2-4-核心组件详细实现.md": "ch2/ch2-4-核心組件詳細實現.md",
        "ch2/ch2-5-数据模型详细定义.md": "ch2/ch2-5-數據模型詳細定義.md",
        "ch2/ch2-6-API详细规范.md": "ch2/ch2-6-API詳細規範.md",
        "ch2/ch2-7-性能优化策略.md": "ch2/ch2-7-效能優化策略.md",
        "ch2/ch2-8-安全考虑.md": "ch2/ch2-8-安全考慮.md",
        "ch2/ch2-9-与其他模块的交互.md": "ch2/ch2-9-與其他模組的交互.md",
        "ch2/ch2-10-最佳实践指南.md": "ch2/ch2-10-最佳實踐指南.md",
        
        # Ch3
        "ch3/ch3-1-模块概述.md": "ch3/ch3-1-模組概述.md",
        "ch3/ch3-2-详细功能清单.md": "ch3/ch3-2-詳細功能清單.md",
        "ch3/ch3-3-技术架构.md": "ch3/ch3-3-技術架構.md",
        "ch3/ch3-4-核心组件详细实现.md": "ch3/ch3-4-核心組件詳細實現.md",
        "ch3/ch3-5-数据模型详细定义.md": "ch3/ch3-5-數據模型詳細定義.md",
        "ch3/ch3-6-API详细规范.md": "ch3/ch3-6-API詳細規範.md",
        "ch3/ch3-7-性能优化策略.md": "ch3/ch3-7-效能優化策略.md",
        "ch3/ch3-8-安全考虑.md": "ch3/ch3-8-安全考慮.md",
        "ch3/ch3-9-与其他模块的交互.md": "ch3/ch3-9-與其他模組的交互.md",
        "ch3/ch3-10-最佳实践指南.md": "ch3/ch3-10-最佳實踐指南.md",
        
        # Ch4
        "ch4/ch4-1-模块概述.md": "ch4/ch4-1-模組概述.md",
        "ch4/ch4-2-详细功能清单.md": "ch4/ch4-2-詳細功能清單.md",
        "ch4/ch4-3-技术架构.md": "ch4/ch4-3-技術架構.md",
        "ch4/ch4-4-核心组件详细实现.md": "ch4/ch4-4-核心組件詳細實現.md",
        "ch4/ch4-5-数据模型详细定义.md": "ch4/ch4-5-數據模型詳細定義.md",
        "ch4/ch4-6-API详细规范.md": "ch4/ch4-6-API詳細規範.md",
        "ch4/ch4-7-性能优化策略.md": "ch4/ch4-7-效能優化策略.md",
        "ch4/ch4-8-安全考虑.md": "ch4/ch4-8-安全考慮.md",
        "ch4/ch4-9-与其他模块的交互.md": "ch4/ch4-9-與其他模組的交互.md",
        
        # Ch5
        "ch5/ch5-1-模块概述.md": "ch5/ch5-1-模組概述.md",
        "ch5/ch5-2-详细功能清单.md": "ch5/ch5-2-詳細功能清單.md",
        "ch5/ch5-3-技术架构.md": "ch5/ch5-3-技術架構.md",
        "ch5/ch5-4-核心组件详细实现.md": "ch5/ch5-4-核心組件詳細實現.md",
        "ch5/ch5-5-数据模型详细定义.md": "ch5/ch5-5-數據模型詳細定義.md",
        "ch5/ch5-6-API详细规范.md": "ch5/ch5-6-API詳細規範.md",
        "ch5/ch5-7-性能优化策略.md": "ch5/ch5-7-效能優化策略.md",
        "ch5/ch5-8-安全与合规.md": "ch5/ch5-8-安全與合規.md",
        "ch5/ch5-9-与其他模块的交互.md": "ch5/ch5-9-與其他模組的交互.md",
        
        # Ch6
        "ch6/ch6-1-模块概述.md": "ch6/ch6-1-模組概述.md",
        "ch6/ch6-2-详细功能清单.md": "ch6/ch6-2-詳細功能清單.md",
        "ch6/ch6-3-技术架构.md": "ch6/ch6-3-技術架構.md",
        "ch6/ch6-4-核心组件详细实现.md": "ch6/ch6-4-核心組件詳細實現.md",
        "ch6/ch6-5-数据模型详细定义.md": "ch6/ch6-5-數據模型詳細定義.md",
        "ch6/ch6-6-API详细规范.md": "ch6/ch6-6-API詳細規範.md",
        "ch6/ch6-7-性能优化策略.md": "ch6/ch6-7-效能優化策略.md",
        "ch6/ch6-8-安全考虑.md": "ch6/ch6-8-安全考慮.md",
        "ch6/ch6-9-与其他模块的交互.md": "ch6/ch6-9-與其他模組的交互.md",
        
        # Ch7
        "ch7/ch7-1-模块概述.md": "ch7/ch7-1-模組概述.md",
        "ch7/ch7-2-详细功能清单.md": "ch7/ch7-2-詳細功能清單.md",
        "ch7/ch7-3-技术架构.md": "ch7/ch7-3-技術架構.md",
        "ch7/ch7-4-核心组件详细实现.md": "ch7/ch7-4-核心組件詳細實現.md",
        "ch7/ch7-5-数据模型详细定义.md": "ch7/ch7-5-數據模型詳細定義.md",
        "ch7/ch7-6-API详细规范.md": "ch7/ch7-6-API詳細規範.md",
        "ch7/ch7-7-性能优化策略.md": "ch7/ch7-7-效能優化策略.md",
        "ch7/ch7-8-安全考虑.md": "ch7/ch7-8-安全考慮.md",
        "ch7/ch7-9-与其他模块的交互.md": "ch7/ch7-9-與其他模組的交互.md",
        
        # Ch8
        "ch8/ch8-1-模块概述.md": "ch8/ch8-1-模組概述.md",
        "ch8/ch8-2-详细功能清单.md": "ch8/ch8-2-詳細功能清單.md",
        "ch8/ch8-3-技术架构.md": "ch8/ch8-3-技術架構.md",
        "ch8/ch8-4-核心组件详细实现.md": "ch8/ch8-4-核心組件詳細實現.md",
        "ch8/ch8-5-数据模型详细定义.md": "ch8/ch8-5-數據模型詳細定義.md",
        "ch8/ch8-6-API详细规范.md": "ch8/ch8-6-API詳細規範.md",
        "ch8/ch8-7-性能优化策略.md": "ch8/ch8-7-效能優化策略.md",
        "ch8/ch8-8-安全考虑.md": "ch8/ch8-8-安全考慮.md",
        "ch8/ch8-9-与其他模块的交互.md": "ch8/ch8-9-與其他模組的交互.md",
        
        # Ch9
        "ch9/ch9-1-模块概述.md": "ch9/ch9-1-模組概述.md",
        "ch9/ch9-2-详细功能清单.md": "ch9/ch9-2-詳細功能清單.md",
        "ch9/ch9-3-技术架构.md": "ch9/ch9-3-技術架構.md",
        "ch9/ch9-4-核心组件详细实现.md": "ch9/ch9-4-核心組件詳細實現.md",
        "ch9/ch9-5-数据模型详细定义.md": "ch9/ch9-5-數據模型詳細定義.md",
        "ch9/ch9-6-API详细规范.md": "ch9/ch9-6-API詳細規範.md",
        "ch9/ch9-7-性能优化策略.md": "ch9/ch9-7-效能優化策略.md",
        "ch9/ch9-8-安全考虑.md": "ch9/ch9-8-安全考慮.md",
        "ch9/ch9-9-与其他模块的交互.md": "ch9/ch9-9-與其他模組的交互.md",
    }
    
    print("=" * 80)
    print("批量重命名文件腳本")
    print("=" * 80)
    
    # 第一階段：Ch9 部署相關文件 (編號調整)
    print("\n階段一：Ch9 部署相關文件重命名 (編號 14-17)")
    print("-" * 80)
    for old_rel, new_rel in ch9_deployment_renames.items():
        old_path = base_dir / old_rel
        new_path = base_dir / new_rel
        
        if old_path.exists():
            try:
                # 讀取內容
                with open(old_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 更新章節編號 (9.4->9.14, 9.5->9.15, etc.)
                old_num = old_rel.split('-')[1]
                new_num = new_rel.split('-')[1]
                content = content.replace(f"## 9.{old_num} ", f"## 9.{new_num} ")
                
                # 寫入新文件
                with open(new_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                # 刪除舊文件
                old_path.unlink()
                
                print(f"✓ {old_rel} -> {new_rel}")
            except Exception as e:
                print(f"✗ 失敗: {old_rel} -> {e}")
        else:
            print(f"⚠ 文件不存在: {old_rel}")
    
    # 第二階段：統一繁體命名
    print("\n階段二：統一繁體中文命名")
    print("-" * 80)
    for old_rel, new_rel in unified_renames.items():
        old_path = base_dir / old_rel
        new_path = base_dir / new_rel
        
        if old_path.exists():
            try:
                shutil.move(str(old_path), str(new_path))
                print(f"✓ {old_rel} -> {new_rel}")
            except Exception as e:
                print(f"✗ 失敗: {old_rel} -> {e}")
        else:
            print(f"⚠ 文件不存在: {old_rel}")
    
    print("\n" + "=" * 80)
    print("重命名完成！")
    print("=" * 80)

if __name__ == "__main__":
    rename_files()

