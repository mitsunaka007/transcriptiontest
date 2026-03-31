import os
import pandas as pd
from faster_whisper import WhisperModel # 例として使用
from evaluate import calculate_cer

# 設定
AUDIO_DIR = "./audio_samples"
GT_DIR = "./ground_truth"
MODEL_SIZE = "large-v3"

def run_benchmark():
    model = WhisperModel(MODEL_SIZE, device="cpu", compute_type="int8")
    results = []

    for filename in os.listdir(AUDIO_DIR):
        if filename.endswith(".wav"):
            base_name = os.path.splitext(filename)[0]
            audio_path = os.path.join(AUDIO_DIR, filename)
            gt_path = os.path.join(GT_DIR, f"{base_name}.txt")

            if not os.path.exists(gt_path): continue

            # 1. 正解データの読み込み
            with open(gt_path, "r", encoding="utf-8") as f:
                reference = f.read()

            # 2. 文字起こし実行
            segments, _ = model.transcribe(audio_path, beam_size=5)
            hypothesis = "".join([s.text for s in segments])

            # 3. 精度評価
            cer = calculate_cer(reference, hypothesis)
            
            results.append({
                "file": filename,
                "model": MODEL_SIZE,
                "cer": cer,
                "text": hypothesis
            })

    # 結果をCSV保存
    df = pd.DataFrame(results)
    df.to_csv("benchmark_results.csv", index=False)
    print("ベンチマーク完了。結果を benchmark_results.csv に保存しました。")

if __name__ == "__main__":
    run_benchmark()