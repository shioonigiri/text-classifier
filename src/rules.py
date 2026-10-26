"""カテゴリ分類のルールベース（v1）。

キーワード辞書でスコアリングし、最もスコアの高いカテゴリを返す。
辞書は実データの頻出語をもとに育てる（評価結果を見て追加・調整する）。
"""

# カテゴリごとのキーワード辞書（初期版）
KEYWORDS: dict[str, list[str]] = {
    "選考・締切": ["応募締切", "エントリー", "面接", "選考", "提出期限", "締切"],
    "就活案内": ["説明会", "インターンシップ", "オープンカンパニー", "座談会", "セミナー"],
    "授業・課題": ["課題", "レポート", "授業", "休講", "教室変更", "成績"],
    "奨学金・手続き": ["奨学金", "留学", "申請", "手続き", "奨学生"],
    "セキュリティ・ログイン": ["ログイン", "パスワード", "認証", "セキュリティ", "確認コード"],
    "支払い・請求": ["請求", "支払い", "利用明細", "口座", "料金"],
}

DEFAULT_CATEGORY = "その他"


def score_categories(text: str) -> dict[str, int]:
    """テキスト中のキーワード出現数でカテゴリ別スコアを返す。"""
    return {
        category: sum(text.count(word) for word in words)
        for category, words in KEYWORDS.items()
    }


def classify_by_rules(text: str) -> tuple[str, float, list[str]]:
    """(カテゴリ, 確信度, 根拠キーワード) を返す。

    TODO: 確信度の計算方法を評価結果に合わせて調整する。
    """
    scores = score_categories(text)
    best = max(scores, key=scores.get)
    if scores[best] == 0:
        return DEFAULT_CATEGORY, 0.0, []
    evidence = [w for w in KEYWORDS[best] if w in text]
    total = sum(scores.values())
    confidence = scores[best] / total if total else 0.0
    return best, confidence, evidence
