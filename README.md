# メモ


- Python3.8

必要なモジュール
- numpy
- scipy
- gensim
- janome



~~Building fastText for Python~~　(Pythonから読み込む必要ないので以下必要なし。自前で学習モデル作る場合は別途ビルドしてexeを使う)

```
$ pip install Cython
$ git clone https://github.com/facebookresearch/fastText.git
$ cd fastText
$ pip install .
```


~~日本語学習済みモデル(5GBくらいある)~~　（このモデルだとうまくいかなかった）

- ~~https://s3-us-west-1.amazonaws.com/fasttext-vectors/wiki.ja.zip~~


fastTextの学習済みモデルを公開しました
- https://qiita.com/Hironsan/items/513b9f93752ecee9e670

モデル読み込み
```
model = gensim.models.KeyedVectors.load_word2vec_format('./vector/model.vec', binary=False)
```


文章の重要度順に並べる
```
import textsummarize
textsummarize.summarize({要約したい文章}, model)
```

Python: オブジェクトを漬物 (Pickle) にする
- http://blog.amedama.jp/entry/2015/12/05/132520


## 学習モデルの作成方法について

FacebookのfastTextでFastに単語の分散表現を獲得する
- https://qiita.com/icoxfog417/items/42a95b279c0b7ad26589

fastText
- https://fasttext.cc/
