"""抽出モジュールのテスト（実ケース）。"""
from datetime import date

from src.extract import extract_amount, extract_deadline, extract_action

TODAY = date(2026, 10, 26)


# --- 金額 ---
def test_amount_yen_with_comma():
    assert extract_amount("今月分の請求金額は12,000円です。") == 12000


def test_amount_yen_symbol():
    assert extract_amount("受講料は ¥3,500 となります。") == 3500


def test_amount_man_en():
    assert extract_amount("初任給は月給25万円、年収は400万円程度です。") == 250000


def test_amount_none():
    assert extract_amount("説明会のご案内です。") is None


def test_amount_does_not_match_year():
    assert extract_amount("2026年11月23日に開催します。") is None


# --- 期限 ---
def test_deadline_month_day():
    assert extract_deadline("応募締切は11月23日です。", today=TODAY) == "2026-11-23"


def test_deadline_full_date_slash():
    assert extract_deadline("申込は2026/12/20 23:59までにお願いします。", today=TODAY) == "2026-12-20"


def test_deadline_full_date_kanji():
    assert extract_deadline("期限は2027年2月15日です。", today=TODAY) == "2027-02-15"


def test_deadline_rolls_to_next_year():
    assert extract_deadline("提出期限は1月10日です。", today=TODAY) == "2027-01-10"


def test_deadline_prefers_keyword_date():
    text = "座談会は11月11日16:00からです。予約の締切は11月9日となります。"
    assert extract_deadline(text, today=TODAY) == "2026-11-09"


def test_deadline_none():
    assert extract_deadline("説明会のご案内です。", today=TODAY) is None


def test_deadline_invalid_date():
    assert extract_deadline("期限は13月40日です。", today=TODAY) is None


# --- 行動 ---
def test_action_oubo():
    assert extract_action("期日までに応募してください。") == "応募"


def test_action_teishutsu():
    assert extract_action("レポートの提出をお願いします。") == "提出"


def test_action_sanka_touroku():
    assert extract_action("参加登録はこちらから行ってください。") == "参加登録"


def test_action_henshin():
    assert extract_action("お早めに返信をお願いいたします。") == "返信"


def test_action_furikomimi():
    assert extract_action("指定の口座へお振込みください。") == "支払い"


def test_action_prefers_requested_verb():
    # 依頼表現（ください）が付いた方を優先する
    text = "申込書を提出し、参加費を支払ってください。"
    assert extract_action(text) == "支払い"


def test_action_none():
    assert extract_action("説明会のご案内です。当日は各社の話を聞けます。") is None
