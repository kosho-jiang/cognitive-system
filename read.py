#改行フラグあり
def load_and_split_text(file_path: str, delimiter: str = "。") -> list[dict]:
    """
    テキストファイルを読み込み、指定した区切り文字で分割し、
    改行があるたびにその後の最初の文にフラグを立てる。

    引数:
        file_path (str): テキストファイルのパス。
        delimiter (str): 区切り文字（デフォルトは句点 "。"）。

    戻り値:
        list[dict]: インデックス、文章、改行フラグを含むリスト。
            例: [{"index": 0, "sentence": "文章1", "isfirst": True}, ...]
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
        
        # 改行でテキストを分割
        lines = text.split("\n")
        result = []
        index = 0  # 文全体のインデックス

        for line in lines:
            # 各行を指定した区切り文字で分割
            sentences = line.split(delimiter)
            for idx, sentence in enumerate(sentences):
                clean_sentence = sentence.strip()
                if clean_sentence:
                    # 改行後最初の文にフラグを立てる
                    isfirst = idx == 0
                    result.append({
                        "index": index,
                        "sentence": clean_sentence + delimiter if delimiter not in clean_sentence else clean_sentence,
                        "isfirst": isfirst
                    })
                    index += 1

        return result

    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return []

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return []

# 使用例
if __name__ == "__main__":
    file_path = "testcases/read1.txt"  # テキストファイルのパスを指定
    result = load_and_split_text(file_path)
    for item in result:
        print(f"Index: {item['index']}, Sentence: {item['sentence']}, Is First Line: {item['isfirst']}")

        output_file_path = "testcases/output.txt"
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            for item in result:
                output_file.write(f"Index: {item['index']}, Sentence: {item['sentence']}, Is First Line: {item['isfirst']}\n")
        print(f"Output written to {output_file_path}")