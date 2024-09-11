# gtfs2oudia

GTFS-JP形式のファイルをOuDiaSecond形式に変換するライブラリ。

A library for converting GTFS-JP files to OuDia file format.

## サポートされているファイル形式 / Supported file types

<!-- * [OuDia](http://take-okm.a.la9.jp/oudia/) -->
* [OuDiaSecond](http://oudiasecond.seesaa.net/)

* [GTFS-JP](https://gtfs.jp/)

## 制約 / Limitations

GTFS-JPとOuDiaSecondとは形式やデータの構造化形式が大きく異なり、互換性がないフォーマットであるため、本ライブラリは、GTFS-JPからOuDiaSecondへの変換に際して、読み取れる限りのデータを対応させ、変換を行っておりますが、OuDiaSecondに非対応のGTFS-JP情報は捨て去られ、逆にGTFS-JP非対応のOuDiaSecond情報は新しく作ることができませんので、変換して得たOuDiaは不完全であり、不足するデータの一部は合理的なデフォルト値や他の値から推論しますが、それ以外の情報は手動で補足しなければなりません。即ち、この変換ツールによって得られたOuDiaデータはあくまで叩き台であり、そのまま利用することはできません。本章では、GTFS-JPのみ対応でOuDiaSecond非対応のものや、GTFS-JP非対応でOuDiaSecondでは必須なものなど、それぞれの要素について言及し、修正すべきデータの指針として提供します。

### 事業者情報（`agency.txt`/`agency.txt`→無し）
OuDiaSecond形式では、事業者が考慮されておりません。事業者情報はそのまま路線のコメント（`Rosen`の`Comment=`属性）として設定されます。


### 駅（`Stop`→`Eki`）

### OuDiaSecond対応、GTFS-JP非対応

##### OuDiaSecond
* 駅時刻形式（`Ekijikokukeisiki`、必須）※`Jikokukeisiki_Hatsu`が自動的に置かれます。
* 駅規模（`Ekikibo`、必須）※`Ekikibo_Ippan`が自動的に置かれます。ただし、停留所と標柱の別ではなく、一般駅と主要駅の区別なので、停留所や標柱がいずれも`Ekikibo_Ippan`になることが多いです。
* 駅名時刻表略称（`EkimeiJikokuRyaku`、任意）
* 駅名時刻表略称（`EkimeiDiaRyaku`、任意）
<!-- * 下り主本線（`DownMain`、必須、OuDiaSecond Ver2.00+で廃止）※`-1`が自動的に置かれます。
* 下り主本線（`UpMain`、必須、OuDiaSecond Ver2.00+で廃止） -->
<!-- * Eki -->

### GTFS-JP対応、OuDia非対応


* 停留留所・標柱ID（`stop_id`、必須） ※ユーザー定義の`generate_stop_id()`（デフォルトは駅の順番の数字）によって自動生成される
* 停留留所・標柱ID（`stop_code`、任意）
* 緯度（`stop_lat`、必須）※`0.0`が自動的に置かれる
* 経度（`stop_lon`、必須）※`0.0`が自動的に置かれる
* 運賃エリアID（`zone_id`、任意）
* 停留所・標柱URL（`stop_url`、任意）
* 停留所・標柱区分（`location_type`、任意）  ※`LocationType.Stop`が自動的に置かれる
* 親停留所情報（`parent_station`、任意）
* のりば情報（`platform_code`、任意）


### 駅停車（`StopTime`→`EkiJikoku`）

#### GTFS-JP対応、OuDia非対応

<!-- * 時刻名（`stop_time_id -->
* 停留所行先（`stop_headsign`、任意）



## 使い方 / Usage
