#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GitHub Trending 文章配图生成器
自动生成所有需要的配图
"""

import sys
sys.stdout.reconfigure(encoding='utf-8')

from PIL import Image, ImageDraw, ImageFont
import os
import json

# 配置
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), 'images')
os.makedirs(OUTPUT_DIR, exist_ok=True)

print(f"[INFO] 图片输出目录：{OUTPUT_DIR}")

# 尝试加载中文字体
def get_font(size):
    """获取中文字体"""
    font_paths = [
        "C:/Windows/Fonts/msyh.ttc",  # 微软雅黑
        "C:/Windows/Fonts/simhei.ttf",  # 黑体
        "C:/Windows/Fonts/simkai.ttf",  # 楷体
    ]
    for path in font_paths:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except:
                continue
    # 默认字体
    return ImageFont.load_default()

# 1. 生成封面图
def generate_cover():
    print("\n[1/8] 生成封面图...")
    
    width, height = 900, 383
    img = Image.new('RGB', (width, height), color='#1a1a2e')
    draw = ImageDraw.Draw(img)
    
    # 绘制渐变背景
    for y in range(height):
        r = int(26 + (y / height) * 20)
        g = int(26 + (y / height) * 20)
        b = int(46 + (y / height) * 40)
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    
    # 添加装饰元素
    for i in range(50):
        x = (i * 37) % width
        y = (i * 23) % height
        r = 2 + (i % 3)
        draw.ellipse([x, y, x+r, y+r], fill=(100, 150, 255, 128))
    
    # 标题文字
    font_large = get_font(48)
    font_medium = get_font(32)
    
    title = "一键看懂 GitHub 热榜！"
    subtitle = "自动翻译 + 自动更新"
    
    # 计算文字位置（居中）
    title_bbox = draw.textbbox((0, 0), title, font=font_large)
    subtitle_bbox = draw.textbbox((0, 0), subtitle, font=font_medium)
    
    title_x = (width - (title_bbox[2] - title_bbox[0])) // 2
    subtitle_x = (width - (subtitle_bbox[2] - subtitle_bbox[0])) // 2
    title_y = height // 2 - 60
    subtitle_y = height // 2 + 20
    
    # 绘制标题
    draw.text((title_x, title_y), title, fill='white', font=font_large)
    draw.text((subtitle_x, subtitle_y), subtitle, fill='#64ffda', font=font_medium)
    
    # 保存
    output_path = os.path.join(OUTPUT_DIR, '00-cover.jpg')
    img.save(output_path, 'JPEG', quality=95)
    print(f"[OK] 封面图已保存：{output_path}")
    return output_path

# 2. 生成项目结构图
def generate_project_structure():
    print("\n[2/8] 生成项目结构图...")
    
    width, height = 800, 600
    img = Image.new('RGB', (width, height), color='#1e1e1e')
    draw = ImageDraw.Draw(img)
    
    font_title = get_font(28)
    font_code = get_font(20)
    
    # 标题
    draw.text((20, 20), "项目结构", fill='#64ffda', font=font_title)
    
    # 文件树
    tree_text = """
projects/github-trending/
├── github_trend.py        # Python 爬虫（带翻译）
├── update-trending.js     # Node.js 更新脚本
├── update.bat             # 一键运行（Windows）⭐
├── package.json           # Node.js 依赖
├── history/               # 历史数据存档
│   ├── github-trending-daily-2026-03-01T12-45-00.json
│   └── ...
└── README.md              # 使用文档

obsidian-vault/
├── GitHub Trending.md     # 展示页面
├── github-trending-daily-latest.json
├── github-trending-weekly-latest.json
└── github-trending-monthly-latest.json
"""
    
    y = 70
    for line in tree_text.strip().split('\n'):
        # 高亮 update.bat
        if 'update.bat' in line:
            draw.text((20, y), line, fill='#ffeb3b', font=font_code)
        elif line.startswith('obsidian'):
            draw.text((20, y), line, fill='#64ffda', font=font_code)
        else:
            draw.text((20, y), line, fill='#d4d4d4', font=font_code)
        y += 28
    
    # 保存
    output_path = os.path.join(OUTPUT_DIR, '01-project-structure.png')
    img.save(output_path, 'PNG')
    print(f"[OK] 项目结构图已保存：{output_path}")
    return output_path

# 3. 生成历史数据图
def generate_history_data():
    print("\n[3/8] 生成历史数据图...")
    
    width, height = 800, 400
    img = Image.new('RGB', (width, height), color='#1e1e1e')
    draw = ImageDraw.Draw(img)
    
    font_title = get_font(28)
    font_code = get_font(18)
    
    # 标题
    draw.text((20, 20), "历史数据存档（history/）", fill='#64ffda', font=font_title)
    
    # 文件列表
    files = [
        "github-trending-daily-2026-03-01T11-32-16.json",
        "github-trending-daily-2026-03-01T12-45-00.json",
        "github-trending-weekly-2026-03-01T11-32-16.json",
        "github-trending-weekly-2026-03-01T12-45-00.json",
        "github-trending-monthly-2026-03-01T11-32-16.json",
        "github-trending-monthly-2026-03-01T12-45-00.json",
    ]
    
    y = 70
    for i, file in enumerate(files):
        # 提取类型
        if 'daily' in file:
            color = '#ff6b6b'
            icon = '📅'
        elif 'weekly' in file:
            color = '#4ecdc4'
            icon = '📆'
        elif 'monthly' in file:
            color = '#ffe66d'
            icon = '📊'
        else:
            color = '#d4d4d4'
            icon = '📄'
        
        draw.text((20, y), f"{icon} {file}", fill=color, font=font_code)
        y += 35
    
    # 说明文字
    draw.text((20, height - 40), "💡 每次更新自动保存，带时间戳，永不覆盖", fill='#888', font=get_font(16))
    
    # 保存
    output_path = os.path.join(OUTPUT_DIR, '02-history-data.png')
    img.save(output_path, 'PNG')
    print(f"[OK] 历史数据图已保存：{output_path}")
    return output_path

# 4. 生成代码卡片 - 爬虫核心
def generate_code_crawler():
    print("\n[4/8] 生成代码卡片：爬虫核心...")
    
    code = """# 抓取 GitHub Trending
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")
repos = soup.find_all("article", class_="Box-row")

for repo in repos:
    title = repo.h2.a.get_text(strip=True)
    link = "https://github.com" + repo.h2.a["href"]
    
    # 翻译描述
    description_zh = translate_text(description)
    
    data.append({
        "name": title,
        "link": link,
        "description_zh": description_zh,
        "total_stars": stars,
        "period_stars": today_stars
    })

# 按 Star 数降序排序
data.sort(key=lambda x: x['period_stars'], reverse=True)"""
    
    generate_code_image(code, '03-code-crawler.png', 'Python')
    print(f"[OK] 爬虫代码卡片已保存")

# 5. 生成代码卡片 - 翻译函数
def generate_code_translator():
    print("\n[5/8] 生成代码卡片：翻译函数...")
    
    code = """from deep_translator import GoogleTranslator

def translate_text(text, max_length=200):
    \"\"\"翻译文本到中文\"\"\"
    try:
        if not text or text == "No description":
            return "无描述"
        result = GoogleTranslator(
            source='en', 
            target='zh-CN'
        ).translate(text[:max_length])
        return result if result else text
    except Exception as e:
        print(f"翻译失败：{e}")
        return text"""
    
    generate_code_image(code, '04-code-translator.png', 'Python')
    print(f"[OK] 翻译代码卡片已保存")

# 6. 生成代码卡片 - Obsidian 展示
def generate_code_dataview():
    print("\n[6/8] 生成代码卡片：Obsidian 展示...")
    
    code = """const file = app.vault.getFileByPath(
    "github-trending-daily-latest.json");
const content = await app.vault.read(file);
const data = JSON.parse(content);

const rows = data.map((row, index) => [
  `**${index + 1}**. [${row.name}](${row.link})`,
  row.description_zh || "无描述",
  `⭐ ${row.period_stars}`,
  `📊 ${row.total_stars}`
]);

dv.table(["项目", "简介", "今日⭐", "总计"], rows);"""
    
    generate_code_image(code, '05-code-dataview.png', 'JavaScript')
    print(f"[OK] Dataview 代码卡片已保存")

# 通用代码图片生成
def generate_code_image(code, filename, language):
    """生成代码图片"""
    width, height = 800, 500
    img = Image.new('RGB', (width, height), color='#282c34')
    draw = ImageDraw.Draw(img)
    
    font_code = get_font(16)
    font_lang = get_font(14)
    
    # 绘制语言标签
    draw.text((20, 15), language, fill='#61afef', font=font_lang)
    
    # 绘制代码
    y = 50
    for i, line in enumerate(code.split('\n'), 1):
        # 行号
        draw.text((10, y), f"{i:3}", fill='#636d83', font=font_code)
        # 代码内容
        draw.text((50, y), line, fill='#abb2bf', font=font_code)
        y += 24
    
    # 保存
    output_path = os.path.join(OUTPUT_DIR, filename)
    img.save(output_path, 'PNG')

# 7. 生成 Obsidian 效果 mockup
def generate_obsidian_mockup():
    print("\n[7/8] 生成 Obsidian 效果 mockup...")
    
    width, height = 900, 600
    img = Image.new('RGB', (width, height), color='#1e1e1e')
    draw = ImageDraw.Draw(img)
    
    font_title = get_font(32)
    font_table = get_font(18)
    font_note = get_font(14)
    
    # 标题
    draw.text((30, 30), "# GitHub Trending 热榜", fill='#d4d4d4', font=font_title)
    draw.text((30, 80), "> 💡 双击 update.bat 更新数据", fill='#888', font=font_note)
    
    # 表格标题
    y = 140
    draw.text((30, y), "## 📅 今日热榜", fill='#64ffda', font=font_title)
    
    # 表格头
    y += 50
    headers = ["🏆 项目", "📝 简介（中文）", "🔥 今日", "⭐ 总计"]
    x_positions = [30, 300, 550, 650]
    
    draw.rectangle([(20, y-10), (width-20, y+30)], fill='#2d2d2d')
    for i, header in enumerate(headers):
        draw.text((x_positions[i], y+5), header, fill='#64ffda', font=font_table)
    
    # 表格内容（示例数据）
    demo_data = [
        ("1. wifi-densepose", "将商用 WiFi 信号转化为实时人体姿势估计...", "⭐ 2152", "14,958"),
        ("2. OpenSandbox", "面向 AI 应用的通用沙箱平台...", "⭐ 1186", "2,875"),
        ("3. markitdown", "用于将文件和 Office 文档转换为 Markdown...", "⭐ 798", "88,694"),
        ("4. ruflo", "Claude 领先的代理编排平台...", "⭐ 766", "16,918"),
        ("5. airi", "自托管的 Grok Companion...", "⭐ 738", "19,685"),
    ]
    
    for i, (name, desc, today, total) in enumerate(demo_data):
        y += 35
        bg_color = '#252526' if i % 2 == 0 else '#1e1e1e'
        draw.rectangle([(20, y-5), (width-20, y+30)], fill=bg_color)
        
        draw.text((30, y+5), name, fill='#61afef', font=font_table)
        draw.text((300, y+5), desc[:35] + "...", fill='#abb2bf', font=font_table)
        draw.text((550, y+5), today, fill='#ffeb3b', font=font_table)
        draw.text((650, y+5), total, fill='#98c379', font=font_table)
    
    # 底部说明
    y += 60
    draw.text((30, y), "💡 一次运行，同时获取最近 1 天/1 周/1 月的数据", fill='#888', font=font_note)
    
    # 保存
    output_path = os.path.join(OUTPUT_DIR, '06-obsidian-mockup.png')
    img.save(output_path, 'PNG')
    print(f"[OK] Obsidian 效果 mockup 已保存：{output_path}")
    return output_path

# 8. 生成更新流程图
def generate_update_process():
    print("\n[8/8] 生成更新流程图...")
    
    width, height = 800, 400
    img = Image.new('RGB', (width, height), color='#1e1e1e')
    draw = ImageDraw.Draw(img)
    
    font_title = get_font(28)
    font_text = get_font(20)
    
    # 标题
    draw.text((20, 20), "一键更新流程", fill='#64ffda', font=font_title)
    
    # 流程图
    steps = [
        ("1", "双击 update.bat", "#61afef"),
        ("2", "执行 Python 爬虫", "#c678dd"),
        ("3", "抓取 GitHub Trending", "#e5c07b"),
        ("4", "自动翻译描述", "#98c379"),
        ("5", "保存历史数据", "#56b6c2"),
        ("6", "更新 Obsidian", "#64ffda"),
        ("✅", "完成！", "#ff6b6b"),
    ]
    
    y = 80
    for i, (num, text, color) in enumerate(steps):
        # 箭头
        if i > 0:
            draw.line([(100, y-15), (100, y-5)], fill='#888', width=2)
            draw.polygon([(95, y-5), (105, y-5), (100, y+5)], fill='#888')
        
        # 步骤编号
        draw.ellipse([(30, y-15), (60, y+15)], fill=color)
        draw.text((37, y-10), num, fill='#1e1e1e', font=font_text)
        
        # 步骤说明
        draw.text((80, y-5), text, fill='#d4d4d4', font=font_text)
        
        y += 50
    
    # 保存
    output_path = os.path.join(OUTPUT_DIR, '07-update-process.png')
    img.save(output_path, 'PNG')
    print(f"[OK] 更新流程图已保存：{output_path}")
    return output_path

# 主函数
def main():
    print("=" * 60)
    print("GitHub Trending 文章配图生成器")
    print("=" * 60)
    
    # 生成所有图片
    generate_cover()
    generate_project_structure()
    generate_history_data()
    generate_code_crawler()
    generate_code_translator()
    generate_code_dataview()
    generate_obsidian_mockup()
    generate_update_process()
    
    print("\n" + "=" * 60)
    print("[OK] 所有配图生成完成！")
    print("=" * 60)
    print(f"\n输出目录：{OUTPUT_DIR}")
    print("\n生成的文件：")
    for f in sorted(os.listdir(OUTPUT_DIR)):
        print(f"  - {f}")
    print("\n提示：图片已保存到 images/ 文件夹，可直接用于文章")

if __name__ == '__main__':
    main()
