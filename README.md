# MLDP Lipid Droplet Localization Research Assistant

## 项目概述

这是一个为藻类MLDP（脂滴定位蛋白）在酵母中的异源表达研究而设计的Web应用。该工具帮助研究人员：

- 📊 **序列分析** - 预测MLDP中的两亲性螺旋结构
- 🧬 **突变体设计** - 自动建议破坏疏水面的突变位点
- 📚 **文献检索** - 搜索相关脂滴定位和螺旋结构研究论文
- 🔬 **实验数据管理** - 记录eYFP共定位和激光共聚焦结果
- 📈 **数据分析** - 自动分析Pearson相关系数和Manders重叠系数
- 📝 **报告生成** - 自动生成科研论文格式的实验报告

## 研究背景

**研究对象**: MLDP (Mud Lipid Droplet Protein)

**研究方向**: 
- MLDP在酵母中的异源表达
- 两亲性螺旋介导的脂滴定位机制
- 通过构建突变体破坏疏水面来验证定位功能

**实验方法**:
- pYES2质粒表达系统
- eYFP融合蛋白标记
- 激光共聚焦显微镜观察
- 黄色荧光和脂滴的共定位分析

## 项目结构

```
MLDP-localization-research/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI主应用
│   │   ├── config.py            # 配置管理
│   │   ├── database.py          # 数据库连接
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── sequence.py      # 序列数据模型
│   │   │   ├── experiment.py    # 实验数据模型
│   │   │   └── mutation.py      # 突变体数据模型
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   ├── sequence.py
│   │   │   ├── experiment.py
│   │   │   └── mutation.py
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── sequences.py     # 序列分析API
│   │   │   ├── mutations.py     # 突变体设计API
│   │   │   ├── experiments.py   # 实验数据管理API
│   │   │   ├── literature.py    # 文献搜索API
│   │   │   └── reports.py       # 报告生成API
│   │   └── services/
│   │       ├── __init__.py
│   │       ├── helix_prediction.py
│   │       ├── mutation_analysis.py
│   │       ├── literature_search.py
│   │       └── report_generator.py
│   ├── requirements.txt
│   ├── .env.example
│   └── Dockerfile
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   └── App.js
│   ├── package.json
│   └── Dockerfile
├── docs/
│   ├── setup.md
│   ├── api.md
│   └── research_guide.md
├── docker-compose.yml
└── .gitignore
```

## 快速开始

### 前置要求
- Python 3.10+
- Node.js 16+
- Docker & Docker Compose
- PostgreSQL 14+
- OpenAI API Key

### 安装步骤

详见 [setup.md](docs/setup.md)

## API 端点

### 序列分析

#### POST /api/sequences/analyze
分析MLDP序列中的两亲性螺旋

```json
{
  "sequence": "MIVPQNRQLKRYTPDEVLKFLQDPPQHQVHQYTPLLEESLQLYEQYQDSLSQEIQLYRQSVQQMRQHQKYNQYQTQQV",
  "name": "MLDP"
}
```

### 突变体设计

#### POST /api/mutations/predict
获取破坏疏水面的突变建议

```json
{
  "sequence": "MIVPQNRQLKRYTPDEVLKFLQDPPQHQVHQYTPLLEESLQLYEQYQDSLSQEIQLYRQSVQQMRQHQKYNQYQTQQV",
  "helix_start": 10,
  "helix_end": 25
}
```

### 实验数据

#### POST /api/experiments/record
记录共定位实验结果

```json
{
  "experiment_id": "MLDP-001-WT",
  "mutant": "野生型",
  "results": {
    "colocalization_pearson": 0.89,
    "colocalization_manders": 0.85,
    "expression_level": 85
  }
}
```

## 功能特性

### 🧬 两亲性螺旋预测
- 使用HELIX算法识别α-螺旋
- 自动识别疏水和亲水残基模式
- 螺旋评分和稳定性分析

### 🔬 突变体设计
- 自动推荐突变位点（L→K, I→K, V→K等）
- 评估突变对螺旋结构的影响
- 生成突变体设计报告

### 📚 文献管理
- 集成PubMed API搜索
- 相关性评分和分类
- OpenAI摘要和分析

### 📊 实验数据管理
- 记录所有突变体的共定位数据
- Pearson相关系数计算
- Manders重叠系数分析
- WT vs 突变体对比

### 📈 数据可视化
- 共定位分布图
- 突变体效应比较
- 螺旋结构示意图

### 📝 自动报告生成
- 完整的论文格式报告
- 摘要、方法、结果、讨论自动生成
- 支持PDF、Word、HTML导出

## 环境变量配置

见 `.env.example`

```bash
DATABASE_URL=postgresql://user:password@localhost/mldp_research
OPENAI_API_KEY=sk-...
PUBMED_API_KEY=your_key
```

## 开发

### 启动开发服务器

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### API文档

FastAPI自动生成的交互式API文档:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 贡献

欢迎提交Issue和Pull Request！

## 许可证

MIT

## 作者

研究者: fakersbs

## 联系方式

如有问题或建议，请提交GitHub Issue。
