# API 文档

## 基础 URL

```
http://localhost:8000
```

## 认证

当前版本不需要认证。生产环境中建议添加 API Key 或 OAuth2 认证。

## 序列分析端点

### POST /api/sequences/analyze

分析蛋白质序列中的两亲性螺旋结构。

**请求**：

```json
{
  "name": "string",
  "sequence": "string",
  "organism": "string (optional)",
  "description": "string (optional)"
}
```

**响应** (200 OK):

```json
{
  "id": "string (UUID)",
  "name": "string",
  "sequence": "string",
  "organism": "string",
  "description": "string",
  "helix_score": 0.75,
  "helix_confidence": 0.82,
  "hydrophobic_residues": 15,
  "hydrophilic_residues": 8,
  "charge": 2.5,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

### GET /api/sequences/{sequence_id}

获取已存储的序列分析结果。

**响应** (200 OK):

同上的序列对象

### GET /api/sequences

列出所有已存储的序列。

**查询参数**：
- `skip`: int (default: 0)
- `limit`: int (default: 100)

**响应** (200 OK):

```json
[
  { /* 序列对象 */ },
  { /* 序列对象 */ }
]
```

---

## 突变体设计端点

### POST /api/mutations/predict

预测破坏两亲性螺旋疏水面的突变。

**请求**：

```json
{
  "sequence": "string (amino acid sequence)",
  "helix_start": integer (0-indexed),
  "helix_end": integer (0-indexed)
}
```

**响应** (200 OK):

```json
[
  {
    "id": "string (UUID)",
    "mutation_name": "L10K",
    "wild_type_residue": "L",
    "mutant_residue": "K",
    "position": 10,
    "helix_start": 5,
    "helix_end": 25,
    "in_hydrophobic_face": "yes",
    "hydrophobicity_change": 7.7,
    "charge_change": 1.0,
    "structure_stability_score": 0.77,
    "predicted_effect": "high",
    "rationale": "Replace hydrophobic L with charged K to disrupt amphipathic helix",
    "design_strategy": "Disrupting hydrophobic face",
    "created_at": "2024-01-15T10:30:00Z"
  }
]
```

### GET /api/mutations/{mutation_id}

获取单个突变设计。

### GET /api/mutations

列出所有突变设计。

---

## 实验数据端点

### POST /api/experiments/record

记录实验结果和共定位数据。

**请求**：

```json
{
  "name": "string",
  "mutant_name": "string",
  "mutation_type": "WT|Point mutation|etc",
  "mutations": "string (optional, JSON list)",
  "plasmid": "pYES2",
  "fusion_tag": "eYFP",
  "expression_level": 85,
  "pearson_correlation": 0.89,
  "manders_coefficient": 0.85,
  "overlap_coefficient": 0.82,
  "replicate_number": 1,
  "experimental_group": "WT",
  "notes": "string (optional)"
}
```

**共定位系数说明**：
- **Pearson Correlation** (-1 到 1):
  - 1: 完全正相关（100% 共定位）
  - 0: 无相关
  - -1: 完全负相关（互斥）
  - 典型值: 0.7-0.9 表示良好共定位

- **Manders Coefficient** (0 到 1):
  - 1: 100% 重叠
  - 0: 0% 重叠
  - 典型值: 0.8-0.95 表示良好共定位

**响应** (200 OK):

```json
{
  "id": "string (UUID)",
  "name": "string",
  "mutant_name": "string",
  "plasmid": "pYES2",
  "fusion_tag": "eYFP",
  "expression_level": 85,
  "pearson_correlation": 0.89,
  "manders_coefficient": 0.85,
  "replicate_number": 1,
  "experimental_group": "WT",
  "created_at": "2024-01-15T10:30:00Z"
}
```

### GET /api/experiments/{experiment_id}

获取单个实验结果。

### GET /api/experiments

列出所有实验。

**查询参数**：
- `skip`: int (default: 0)
- `limit`: int (default: 100)
- `mutant_name`: string (optional, 用于过滤)

### GET /api/experiments/compare/wt-vs-mutants

比较野生型和突变体的结果。

**响应**:

```json
{
  "wild_type": [ /* 野生型实验 */ ],
  "mutants": [ /* 突变体实验 */ ],
  "comparison": {
    "wt_avg_pearson": 0.87,
    "mutant_avg_pearson": 0.45
  }
}
```

---

## 文献搜索端点

### GET /api/literature/search

搜索 PubMed 文献。

**查询参数**：
- `query`: string (必需，搜索关键词)
- `keywords`: list (optional，额外关键词)
- `max_results`: int (default: 10)

**推荐的搜索词**：
- "lipid droplet proteins"
- "amphipathic helix localization"
- "protein targeting yeast"
- "heterologous expression"
- "eYFP colocalization"

**响应** (200 OK):

```json
{
  "query": "string",
  "total_results": 125,
  "results": [
    {
      "pmid": "12345678",
      "title": "Paper title",
      "authors": ["Author 1", "Author 2"],
      "source": "Journal Name",
      "pubdate": "2023 Jan",
      "url": "https://pubmed.ncbi.nlm.nih.gov/12345678/"
    }
  ]
}
```

### GET /api/literature/summary/{pmid}

获取论文摘要（使用 OpenAI 进行智能总结）。

**响应** (200 OK):

```json
{
  "pmid": "12345678",
  "title": "Paper title",
  "authors": ["Author 1"],
  "abstract": "[摘要文本]",
  "url": "https://pubmed.ncbi.nlm.nih.gov/12345678/"
}
```

---

## 报告生成端点

### POST /api/reports/generate

生成科研论文格式的自动报告。

**请求**：

```json
{
  "title": "MLDP Localization Study",
  "experiment_ids": ["exp-id-1", "exp-id-2"],
  "format": "md|html|pdf|docx"
}
```

**响应** (200 OK):

```json
{
  "title": "string",
  "format": "string",
  "generated_at": "2024-01-15T10:30:00Z",
  "experiment_count": 2,
  "content": "[报告内容]"
}
```

**报告包含**：
- 摘要 (Abstract)
- 介绍 (Introduction)
- 方法 (Methods)
- 结果 (Results) - 包含数据表格
- 讨论 (Discussion)
- 结论 (Conclusions)
- 参考文献 (References)

---

## 错误响应

### 400 Bad Request

```json
{
  "detail": "Invalid amino acid sequence"
}
```

### 404 Not Found

```json
{
  "detail": "Sequence not found"
}
```

### 500 Internal Server Error

```json
{
  "detail": "Error analyzing sequence: [error message]"
}
```

---

## 速率限制

当前无速率限制。生产环境中建议添加。

## 版本

API 版本：1.0.0

最后更新：2024-01-15
