# yolo11_to_sumo

## 概要

このプロジェクトは、動画から物体を検出し、その追跡結果を元にSUMO (Simulation of Urban MObility) のシミュレーションファイルを生成するものです。

## 使い方

### 1. 依存ライブラリのインストール

以下のコマンドを実行して、必要なPythonライブラリをインストールします。

```bash
pip install opencv-python numpy pandas ultralytics scipy
```

### 2. 物体検出と追跡の実行

`task1_detection_tracking_simple.py` を実行して、動画 (`Solving the Long-Tail_cyclist.mp4`) から物体を検出し、追跡結果をCSVファイルに出力します。

```bash
python task1_detection_tracking_simple.py
```

このコマンドにより、`task1_simple_output` ディレクトリに `tracking_results.csv` が生成されます。

### 3. SUMOファイルの生成

`generate_sumo_files.py` を実行して、`tracking_results.csv` からSUMOシミュレーションに必要なファイルを生成します。

```bash
python generate_sumo_files.py
```

このコマンドにより、`sumo` ディレクトリに以下のファイルが生成されます。

*   `generated.net.xml`: 道路ネットワークファイル
*   `generated.rou.xml`: 車両・歩行者のルートファイル
*   `generated.sumocfg`: SUMOシミュレーション設定ファイル
*   `generated.netecfg`: netedit設定ファイル

### 4. SUMOシミュレーションの実行

生成された設定ファイルを使って、SUMOシミュレーションを実行します。

```bash
sumo -c sumo/generated.sumocfg
```

**注:** SUMOがシステムにインストールされている必要があります。

## 使い方

### 1. 依存ライブラリのインストール

以下のコマンドを実行して、必要なPythonライブラリをインストールします。

```bash
pip install opencv-python numpy pandas ultralytics scipy
```

### 2. 物体検出と追跡の実行

`task1_detection_tracking_simple.py` を実行して、動画 (`Solving the Long-Tail_cyclist.mp4`) から物体を検出し、追跡結果をCSVファイルに出力します。

```bash
python task1_detection_tracking_simple.py
```

このコマンドにより、`task1_simple_output` ディレクトリに `tracking_results.csv` が生成されます。

### 3. SUMOファイルの生成

`generate_sumo_files.py` を実行して、`tracking_results.csv` からSUMOシミュレーションに必要なファイルを生成します。

```bash
python generate_sumo_files.py
```

このコマンドにより、`sumo` ディレクトリに以下のファイルが生成されます。

*   `generated.net.xml`: 道路ネットワークファイル
*   `generated.rou.xml`: 車両・歩行者のルートファイル
*   `generated.sumocfg`: SUMOシミュレーション設定ファイル

### 4. SUMOシミュレーションの実行

生成された設定ファイルを使って、SUMOシミュレーションを実行します。

```bash
sumo -c sumo/generated.sumocfg
```

**注:** SUMOがシステムにインストールされている必要があります。