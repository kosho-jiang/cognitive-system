import os
import matplotlib.pyplot as plt
from main import main
from read import load_and_split_text_with_length

def plot_scores_from_main(file_path, openai_api_key, isarasuji=True, isbert=False):
    # テキストデータを読み込む
    text = load_and_split_text_with_length(file_path)

    # main関数を実行してスコア計算を完了
    scored_text = main(text, openai_api_key, isarasuji, isbert)

    # インデックスとスコアを抽出
    indices = [entry["index"] for entry in scored_text]
    scores = [entry["score"] for entry in scored_text]

    # グラフを描画
    plt.figure(figsize=(10, 6))
    plt.plot(indices, scores, marker="o", linestyle="-", color="b", label="Score")

    # グラフ装飾
    plt.title("Score by Line Index", fontsize=16)
    plt.xlabel("Line Index", fontsize=14)
    plt.ylabel("Score", fontsize=14)
    plt.grid(True, linestyle="--", alpha=0.7)
    plt.legend(fontsize=12)
    plt.tight_layout()

    # グラフを表示
    plt.show()


if __name__ == "__main__":
    # ファイルパスとAPIキーを設定
    file_path = "testcases/usakusai.txt"
    openai_api_key = os.environ.get("OPENAI_API_KEY")

    # グラフをプロット
    plot_scores_from_main(file_path, openai_api_key, isarasuji=False, isbert=False)

