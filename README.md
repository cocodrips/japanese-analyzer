## 必要なもの
- mecab

## モジュール
1. mecab_parser macabの出力結果をオブジェクトにする
2. morpheme_merger 定義した形態素組み合わせルールのみを抜き出す 

## インストール

```
python setup.py install
```

## テスト

リポジトリルートで以下を実行
```
pytest
```

## 使い方 
```python

from morpheme_merger import MorphemeMerger
mm = MorphemeMerger()
mm.set_rule_from_excel('rule path')

words, posses = mm.get_rule_pattern('XXXX')
print (words)
```

