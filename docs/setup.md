# 安装和配置指南

## 前置要求

- Python 3.10 或更高版本
- PostgreSQL 14 或更高版本
- Node.js 16+ (仅用于前端)
- Docker & Docker Compose (可选，用于容器化部署)
- OpenAI API Key (用于论文摘要功能)

## 快速开始 (开发模式)

### 1. 克隆仓库

```bash
cd MLDP-localization-research
```

### 2. 设置后端

#### 2.1 创建虚拟环境

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows
```

#### 2.2 安装依赖

```bash
pip install -r requirements.txt
```

#### 2.3 配置环境变量

```bash
cp .env.example .env
# 编辑 .env 文件，填入您的配置
nano .env  # 或使用其他文本编辑器
```

**关键配置项**：

```bash
# 数据库 (修改密码)
DATABASE_URL=postgresql://mldp_user:mldp_password@localhost:5432/mldp_research

# OpenAI API (可选，用于论文摘要)
OPENAI_API_KEY=sk-your-api-key-here

# PubMed 搜索 (可选)
PUBMED_EMAIL=your-email@example.com
```

#### 2.4 创建数据库

```bash
# 使用 PostgreSQL
psql -U postgres

CREATE ROLE mldp_user WITH LOGIN PASSWORD 'mldp_password';
CREATE DATABASE mldp_research OWNER mldp_user;
ALTER ROLE mldp_user CREATEDB;
\q  # 退出 psql
```

#### 2.5 启动后端服务器

```bash
uvicorn app.main:app --reload
```

服务器将在 `http://localhost:8000` 启动

**API 文档**：
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 使用 Docker (推荐)

### 1. 构建和运行容器

```bash
docker-compose up -d
```

这会自动：
- 启动 PostgreSQL 数据库
- 启动 FastAPI 后端
- 启动 React 前端 (当完成时)

### 2. 查看日志

```bash
docker-compose logs -f backend
```

### 3. 停止服务

```bash
docker-compose down
```

## API 使用示例

### 1. 分析序列

```bash
curl -X POST http://localhost:8000/api/sequences/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "name": "MLDP",
    "sequence": "MIVPQNRQLKRYTPDEVLKFLQDPPQHQVHQYTPLLEESLQLYEQYQDSLSQEIQLYRQSVQQMRQHQKYNQYQTQQV",
    "organism": "Chlamydomonas"
  }'
```

### 2. 预测突变

```bash
curl -X POST http://localhost:8000/api/mutations/predict \
  -H "Content-Type: application/json" \
  -d '{
    "sequence": "MIVPQNRQLKRYTPDEVLKFLQDPPQHQVHQYTPLLEESLQLYEQYQDSLSQEIQLYRQSVQQMRQHQKYNQYQTQQV",
    "helix_start": 10,
    "helix_end": 25
  }'
```

### 3. 记录实验结果

```bash
curl -X POST http://localhost:8000/api/experiments/record \
  -H "Content-Type: application/json" \
  -d '{
    "name": "MLDP WT - Replicate 1",
    "mutant_name": "Wild-Type",
    "mutation_type": "WT",
    "plasmid": "pYES2",
    "fusion_tag": "eYFP",
    "expression_level": 85,
    "pearson_correlation": 0.89,
    "manders_coefficient": 0.85,
    "replicate_number": 1,
    "experimental_group": "WT"
  }'
```

### 4. 文献搜索

```bash
curl "http://localhost:8000/api/literature/search?query=lipid%20droplet%20proteins&max_results=5"
```

### 5. 生成报告

```bash
curl -X POST http://localhost:8000/api/reports/generate \
  -H "Content-Type: application/json" \
  -d '{
    "title": "MLDP Localization Study",
    "experiment_ids": ["exp-id-1", "exp-id-2"],
    "format": "md"
  }'
```

## 项目结构

```
backend/
├── app/
│   ├── models/          # SQLAlchemy 数据模型
│   ├── schemas/         # Pydantic 请求/响应模式
│   ├── api/            # API 路由
│   ├── services/       # 业务逻辑
│   ├── config.py       # 配置管理
│   ├── database.py     # 数据库连接
│   └── main.py         # FastAPI 应用
├── requirements.txt     # Python 依赖
└── .env.example        # 环境变量示例
```

## 故障排查

### 数据库连接错误

**问题**：`psycopg2.OperationalError: could not connect to server`

**解决**：
1. 确保 PostgreSQL 正在运行
2. 检查数据库凭证在 `.env` 中是否正确
3. 验证数据库是否存在

### 模块导入错误

**问题**：`ModuleNotFoundError: No module named 'app'`

**解决**：
1. 确保在 `backend` 目录中
2. 虚拟环境已激活
3. 运行 `pip install -r requirements.txt`

### OpenAI API 错误

**问题**：`openai.error.AuthenticationError`

**解决**：
1. 检查 `.env` 中的 `OPENAI_API_KEY` 是否正确
2. 从 https://platform.openai.com/account/api-keys 获取新密钥

## 下一步

- [ ] 创建 React 前端应用
- [ ] 配置 PostgreSQL 持久化存储
- [ ] 完整的单元测试
- [ ] 部署到云服务 (AWS, Azure, GCP)
- [ ] 集成机器学习模型进行更精确的预测

## 获取帮助

如有问题，请：
1. 查看 [API 文档](./api.md)
2. 提交 GitHub Issue
3. 查看 FastAPI 官方文档: https://fastapi.tiangolo.com/
