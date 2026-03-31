# transcriptiontest

日本語 Speech-to-Text（音声認識）のオープンソースを毎日自動リサーチし、精度ベンチマークを計測するツールです。

---

## 機能

### 1. 毎日自動リサーチ（`research_script.py`）
GitHub APIを使い、日本語STT関連リポジトリを毎日自動収集します。
- キーワード：`japanese speech-to-text` / `whisper japanese` / `日本語 音声認識`
- 過去24時間以内に更新されたリポジトリを対象
- スター数5以上でフィルタリング
- GitHub Actionsで毎日午前9時（JST）に自動実行

### 2. 精度ベンチマーク（`benchmark_runner.py`）
faster-whisperモデルを使い、音声ファイルの文字起こし精度を計測します。
- モデル：`large-v3`（CPU / int8）
- 評価指標：CER（文字誤り率）
- 結果を `benchmark_results.csv` に保存

### 3. CER計算（`evaluate.py`）
正解テキストと文字起こし結果を比較し、文字誤り率（CER）を算出します。

---

## ディレクトリ構成

```
transcriptiontest/
├── research_script.py       # GitHubリサーチスクリプト
├── benchmark_runner.py      # ベンチマーク実行スクリプト
├── evaluate.py              # CER計算モジュール
├── requirements.txt         # 依存ライブラリ
├── audio_samples/           # ベンチマーク用音声ファイル（.wav）
│   ├── sample1.wav
│   ├── sample2.wav
│   └── sample3.wav
└── ground_truth/            # 正解テキスト
    ├── sample1.txt
    ├── sample2.txt
    └── sample3.txt

.github/
└── workflows/
    └── daily_research.yml   # GitHub Actions ワークフロー定義
```

---

## セットアップ

### 依存ライブラリのインストール

```bash
pip install -r transcriptiontest/requirements.txt
```

### 依存ライブラリ一覧

| ライブラリ | 用途 |
|-----------|------|
| `requests` | GitHub API呼び出し |
| `pandas` | ベンチマーク結果のCSV出力 |
| `jiwer` | CER（文字誤り率）計算 |

---

## 使い方

### リサーチスクリプトをローカルで実行

```bash
# GITHUB_TOKENを設定すると取得件数の上限が増加（任意）
export GITHUB_TOKEN=your_token_here

python transcriptiontest/research_script.py
```

**出力例：**
```
--- 2026-03-31 のリサーチ結果 ---
【名前】: someuser/whisper-japanese
【URL】: https://github.com/someuser/whisper-japanese
【説明】: Japanese STT tool based on Whisper
【Star】: 120
------------------------------
```

### ベンチマークをローカルで実行

```bash
cd transcriptiontest
python benchmark_runner.py
```

結果は `benchmark_results.csv` に保存されます。

---

## GitHub Actions（自動実行）

### スケジュール
毎日 **午前9時（JST）** に自動実行されます。

### 手動実行
GitHub の `Actions` タブ → `Daily STT Research` → `Run workflow` ボタンで即時実行できます。

### 実行結果の確認
`Actions` タブ → 該当のworkflow run → `build` → `Run research script` を展開するとログが確認できます。

### 必要なシークレット
GitHub リポジトリの `Settings` → `Secrets and variables` → `Actions` に以下を設定することでAPI制限を緩和できます（任意）。

| シークレット名 | 内容 |
|--------------|------|
| `GITHUB_TOKEN` | 自動付与されるため設定不要 |

---

## 評価指標：CER（文字誤り率）について

CER（Character Error Rate）は日本語音声認識の精度評価に使われる指標です。

```
CER = (置換 + 削除 + 挿入) / 正解文字数
```

- **0%** = 完全一致
- **低いほど高精度**

---

## 注意事項

- `benchmark_runner.py` は `faster-whisper` を使用しています。実行には別途インストールが必要です。
- 音声ファイルは `.wav` 形式のみ対応しています。
- GitHub API の未認証リクエストは1時間あたり60回の制限があります。
