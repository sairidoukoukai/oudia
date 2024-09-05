# oudia

OuDiaファイル形式の読み取り、書き出し用ライブラリ。

A library for parsing and exporting OuDia file format.

## サポートされているファイル形式 / Supported file types

* [OuDia](http://take-okm.a.la9.jp/oudia/)
* [OuDiaSecond](http://oudiasecond.seesaa.net/)

## 使い方 / Usage

```python
import oudia

with open("meronking_line.oud", "r") as f:
    dia = oudia.load(f)
    print(dia.file_type)
    print(dia.rosen)
```

## 参考 / References

* [OuDia](http://take-okm.a.la9.jp/oudia/)
* [OuDiaSecond](http://oudiasecond.seesaa.net/)
* [AOdia](https://kamelong.com/aodia/)
* [CloudDia](http://onemu.starfree.jp/clouddia/)
