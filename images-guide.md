# 📸 配图准备指南

## ✅ 需要准备的图片（5 张）

### 1. 封面图
**工具：** Canva (canva.com) 或 稿定设计

**尺寸：** 900x383px（微信封面比例 2.35:1）

**文案：**
```
主标题：一键看懂 GitHub 热榜！
副标题：自动翻译 + 自动更新
```

**风格建议：**
- 科技感、简洁
- 蓝紫色调
- 可以加 GitHub Logo 元素

**参考：** Canva 搜索"科技封面"有很多模板

---

### 2. Obsidian 效果截图 ⭐ 重要
**内容：** GitHub Trending.md 展示页面

**步骤：**
1. 打开 Obsidian
2. 打开 `GitHub Trending.md` 文件
3. 按 `Ctrl+P` → `Dataview: Force refresh all views and blocks`
4. 确保表格显示正常
5. 按 `Win+Shift+S` 截图

**要展示：**
- ✅ 热榜表格（带排名）
- ✅ 中文简介
- ✅ Star 数显示
- ✅ emoji 图标

**截图范围：** 整个表格 + 部分标题

---

### 3. 项目结构截图
**内容：** 文件资源管理器

**步骤：**
1. 打开 `C:\Users\Administrator\.openclaw\workspace\projects\github-trending`
2. 显示完整文件树
3. 按 `Win+Shift+S` 截图

**要展示：**
```
projects/github-trending/
├── github_trend.py
├── update-trending.js
├── update.bat
├── package.json
├── history/
└── README.md
```

**标注建议：** 用红框标出 `update.bat`（一键运行）

---

### 4. 更新流程截图
**内容：** 双击 update.bat 的运行结果

**步骤：**
1. 打开命令提示符
2. 运行：`cd projects/github-trending`
3. 运行：`node update-trending.js`
4. 截图运行输出

**要展示：**
```
正在更新 daily 热榜...
📁 历史数据已保存：github-trending-daily-2026-03-01T12-45-00.json
✅ daily 热榜已更新，共 13 个项目

正在更新 weekly 热榜...
✅ weekly 热榜已更新，共 13 个项目

正在更新 monthly 热榜...
✅ monthly 热榜已更新，共 18 个项目

🎉 全部更新完成！
```

**形式：** 静态截图即可（GIF 太麻烦）

---

### 5. 历史数据截图
**内容：** history 文件夹的文件列表

**步骤：**
1. 打开 `projects/github-trending/history`
2. 显示所有 JSON 文件
3. 按 `Win+Shift+S` 截图

**要展示：**
```
github-trending-daily-2026-03-01T11-32-16.json
github-trending-daily-2026-03-01T12-45-00.json
github-trending-weekly-2026-03-01T11-32-16.json
github-trending-weekly-2026-03-01T12-45-00.json
github-trending-monthly-2026-03-01T11-32-16.json
github-trending-monthly-2026-03-01T12-45-00.json
```

**说明：** 带时间戳的文件名，展示历史存档

---

## 🎨 代码卡片（3 张，用 Carbon）

**网站：** https://carbon.now.sh

### 代码 1：爬虫核心

**代码内容：**
```python
# 抓取 GitHub Trending
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")
repos = soup.find_all("article", class_="Box-row")

for repo in repos:
    title = repo.h2.a.get_text(strip=True)
    link = "https://github.com" + repo.h2.a["href"]
    stars = repo.find("a", href="/stargazers").get_text()
    
    # 翻译描述
    description_zh = translate_text(description)
    
    data.append({
        "name": title,
        "link": link,
        "description": description,
        "description_zh": description_zh,
        "total_stars": stars,
        "period_stars": today_stars
    })

# 按 Star 数降序排序
data.sort(key=lambda x: x['period_stars'], reverse=True)
```

**Carbon 设置：**
- 主题：Seti
- 语言：Python
- 背景：模糊效果
- 导出：PNG（1x 即可）

---

### 代码 2：翻译函数

**代码内容：**
```python
from deep_translator import GoogleTranslator

def translate_text(text, max_length=200):
    """翻译文本到中文"""
    try:
        if not text or text == "No description":
            return "无描述"
        text_to_translate = text[:max_length]
        result = GoogleTranslator(source='en', target='zh-CN').translate(text_to_translate)
        return result if result else text
    except Exception as e:
        print(f"翻译失败：{e}")
        return text
```

**Carbon 设置：** 同上

---

### 代码 3：Obsidian 展示

**代码内容：**
```dataviewjs
const file = app.vault.getFileByPath("github-trending-daily-latest.json");
const content = await app.vault.read(file);
const data = JSON.parse(content);

const rows = data.map((row, index) => [
  `**${index + 1}**. [${row.name}](${row.link})`,
  row.description_zh || "无描述",
  `⭐ ${row.period_stars}`,
  `📊 ${row.total_stars.toLocaleString()}`
]);

dv.table(["🏆 项目", "📝 简介（中文）", "🔥 今日", "⭐ 总计"], rows);
```

**Carbon 设置：**
- 主题：Seti
- 语言：JavaScript
- 其他同上

---

## 📷 截图工具推荐

### Windows 自带
- **Win + Shift + S** - 区域截图（推荐）
- **Win + PrtScn** - 全屏截图

### 专业工具
- **Snipaste** - 免费、可标注（推荐）
- **ShareX** - 开源、功能强大

---

## 📁 图片命名规范

```
cover.jpg                        # 封面图
01-obsidian-effect.png           # Obsidian 效果
02-project-structure.png         # 项目结构
03-update-process.png            # 更新流程
04-history-data.png              # 历史数据
05-code-crawler.png              # 代码卡片 1
06-code-translator.png           # 代码卡片 2
07-code-dataview.png             # 代码卡片 3
```

---

## ✅ 配图位置（插入到文章中）

| 图片 | 插入位置 |
|------|---------|
| 封面图 | 文章开头，标题下方 |
| Obsidian 效果 | "最终效果"章节 |
| 项目结构 | "项目结构"章节后 |
| 更新流程 | "最终效果 - 更新流程" |
| 历史数据 | "最终效果 - 历史数据" |
| 代码卡片 1-3 | 对应代码块下方 |

---

*配图指南 | 2026-03-01*
