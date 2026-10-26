"""抽出モジュールのテスト。実装ステップに合わせて中身を増やす。"""
from src.extract import extract_amount, extract_deadline, extract_action


def test_extract_functions_callable():
    # 未実装の間は None を返す（ステップ2・3で実ケースに差し替える）
    assert extract_amount("サンプル文章") is None
    assert extract_deadline("サンプル文章") is None
    assert extract_action("サンプル文章") is None
