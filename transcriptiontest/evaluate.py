import jiwer

def calculate_cer(reference, hypothesis):
    """
    日本語の文字誤り率 (CER) を計算します。
    """
    # 空白や改行を削除して文字単位のリストに変換
    ref_chars = list(reference.strip().replace(" ", "").replace("\n", ""))
    hyp_chars = list(hypothesis.strip().replace(" ", "").replace("\n", ""))
    
    # 文字を「単語」と見なしてjiwerで計算
    cer = jiwer.wer(ref_chars, hyp_chars)
    return cer

# テスト実行例
if __name__ == "__main__":
    ref = "本日は晴天なり。"
    hyp = "今日は晴天なり"
    score = calculate_cer(ref, hyp)
    print(f"CER: {score:.2%} (低いほど高精度)")