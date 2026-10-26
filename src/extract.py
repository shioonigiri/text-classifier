"""期限・金額・行動項目の抽出（正規表現ベース）。

抽出系はルールが強いため、v2（機械学習）でもこのモジュールを併用する。
"""
import re

# 金額: 「12,000円」「¥12,000」など
AMOUNT_PATTERN = re.compile(r"(?:¥|￥)?\s?(\d{1,3}(?:,\d{3})+|\d+)\s?円|(?:¥|￥)\s?(\d{1,3}(?:,\d{3})+|\d+)")

# 日付: 「2026年11月23日」「2026/11/23」「11月23日」など
DATE_PATTERN = re.compile(
    r"(?P<year>20\d{2})[年/](?P<month>\d{1,2})[月/](?P<day>\d{1,2})日?"
    r"|(?P<month2>\d{1,2})月(?P<day2>\d{1,2})日"
)

# 行動: 動詞パターン → 行動ラベル
ACTION_PATTERNS: dict[str, str] = {
    "提出": "提出",
    "申込": "申込",
    "申し込": "申込",
    "応募": "応募",
    "参加登録": "参加登録",
    "予約": "予約",
    "返信": "返信",
    "支払": "支払い",
    "振込": "支払い",
    "出席": "出席",
}


def extract_amount(text: str) -> int | None:
    """金額（円）を抽出する。見つからなければ None。"""
    # TODO: 実装（ステップ2）
    return None


def extract_deadline(text: str, today=None) -> str | None:
    """期限の日付を ISO 形式（YYYY-MM-DD）で返す。見つからなければ None。

    TODO: 実装（ステップ2）。「来週金曜」等の相対表現は後回し。
    """
    return None


def extract_action(text: str) -> str | None:
    """必要な行動を抽出する。見つからなければ None。"""
    # TODO: 実装（ステップ3でカテゴリ分類と合わせて調整）
    return None
