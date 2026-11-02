"""v3（単語ベース）の学習と比較評価。

v2 と同じ評価条件（層化4分割交差検証、random_state=42）で
v1（ルール）/ v2（文字 n-gram）/ v3（単語ベース）を比較し、
結果を results/ に保存する。

使い方:
    python -m src.train_v3
"""
from datetime import date
from pathlib import Path

from sklearn.model_selection import StratifiedKFold, cross_val_predict

from .evaluate import CATEGORIES, evaluate, load_data, summarize, to_markdown
from .ml import build_pipeline
from .ml_words import build_word_pipeline


def macro_f1(result: dict) -> float:
    f1s = [result["per_category"][c]["f1"] for c in CATEGORIES]
    return sum(f1s) / len(f1s)


def comparison_markdown(v1: dict, v2: dict, v3: dict, data_name: str) -> str:
    lines = [
        f"# v1 / v2 / v3 比較 {date.today().isoformat()}",
        "",
        "| バージョン | 方式 | 正解率 | マクロF1 |",
        "|---|---|---:|---:|",
        f"| v1 | ルールベース（キーワード辞書） | {v1['accuracy']:.1%} | {macro_f1(v1):.2f} |",
        f"| v2 | 機械学習（文字n-gram TF-IDF + ロジスティック回帰、4分割交差検証） | {v2['accuracy']:.1%} | {macro_f1(v2):.2f} |",
        f"| v3 | 機械学習（SudachiPy分かち書き 単語unigram TF-IDF + ロジスティック回帰、4分割交差検証） | {v3['accuracy']:.1%} | {macro_f1(v3):.2f} |",
        "",
        "## 評価方法の注意",
        "",
        "- v1 は辞書を作ったデータと相性が良い合成データで測っているため高めに出る",
        "- v2 / v3 は交差検証（学習に使っていないデータで予測）で測っているため、素の実力に近い",
        "- 学習データが56件と少ない。v2 と v3 の差が数件分しかない場合は、優劣の断定はできない",
        f"- データ: {data_name}（56件）",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    rows = load_data(root / "data" / "samples" / "eval.csv")
    texts = [r["text"] for r in rows]
    labels = [r["category"] for r in rows]

    v1 = evaluate(rows)

    skf = StratifiedKFold(n_splits=4, shuffle=True, random_state=42)
    v2_pred = cross_val_predict(build_pipeline(), texts, labels, cv=skf)
    v2 = summarize(rows, [str(p) for p in v2_pred])

    skf = StratifiedKFold(n_splits=4, shuffle=True, random_state=42)
    v3_pred = cross_val_predict(build_word_pipeline(), texts, labels, cv=skf)
    v3 = summarize(rows, [str(p) for p in v3_pred])

    print(f"v1 正解率: {v1['accuracy']:.1%} / マクロF1: {macro_f1(v1):.2f}")
    print(f"v2 正解率: {v2['accuracy']:.1%} / マクロF1: {macro_f1(v2):.2f}（交差検証）")
    print(f"v3 正解率: {v3['accuracy']:.1%} / マクロF1: {macro_f1(v3):.2f}（交差検証）")

    today = date.today().isoformat()
    out_path = root / "results" / f"{today}_v3-sudachi.md"
    detail = to_markdown(v3, "eval.csv", title="v3 単語ベース（SudachiPy）")
    out_path.write_text(comparison_markdown(v1, v2, v3, "eval.csv") + "\n" + detail, encoding="utf-8")
    print(f"結果を保存しました: {out_path}")


if __name__ == "__main__":
    main()
