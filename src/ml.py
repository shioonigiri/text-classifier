"""v2: 機械学習によるカテゴリ分類。

日本語は分かち書き（形態素解析）が別途必要になるため、文字 n-gram の
TF-IDF で特徴量化し、ロジスティック回帰で分類する。形態素解析器なしで
動く構成にしてある。
"""
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline


def build_pipeline() -> Pipeline:
    return Pipeline(
        [
            ("tfidf", TfidfVectorizer(analyzer="char_wb", ngram_range=(2, 4), min_df=1)),
            ("clf", LogisticRegression(max_iter=1000)),
        ]
    )


class MLClassifier:
    """学習済みパイプラインの薄いラッパー。"""

    def __init__(self) -> None:
        self.pipeline = build_pipeline()

    def fit(self, texts: list[str], labels: list[str]) -> "MLClassifier":
        self.pipeline.fit(texts, labels)
        return self

    def predict(self, text: str) -> str:
        return str(self.pipeline.predict([text])[0])

    def predict_with_confidence(self, text: str) -> tuple[str, float]:
        proba = self.pipeline.predict_proba([text])[0]
        return str(self.pipeline.classes_[proba.argmax()]), float(proba.max())
