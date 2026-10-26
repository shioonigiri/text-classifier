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
