import os
import matplotlib.pyplot as plt
from main import main, text, OpenAI_API_KEY  # main.pyから関数と変数をインポート

# 必要なモジュールがインストールされていなければインストール
try:
    import matplotlib
except ImportError:
    os.system("pip install matplotlib")

def plot_all_patterns_and_save_scores(text, OpenAI_API_KEY):
    patterns = [
        {"isarasuji": True, "isbert": True},
        {"isarasuji": True, "isbert": False},
        {"isarasuji": False, "isbert": True},
        {"isarasuji": False, "isbert": False},
    ]

    # スコア保存用ファイル
    output_file = "scores_output.txt"

    with open(output_file, "w") as file:
        file.write("Scores for Different Configurations\n")
        file.write("=" * 40 + "\n\n")

        plt.figure(figsize=(10, 6))  # グラフのサイズを設定
        for pattern in patterns:
            # 各パターンに対してスコアを計算
            updated_text = main(text.copy(), OpenAI_API_KEY, pattern["isarasuji"], pattern["isbert"])

            # 行数とスコアを抽出
            x = [entry['index'] for entry in updated_text if 'score' in entry]
            y = [entry['score'] for entry in updated_text if 'score' in entry]

            # スコアをテキストファイルに保存
            file.write(f"Pattern: isarasuji={pattern['isarasuji']}, isbert={pattern['isbert']}\n")
            for index, score in zip(x, y):
                file.write(f"  Line {index}: Score = {score}\n")
            file.write("\n")

            # グラフをプロット
            label = f"isarasuji={pattern['isarasuji']}, isbert={pattern['isbert']}"
            plt.plot(x, y, label=label, marker='o')  # マーカーを追加して視認性を向上

        # グラフの装飾
        plt.title("Similarity Scores for Different Configurations")
        plt.xlabel("Line Number")
        plt.ylabel("Score")
        plt.legend()  # 凡例を表示
        plt.grid(True)  # グリッドを表示
        plt.tight_layout()

        # 保存完了メッセージ
        print(f"Scores have been saved to {output_file}")

        # グラフを表示
        plt.show()


if __name__ == "__main__":
    plot_all_patterns_and_save_scores(text, OpenAI_API_KEY)
