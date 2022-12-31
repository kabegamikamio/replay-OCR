# WoTB replay parser by OCR
Coded by kabegamikamio (discord: 壁紙紙雄#1616)

- [WoTB replay parser by OCR](#wotb-replay-parser-by-ocr)
  - [このプログラムについて](#このプログラムについて)
    - [チェンジログ](#チェンジログ)
    - [動作確認環境](#動作確認環境)
    - [必要パッケージ等](#必要パッケージ等)
    - [できること](#できること)
    - [できないこと(今後実装予定の機能)](#できないこと今後実装予定の機能)
  - [How to Use](#how-to-use)
    - [実行例](#実行例)
  - [設計](#設計)
    - [主要関数](#主要関数)
      - [`captureVideo()` (in mycapture.py)](#capturevideo-in-mycapturepy)
      - [`OCRcore()` (in myocr.py)](#ocrcore-in-myocrpy)
      - [`OCRmain()` (in myocr.py)](#ocrmain-in-myocrpy)
      - [`slaveOCR()` (in myocr.py)](#slaveocr-in-myocrpy)
      - [`parallelOCR()` (in myocr.py)](#parallelocr-in-myocrpy)
      - [`sequentialOCR()` (in myocr.py)](#sequentialocr-in-myocrpy)
      - [`pic2bin()` (in myimage.py)](#pic2bin-in-myimagepy)
      - [`cropPicture4x3()` (in myimage.py)](#croppicture4x3-in-myimagepy)
      - [`if*()` (in myocr.py)](#if-in-myocrpy)
      - [`preprocessTest()` (in myocr.py)](#preprocesstest-in-myocrpy)
      - [`concateLogs()` (in streamprocess.py)](#concatelogs-in-streamprocesspy)
      - [`stripTimeStream()` (in streamprocess.py)](#striptimestream-in-streamprocesspy)
    - [並列処理](#並列処理)
  - [よく見られる不具合](#よく見られる不具合)
    - [`stream 1, missing mandatory atoms, broken header`](#stream-1-missing-mandatory-atoms-broken-header)
    - [`Empty input file. stripTimeStream will terminate the process.`](#empty-input-file-striptimestream-will-terminate-the-process)


## このプログラムについて
YouTubeに投稿されているWoTBのリプレイ動画から試合の勝敗等のデータを抽出するプログラムです。

### チェンジログ
[2022/12/31] beta v1.0 リリース

### 動作確認環境
- Lenovo ideaPad 720s
  - Core i5-8250U
  - 8GB RAM
- Python 3.11.1
- Tesseract-OCR v5.3.0.20221222

### 必要パッケージ等
同梱バッチファイル `package.bat` または `package` をコマンドプロンプトやPowerShell上で実行することで自動インストールが可能。
- Tesseract-OCR
- pafy
- cv2
- PIL
- tqdm
- pyocr
- youtube-dl (2020.12.2)
  - これ以降のバージョンでは動作未確認

### できること
- リプレイ動画から1秒ごとにSSしPNGで書き出し
  - `captureVideo(writeout=True)` でPNG書き出し有効
- 試合開始・終了画面がある動画から試合結果を取得しCSV書き出し
  - 勝敗と勝因・敗因(殲滅・キャプ)が利用可能

### できないこと(今後実装予定の機能)
- 試合開始・終了画面がない動画から試合結果を取得
  - 優勢戦のポイントバーから試合結果を推定
- 対戦チーム名を取得
- ミニマップから戦術を推定
- 動画のアスペクト比から最適な切り抜きを実現
- ワイプやフレームがある動画への対応

## How to Use
`runCaptureOCR.py` のコマンドライン引数にリプレイURLを指定して実行する。

### 実行例
```
> python runCaptureOCR.py https://youtu.be/iUfvSm69Exs
```

## 設計
定義ファイルは `import mydefs` で利用可能。実行ファイル (`run*.py`) をコンパイルして実行する。
```
WT101
|-runCaptureOCR.py      # メインのpyファイル。これを実行
|-runCapture.py         # PNG書き出し有効でキャプチャ実行
|-runOCR.py             # 指定ディレクトリ内のPNGファイルをOCR
|-runStreamProcess.py   # OCRによって得られた時系列データの処理
|-mydefs
  |-mycapture.py        # 動画キャプチャの定義ファイル
  |-myocr.py            # OCRの定義ファイル
  |-myimage.py          # 画像の前処理などに関係する定義ファイル
  |-myutil.py           # 文字列処理などに関係する定義ファイル
  |-streamprocess.py    # 時系列データ処理の定義ファイル
```

### 主要関数
以下では主な関数の仕様について説明している。

#### `captureVideo()` (in mycapture.py)
URLで指定された動画の`start`秒から`end`秒を取得し、引数によりPNG書き出しかOCRの実行を行う。
- 引数
  - `url`: 動画のURL。直接YouTubeのURLを指定せず、Pafyの`best.url`を使用することを推奨。
  - `start`: キャプチャを開始する時間
  - `end`: キャプチャを終了する時間
  - `dir`: 出力ファイル(PNGファイルやログファイル)の出力先ディレクトリ
  - `writeout`: PNG書き出し。初期値は`True`。`True`のときPNGを書き出し、`False`のときPNGは書き出しせずログファイルのみ出力する。
- 返り値
  - なし

#### `OCRcore()` (in myocr.py)
OCRの実行とテキストの取得を行う。
- 引数
  - `im`: NumPy.ndarray形式の画像データ
  - `engine`: pyocrのOCRエンジン
  - `builder`: `pyocr.builders.TextBuilder()` (pyocrの設定)
  - `lang`: OCRを実行する言語。初期値は`'jpn'` (日本語)
- 返り値
  - OCRにより得られたテキスト

#### `OCRmain()` (in myocr.py)
OCRを実行し、勝敗やマップの情報があればそれを返り値として与える。
- 引数
  - `im`: NumPy.ndarray形式の画像データ
- 返り値
  - ローディング画面を認識した際は `loading, (map)`
  - 勝敗を認識した際は `(win or lose), (elimination or points)`
  - これらの情報がない場合 `False`

#### `slaveOCR()` (in myocr.py)
OCRを並列に実行する `parallelOCR()` のスレーブ関数。**現在は使用していない。**
- 引数
  - `dir`: ディレクトリ
  - `start`: OCR開始時間
  - `end`: OCR終了時間
- 返り値
  - なし

#### `parallelOCR()` (in myocr.py)
OCRを並列実行する。**現在は使用していない。**
- 引数
  - `dir`: ディレクトリ
- 返り値
  - なし

#### `sequentialOCR()` (in myocr.py)
OCRを直列実行し、ログファイルに取得した試合情報を出力する。
- 引数
  - `dir`: ディレクトリ
- 返り値
  - なし

#### `pic2bin()` (in myimage.py)
画像の前処理。画像を二値化することでOCRの精度を向上する。
- 引数
  - `image`: NumPy.ndarray形式の画像データ
  - `border`: 二値化のしきい値
- 返り値
  - 二値化されたNumPy.ndarray形式の画像データ

#### `cropPicture4x3()` (in myimage.py)
画像の前処理。4:3の画像からOCRに必要な部分だけ切り抜き、OCRの精度を向上する。iPhoneやiPadなどで録画された動画に有効。
- 引数
  - `im`: NumPy.ndarray形式の画像データ
- 返り値
  - 切り抜かれた複数の画像片(リスト形式)

#### `if*()` (in myocr.py)
与えられたテキストが `*` であるか (例えば、ロード画面であるか) をレーベンシュタイン距離に基づき判定する。つまり、ある程度の誤りを許容しつつテキストの比較を行う。
- 引数
  - `txt`: 判定を行うテキスト
- 返り値
  - 真偽値、または文字列 (例、マップ名など)

#### `preprocessTest()` (in myocr.py)
OCRのテスト用。

#### `concateLogs()` (in streamprocess.py)
並列処理によって生成された複数のログファイル(時系列データ)を順序を保ったまま単一CSVファイル `stream.csv` に統合する。
- 引数
  - `dir`: ログファイルが存在するディレクトリ
- 返り値
  - なし

#### `stripTimeStream()` (in streamprocess.py)
時系列データを要約して非時系列データに変換する。時系列データに関しては「並列処理」を参照。
- 引数
  - `inputfile`: 入力時系列データ(CSV)
  - `outputfile`: 出力非時系列データ(CSV)

### 並列処理
このプログラムでは動画のキャプチャとOCRにおいてメモリ非共有の並列処理を可能としている。特に並列OCR処理の各プロセスは独立したログファイルを出力するため、OCR実行後にはログファイルの統合が必要となる。
またOCRで生成されるログファイルは時系列データである。例えば次のような構造を持つ。

```
66,loading,アルペンシュタット
67,loading,アルペンシュタット
68,loading,アルペンシュタット
260,win,elimination
261,win,elimination
262,win,elimination
369,loading,アルペンシュタット
370,loading,アルペンシュタット
371,loading,アルペンシュタット
591,win,elimination
592,win,elimination
593,win,elimination
```

このデータは動画時間で66 - 68秒の間がローディング画面、260 - 262秒の間が勝利画面、369 - 371秒の間が2回目のローディング画面、591 - 593秒の間が2回目の勝利画面であることを表している。ひとつの画面が数秒持続することから、このデータは時系列データ (ストリームデータ) である。
一方、目的とするデータは頻度データ (非時系列データ) であるから `stripTimeStream()` を用いて変換を行う必要がある。

## よく見られる不具合
### `stream 1, missing mandatory atoms, broken header`
直接の原因は不明だが、URLで指定された動画から `cv2.captureVideo` が対応しているコーデックを取得できない場合にこのエラーが発生すると考えられる。
対処法としては、動画URLをURL窓からコピペするのではなく動画の共有メニューから得られるURLとするなど。

### `Empty input file. stripTimeStream will terminate the process.`
この例外は統合されたログファイル (このプログラムでは一般に `stream.csv` という名称を使用している) の中身が空であるときに発生する。この例外の原因はOCRがリプレイから試合状況を取得できないことが考えられる。例えばbeta v1.0ではロード画面や試合終了画面から試合状況を取得するため、これらの画面がないリプレイを処理すると空のログファイルが生成される。
現時点で対処法はないため、今後のアップデートで対応するのを待たれたい。この例外に遭遇した場合は実行時に指定したURLを discord 壁紙紙雄#1616 まで共有されたし。