# 📸 文章配图清单

## ✅ 已完成

| 图片 | 状态 | 说明 |
|------|------|------|
| 文章初稿 | ✅ | `article.md` |
| 配图说明 | ✅ | `article-images.md` |
| 微信布局分析 | ✅ | 西蒙斯完成报告 |

---

## 📷 需要准备的图片

### 1. 封面图
- **尺寸：** 900x383px
- **工具：** Canva / 稿定设计
- **文案：** "GitHub 热榜自动情报系统" + "3 小时从 0 到 1 复现"
- **风格：** 科技感、蓝紫色调

### 2. Obsidian 效果截图
- **内容：** GitHub Trending.md 展示页面
- **要展示：** 热榜表格、中文简介、Star 数
- **方法：** Obsidian 打开文件 → 截图

### 3. 项目结构截图  
- **内容：** 文件资源管理器
- **路径：** `projects/github-trending/`
- **标注：** 红框标出关键文件

### 4. 更新流程截图
- **内容：** 双击 update.bat 的运行结果
- **形式：** 命令行截图或 GIF

### 5. 历史数据截图
- **内容：** history 文件夹
- **要展示：** 带时间戳的 JSON 文件列表

---

## 🎨 代码卡片（用 Carbon 生成）

### 代码 1：爬虫核心
```python
# 抓取 GitHub Trending
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")
repos = soup.find_all("article", class_="Box-row")

for repo in repos:
    title = repo.h2.a.get_text(strip=True)
    link = "https://github.com" + repo.h2.a["href"]
    stars = repo.find("a", href="/stargazers").get_text()
```

### 代码 2：翻译函数
```python
from deep_translator import GoogleTranslator

def translate_text(text, max_length=200):
    try:
        if not text or text == "No description":
            return "无描述"
        result = GoogleTranslator(source='en', target='zh-CN').translate(text[:max_length])
        return result if result else text
    except Exception as e:
        print(f"翻译失败：{e}")
        return text
```

### 代码 3：Obsidian 展示
```dataviewjs
const file = app.vault.getFileByPath("github-trending-daily-latest.json");
const content = await app.vault.read(file);
const data = JSON.parse(content);

const rows = data.map(row => [
  `[${row.name}](${row.link})`,
  row.description_zh,
  `⭐ ${row.period_stars}`,
  `📊 ${row.total_stars}`
]);

dv.table(["项目", "简介", "今日⭐", "总计"], rows);
```

---

## 📋 配图位置（根据微信文章分析）

| 位置 | 字数 | 配图类型 |
|------|------|---------|
| 标题后 | 0 | 封面图 |
| "写在前面"后 | ~300 | 痛点场景图（可选） |
| "核心代码"后 | ~1500 | 代码卡片 + 效果截图 |
| "最终效果"后 | ~2500 | Obsidian 展示截图 |
| 文末 | ~3500 | 作者信息（自动生成） |

**总计：** 5-6 张图（不含代码卡片）

---

## 🛠️ 截图工具

- **Windows 自带：** Win + Shift + S
- **Snipaste：** 免费、可标注
- **Carbon：** 代码卡片美化 (carbon.now.sh)

---

*配图清单 | 2026-03-01*
