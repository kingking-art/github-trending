#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GitHub Trending 爬虫（带中文翻译）
抓取 GitHub 热榜项目，输出 JSON 格式（含中文翻译）
"""

import sys
import os

# 设置标准输出为 UTF-8
sys.stdout.reconfigure(encoding='utf-8')

import requests
from bs4 import BeautifulSoup
import json
from deep_translator import GoogleTranslator

# 有效周期
valid_periods = {"daily", "weekly", "monthly"}

# 默认周期
period = "daily"

# 命令行参数
if len(sys.argv) > 1:
    arg = sys.argv[1].lower()
    if arg in valid_periods:
        period = arg

# 构建 URL
base_url = "https://github.com/trending"
if period == "daily":
    url = base_url
else:
    url = f"{base_url}?since={period}"

# 请求头
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def translate_text(text, max_length=200):
    """翻译文本到中文"""
    try:
        if not text or text == "No description":
            return "无描述"
        # 只翻译前 200 个字符（节省时间）
        text_to_translate = text[:max_length]
        result = GoogleTranslator(source='en', target='zh-CN').translate(text_to_translate)
        return result if result else text
    except Exception as e:
        print(f"翻译失败：{e}", file=sys.stderr)
        return text[:max_length] if len(text) > max_length else text

try:
    # 发送请求（如果不需要代理，去掉 proxies=proxies）
    response = requests.get(url, headers=headers, timeout=10)
    # response = requests.get(url, headers=headers, proxies=proxies, timeout=10)
    response.raise_for_status()
except requests.exceptions.RequestException as e:
    print(f"请求失败：{e}", file=sys.stderr)
    sys.exit(1)

# 解析 HTML
soup = BeautifulSoup(response.text, "html.parser")

# 查找所有项目
repos = soup.find_all("article", class_="Box-row")

data = []

for repo in repos:
    # 项目名称
    title = repo.h2.a.get_text(strip=True)
    
    # 项目链接
    link = "https://github.com" + repo.h2.a["href"]
    
    # 项目描述
    desc_tag = repo.find("p")
    description = desc_tag.get_text(strip=True) if desc_tag else "No description"
    
    # 总 Star 数
    star_tag = repo.find("a", href=lambda x: x and x.endswith("/stargazers"))
    total_stars = star_tag.get_text(strip=True) if star_tag else "0"
    
    # 周期内新增 Star（今日/本周/本月）
    period_stars = 0
    for span in repo.find_all("span"):
        text = span.get_text(strip=True)
        if "stars" in text and "today" in text:
            period_stars = int(text.replace("stars today", "").replace(",", "").strip())
            break
        elif "stars" in text and "week" in text:
            period_stars = int(text.split()[0].replace(",", ""))
            break
        elif "stars" in text and "month" in text:
            period_stars = int(text.split()[0].replace(",", ""))
            break
    
    # 翻译描述到中文
    description_zh = translate_text(description)
    if description_zh != description:
        print(f"已翻译：{title}", file=sys.stderr)
    
    repo_info = {
        "period": period,
        "name": title,
        "link": link,
        "description": description,
        "description_zh": description_zh,  # 中文翻译
        "total_stars": int(total_stars.replace(',', '').replace(' ', '')),
        "period_stars": period_stars
    }
    
    data.append(repo_info)

# 按周期内新增 Star 数降序排序
data.sort(key=lambda x: x['period_stars'], reverse=True)

# 输出 JSON
json_output = json.dumps(data, ensure_ascii=False, indent=2)
print(json_output)
