# React 前端部署和开发指南

## 📋 前置要求

- Node.js 16+ （推荐 18+）
- npm 或 yarn
- Python 3.10+（用于后端 API）

## 🚀 快速开始

### 1. 安装依赖

```bash
cd frontend
npm install
```

### 2. 环境配置

复制 `.env.example` 为 `.env` 并填入配置：

```bash
cp .env.example .env
```

编辑 `.env` 文件：

```env
REACT_APP_API_URL=http://localhost:8000/api
REACT_APP_OPENAI_API_KEY=sk-your-openai-api-key
```

### 3. 启动开发服务器

```bash
npm start
```

应用将在 `http://localhost:3000` 打开

## 🛠️ 开发

### 项目结构

```
frontend/
├── public/
│   └── index.html
├── src/
│   ├── components/          # React 组件
│   │   ├── SequenceAnalysis.jsx
│   │   ├── MutationDesign.jsx
│   │   ├── ExperimentData.jsx
│   │   ├── DataAnalysis.jsx
│   │   └── LiteratureSearch.jsx
│   ├── services/
│   │   └── api.js          # API 服务层 + OpenAI 集成
│   ├── App.jsx             # 主应用
│   ├── App.css             # 全局样式
│   └── index.jsx           # 入口文件
├── package.json
└── .env.example
```

### 可用命令

```bash
# 开发模式
npm start

# 生产构建
npm run build

# 运行测试
npm test

# 代码分析
npm run eject
```

## 🔌 API 集成

### 后端 API 地址

所有请求都会发送到 `REACT_APP_API_URL` 配置的地址。默认为 `http://localhost:8000/api`

### 完整的 OpenAI 集成

在 `src/services/api.js` 中实现了完整的 OpenAI GPT-4 集成：

```javascript
// 序列分析
const analysis = await openaiService.analyzeSequence(sequence);

// 突变体实验计划生成
const plan = await openaiService.generateMutationPlan(mutationData);

// 论文摘要生成
const summary = await openaiService.summarizePaper(paperContent);

// 实验报告生成
const report = await openaiService.generateReport(experimentData);

// Gpt-rosalind 对接
const result = await openaiService.callRosalind(query, 'protein-structure');
```

## 💾 本地数据库

### IndexedDB 集成

前端使用浏览器 IndexedDB 进行本地存储，存储表：

- `sequences` - 蛋白序列
- `helices` - 螺旋预测结果
- `mutations` - 突变体设计
- `experiments` - 实验数据
- `literature` - 文献记录
- `analysis_cache` - 分析缓存

### 后端 SQLite 数据库

后端使用 SQLite 存储所有数据，详见 `database_local.py`

```python
from database_local import db

# 保存实验
db.save_experiment(
    experiment_id='MLDP-001',
    mutation_id=1,
    mutant_name='野生型',
    pearson=0.89,
    manders=0.85,
    expression_level=85
)

# 获取统计
stats = db.get_experiment_statistics()
```

## 📦 生产部署

### Docker 部署

```dockerfile
# Dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .

RUN npm run build

EXPOSE 3000

CMD ["npm", "start"]
```

### Docker Compose

```yaml
version: '3.8'
services:
  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      - REACT_APP_API_URL=http://backend:8000/api
      - REACT_APP_OPENAI_API_KEY=${OPENAI_API_KEY}
    depends_on:
      - backend

  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
```

### Vercel 部署

```bash
# 安装 Vercel CLI
npm i -g vercel

# 部署
vercel
```

### GitHub Pages 部署

```bash
# 安装依赖
npm install --save-dev gh-pages

# 添加到 package.json
"homepage": "https://yourusername.github.io/repo-name",
"deploy": "npm run build && gh-pages -d build"

# 部署
npm run deploy
```

## 🔐 环境变量说明

| 变量名 | 说明 | 示例 |
|--------|------|------|
| REACT_APP_API_URL | 后端 API 地址 | http://localhost:8000/api |
| REACT_APP_OPENAI_API_KEY | OpenAI API 密钥 | sk-... |
| REACT_APP_ENV | 运行环境 | development/production |

## 🐛 故障排除

### 无法连接后端 API

1. 检查后端是否启动：`http://localhost:8000`
2. 检查 CORS 设置
3. 确认 `REACT_APP_API_URL` 配置正确

### OpenAI API 错误

1. 检查 API 密钥是否正确
2. 确认账户配额充足
3. 查看 OpenAI 官方文档

### IndexedDB 数据丢失

1. 清除浏览器缓存
2. 检查隐私浏览模式（会禁用 IndexedDB）
3. 检查浏览器存储配额

## 📚 相关文档

- [React 官方文档](https://react.dev)
- [Ant Design 文档](https://ant.design)
- [OpenAI API 文档](https://platform.openai.com/docs)
- [Recharts 文档](https://recharts.org)

## 💬 支持

如有问题，请提交 GitHub Issue 或联系开发者。

