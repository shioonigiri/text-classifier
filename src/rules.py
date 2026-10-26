"""カテゴリ分類のルールベース（v1）。

キーワード辞書でスコアリングし、最もスコアの高いカテゴリを返す。
辞書は実データの頻出語をもとに育てる（評価結果を見て追加・調整する）。
"""
# カテゴリごとのキーワード辞書
KEYWORDS: dict[str, list[str]] = {
    "選考・締切": ["応募締切", "エントリー", "面接", "面談", "選考", "書類選考", "結果", "提出期限", "締切"],
    "就活案内": ["説明会", "会社説明会", "インターンシップ", "オープンカンパニー", "座談会", "セミナー", "採用", "募集"],
    "授業・課題": ["課題", "レポート", "授業", "講義", "休講", "教室変更", "成績", "試験"],
    "奨学金・手続き": ["奨学金", "留学", "申請", "手続き", "奨学生", "願書", "届出"],
    "セキュリティ・ログイン": ["ログイン", "パスワード", "認証", "セキュリティ", "確認コード", "本人確認", "ワンタイム"],
    "支払い・請求": ["請求", "支払い", "利用明細", "口座", "料金", "振替", "決済", "領収書"],
}

# 同点のときの優先順位（行動が必要なカテゴリを優先する）
PRIORITY: list[str] = [
    "選考・締切",
    "支払い・請求",
    "奨学金・手続き",
    "授業・課題",
    "就活案内",
    "セキュリティ・ログイン",
]

DEFAULT_CATEGORY = "その他"


def score_categories(text: str) -> dict[str, int]:
    """テキスト中のキーワード出現数でカテゴリ別スコアを返す。"""
    return {
        category: sum(text.count(word) for word in words)
        for category, words in KEYWORDS.items()
    }


def classify_by_rules(text: str) -> tuple[str, float, list[str]]:
    """(カテゴリ, 確信度, 根拠キーワード) を返す。

    確信度は「最上位カテゴリのスコア ÷ 全スコア」。同点の場合は
    PRIORITY の順で決める。根拠はテキスト中の出現順に並べる。
    """
    scores = score_categories(text)
    ranked = sorted(
        scores.items(),
        key=lambda kv: (-kv[1], PRIORITY.index(kv[0]) if kv[0] in PRIORITY else len(PRIORITY)),
    )
    best, best_score = ranked[0]
    if best_score == 0:
        return DEFAULT_CATEGORY, 0.0, []
    evidence = sorted((w for w in KEYWORDS[best] if w in text), key=text.index)
    total = sum(scores.values())
    confidence = best_score / total if total else 0.0
    return best, confidence, evidence
