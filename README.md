# GitHub Trending 自动情报系统

> 💡 一键看懂 GitHub 热榜！自动翻译 + 自动更新 | 日榜/周榜/月榜一次搞定

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![GitHub stars](https://img.shields.io/badge/GitHub-Trending-green.svg)](https://github.com/trending)

---

## 🎯 项目简介

**GitHub Trending 自动情报系统** 是一个自动化工具，可以：

- 🕵️ **自动抓取** GitHub Trending（日榜/周榜/月榜）
- 🇨🇳 **自动翻译** 项目描述成中文
- 📊 **自动更新** Obsidian 笔记
- 🎨 **自动展示** 成漂亮的表格

**一次运行，同时获取最近 1 天/1 周/1 月的热榜数据！**

---

## ✨ 核心特性

- ✅ **简单**：双击一个按钮就能更新
- ✅ **稳定**：不用折腾复杂的配置
- ✅ **好看**：在 Obsidian 里展示效果漂亮
- ✅ **中文**：自动翻译项目描述，直接看中文
- ✅ **历史存档**：每次更新自动保存历史数据
- ✅ **开源免费**：MIT 许可证，完全免费

---

## 🚀 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/YOUR_USERNAME/github-trending.git
cd github-trending
```

### 2. 安装依赖

```bash
# Python 依赖
pip install -r requirements.txt

# Node.js 依赖
npm install
```

### 3. 运行

```bash
# Windows 用户
update.bat

# 或者手动运行
node update-trending.js
```

### 4. 查看结果

打开 `obsidian-vault/GitHub Trending.md` 查看热榜数据。

---

## 📦 项目结构

```
github-trending/
├── github_trend.py        # Python 爬虫（带翻译）
├── update-trending.js     # Node.js 更新脚本
├── update.bat             # 一键运行（Windows）
├── package.json           # Node.js 依赖
├── requirements.txt       # Python 依赖
├── history/               # 历史数据存档
├── obsidian-vault/        # Obsidian 展示页面
└── README.md              # 本文档
```

---

## 💡 使用场景

### 1. 每日技术趋势追踪

自动获取 GitHub 热榜，了解最新技术动态。

### 2. 技术情报分析

分析热榜项目所属领域，生成趋势报告。

### 3. 自动化情报周报

系统支持每日/每周/每月自动更新，可生成情报周报。

---

## 📊 效果展示

### Obsidian 展示效果

![Obsidian 效果](images/06-obsidian-mockup.png)

### 更新流程

![更新流程](images/07-update-process.png)

### 历史数据存档

![历史数据](images/02-history-data.png)

---

## 🔧 配置说明

### Python 环境

- Python 3.8+
- 依赖包：`requests`, `beautifulsoup4`, `deep-translator`

### Node.js 环境

- Node.js 14+
- 依赖包：`js-yaml`

### Obsidian 插件

- **Dataview** - 用于渲染表格（必须）
- 启用 `Enable JavaScript Queries`
- 启用 `Enable inline JavaScript queries`

---

## 📝 更新日志

### v1.0.0 (2026-03-01)

- ✅ 初始版本发布
- ✅ 支持日榜/周榜/月榜抓取
- ✅ 自动翻译中文
- ✅ Obsidian 集成
- ✅ 历史数据存档

---

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

1. Fork 本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

---

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

---

## 🙏 致谢

感谢以下开源项目：

- [requests](https://github.com/psf/requests) - HTTP 库
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) - HTML 解析
- [deep-translator](https://github.com/nidhaloff/deep-translator) - 翻译工具
- [Dataview](https://github.com/blacksmithgu/obsidian-dataview) - Obsidian 插件

---

## 📬 联系方式

- **项目地址**: https://github.com/YOUR_USERNAME/github-trending
- **问题反馈**: https://github.com/YOUR_USERNAME/github-trending/issues

---

*如果这个项目对你有帮助，欢迎 ⭐ Star 支持一下！*
