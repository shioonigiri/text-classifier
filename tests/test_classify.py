"""classify_text の出力形式を確認するスモークテスト。"""
from src.classify import classify_text


def test_output_structure():
    result = classify_text("説明会のご案内です。")
    assert set(result) == {"category", "deadline", "amount", "action", "confidence", "evidence"}
    assert isinstance(result["category"], str)
    assert 0.0 <= result["confidence"] <= 1.0
    assert isinstance(result["evidence"], list)


def test_keyword_category():
    result = classify_text("合同企業説明会のご案内です。")
    assert result["category"] == "就活案内"
    assert "説明会" in result["evidence"]


def test_full_pipeline():
    result = classify_text("今月分の請求金額は12,000円です。支払期限は11月9日となります。お振込みください。")
    assert result["category"] == "支払い・請求"
    assert result["amount"] == 12000
    assert result["deadline"] is not None
    assert result["action"] == "支払い"


def test_samples_csv_all_correct():
    # 合成サンプル全件でカテゴリが一致すること（評価の最小形）
    import csv
    from pathlib import Path

    path = Path(__file__).resolve().parents[1] / "data" / "samples" / "sample.csv"
    with path.open(encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    assert rows, "サンプルが空です"
    for row in rows:
        result = classify_text(row["text"])
        assert result["category"] == row["category"], f"不一致: {row['text'][:20]}… → {result['category']}（正解: {row['category']}）"
