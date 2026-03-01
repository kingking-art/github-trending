#!/usr/bin/env node
/**
 * GitHub Trending 自动更新脚本
 * 调用 Python 爬虫并更新 Obsidian frontmatter
 */

const { exec } = require('child_process');
const fs = require('fs');
const path = require('path');

// 配置
const PYTHON_PATH = 'python';
const SCRIPT_PATH = path.join(__dirname, 'github_trend.py');
const HISTORY_DIR = path.join(__dirname, 'history');
const OBSIDIAN_DIR = path.resolve(__dirname, '..', '..', 'obsidian-vault');

// 确保目录存在
if (!fs.existsSync(HISTORY_DIR)) {
  fs.mkdirSync(HISTORY_DIR, { recursive: true });
}
if (!fs.existsSync(OBSIDIAN_DIR)) {
  fs.mkdirSync(OBSIDIAN_DIR, { recursive: true });
}

// 执行命令
function execAsync(cmd) {
  return new Promise((resolve, reject) => {
    exec(cmd, { encoding: 'utf8' }, (err, stdout, stderr) => {
      if (err) {
        reject(err);
        return;
      }
      resolve(stdout);
    });
  });
}

// 更新热榜数据
async function updateTrending(period) {
  console.log(`正在更新${period}热榜...`);
  
  try {
    // 执行 Python 脚本
    const stdout = await execAsync(`${PYTHON_PATH} "${SCRIPT_PATH}" ${period}`);
    const data = JSON.parse(stdout);
    
    // 保存历史数据（带时间戳）
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-').slice(0, -5);
    const historyFile = path.join(HISTORY_DIR, `github-trending-${period}-${timestamp}.json`);
    fs.writeFileSync(historyFile, JSON.stringify(data, null, 2), 'utf8');
    console.log(`📁 历史数据已保存：${path.basename(historyFile)}`);
    
    // 复制最新数据到 Obsidian 目录（供 Datacore 读取）
    const latestFile = path.join(OBSIDIAN_DIR, `github-trending-${period}-latest.json`);
    fs.writeFileSync(latestFile, JSON.stringify(data, null, 2), 'utf8');
    console.log(`📄 最新数据已复制：github-trending-${period}-latest.json`);
    console.log(`✅ ${period}热榜已更新，共 ${data.length} 个项目`);
    
  } catch (error) {
    console.error(`❌ 更新失败：${error.message}`);
    process.exit(1);
  }
}

// 主函数
async function main() {
  const periods = process.argv.slice(2);
  
  if (periods.length === 0) {
    // 默认更新所有周期
    await updateTrending('daily');
    await updateTrending('weekly');
    await updateTrending('monthly');
  } else {
    // 更新指定周期
    for (const period of periods) {
      await updateTrending(period);
    }
  }
  
  console.log('🎉 全部更新完成！');
}

main();
