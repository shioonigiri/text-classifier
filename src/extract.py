"""期限・金額・行動項目の抽出（正規表現ベース）。

抽出系はルールが強いため、v2（機械学習）でもこのモジュールを併用する。
"""
import re
from datetime import date

# 金額: 「12,000円」「¥12,000」「12000円」など
AMOUNT_PATTERN = re.compile(
    r"[¥￥]\s?(\d{1,3}(?:,\d{3})+|\d+)|(\d{1,3}(?:,\d{3})+|\d+)\s?円"
)
# 金額（万円単位）: 「400万円」「1.5万円」など
MAN_AMOUNT_PATTERN = re.compile(r"(\d+(?:\.\d+)?)\s?万円")

# 日付（年あり）: 「2026年11月23日」「2026/11/23」
FULL_DATE_PATTERN = re.compile(
    r"(?P<year>20\d{2})[年/](?P<month>\d{1,2})[月/](?P<day>\d{1,2})日?"
)
# 日付（年なし・漢字）: 「11月23日」
MONTH_DAY_PATTERN = re.compile(r"(?P<month>\d{1,2})月(?P<day>\d{1,2})日")
# 日付（年なし・スラッシュ）: 「11/23」
SLASH_DATE_PATTERN = re.compile(r"(?<!\d)(?P<month>\d{1,2})/(?P<day>\d{1,2})(?!\d)")

# 期限を示すキーワード（直後に日付があれば、それを期限とみなす）
DEADLINE_KEYWORDS = ("締切", "期限", "必着", "締め切り")

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
    """金額（円）を抽出する。見つからなければ None。

    「万円」表記は円に換算する。年（2026年など）は金額として拾わない。
    """
    m = MAN_AMOUNT_PATTERN.search(text)
    if m:
        return int(float(m.group(1)) * 10000)
    m = AMOUNT_PATTERN.search(text)
    if m:
        num = m.group(1) or m.group(2)
        return int(num.replace(",", ""))
    return None


def _to_iso(year: int, month: int, day: int) -> str | None:
    try:
        return date(year, month, day).isoformat()
    except ValueError:
        return None


def _infer_year(month: int, day: int, today: date) -> str | None:
    """年がない日付は、今年（過ぎていれば来年）とみなす。"""
    iso = _to_iso(today.year, month, day)
    if iso is None:
        return None
    if date(today.year, month, day) < today:
        return _to_iso(today.year + 1, month, day)
    return iso


def _find_dates(text: str, today: date) -> list[tuple[int, str]]:
    """(出現位置, ISO日付) の一覧を返す。"""
    found: list[tuple[int, str]] = []
    for m in FULL_DATE_PATTERN.finditer(text):
        iso = _to_iso(int(m.group("year")), int(m.group("month")), int(m.group("day")))
        if iso:
            found.append((m.start(), iso))
    for pattern in (MONTH_DAY_PATTERN, SLASH_DATE_PATTERN):
        for m in pattern.finditer(text):
            # 年あり表記と重なる位置は二重に数えない
            if any(abs(m.start() - pos) < 6 for pos, _ in found):
                continue
            iso = _infer_year(int(m.group("month")), int(m.group("day")), today)
            if iso:
                found.append((m.start(), iso))
    return sorted(found)


def extract_deadline(text: str, today: date | None = None) -> str | None:
    """期限の日付を ISO 形式（YYYY-MM-DD）で返す。見つからなければ None。

    ルール:
    - 日付が複数ある場合、「締切・期限・必着」の直後（12文字以内）にある日付を優先する
    - 年がない日付は今年とみなし、過ぎていれば来年にする
    - 「来週金曜」等の相対表現は未対応（将来の課題）
    """
    if today is None:
        today = date.today()
    dates = _find_dates(text, today)
    if not dates:
        return None
    for pos, iso in dates:
        window = text[max(0, pos - 12):pos]
        if any(kw in window for kw in DEADLINE_KEYWORDS):
            return iso
    return dates[0][1]


def extract_action(text: str) -> str | None:
    """必要な行動を抽出する。見つからなければ None。"""
    # TODO: 実装（ステップ3でカテゴリ分類と合わせて調整）
    return None
