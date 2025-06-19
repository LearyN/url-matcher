
# 🔧 URL Title Matching Tool / URL 标题匹配工具

A desktop tool for mapping old webpage titles to the most semantically similar new titles using sentence-transformers.  
一个用于将旧网页标题匹配到最相关新标题的桌面工具，支持语义模型匹配。

---

## 📂 Input Format / 输入格式

Input file must be a `.csv` with **four columns**:  
输入文件必须是 `.csv` 格式，且包含以下四列：

| Column Name | Description (EN)               | 描述（中文）               |
|-------------|--------------------------------|----------------------------|
| `old_url`   | URL of the original page       | 原始页面的链接              |
| `old_title` | Title of the original page     | 原始页面的标题              |
| `new_url`   | URL of the candidate new page  | 候选新页面的链接            |
| `new_title` | Title of the candidate new page| 候选新页面的标题            |

> ⚠ File should be saved in UTF-8 encoding (UTF-8 with BOM recommended for Excel).
> ⚠ 文件应使用 UTF-8 编码保存（推荐使用带 BOM 的 UTF-8 以兼容 Excel）。

---

## ⚙️ How to Use / 使用方法

1. Open the `.exe` file
2. Select your input `.csv` file
3. Choose matching algorithm: `semantic` (default) or `tfidf`
4. Click **Start Matching**
5. Results will be saved and automatically opened

1. 打开 `.exe` 文件  
2. 选择输入的 `.csv` 文件  
3. 选择匹配算法：`semantic`（默认）或 `tfidf`  
4. 点击【开始匹配】  
5. 程序将自动保存并打开匹配结果  

---

## 🧠 Matching Algorithms / 匹配算法说明

### ✅ Semantic (default) / 语义匹配（默认）

Uses pre-trained model `all-MiniLM-L6-v2` to compute sentence embeddings and find semantically similar titles.  
使用 `all-MiniLM-L6-v2` 模型进行句向量匹配，支持语言差异和表达变化。

### ✅ TF-IDF

Matches titles based on term frequency and cosine similarity. Faster but less flexible.  
基于关键词频率的快速匹配，速度快但容错低。

---

## 📤 Output Format / 输出格式

Output file is a `.csv` with the following columns:  
输出文件包含以下字段：

| Column | Description / 描述                       |
|--------|------------------------------------------|
| `old_url` | Original page URL / 原始链接         |
| `old_title` | Original title / 原始标题          |
| `matched_new_url` | Matched new page URL / 匹配的新链接 |
| `matched_new_title` | Matched title / 匹配的新标题 |
| `similarity` | Cosine similarity score / 相似度分数 |

---

## 🧪 Test Files / 测试文件

- `match_test_10x10.csv` (中文)
- `match_test_english_10x10.csv` (English)
- `match_test_10x10_shuffled.csv` (乱序测试)

---

## 🛠 Troubleshooting / 常见问题

| Issue / 问题                               | Solution / 解决方案                    |
|-------------------------------------------|-----------------------------------------|
| Garbled characters / 中文乱码             | Use UTF-8 with BOM encoding              |
| All matches point to the same new URL 全部匹配相同新链接 | Ensure input has diverse titles 内容应多样 |
| Program doesn't open / 程序打不开         | Repack with pyinstaller, allow in antivirus |
| Matching is slow / 匹配速度慢              | Wait for model loading (~30s–1min)      |

---

## 📦 Tech Stack / 技术栈

- Python 3.10+
- PyInstaller
- sentence-transformers
- pandas, scikit-learn, numpy
- tkinter

---

© 2025. All rights reserved.
