def load_and_split_text(file_path: str, delimiter: str = "。") -> list[dict]:
    """
    テキストファイルを読み込み、指定した区切り文字で分割する。

    引数:
        file_path (str): テキストファイルのパス。
        delimiter (str): 区切り文字（デフォルトは句点 "。"）。

    戻り値:
        list[dict]: インデックスと文章を含むリスト。
            例: [{"index": 0, "sentence": "文章1"}, {"index": 1, "sentence": "文章2"}]
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
        
        # 区切り文字で分割してインデックスを付ける
        sentences = text.split(delimiter)
        # 空白の文を除外し、辞書形式でリストに格納
        result = [
            {"index": idx, "sentence": sentence.strip() + delimiter if sentence.strip() else ""}
            for idx, sentence in enumerate(sentences) if sentence.strip()
        ]
        
        return result

    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return []

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return []

# 使用例
if __name__ == "__main__":
    file_path = "example (1).txt"  # テキストファイルのパスを指定
    result = load_and_split_text(file_path)
    for item in result:
        print(f"Index: {item['index']}, Sentence: {item['sentence']}")
