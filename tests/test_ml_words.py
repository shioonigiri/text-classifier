"""v3（単語ベース分類・分かち書き）のテスト。"""
from src.ml_words import WordMLClassifier
from src.tokenize import tokenize_text


def test_tokenize_extracts_content_words():
    tokens = tokenize_text("エントリーシートの提出期限は今週金曜日です")
    assert "金曜日" in tokens
    # 助詞は含まれない
    assert "は" not in tokens
    assert "の" not in tokens


def test_tokenize_keeps_compound_as_one_token():
    # 分割モード C では複合語がまとまる
    tokens = tokenize_text("エントリーシートの提出期限は今週金曜日です")
    assert "提出期限" in tokens


def test_word_classifier_learns_and_predicts():
    texts = [
        "エントリーシートの提出期限について",
        "面接の日程を調整してください",
        "パスワードの再設定が必要です",
        "ログインに失敗しました",
    ]
    labels = ["選考・締切", "選考・締切", "セキュリティ・ログイン", "セキュリティ・ログイン"]
    clf = WordMLClassifier().fit(texts, labels)
    assert clf.predict("提出期限の確認") in {"選考・締切", "セキュリティ・ログイン"}
    label, conf = clf.predict_with_confidence("パスワードを忘れました")
    assert label in {"選考・締切", "セキュリティ・ログイン"}
    assert 0.0 < conf <= 1.0
