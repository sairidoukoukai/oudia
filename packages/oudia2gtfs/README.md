# oudia2gtfs

OuDiaファイル形式をGTFS形式に変換するライブラリ。

A library for converting OuDia file to GTFS files.

## サポートされているファイル形式 / Supported file types

* [OuDia](http://take-okm.a.la9.jp/oudia/)
* [OuDiaSecond](http://oudiasecond.seesaa.net/)

* [GTFS-JP](https://gtfs.jp/)

## 制約 / Limitations

OuDia/OuDiaSecondとGTFS-JPとは大きく異なり、互換性がないフォーマットであるため、本ライブラリは、OuDia/OuDiaSecondからGTFS-JPへの変換に際して、読み取れる限りのデータを対応させ、変換を行っておりますが、GTFS-JPに非対応のOuDia/OuDiaSecond情報は捨て去られ、逆にOuDia/OuDiaSecond非対応のGTFS-JP情報は新しく作ることができないので、変換して得たGTFS-JPは不完全であり、不足するデータ手動で補足しなければなりません。即ち、この変換ツールによって得られたGTFS-JPデータはあくまで叩き台であり、そのまま利用することはできません。本章では、それぞれの要素について言及し、修正すべきデータの指針として提供します。

### 駅（`Eki`→`Stop`）

#### OuDia/OudiaSecond対応GTFS-JP非対応

##### OuDia
* 駅時刻形式（`Ekijikokukeisiki`、必須）
* 駅規模（`Ekikibo`、必須）

##### OuDiaSecond
* 下り主本線（`DownMain`、必須）
* 下り主本線（`DownMain`、必須）
* 

### OuDia非対応GTFS-JP対応

（GTFSで必須か任意のものがGTFS-JPでは不要なものについては省略、以下同じ）

* 停留留所・標柱ID（`stop_id`、必須） ※ユーザー定義の`generate_stop_id()`（デフォルトは駅の順番の数字）によって自動生成される
* 停留留所・標柱ID（`stop_code`、任意）
* 緯度（`stop_lat`、必須）※`0.0`が自動的に置かれる
* 経度（`stop_lon`、必須）※`0.0`が自動的に置かれる
* 運賃エリアID（`zone_id`、任意）
* 停留所・標柱URL（`stop_url`、任意）
* 停留所・標柱区分（`location_type`、任意）  ※`LocationType.Stop`が自動的に置かれる
* 親停留所情報（`parent_station`、任意）
* のりば情報（`platform_code`、任意）

## 使い方 / Usage
