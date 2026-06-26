# NLP Final Project 实验进度记录

项目名称：When LLMs Misunderstand Course Policies: Evaluating Hallucination and Rule Reasoning in Educational Question Answering

当前时间：2026-05-03 16:36

---

## 1. 项目目录初始化

已在本地创建项目目录：

    E:\Working\edu_policy_qa

当前项目采用如下主要目录结构：

    edu_policy_qa/
    ├── data/
    │   ├── raw_docs/
    │   ├── processed_docs/
    │   ├── questions/
    │   ├── outputs/
    │   ├── external/
    │   └── metadata/
    ├── indexes/
    │   └── faiss_index/
    ├── notebooks/
    ├── src/
    ├── results/
    │   └── figures/
    ├── reports/
    ├── requirements.txt
    ├── environment.yml
    ├── README.md
    └── .gitignore

---

## 2. Anaconda 环境配置

已创建并激活 Conda 环境：

    edu_policy_qa

Python 版本：

    Python 3.10.x

项目工作路径：

    E:\Working\edu_policy_qa

---

## 3. Python 依赖安装

已安装主要实验依赖，包括：

    torch
    torchvision
    torchaudio
    transformers
    accelerate
    datasets
    sentence-transformers
    faiss-cpu
    pandas
    numpy
    scikit-learn
    tqdm
    pypdf
    pymupdf
    python-docx
    matplotlib
    seaborn
    evaluate
    jupyter
    notebook
    ipykernel

已注册 Jupyter Kernel：

    Python (edu_policy_qa)

已生成环境记录文件：

    environment.yml
    requirements.txt

---

## 4. 已下载的数据源

已下载并整理以下公开课程文档/数据集：

| 数据源 | 本地路径 | 用途 |
|---|---|---|
| SyllabusQA | `data/external/syllabusqa` | 主要课程政策 QA 数据源 |
| UMich Syllabus Collection | `data/external/umich_syllabus_collection` | 补充课程 syllabus 文档 |
| macloo Course Syllabi | `data/external/macloo_course_syllabi` | 补充公开 syllabus PDF |

已记录数据源文件：

    data/metadata/dataset_sources.csv

---

## 5. 原始课程文档整理

已运行脚本：

    src/collect_raw_docs.py

该脚本已将外部数据源中的课程相关文件复制到：

    data/raw_docs/

并生成原始元数据文件：

    data/metadata/raw_docs_metadata.csv

原始元数据统计：

    Input rows: 222

---

## 6. 元数据清洗

已运行脚本：

    src/clean_raw_docs_metadata.py

该脚本完成了以下处理：

- 删除无关文件记录，例如 `README.md`、`requirements.txt`、`playlists.md`
- 删除数据集 split 文件，例如 `.csv`、`.json`
- 对重复文档优先保留 `.txt` 格式
- 若无 `.txt`，保留 `.pdf`
- 自动补充数据源链接
- 自动提取部分 publication date
- 自动标记是否为 official course material

生成清洗后的元数据文件：

    data/metadata/raw_docs_metadata_clean.csv

运行结果：

    Input rows: 222
    Clean rows: 84
    Saved to: E:\Working\edu_policy_qa\data\metadata\raw_docs_metadata_clean.csv

---

## 7. 当前可用文档统计

清洗后共有课程文档：

    total: 84

按数据源统计：

    SyllabusQA                   63
    UMich Syllabus Collection    18
    macloo Course Syllabi         3

---

## 8. 当前关键文件

目前项目中已经生成或准备好的关键文件包括：

    data/raw_docs/
    data/external/
    data/metadata/dataset_sources.csv
    data/metadata/raw_docs_metadata.csv
    data/metadata/raw_docs_metadata_clean.csv
    src/collect_raw_docs.py
    src/clean_raw_docs_metadata.py
    environment.yml
    requirements.txt
    README.md

---

## 9. 当前实验状态

当前已完成：

- 项目目录创建
- Conda 环境创建
- Python 依赖安装
- 公开课程文档数据源下载
- 原始课程文档收集
- 原始文档元数据生成
- 元数据自动清洗
- 获得 84 个可用于后续实验的课程政策文档

当前尚未开始：

- 文档文本解析为 `documents.jsonl`
- 文档切分为 `chunks.jsonl`
- 构建问题集
- 构建 embedding
- 构建 FAISS 索引
- 实现 RAG 检索
- 运行 LLM 实验
- 评估与错误分析


---

## 10. 文档文本解析

已完成第 5.2 步：解析文档文本。

本步骤使用脚本：

    src/document_loader.py

输入元数据文件：

    data/metadata/raw_docs_metadata_clean.csv

输入原始文档目录：

    data/raw_docs/

输出解析后的 JSONL 文件：

    data/processed_docs/documents.jsonl

输出解析错误记录文件：

    data/processed_docs/document_parse_errors.csv

---

## 11. 文档解析脚本功能

`document_loader.py` 已支持解析以下文件格式：

- `.txt`
- `.pdf`
- `.docx`
- `.md`
- `.html`
- `.htm`

解析逻辑如下：

- 对 `.txt`、`.md`、`.html`、`.htm` 文件按整体文本读取
- 对 `.pdf` 文件使用 PyMuPDF 逐页提取文本
- 对 `.docx` 文件提取段落文本和表格文本
- 对所有文本进行基础清洗
- 输出为 JSONL 格式
- 每一行代表一个页面或一个文档级文本片段

每条 JSONL 记录包含以下字段：

    doc_id
    source
    doc_type
    publication_date
    data_source
    source_url
    is_official_course_material
    page
    text

---

## 12. 文档解析运行结果

运行命令：

    python src\document_loader.py

运行输出：

    Parsing documents: 100%|████████████████████████████████████████| 84/84 [00:01<00:00, 70.91it/s]
    Documents in metadata: 84
    Parsed records: 191
    Parse errors: 1
    Saved documents to: E:\Working\edu_policy_qa\data\processed_docs\documents.jsonl
    Saved errors to: E:\Working\edu_policy_qa\data\processed_docs\document_parse_errors.csv

---

## 13. 当前 processed_docs 目录状态

当前目录：

    data/processed_docs/

目录内容：

    chunks.jsonl
    documents.jsonl
    document_parse_errors.csv

其中：

    documents.jsonl                  1,459,827 bytes
    document_parse_errors.csv              150 bytes
    chunks.jsonl                            0 bytes

说明：

- `documents.jsonl` 已成功生成
- `document_parse_errors.csv` 已成功生成
- `chunks.jsonl` 当前仍为空，后续文档切分步骤会生成该文件内容

---

## 14. 文档解析统计结果

对 `documents.jsonl` 进行统计后结果如下：

    records: 191
    docs: 83
    sources: Counter({'UMich Syllabus Collection': 96, 'SyllabusQA': 63, 'macloo Course Syllabi': 32})

解释：

- 共解析出 191 条文本记录
- 覆盖 83 个文档
- 原始清洗元数据中共有 84 个文档
- 其中 1 个文档解析失败
- UMich Syllabus Collection 的 PDF 按页面解析，因此记录数多于文档数
- SyllabusQA 多数优先使用 `.txt` 文件，因此每个文档通常对应 1 条记录
- macloo Course Syllabi 的 PDF 按页面解析，因此产生 32 条记录

---

## 15. 文档解析错误记录

解析错误文件：

    data/processed_docs/document_parse_errors.csv

当前仅有 1 条错误：

    doc_id: eecs_281_data_structures_and_algorithms_fall_2020
    file_name: EECS 281_Data Structures and Algorithms_Fall 2020.pdf
    error: empty parsed text

该错误说明：

- 该 PDF 文件无法直接通过文本抽取获得内容
- 可能原因是该 PDF 为扫描版、图片型 PDF，或内部文本层不可读取
- 当前暂时保留该错误记录
- 后续如有需要，可使用 OCR 工具进一步处理该文件

---

## 16. 文档解析样例检查

已检查 `documents.jsonl` 前 3 条记录，确认字段结构正常，文本内容可读取。

样例文档包括：

    1._syllabus_2023
    101_f22_syll
    130_syllabus_2_s_2023

样例字段包括：

    doc_id
    source
    doc_type
    publication_date
    data_source
    source_url
    is_official_course_material
    page
    text

检查结果：

- JSONL 格式正常
- 文本字段成功解析
- metadata 字段保留完整
- 可以进入下一步文档切分

---

## 17. 当前实验状态更新

截至目前，已完成：

- 项目目录创建
- Conda 环境创建
- Python 依赖安装
- 公开课程文档数据源下载
- 原始课程文档收集
- 原始文档元数据生成
- 元数据自动清洗
- 获得 84 个可用于后续实验的课程政策文档
- 将课程文档解析为 `documents.jsonl`
- 获得 191 条可检索文本记录
- 确认 83 个文档成功解析
- 记录 1 个 PDF 文本解析失败案例

当前尚未开始：

- 文档切分为 `chunks.jsonl`
- 构建问题集
- 构建 embedding
- 构建 FAISS 索引
- 实现 RAG 检索
- 运行 LLM 实验
- 评估与错误分析


---

## 18. 文档切分

已完成第 5.3 步：文档切分。

本步骤使用脚本：

    src/chunk_documents.py

输入文件：

    data/processed_docs/documents.jsonl

输出文件：

    data/processed_docs/chunks.jsonl

---

## 19. 文档切分参数

当前切分参数如下：

    CHUNK_SIZE = 400
    CHUNK_OVERLAP = 80

切分方式：

- 按单词数量切分
- 每个 chunk 约 400 words
- 相邻 chunk 保留 80 words overlap
- 保留原始文档顺序
- 为每个 chunk 生成唯一 `chunk_id`
- 保留文档级 metadata
- 尝试自动识别 `section`

---

## 20. chunk 字段结构

每条 chunk 记录包含以下字段：

    chunk_id
    doc_id
    source
    doc_type
    publication_date
    data_source
    source_url
    is_official_course_material
    page
    chunk_index
    start_word
    end_word
    section
    text

示例 chunk_id 格式：

    1._syllabus_2023_p1_c1

---

## 21. 文档切分运行结果

运行命令：

    python src\chunk_documents.py

运行输出：

    Chunking documents: 100%|███████████████████████████████████| 191/191 [00:00<00:00, 1824.32it/s]
    Input records: 191
    Output chunks: 693
    Saved to: E:\Working\edu_policy_qa\data\processed_docs\chunks.jsonl

---

## 22. 当前 processed_docs 目录状态

当前目录：

    data/processed_docs/

目录内容：

    chunks.jsonl
    documents.jsonl
    document_parse_errors.csv

文件大小：

    chunks.jsonl                    1,924,316 bytes
    documents.jsonl                 1,459,827 bytes
    document_parse_errors.csv             150 bytes

说明：

- `chunks.jsonl` 已成功生成
- `documents.jsonl` 保留为原始解析文本
- `document_parse_errors.csv` 保留解析错误记录

---

## 23. 文档切分统计结果

对 `chunks.jsonl` 进行统计后结果如下：

    chunks: 693
    docs: 83

解释：

- 共生成 693 个文本 chunk
- 覆盖 83 个成功解析的文档
- 与上一阶段 `documents.jsonl` 中的 83 个文档一致
- 1 个 PDF 文档因无法解析文本，未进入 chunk 构建

---

## 24. chunk 样例检查

已检查 `chunks.jsonl` 前 3 条记录。

样例 chunk 包括：

    1._syllabus_2023_p1_c1
    1._syllabus_2023_p1_c2
    1._syllabus_2023_p1_c3

检查结果：

- JSONL 格式正常
- chunk_id 唯一格式正常
- doc_id、source、page 等 metadata 已保留
- start_word 与 end_word 字段正常
- chunk overlap 正常，例如：
    - 第 1 个 chunk: start_word = 0, end_word = 400
    - 第 2 个 chunk: start_word = 320, end_word = 720
    - overlap = 80 words
- text 字段内容可读取
- 可进入后续评测问题集构建与 RAG 索引构建步骤

---

## 25. 当前实验状态更新

截至目前，已完成：

- 项目目录创建
- Conda 环境创建
- Python 依赖安装
- 公开课程文档数据源下载
- 原始课程文档收集
- 原始文档元数据生成
- 元数据自动清洗
- 获得 84 个可用于后续实验的课程政策文档
- 将课程文档解析为 `documents.jsonl`
- 获得 191 条可检索文本记录
- 确认 83 个文档成功解析
- 记录 1 个 PDF 文本解析失败案例
- 将解析后的文档切分为 `chunks.jsonl`
- 获得 693 个文本 chunk

当前尚未开始：

- 构建问题集
- 构建 embedding
- 构建 FAISS 索引
- 实现 RAG 检索
- 运行 LLM 实验
- 评估与错误分析

## 6. 问题集构建与人工修订

### 6.1 文档切分完成

已完成对解析后文档的切分处理。

- 输入文件：`data/processed_docs/documents.jsonl`
- 输出文件：`data/processed_docs/chunks.jsonl`
- 切分脚本：`src/chunk_documents.py`
- 参数设置：
  - `CHUNK_SIZE = 400`
  - `CHUNK_OVERLAP = 80`
- 处理结果：
  - 原始记录数：191
  - 成功生成 Chunk 数：693
  - 覆盖成功解析文档数：83

---

### 6.2 自动问题集生成

已完成自动化问题集初稿生成。

- 自动生成脚本：`src/auto_generate_questions.py`
- 初始输出文件：`data/questions/questions_with_reference_auto.csv`
- 初始目标数量：80 条问题
- 目标类别分布：
  - `factual_extraction`：20
  - `rule_understanding`：20
  - `multi_condition_reasoning`：15
  - `exception_handling`：15
  - `unanswerable_insufficient_evidence`：10

---

### 6.3 问题质量检查与清洗

已完成自动生成问题集的质量检查与基础清洗。

相关脚本：

- `src/check_question_quality.py`
- `src/clean_auto_questions.py`
- `src/finalize_question_draft.py`

中间文件：

- `data/questions/questions_with_reference_clean_draft.csv`
- `data/questions/questions_with_reference_final_candidate.csv`

主要处理内容：

- 清理乱码与异常字符
- 规范 `evidence_page`
- 修复不可回答问题的证据字段
- 增加并使用 `quality_flags` 辅助人工审查
- 标记泛化问题、类别疑似不匹配问题、多条件推理较弱问题

---

### 6.4 人工修订脚本化完成

已将人工检查意见整理为脚本，并批量应用到最终问题集。

人工修订脚本：

- `src/apply_manual_question_fixes.py`

修订内容包括：

- 重写 Q001–Q070 中过于泛化的问题文本
- 优化 reference answer，使其更直接、更可评估
- 修正部分问题类别
- 保持类别分布不变
- 修复 Q071–Q080 的不可回答问题证据字段
- 输出正式版与审计版文件

生成文件：

- `data/questions/questions_with_reference_final.csv`
- `data/questions/questions_with_reference_final_audit.csv`
- `data/questions/questions_with_reference.csv`

其中：

- `questions_with_reference.csv` 为当前正式评测问题集
- `questions_with_reference_final.csv` 为正式修订版副本
- `questions_with_reference_final_audit.csv` 为带审计字段的追踪版本

---

### 6.5 最终问题集验证通过

已运行最终验证脚本：

```bat
python src\validate_questions.py

## 10. Closed-book LLM 实验记录

### 10.1 实验设置

已完成 **Closed-book LLM** 实验设置。

该实验中，模型只能看到问题本身，不能看到课程文档内容。

实验目的：

- 测试模型在没有课程文档 grounding 的情况下如何回答课程政策问题
- 观察模型是否会承认信息不足
- 为后续方法提供 baseline 对比结果

---

### 10.2 OpenAI API 方案尝试

最初使用 OpenAI API 运行 Closed-book LLM 实验。

脚本：

    src/run_closed_book_llm.py

输出文件：

    data/results/closed_book_llm_results.csv

运行后发现 OpenAI API 请求失败。

错误类型：

    Error code: 401

错误原因：

    account_deactivated

错误信息显示：

    The OpenAI account associated with this API key has been deactivated.

因此，OpenAI API 路线暂时不可用。

---

### 10.3 改用本地 Ollama 模型

由于当前无法使用 OpenAI API，实验切换为本地 LLM 方案。

已安装 Ollama：

    winget install Ollama.Ollama

安装结果：

    Ollama [Ollama.Ollama] version 0.22.1 installed successfully

已下载本地模型：

    ollama pull qwen2.5:3b

模型下载结果：

    success

本地模型列表确认命令：

    ollama list

输出：

    NAME          ID              SIZE      MODIFIED
    qwen2.5:3b    357c53fb659c    1.9 GB    7 minutes ago

---

### 10.4 Ollama 模型可用性测试

运行本地模型：

    ollama run qwen2.5:3b

测试输入：

    Hello

模型正常返回：

    Hello! It's nice to meet you. How can I assist you today?

随后退出交互：

    /bye

说明本地 Ollama 模型可正常调用。

---

### 10.5 本地 Closed-book 脚本

新增本地 Closed-book 实验脚本：

    src/run_closed_book_llm_ollama.py

该脚本使用本地模型：

    qwen2.5:3b

调用方式：

    http://localhost:11434/api/generate

Prompt 设置：

    You are answering questions about a course policy.
    Answer the question as accurately as possible.

    Question:
    {question}

    Answer:

输入文件：

    data/questions/questions_with_reference.csv

输出文件：

    data/results/closed_book_llm_results.csv

实验设置：

| 项目 | 设置 |
|---|---|
| 实验类型 | Closed-book LLM |
| 模型 | qwen2.5:3b |
| 运行方式 | 本地 Ollama |
| 文档 grounding | 无 |
| 输入内容 | question only |
| 输出字段 | closed_book_answer |
| API 依赖 | 无 OpenAI API 依赖 |

---

### 10.6 Closed-book 实验运行结果

运行命令：

    python src\run_closed_book_llm_ollama.py

运行过程成功覆盖全部 80 个问题：

    [1/80] Running local closed-book LLM for Q001
    [2/80] Running local closed-book LLM for Q002
    ...
    [80/80] Running local closed-book LLM for Q080

脚本完成后输出：

    Saved closed-book results to: E:\Working\edu_policy_qa\data\results\closed_book_llm_results.csv
    Total rows: 80
    Error rows: 1

---

### 10.7 输出文件检查

检查命令：

    python -c "import pandas as pd; df=pd.read_csv('data/results/closed_book_llm_results.csv'); print('rows:', len(df)); print('errors:', (df['error'].fillna('')!='').sum()); print(df[['question_id','closed_book_answer','error']].head())"

检查结果：

    rows: 80
    errors: 1

前 5 条输出示例：

    question_id    closed_book_answer                                      error
    Q001           I'm sorry, but I don't have specific informati...        NaN
    Q002           I'm sorry, but based on the information you've...        NaN
    Q003           I'm sorry, but I don't have specific informati...        NaN
    Q004           I'm sorry, but I don't have specific informati...        NaN
    Q005           I'm sorry, but I don't have specific informati...        NaN

---

### 10.8 当前实验产物

当前已生成 Closed-book LLM 结果文件：

    data/results/closed_book_llm_results.csv

文件包含 80 行结果。

字段包括：

    question_id
    question
    category
    answerable
    reference_answer
    closed_book_answer
    error

当前状态：

| 项目 | 结果 |
|---|---|
| 总问题数 | 80 |
| 成功生成结果 | 79 |
| 错误行数 | 1 |
| 使用模型 | qwen2.5:3b |
| 文档 grounding | 无 |
| 输出文件 | data/results/closed_book_llm_results.csv |

---

### 10.9 当前里程碑更新

截至当前，项目已完成：

    Closed-book LLM baseline experiment completed with local Ollama model.

当前 Closed-book baseline 文件为：

    data/results/closed_book_llm_results.csv

本阶段使用本地模型替代 OpenAI API，解决了 API key 不可用的问题。

实验目前状态：

    Closed-book LLM run completed.
    Rows generated: 80
    Error rows: 1
    Model: qwen2.5:3b
    Execution mode: local Ollama

## 7.2 实验设置二：Full-context Prompting

### 7.2.1 实验说明

已完成 **Full-context Prompting** 实验。

该实验中，将课程文档内容作为上下文放入 prompt，使模型基于提供的课程文档回答问题。

实验使用本地 Ollama 模型运行，不依赖 OpenAI API。

---

### 7.2.2 实验设置

本次实验使用的模型：

    qwen2.5:3b

运行方式：

    本地 Ollama

输入问题文件：

    data/questions/questions_with_reference.csv

输入文档文件：

    data/processed_docs/documents.jsonl

输出结果文件：

    data/results/full_context_prompting_results.csv

实验脚本：

    src/run_full_context_prompting_ollama.py

Prompt 类型：

    Full-context Prompting

文档 grounding：

    有

---

### 7.2.3 模型确认

运行命令：

    ollama list

输出结果：

    NAME          ID              SIZE      MODIFIED
    qwen2.5:3b    357c53fb659c    1.9 GB    21 minutes ago

确认本地模型 `qwen2.5:3b` 已存在并可用于实验。

---

### 7.2.4 实验运行

运行命令：

    python src\run_full_context_prompting_ollama.py

运行开始后，脚本成功加载课程文档：

    Loaded documents: 191

实验共处理 80 个问题。

运行过程显示：

    [1/80] Running full-context prompting for Q001
    [2/80] Running full-context prompting for Q002
    [3/80] Running full-context prompting for Q003
    [4/80] Running full-context prompting for Q004
    [5/80] Running full-context prompting for Q005
    ...
    [80/80] Running full-context prompting for Q080

实验成功运行至最后一个问题。

---

### 7.2.5 实验输出

脚本运行完成后输出：

    Saved full-context results to: E:\Working\edu_policy_qa\data\results\full_context_prompting_results.csv
    Total rows: 80
    Error rows: 1

生成结果文件：

    data/results/full_context_prompting_results.csv

---

### 7.2.6 输出文件检查

检查命令：

    python -c "import pandas as pd; df=pd.read_csv('data/results/full_context_prompting_results.csv'); print('rows:', len(df)); print('errors:', (df['error'].fillna('')!='').sum()); print(df[['question_id','full_context_answer','context_chars','error']].head())"

检查结果：

    rows: 80
    errors: 1

前 5 条结果示例：

    question_id    full_context_answer                                      context_chars    error
    Q001           The office hours for the Federal Budgeting Pro...          6956             NaN
    Q002           The penalty for more than two unexcused absenc...          6956             NaN
    Q003           Absences are excused if supported by an approp...          6956             NaN
    Q004           The penalty for late assignments is a drop of ...          6956             NaN
    Q005           The grade consequence for academic dishonesty,...          6956             NaN

---

### 7.2.7 当前实验结果汇总

| 项目 | 结果 |
|---|---|
| 实验名称 | Full-context Prompting |
| 模型 | qwen2.5:3b |
| 运行方式 | 本地 Ollama |
| 输入问题数 | 80 |
| 加载文档数 | 191 |
| 输出结果数 | 80 |
| 错误行数 | 1 |
| 文档 grounding | 有 |
| 输出文件 | data/results/full_context_prompting_results.csv |

---

### 7.2.8 当前进度记录

当前实验状态：

    7.2 Full-context Prompting experiment completed.

实验记录：

    Model: qwen2.5:3b
    Execution mode: local Ollama
    Input questions: data/questions/questions_with_reference.csv
    Input documents: data/processed_docs/documents.jsonl
    Loaded documents: 191
    Output: data/results/full_context_prompting_results.csv
    Rows generated: 80
    Error rows: 1
    Document grounding: full-context prompting

7.3 实验设置三：Basic RAG
实验状态
Basic RAG 实验已完成一次完整运行。系统成功读取 FAISS 向量索引和 chunk metadata，并对全部 80 条评测问题执行了 retrieval-generation 流程。

本次实验最终生成结果文件：data/results/basic_rag_results.csv

运行完成后统计结果如下：

Total rows: 80
Error rows: 3
因此，本阶段状态记录为：Basic RAG experiment completed with 80 total questions and 3 generation error rows.

实验流程记录
1. Retrieval 阶段
Basic RAG 的 retrieval 阶段基于已经构建好的 FAISS index 执行。系统根据每个问题生成 query embedding，然后从向量数据库中检索 top-k 个最相关的文档 chunks。

本次使用的向量数据库信息如下：

Embedding backend: Ollama nomic-embed-text
Vector index: FAISS
Number of indexed chunks: 693
Embedding dimension: 768
Top-k: 5
Index file: data/vector_store/faiss.index
Metadata file: data/vector_store/chunk_metadata.jsonl
运行时系统成功加载：

FAISS vectors: 693
Metadata rows: 693
这说明 FAISS index 与 metadata 数量一致，retrieval 数据结构有效。

2. Generation 阶段
在 generation 阶段，系统将检索到的 top-k chunks 与原始问题一起输入本地 Ollama LLM，生成最终回答。

本次使用的生成模型为：

LLM model: Ollama qwen2.5:3b
Execution mode: local Ollama
Prompt 模板如下：

You are answering questions based only on the retrieved course document passages.

Use only the information in the passages.

If the passages do not contain enough evidence, say that the documents do not provide enough information.

Retrieved Passages:

{retrieved_chunks}

Question:

{question}

Answer:

输出文件
Basic RAG 实验输出文件为：data/results/basic_rag_results.csv

该文件包含 80 条问题的 RAG 结果，每条记录包括：

question_id
question
category
answerable
reference_answer
evidence_doc
rag_answer
top_k
retrieved_chunk_ids
retrieved_scores
retrieved_sources
retrieved_chunks
error
运行检查命令为：

python -c "import pandas as pd; df=pd.read_csv('data/results/basic_rag_results.csv'); print('rows:', len(df)); print('errors:', (df['error'].fillna('')!='').sum()); print(df[['question_id','rag_answer','top_k','retrieved_chunk_ids','error']].head())"

检查结果如下：

rows: 80
errors: 3
错误记录
本次 Basic RAG 实验中，有 3 条问题在 generation 阶段出现 Ollama 模型运行错误。

错误问题编号为：

Q022
Q071
Q078
错误信息为：

Generation HTTPError 500: {"error":"model runner has unexpectedly stopped, this may be due to resource limitations or an internal error, check ollama server logs for details"}

该错误说明 Python 脚本已经成功完成 retrieval，并成功向 Ollama 发送 generation 请求，但 Ollama 本地模型运行器在生成阶段异常停止。该问题通常与本地资源限制、上下文长度、模型运行稳定性或 Ollama 后端内部错误有关。

本次实验未中断，脚本已将错误写入结果文件中的 error 字段，并继续完成剩余问题。

当前阶段结论
本阶段已完成：

Embedding construction completed.
FAISS index construction completed.
Basic RAG retrieval-generation experiment completed.
Result file generated successfully.
80 evaluation questions processed.
本阶段存在的问题：

3 out of 80 questions failed during the generation stage due to Ollama HTTP 500 model runner errors.
最终状态：

Basic RAG experiment completed with partial generation errors.
Total questions: 80
Successful rows: 77
Error rows: 3
Output file: data/results/basic_rag_results.csv

7.4 实验设置四：Citation-constrained RAG
实验状态
Citation-constrained RAG 实验已完成一次完整运行。系统成功读取 FAISS 向量索引和 chunk metadata，并对全部 80 条评测问题执行了带 citation constraint 的 retrieval-generation 流程。

本次实验最终生成结果文件：data/results/citation_rag_results.csv

运行完成后统计结果如下：

Total rows: 80
Error rows: 0
因此，本阶段状态记录为：Citation-constrained RAG experiment completed successfully with 80 total questions and 0 error rows.

实验流程记录
1. Retrieval 阶段
Citation-constrained RAG 的 retrieval 阶段继续基于已构建的 FAISS index 执行。系统根据每个问题生成 query embedding，然后从向量数据库中检索 top-k 个最相关的 document chunks。

本次使用的检索设置如下：

Embedding backend: Ollama nomic-embed-text
Vector index: FAISS
Number of indexed chunks: 693
Embedding dimension: 768
Top-k: 5
Index file: data/vector_store/faiss.index
Metadata file: data/vector_store/chunk_metadata.jsonl
运行时系统成功加载：

FAISS vectors: 693
Metadata rows: 693
这说明 FAISS index 与 metadata 数量一致，retrieval 数据结构有效。

2. Generation 阶段
在 generation 阶段，系统将检索到的 top-k chunks 与原始问题一起输入本地 Ollama LLM，并要求模型按照固定格式输出答案、证据引用和置信度。

本次使用的生成模型为：

LLM model: Ollama qwen2.5:3b
Execution mode: local Ollama
Constraint type: citation-constrained generation
本实验要求模型遵守以下规则：

只能使用 retrieved passages 中的信息。
如果 passages 不支持答案，则回答：The provided course documents do not specify this.
每个答案必须包含至少一个 citation。
Citation 必须包含 source、page 和 chunk_id。
不允许模型使用外部知识或猜测。
Prompt 设置
本实验使用的 prompt 结构如下：

You are answering questions based only on the retrieved course document passages.

Rules:

Use only the retrieved passages.
If the passages do not support an answer, say: "The provided course documents do not specify this."
Every answer must include at least one citation.
A citation must include source, page, and chunk_id.
Do not guess or use outside knowledge.
Retrieved Passages:

{retrieved_chunks}

Question:

{question}

Please answer in the following format:

Answer:

Evidence:

[source: ..., page: ..., chunk_id: ...] ...
Confidence:
输出文件
Citation-constrained RAG 实验输出文件为：data/results/citation_rag_results.csv

该文件包含 80 条问题的 citation-constrained RAG 结果，每条记录包括：

question_id
question
category
answerable
reference_answer
evidence_doc
citation_rag_answer
top_k
retrieved_chunk_ids
retrieved_scores
retrieved_sources
retrieved_pages
retrieved_chunks
error
运行命令记录
本实验运行命令如下：

python src\run_citation_rag_ollama.py

运行完成后，系统输出：

Saved Citation-constrained RAG results to: E:\Working\edu_policy_qa\data\results\citation_rag_results.csv
Total rows: 80
Error rows: 0
结果检查记录
结果文件检查命令如下：

python -c "import pandas as pd; df=pd.read_csv('data/results/citation_rag_results.csv'); print('rows:', len(df)); print('errors:', (df['error'].fillna('')!='').sum()); print(df[['question_id','citation_rag_answer','top_k','retrieved_chunk_ids','error']].head())"

检查结果如下：

rows: 80
errors: 0
错误问题检查命令如下：

python -c "import pandas as pd; df=pd.read_csv('data/results/citation_rag_results.csv'); e=df[df['error'].fillna('')!='']; print(e[['question_id','error']])"

检查结果如下：

Empty DataFrame
Columns: question_id, error
Index: empty
这说明本次 Citation-constrained RAG 实验没有 generation error，也没有 retrieval error。

Citation 输出格式抽查
抽查第一条结果的命令如下：

python -c "import pandas as pd; df=pd.read_csv('data/results/citation_rag_results.csv'); print(df.loc[0,'citation_rag_answer'])"

抽查输出如下：

Answer:

Evidence:

EECS 484_Database Management Systems_Winter 2021.pdf, page: 2, chunk_id: eecs_484_database_management_systems_winter_2021_p2_c1
Confidence:
The provided course documents do not specify this.
该输出包含 citation 信息，包括 source、page 和 chunk_id，说明 citation-constrained prompt 已成功影响模型输出格式。

当前阶段结论
本阶段已完成：

FAISS index 加载成功。
Chunk metadata 加载成功。
Citation-constrained RAG 脚本运行成功。
全部 80 条评测问题处理完成。
输出文件 citation_rag_results.csv 生成成功。
错误行数为 0。
抽查结果中包含 citation 信息。
本阶段最终状态：

Citation-constrained RAG experiment completed successfully.
Total questions: 80
Successful rows: 80
Error rows: 0
Output file: data/results/citation_rag_results.csv
实验记录摘要
Experiment name: Citation-constrained RAG
Retrieval backend: FAISS
Embedding backend: Ollama nomic-embed-text
Embedding dimension: 768
Number of indexed chunks: 693
Top-k: 5
Generation model: Ollama qwen2.5:3b
Input questions: data/questions/questions_with_reference.csv
Number of questions: 80
Output file: data/results/citation_rag_results.csv
Error rows: 0
Final status: Completed successfully

Local model selection completed. The local experiments used Ollama qwen2.5:3b as the generation model and nomic-embed-text as the embedding model. The local setup successfully supported the full experimental pipeline.

9.3 第 6 步：检查检索结果是否包含正确 Evidence
实验状态
本步骤已完成。

系统已基于 Basic RAG 的检索结果文件 data/results/basic_rag_results.csv，检查每个可回答问题的正确 evidence 是否出现在 top-k 检索结果中，并计算 retrieval recall。

本次实验生成结果文件：

data/results/retrieval_recall_results.csv
实验输入与输出
输入文件
data/results/basic_rag_results.csv
该文件包含 Basic RAG 阶段每个问题的检索结果，包括：

question_id
category
answerable
evidence_doc
retrieved_chunk_ids
retrieved_sources
retrieved_chunks
输出文件
data/results/retrieval_recall_results.csv
该文件记录每个问题的 evidence 命中情况，包括：

question_id
category
answerable
evidence_doc
retrieved_chunk_ids
retrieved_sources
retrieval_hit
match_type
运行结果
运行命令：

python src\evaluate_retrieval_recall.py

运行完成后输出结果如下：

Total questions: 80
Answerable questions: 70
Retrieval hits among answerable questions: 20
Retrieval recall@top_k: 0.2857
因此，本次 top-k retrieval recall 为：

Retrieval recall@top_k = 0.2857
即 70 个可回答问题中，有 20 个问题的正确 evidence 出现在 top-k 检索结果中。
各类别 Retrieval Recall
Category	Count	Hits	Recall
exception_handling	15	7	0.4667
factual_extraction	20	3	0.1500
multi_condition_reasoning	15	0	0.0000
rule_understanding	20	10	0.5000
未命中情况
在 70 个可回答问题中：

Retrieval hit: 20
Retrieval miss: 50
未命中的问题数量为 50 条，match_type 均为：

not_found
这表示这些问题的 evidence_doc 未能在 top-k 检索结果的 source 或 retrieved chunk text 中匹配到。

当前阶段结论
9.3 第 6 步已完成。

本阶段已完成内容：

检查 top-k 检索结果是否包含正确 evidence。
计算整体 retrieval recall。
计算不同问题类别下的 retrieval recall。
生成 retrieval_recall_results.csv。
识别未命中的 answerable questions。
最终记录：

Total questions: 80
Answerable questions: 70
Retrieval hits: 20
Retrieval misses: 50
Retrieval recall@top_k: 0.2857
Output file: data/results/retrieval_recall_results.csv

# 9.5 阶段五：Kaggle 批量实验记录

## 实验目标

本阶段在 Kaggle 平台上执行完整批量实验，使用上传后的 questions、chunks、FAISS index 和相关 metadata 文件，运行四种实验设置，并保存每个问题对应的模型输出结果。

本阶段实验设置包括：

- Closed-book
- Full-context
- Basic RAG
- Citation-constrained RAG

---

## 实验环境

实验平台：

- Kaggle Notebook

运行设备：

- Tesla T4 GPU × 2

模型配置：

- Generation model: `Qwen/Qwen2.5-7B-Instruct`
- Embedding model: `nomic-ai/nomic-embed-text-v1.5`
- Retrieval top-k: `5`

数据集路径：

    /kaggle/input/datasets/williamjkyoung/edu-policy-qa-data

---

## 输入文件

Kaggle Dataset 中已成功上传并识别以下文件：

    questions_with_reference.csv
    chunks.jsonl
    documents.jsonl
    faiss.index
    chunk_metadata.jsonl
    kaggle_run_all_experiments.py

其中：

- `questions_with_reference.csv`：包含实验问题、类别、可回答性、参考答案和 evidence 信息。
- `chunks.jsonl`：保存切分后的文本 chunks。
- `documents.jsonl`：保存原始文档文本。
- `faiss.index`：用于 Basic RAG 和 Citation-constrained RAG 的向量检索索引。
- `chunk_metadata.jsonl`：保存 chunk_id、source、page 等检索元数据。
- `kaggle_run_all_experiments.py`：Kaggle 批量实验运行脚本。

---

## 实验步骤

### 1. 检查 Kaggle 运行环境

首先在 Kaggle Notebook 中检查 GPU 状态和输入文件。

GPU 检查结果显示 Kaggle 当前分配了两张 Tesla T4：

    Tesla T4 × 2

输入文件检查结果确认数据集完整，所有实验所需文件均已存在。

---

### 2. 安装依赖

在 Kaggle Notebook 中安装实验所需依赖：

    transformers
    accelerate
    bitsandbytes
    sentence-transformers
    faiss-cpu

依赖安装完成后，实验脚本可以正常加载模型、embedding 模型和 FAISS index。

---

### 3. 修正并复制实验脚本

实验脚本从 Kaggle Dataset 路径复制到 working directory：

    /kaggle/working/kaggle_run_all_experiments.py

同时确认脚本中的数据路径已修正为：

    DATA_DIR = Path("/kaggle/input/datasets/williamjkyoung/edu-policy-qa-data")

脚本关键配置如下：

    MODEL_NAME = "Qwen/Qwen2.5-7B-Instruct"
    EMBEDDING_MODEL_NAME = "nomic-ai/nomic-embed-text-v1.5"
    TOP_K = 5

---

### 4. 运行四种实验设置

实验脚本对全部 80 个问题分别运行四种设置：

| Setting | Description |
|---|---|
| `closed_book` | 不提供外部文档，仅依靠模型自身知识回答 |
| `full_context` | 将完整文档上下文提供给模型回答 |
| `basic_rag` | 先检索 top-k chunks，再基于检索内容回答 |
| `citation_rag` | 先检索 top-k chunks，再要求模型输出带 citation 的答案 |

每个问题在每种设置下都会生成一条结果记录。

---

## 输出文件

实验完成后，Kaggle 生成以下结果文件：

    /kaggle/working/results/kaggle_all_experiment_results.csv
    /kaggle/working/results/kaggle_all_experiment_results.jsonl

同时将结果打包为：

    /kaggle/working/kaggle_results.zip

输出文件大小：

| File | Size |
|---|---:|
| `kaggle_all_experiment_results.csv` | 1.3M |
| `kaggle_all_experiment_results.jsonl` | 1.3M |
| `kaggle_results.zip` | 356K |

---

## 实验结果统计

本次实验共包含：

- 问题数量：80
- 实验设置数量：4
- 总输出记录数：320

运行结果如下：

| Metric | Value |
|---|---:|
| Total rows | 320 |
| Error records | 0 |

各实验设置的输出数量如下：

| Setting | Records |
|---|---:|
| `basic_rag` | 80 |
| `citation_rag` | 80 |
| `closed_book` | 80 |
| `full_context` | 80 |

所有设置均成功运行，没有出现错误记录。

---

## 输出字段格式

最终输出文件采用统一结构，每条记录包含以下字段：

    question_id
    category
    answerable
    setting
    question
    model_answer
    retrieved_chunks
    reference_answer
    evidence_doc
    model_name
    error

其中：

- `question_id`：问题编号。
- `category`：问题类别。
- `answerable`：该问题是否可由文档回答。
- `setting`：当前实验设置。
- `question`：输入问题。
- `model_answer`：模型生成答案。
- `retrieved_chunks`：RAG 设置下检索到的 chunks。
- `reference_answer`：人工参考答案。
- `evidence_doc`：标准 evidence 所在文档。
- `model_name`：使用的模型名称。
- `error`：运行错误信息。

JSONL 文件已验证可以正常读取，共包含：

    JSONL rows: 320

---

## 样例输出观察

以 Q001 为例，问题为：

    What office hours are stated for Federal Budgeting Process in Spring 2023?

参考答案为：

    Office hours are by appointment.

不同设置下的表现如下：

| Setting | Output Observation |
|---|---|
| `closed_book` | 模型无法获得具体课程信息，给出较泛化回答 |
| `full_context` | 能够基于完整上下文回答出 office hours 信息 |
| `basic_rag` | 依赖检索 chunks，如果检索内容不足，回答可能偏保守 |
| `citation_rag` | 输出包含 Answer、Evidence 和 citation 信息 |

该样例说明，closed-book 设置容易缺乏具体课程事实，而 full-context 和 citation-rag 更容易利用文档证据生成答案。

---

## 实验结论

本阶段 Kaggle 批量实验已成功完成。

本阶段确认：

- Kaggle Dataset 已成功上传并挂载。
- Kaggle Notebook 能够正常访问所有输入文件。
- GPU 环境可用。
- 7B 指令模型成功加载并完成推理。
- Embedding 模型和 FAISS index 成功用于 RAG 检索。
- 四种实验设置均完整运行。
- 每个问题的模型输出均已保存。
- CSV 和 JSONL 两种格式均成功生成。
- 输出记录数量正确，共 320 条。
- 错误记录数量为 0。
- 结果已打包为 `kaggle_results.zip`，可下载回本地用于后续评估。

最终结果文件：

    kaggle_all_experiment_results.csv
    kaggle_all_experiment_results.jsonl
    kaggle_results.zip

