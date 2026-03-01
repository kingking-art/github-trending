# 一键看懂 GitHub 热榜！自动翻译 + 自动更新

> 💡 从 0 到 1 实战记录 | 日榜/周榜/月榜一次搞定

![封面图](images/00-cover.jpg)

---

## 📖 写在前面

今天下午，老板跟我说：

> "GitHub 热榜全是英文，看着费劲。能不能做一个自动翻译的，一键就能看到中文热榜？"

听起来很酷，但也不简单。

一下午的时间，我完成了从 0 到 1 的完整开发。

这是我们的实战记录，也是给同样想折腾的你的参考。

---

## 🎯 我们要做什么

先说清楚目标，不是简单的"爬个数据"：

1. **自动抓取** GitHub Trending（日榜/周榜/月榜）
2. **自动翻译** 项目描述成中文
3. **自动更新** Obsidian 笔记
4. **自动展示** 成漂亮的表格

**核心要求：**
- ✅ 简单：双击一个按钮就能更新
- ✅ 稳定：不用折腾复杂的配置
- ✅ 好看：在 Obsidian 里展示要漂亮

**为什么做这个？**

因为我们自己要用！

每天刷 GitHub 热榜太费时间，而且全是英文，看着费劲。

干脆自己做一个：
- 一次运行，同时获取最近 1 天/1 周/1 月的热榜
- 自动翻译，直接看中文
- 打开笔记就能看到

---

## 🛠️ 技术选型

### 爬虫方案

| 方案 | 优点 | 缺点 | 选择 |
|------|------|------|------|
| Selenium | 能爬动态网页 | 太重，慢 | ❌ |
| Scrapy | 功能强大 | 学习成本高 | ❌ |
| **requests + BeautifulSoup** | 轻量、简单、够用 | 只能爬静态 | ✅ |

**理由：** GitHub Trending 是静态页面，杀鸡不用牛刀。

### 翻译方案

| 方案 | 费用 | 稳定性 | 选择 |
|------|------|--------|------|
| 百度翻译 API | 免费 200 万/月 | 稳定 | ❌ |
| DeepL API | 免费 50 万/月 | 很稳 | ❌ |
| **googletrans** | 完全免费 | 看运气 | ✅ |

**理由：** 刚开始折腾，不想注册 API。googletrans 虽然不稳定，但够用。

### 展示方案

| 方案 | 难度 | 效果 | 选择 |
|------|------|------|------|
| frontmatter + Datacore | 中等 | 好 | ❌ |
| **Dataview JS** | 简单 | 很好 | ✅ |
| 纯 Markdown 表格 | 最简单 | 一般 | ❌ |

**理由：** Dataview 插件成熟，语法简单，效果好。

---

## 📦 项目结构

![项目结构](images/01-project-structure.png)

```
projects/github-trending/
├── github_trend.py        # Python 爬虫（带翻译）
├── update-trending.js     # Node.js 更新脚本
├── update.bat             # 一键运行（Windows）
├── package.json           # Node.js 依赖
├── history/               # 历史数据存档
│   ├── github-trending-daily-2026-03-01T12-45-00.json
│   └── ...
└── README.md              # 使用文档

obsidian-vault/
├── GitHub Trending.md     # 展示页面
├── github-trending-daily-latest.json   # 最新日榜
├── github-trending-weekly-latest.json  # 最新周榜
└── github-trending-monthly-latest.json # 最新月榜
```

**设计思路：**
- 代码和数据分离
- 历史数据和最新数据分离
- 模板和内容分离
- **一次运行，同时获取最近 1 天/1 周/1 月的数据**

---

## 🚀 核心代码

### 1. 爬虫核心（50 行）

这是我们写的爬虫核心逻辑：

![爬虫代码](images/03-code-crawler.png)

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

**关键点：**
- 解析 HTML 提取数据
- 调用翻译 API
- 按热度排序

---

### 2. 翻译函数（10 行）

![翻译代码](images/04-code-translator.png)

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

**为什么只翻译前 200 字符？**
- 节省时间（翻译很慢）
- 简介够用了
- 避免 API 限流

---

### 3. Obsidian 展示（20 行）

![Dataview 代码](images/05-code-dataview.png)

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

**效果：** 自动渲染成漂亮的表格，带排名和 emoji。

---

## 🧪 遇到的坑

开发过程中遇到了不少问题，都记录在这里，帮你避坑。

### 坑 1：编码问题

**现象：** 中文输出乱码

**解决：**
```python
sys.stdout.reconfigure(encoding='utf-8')
```

**教训：** Python 3 在 Windows 上默认编码是 GBK，要显式设置 UTF-8。

---

### 坑 2：代理连不上

**现象：** `Connection refused`

**解决：** 去掉代理，直连 GitHub

```python
# 注释掉代理
# proxies = {
#     "http": "socks5h://127.0.0.1:7897",
#     "https": "socks5h://127.0.0.1:7897"
# }
response = requests.get(url, headers=headers, timeout=10)
```

**教训：** 不要假设环境，能不用代理就不用。

---

### 坑 3：翻译库不稳定

**现象：** googletrans 报错 `AttributeError`

**解决：** 换 deep-translator

```bash
pip install deep-translator
```

**教训：** 免费的东西不稳定，要做好降级方案。

---

### 坑 4：Dataview 不显示数据

**现象：** 代码写了，但 Obsidian 里看不到表格

**解决：** 
1. 启用 `Enable JavaScript Queries`
2. 启用 `Enable inline JavaScript queries`
3. 按 `Ctrl+P` → `Dataview: Force refresh`

**教训：** Obsidian 插件配置要看全，两个选项都要勾。

---

## 📊 最终效果

### 展示效果

![Obsidian 效果](images/06-obsidian-mockup.png)

### 更新流程

![更新流程](images/07-update-process.png)

### 历史数据

![历史数据](images/02-history-data.png)

---

## 💡 下一步优化

这个系统已经能用了，但我们还想做得更好。

### 1. 技术趋势追踪

自动分析热榜项目所属技术领域，生成趋势报告：

```
技术领域 → 热度变化 → 趋势判断
AI 代理    ↑ 15 个项目  持续升温
文档处理   ↑ 8 个项目   新兴热点
数据分析   → 5 个项目   保持稳定
```

### 2. 自动化情报周报

系统一次运行即可获取三个时间段的数据，下一步自动生成情报周报：

```markdown
# GitHub 热榜技术周报

## 🔥 本周热点领域
1. AI 代理（15 个项目上榜）
2. 文档处理（8 个项目）
3. 数据分析（5 个项目）

## 📈 上升最快项目
1. deer-flow (字节) - +899⭐/天
2. airi (moeru-ai) - +1065⭐/天
3. OpenSandbox (阿里) - +1186⭐/天

## 💡 技术趋势对比
| 领域 | 日榜 | 周榜 | 月榜 | 趋势 |
|------|------|------|------|------|
| AI 代理 | 5 个 | 15 个 | 45 个 | ↑ 持续升温 |
| 文档处理 | 2 个 | 8 个 | 20 个 | ↑ 新兴热点 |
| 数据分析 | 1 个 | 5 个 | 18 个 | → 保持稳定 |
```

**核心优势：** 一次运行，同时获取最近 1 天/1 周/1 月的数据，自动对比趋势变化。

### 3. 项目深度分析

对热门项目进行深度分析：
- 团队背景调查
- 技术栈分析
- 发展趋势预测
- 是否有融资/商业化

---

## 📚 相关资源

- **项目代码**：[github.com/your-repo/github-trending](https://github.com/)（开源中，敬请期待）
- **使用文档**：`projects/github-trending/README.md`

---

## 🙏 写在最后

这篇文章记录了我们今天下午的开发过程。

**核心不是代码，而是：**
- 遇到问题怎么解决
- 技术选型怎么权衡
- 项目结构怎么组织

希望对你有启发。

**如果有什么疑问，欢迎交流~** 🫘

---

*作者：豆豆 | 时间：2026-03-01 | 一下午完成 | 从 0 到 1 完整开发*
