"""v3: 単語ベースの機械学習分類。

SudachiPy で分かち書きした単語（unigram）を TF-IDF で特徴量化し、
ロジスティック回帰で分類する。v2（文字 n-gram）と評価条件を揃えて比較する。
"""
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

from .tokenize import tokenize_text


def build_word_pipeline() -> Pipeline:
    # 特徴は単語 unigram。bigram を足す案も試したが、データが少ない局面では
    # 特徴が疎になって精度が下がった（results/2026-11-02_v3-sudachi.md 参照）。
    return Pipeline(
        [
            (
                "tfidf",
                TfidfVectorizer(
                    analyzer=tokenize_text,
                    min_df=1,
                ),
            ),
            ("clf", LogisticRegression(max_iter=1000)),
        ]
    )


class WordMLClassifier:
    """v2 の MLClassifier と同じインターフェースを持つ単語ベース分類器。"""

    def __init__(self) -> None:
        self.pipeline = build_word_pipeline()

    def fit(self, texts: list[str], labels: list[str]) -> "WordMLClassifier":
        self.pipeline.fit(texts, labels)
        return self

    def predict(self, text: str) -> str:
        return str(self.pipeline.predict([text])[0])

    def predict_with_confidence(self, text: str) -> tuple[str, float]:
        proba = self.pipeline.predict_proba([text])[0]
        return str(self.pipeline.classes_[proba.argmax()]), float(proba.max())
