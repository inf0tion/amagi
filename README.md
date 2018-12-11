# Amagiプロジェクト

# 非同期で取得したデータファイルとGPSデータを統合する

Garminを持って外に出て，何らかのデータを取得する．
何らかのデータを取得した時刻が明確になっている場合．
取得したデータの時刻とGPSデータの時刻から実際に取得した座標を推定する．

## 必要なもの

* ライブラリ
    * gpxpy
    * simplekml
        * KMLファイルを生成する場合
* データ
    * 時刻の入ったデータファイル
    * GPXファイル

## ファイル構成

* DefDev.py
    * デバイスデータ
    * DevDataLクラス
    * DevDataクラス
* devgps.py
    * デバイスデータに座標情報を入れたもの
    * DevGPSLクラス
    * DevGPSクラス
* genkml.py
    * DevGPSLをKMLで出力
    * KmlStyleクラス
* sample2kml.py
    * サンプルのメインファイル
    * サンプルのデータ形式と出力形式に依存
    * GPXファイルとサンプルのJSONファイルから，KMLファイルを生成
* dataset\_sample.py
    * サンプルのデータ形式に依存する部分
        * DevDataL_Sample
        * DevData_Sample
        * DevGPS_Sample
* kmlstyle\_sample.py
    * KMLファイル出力用のスタイル定義
    * サンプルのデータ形式とKMLファイルの形式に依存する部分
    * KmlStyle抽象クラス

## 仕組み

### 概念図

```
                     gpx       +------+
(GPX file)->[gpx]------------->|      | DevGPSL  +--------+
                     DevDataL  |devgps|--------->|generate|-->(output)
(data file)->[load]----------->|      |      +-->|        |
                               +------+      |   +--------+
                                    +-----+  |
                                    |style|--+
                                    +-----+
```

### 解説

GERMINのGPS端末はGPX形式のファイルを生成するので，それを扱うためにgpxpyライブラリを利用する．

データファイルの形式はそれぞれで共通化は難しいので，`DevData`オブジェクトを継承した新しいオブジェクトを各自作ることになる(概念図で`load`の部分)．`DevData`オブジェクトは時刻データとステータスだけを持っている．サンプルでは，JSON形式のファイルを読んで，`DevData_Sample`クラスを定義している．

`DevDataL`は`DevData`のリストを持つオブジェクトで，リスト処理のためのメソッドが用意されている．

`devgps`で`DevDataL`に座標データを付加した新しいオブジェクト`DevGPSL`を生成する．ここでは`DevData`の時刻データしか参照する必要が無い．サンプルでは`DevGPSL`のリスト処理用メソッドを付加するため，これを継承した`DevGPSL_Sample`クラスを定義している．

`generate`では，`DevGPSL`を実際に欲しいファイル形式に変換して出力する．サンプルではKMLファイルを生成している．実際に出力させる内容は各自が決めたいところなので，スタイルオブジェクトを読み込む形で，自由度を持たせている．

# 実行

```shell
$ python3 sample2kml.py foo.gpx bar.json sample.kml
```

`-i=[seconds]` オプション

データ取得をseconds[秒]間隔で実行していて，何らかの事情で取得できなかった場合で，そこのデータを補間したい場合を想定．

例：60秒間隔でデータ取得をしていた場合

```shell
$ python3 sample2kml.py foo.gpx bar.json sample.kml -i=60
```

