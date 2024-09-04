# gtfs-jp

静的バス情報フォーマット（GTFS-JP）形式の読み取り、書き出し用ライブラリ。

## サポートされているファイル形式 / Supported file types

* [静的バス情報フォーマット（GTFS-JP）仕様書［第3版］](https://www.mlit.go.jp/sogoseisaku/transport/content/001419163.pdf)準拠のもの


## 使い方 / Usage

```python
from gtfs_jp import GTFSJP

gtfs = GTFSJP("meronking_line.zip")
for stop in gtfs.stops:
    print(stop.stop_name)
```
