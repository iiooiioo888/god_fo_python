#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

base_path = Path(r'E:\Jerry_python\腳本平台\doc\鏡界')

# 統計新文件名的文件
new_files = list(base_path.glob('ch*/ch*-[0-9]-*.md'))
old_files = list(base_path.glob('ch*/ch*-[0-9].md'))

print(f"✅ 新文件名（已重命名）: {len(new_files)} 個")
print(f"⚠️ 舊文件名（未重命名）: {len(old_files)} 個")
print(f"\n📊 章節詳情：")

for ch in range(1, 10):
    ch_dir = base_path / f'ch{ch}'
    if ch_dir.exists():
        new = len(list(ch_dir.glob('ch*-[0-9]-*.md')))
        old = len(list(ch_dir.glob('ch*-[0-9].md')))
        status = "✅" if old == 0 else "⚠️"
        print(f"  {status} Ch{ch}: {new} 個新文件, {old} 個舊文件")

print(f"\n{'='*50}")
print(f"✅ 總計: {len(new_files)} 個文件已成功重命名")
print(f"{'='*50}

if len(old_files) == 0:
    print("\n🎉 所有文件已完成重命名！項目完成度: 100%")
else:
    print(f"\n⚠️ 還有 {len(old_files)} 個文件待重命名")
