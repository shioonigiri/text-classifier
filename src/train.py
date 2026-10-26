"""v2（機械学習）の学習と比較評価。

学習データが少ないため、評価は層化交差検証（Stratified K-Fold）で行う。
全データを学習と評価に順番に使い回すことで、56件でも公平に測れる。
v1（ルールベース）の結果も同じデータで出し、比較表を results/ に保存する。

使い方:
    python -m src.train
"""
from datetime import date
from pathlib import Path

from sklearn.model_selection import StratifiedKFold, cross_val_predict

from .evaluate import CATEGORIES, evaluate, load_data, summarize, to_markdown
from .ml import build_pipeline


def macro_f1(result: dict) -> float:
    f1s = [result["per_category"][c]["f1"] for c in CATEGORIES]
    return sum(f1s) / len(f1s)


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    rows = load_data(root / "data" / "samples" / "eval.csv")
    texts = [r["text"] for r in rows]
    labels = [r["category"] for r in rows]

    # v1
    v1 = evaluate(rows)

    # v2: 交差検証で全件分の予測を作る
    skf = StratifiedKFold(n_splits=4, shuffle=True, random_state=42)
    predictions = cross_val_predict(build_pipeline(), texts, labels, cv=skf)
    v2 = summarize(rows, [str(p) for p in predictions])

    print(f"v1 正解率: {v1['accuracy']:.1%} / マクロF1: {macro_f1(v1):.2f}")
    print(f"v2 正解率: {v2['accuracy']:.1%} / マクロF1: {macro_f1(v2):.2f}（交差検証）")

    # 比較ファイル（v2 の詳細つき）
    header = [
        f"# v1 / v2 比較 {date.today().isoformat()}",
        "",
        "| バージョン | 方式 | 正解率 | マクロF1 |",
        "|---|---|---:|---:|",
        f"| v1 | ルールベース（キーワード辞書） | {v1['accuracy']:.1%} | {macro_f1(v1):.2f} |",
        f"| v2 | 機械学習（文字n-gram TF-IDF + ロジスティック回帰、4分割交差検証） | {v2['accuracy']:.1%} | {macro_f1(v2):.2f} |",
        "",
        "## 評価方法の注意",
        "",
        "- v1 は辞書を作ったデータと相性が良い合成データで測っているため高めに出る",
        "- v2 は交差検証（学習に使っていないデータで予測）で測っているため、素の実力に近い",
        "- 学習データが56件と少ない。実データが増えれば v2 が伸びる余地が大きい",
        "",
    ]
    detail = to_markdown(v2, "eval.csv", title="v2 機械学習（交差検証）")
    detail_body = "\n".join(detail.split("\n")[1:])  # 見出し行を比較表に差し替え
    out = root / "results" / f"{date.today().isoformat()}_v2-ml.md"
    out.write_text("\n".join(header) + detail_body, encoding="utf-8")
    print(f"比較結果を保存しました: {out}")


if __name__ == "__main__":
    main()
