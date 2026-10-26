"""分類の入口。文章を受け取り、統一形式の dict を返す。"""
from .rules import classify_by_rules
from .extract import extract_amount, extract_deadline, extract_action


def classify_text(text: str) -> dict:
    """文章を分類し、抽出結果をまとめて返す。

    戻り値の形式:
        {
            "category": str,        # カテゴリ
            "deadline": str | None, # 期限（YYYY-MM-DD）
            "amount": int | None,   # 金額（円）
            "action": str | None,   # 必要な行動
            "confidence": float,    # 確信度 0〜1
            "evidence": list[str],  # 根拠になった語句
        }
    """
    category, confidence, evidence = classify_by_rules(text)
    return {
        "category": category,
        "deadline": extract_deadline(text),
        "amount": extract_amount(text),
        "action": extract_action(text),
        "confidence": confidence,
        "evidence": evidence,
    }


if __name__ == "__main__":
    sample = "1Dayインターンシップの応募締切は11月23日です。参加を希望する方は期日までに応募してください。"
    print(classify_text(sample))
