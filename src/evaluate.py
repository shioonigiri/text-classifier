"""精度評価。正解ラベル付きデータで正解率・F1・混同行列を出す。

使い方:
    python -m src.evaluate [CSVパス] [出力Markdownパス]
省略時は data/samples/eval.csv を評価し、results/ に日付つきで保存する。
"""
import csv
import sys
from collections import defaultdict
from datetime import date
from pathlib import Path

from .classify import classify_text

CATEGORIES = [
    "選考・締切",
    "就活案内",
    "授業・課題",
    "奨学金・手続き",
    "セキュリティ・ログイン",
    "支払い・請求",
    "その他",
]


def load_data(path: Path) -> list[dict]:
    with path.open(encoding="utf-8") as f:
        return list(csv.DictReader(f))


def evaluate(rows: list[dict]) -> dict:
    confusion: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    wrong: list[dict] = []
    correct = 0
    for row in rows:
        predicted = classify_text(row["text"])["category"]
        confusion[row["category"]][predicted] += 1
        if predicted == row["category"]:
            correct += 1
        else:
            wrong.append({"text": row["text"], "true": row["category"], "predicted": predicted})

    per_category = {}
    for cat in CATEGORIES:
        tp = confusion[cat][cat]
        fp = sum(confusion[other][cat] for other in CATEGORIES) - tp
        fn = sum(confusion[cat].values()) - tp
        precision = tp / (tp + fp) if (tp + fp) else 0.0
        recall = tp / (tp + fn) if (tp + fn) else 0.0
        f1 = 2 * precision * recall / (precision + recall) if (precision + recall) else 0.0
        per_category[cat] = {"precision": precision, "recall": recall, "f1": f1, "support": sum(confusion[cat].values())}

    return {
        "total": len(rows),
        "correct": correct,
        "accuracy": correct / len(rows) if rows else 0.0,
        "per_category": per_category,
        "confusion": {k: dict(v) for k, v in confusion.items()},
        "wrong": wrong,
    }


def to_markdown(result: dict, data_name: str) -> str:
    lines = [
        f"# 評価結果 {date.today().isoformat()}（v1 ルールベース）",
        "",
        f"- データ: {data_name}（{result['total']}件）",
        f"- 正解率: {result['accuracy']:.1%}（{result['correct']}/{result['total']}）",
        "",
        "## カテゴリ別指標",
        "",
        "| カテゴリ | 適合率 | 再現率 | F1 | 件数 |",
        "|---|---:|---:|---:|---:|",
    ]
    for cat in CATEGORIES:
        m = result["per_category"][cat]
        lines.append(f"| {cat} | {m['precision']:.2f} | {m['recall']:.2f} | {m['f1']:.2f} | {m['support']} |")
    lines += ["", "## 混同行列（行=正解、列=予測）", ""]
    lines.append("| 正解＼予測 | " + " | ".join(CATEGORIES) + " |")
    lines.append("|---|" + "---:|" * len(CATEGORIES))
    for true_cat in CATEGORIES:
        row = result["confusion"].get(true_cat, {})
        lines.append(f"| {true_cat} | " + " | ".join(str(row.get(pred, 0)) for pred in CATEGORIES) + " |")
    lines += ["", "## 誤分類した例", ""]
    if result["wrong"]:
        for w in result["wrong"]:
            lines.append(f"- 正解: {w['true']} / 予測: {w['predicted']} … {w['text']}")
    else:
        lines.append("（なし）")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    data_path = Path(sys.argv[1]) if len(sys.argv) > 1 else root / "data" / "samples" / "eval.csv"
    out_path = (
        Path(sys.argv[2])
        if len(sys.argv) > 2
        else root / "results" / f"{date.today().isoformat()}_v1-rules.md"
    )
    rows = load_data(data_path)
    result = evaluate(rows)
    md = to_markdown(result, data_path.name)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(md, encoding="utf-8")
    print(f"正解率: {result['accuracy']:.1%}（{result['correct']}/{result['total']}）")
    print(f"結果を保存しました: {out_path}")


if __name__ == "__main__":
    main()
