#!/usr/bin/env python3
"""簡單測試beautifulsoup4導入"""

from bs4 import BeautifulSoup

print("✅ BeautifulSoup導入成功")

# 測試基本功能
html = "<html><body><h1>Hello</h1></body></html>"
soup = BeautifulSoup(html, 'lxml')
title = soup.h1.text
print(f"✅ HTML解析成功: {title}")
