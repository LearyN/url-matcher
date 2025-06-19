
import pandas as pd
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.ttk import Combobox
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os
import sys

try:
    from sentence_transformers import SentenceTransformer, util
    has_sentence_transformers = True
except ImportError:
    has_sentence_transformers = False

def match_titles(df, method="semantic"):
    # 去重获取所有 old 和 new 列表
    old_df = df[["old_url", "old_title"]].dropna().drop_duplicates().reset_index(drop=True)
    new_df = df[["new_url", "new_title"]].dropna().drop_duplicates().reset_index(drop=True)

    old_titles = old_df["old_title"].astype(str).tolist()
    new_titles = new_df["new_title"].astype(str).tolist()

    if method == "semantic" and has_sentence_transformers:
        model = SentenceTransformer("all-MiniLM-L6-v2")
        old_embeddings = model.encode(old_titles, convert_to_tensor=True, show_progress_bar=True)
        new_embeddings = model.encode(new_titles, convert_to_tensor=True, show_progress_bar=True)

        matches = []
        for i, old_emb in enumerate(old_embeddings):
            scores = util.pytorch_cos_sim(old_emb, new_embeddings)[0]  # 修复核心 bug
            best_idx = scores.argmax().item()
            best_score = scores[best_idx].item()

            matches.append({
                "old_url": old_df.loc[i, "old_url"],
                "old_title": old_titles[i],
                "matched_new_url": new_df.loc[best_idx, "new_url"],
                "matched_new_title": new_titles[best_idx],
                "similarity": round(best_score, 4)
            })

        return pd.DataFrame(matches)

    elif method == "tfidf":
        old_texts = old_df["old_title"].astype(str).tolist()
        new_texts = new_df["new_title"].astype(str).tolist()

        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(old_texts + new_texts)
        old_matrix = tfidf_matrix[:len(old_texts)]
        new_matrix = tfidf_matrix[len(old_texts):]

        sim_matrix = cosine_similarity(old_matrix, new_matrix)
        best_idx = np.argmax(sim_matrix, axis=1)

        matched_df = pd.DataFrame({
            "old_url": old_df["old_url"],
            "old_title": old_df["old_title"],
            "matched_new_url": new_df["new_url"].iloc[best_idx].values,
            "matched_new_title": new_df["new_title"].iloc[best_idx].values,
            "similarity": sim_matrix[np.arange(len(old_df)), best_idx]
        })
        return matched_df

    else:
        raise ValueError("Unsupported method or missing sentence-transformers package.")

def run_gui():
    def on_browse():
        file_path.set(filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")]))

    def on_run():
        try:
            input_path = file_path.get()
            if not os.path.exists(input_path):
                raise FileNotFoundError("文件未找到")
            try:
                with open(input_path, encoding="utf-8", errors="replace") as f:
                    df = pd.read_csv(f)
            except TypeError:
                df = pd.read_csv(input_path, encoding="utf-8")
            method = algo_choice.get()
            result = match_titles(df, method)
            save_path = os.path.splitext(input_path)[0] + f"_{method}_matched.csv"
            result.to_csv(save_path, index=False, encoding="utf-8-sig")
            messagebox.showinfo("完成", f"匹配完成，结果已保存到：\n{save_path}")
            os.startfile(save_path)
        except Exception as e:
            messagebox.showerror("出错", str(e))

    root = tk.Tk()
    root.title("URL 匹配工具")
    root.geometry("500x200")

    tk.Label(root, text="选择输入 CSV 文件：").pack(pady=5)
    file_path = tk.StringVar()
    tk.Entry(root, textvariable=file_path, width=50).pack()
    tk.Button(root, text="浏览", command=on_browse).pack(pady=5)

    tk.Label(root, text="选择匹配算法：").pack(pady=5)
    algo_choice = Combobox(root, values=["semantic", "tfidf"])
    algo_choice.set("semantic" if has_sentence_transformers else "tfidf")
    algo_choice.pack()

    tk.Button(root, text="开始匹配", command=on_run, bg="blue", fg="white").pack(pady=15)

    root.mainloop()

if __name__ == "__main__":
    run_gui()
