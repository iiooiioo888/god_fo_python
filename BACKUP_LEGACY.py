#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
from pathlib import Path
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(r'E:\Jerry_python\腳本平台\doc\鏡界')
BACKUP_ROOT = ROOT / '_backup_legacy'

# 需要處理的章節及其子節數量（ch9 只有 7 個）
CHAPTER_SIZES = {1: 9, 5: 9, 6: 9, 7: 9, 8: 9, 9: 7}

BANNER_TMPL = (
    
    "<!-- LEGACY FILE NOTICE -->\n"
    "> ⚠️ 此檔案為舊版備份，已被新檔取代： [{new_name}]({new_name})\\n"
    "> 備份時間：{ts}\\n"
    "\n---\n\n"
)

def find_new_file(ch_dir: Path, chapter: int, idx: int) -> str | None:
    # 透過 glob 尋找 chX-i-*.md 新檔名
    pattern = f'ch{chapter}-{idx}-*.md'
    matches = list(ch_dir.glob(pattern))
    if matches:
        # 取最先匹配的
        return matches[0].name
    return None


def backup_legacy_file(chapter: int, idx: int) -> bool:
    ch_dir = ROOT / f'ch{chapter}'
    src = ch_dir / f'ch{chapter}-{idx}.md'
    if not src.exists():
        return False

    # 找新檔名
    new_name = find_new_file(ch_dir, chapter, idx)
    if new_name is None:
        # 若找不到新檔，仍然備份但標記沒有新檔資訊
        new_name = f'ch{chapter}-{idx}-<未找到新檔名>.md'

    # 讀舊檔內容
    content = src.read_text(encoding='utf-8', errors='ignore')

    # 建立備份目錄 chX
    backup_dir = BACKUP_ROOT / f'ch{chapter}'
    backup_dir.mkdir(parents=True, exist_ok=True)

    # 寫入備份檔（加上醒目標記）
    backup_path = backup_dir / src.name
    ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    banner = BANNER_TMPL.format(new_name=new_name, ts=ts)
    backup_path.write_text(banner + content, encoding='utf-8')

    # 刪除原始舊檔
    src.unlink(missing_ok=True)
    print(f'✅ 備份並移除: {src} -> {backup_path}')
    return True


def main():
    print('開始備份舊格式檔案 (chX-Y.md) 到 _backup_legacy ...')
    total = 0
    for ch, size in CHAPTER_SIZES.items():
        for i in range(1, size + 1):
            try:
                if backup_legacy_file(ch, i):
                    total += 1
            except Exception as e:
                print(f'❌ 處理 ch{ch}-{i}.md 失敗: {e}')
    print(f'完成。共移動 {total} 個舊檔至 {BACKUP_ROOT}')

if __name__ == '__main__':
    main()
