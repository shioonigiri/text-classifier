"""v2（機械学習）のスモークテスト。"""
import csv
from pathlib import Path

from src.ml import MLClassifier

ROOT = Path(__file__).resolve().parents[1]


def _load(name: str) -> list[dict]:
    with (ROOT / "data" / "samples" / name).open(encoding="utf-8") as f:
        return list(csv.DictReader(f))


def test_fit_and_predict():
    rows = _load("eval.csv")
    clf = MLClassifier().fit([r["text"] for r in rows], [r["category"] for r in rows])
    predicted, confidence = clf.predict_with_confidence("合同企業説明会のご案内です。採用担当が参加します。")
    assert predicted in {r["category"] for r in rows}
    assert 0.0 <= confidence <= 1.0


def test_predict_obvious_case():
    rows = _load("eval.csv")
    clf = MLClassifier().fit([r["text"] for r in rows], [r["category"] for r in rows])
    assert clf.predict("新しい端末からのログインを確認しました。パスワードを変更してください。") == "セキュリティ・ログイン"
