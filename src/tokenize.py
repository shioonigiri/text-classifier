"""SudachiPy による日本語の分かち書き。

内容語（名詞・動詞・形容詞・副詞）の辞書形をトークンとして返す。
助詞・助動詞・記号などは分類の手がかりになりにくいため除く。
分割モードは C（複合語をまとめる。例：「提出期限」を1トークンにする）。

辞書の読み込みは数秒かかるため、トークナイザは遅延生成して使い回す。
"""
from sudachipy import dictionary, tokenizer

_TOKENIZER = None
_MODE = tokenizer.Tokenizer.SplitMode.C
_KEEP_POS = {"名詞", "動詞", "形容詞", "副詞"}


def _get_tokenizer():
    global _TOKENIZER
    if _TOKENIZER is None:
        _TOKENIZER = dictionary.Dictionary().tokenizer()
    return _TOKENIZER


def tokenize_text(text: str) -> list[str]:
    """テキストを内容語の辞書形トークンのリストに変換する。"""
    tokens: list[str] = []
    for morpheme in _get_tokenizer().tokenize(text, _MODE):
        pos = morpheme.part_of_speech()
        if pos and pos[0] in _KEEP_POS:
            form = morpheme.dictionary_form()
            if form:
                tokens.append(form)
    return tokens
