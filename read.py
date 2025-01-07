#改行フラグ・文字数・句点なし改行あり
def load_and_split_text_with_length(file_path: str, delimiter: str = "。") -> list[dict]:
    """
    テキストファイルを読み込み、指定した区切り文字で分割し、
    改行があるたびにその後の最初の文にフラグを立て、各文の長さを記録する。
    改行で区切られた文に句点がない場合は末尾に句点を付けない。

    引数:
        file_path (str): テキストファイルのパス。
        delimiter (str): 区切り文字（デフォルトは句点 "。"）。

    戻り値:
        list[dict]: インデックス、文章、改行フラグ、文の長さを含むリスト。
            例: [{"index": 0, "sentence": "文章1", "is_first_line": True, "length": 5}, ...]
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
                    is_first_line = idx == 0
                    # 文の長さを計算
                    sentence_length = len(clean_sentence)
                    # 改行のみの文には句点を追加しない
                    if idx == len(sentences) - 1 and clean_sentence and delimiter not in clean_sentence:
                        result.append({
                            "index": index,
                            "sentence": clean_sentence,  # 句点を追加しない
                            "is_first_line": is_first_line,
                            "length": sentence_length
                        })
                    else:
                        result.append({
                            "index": index,
                            "sentence": clean_sentence + delimiter if delimiter not in clean_sentence else clean_sentence,
                            "is_first_line": is_first_line,
                            "length": sentence_length
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

    result = load_and_split_text_with_length(file_path)
    for item in result:
        print(f"Index: {item['index']}, Sentence: {item['sentence']}, "
              f"Is First Line: {item['is_first_line']}, Length: {item['length']}")
        output_file_path = "testcases/output.txt"
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            for item in result:
                output_file.write(f"Index: {item['index']}, Sentence: {item['sentence']}, Is First Line: {item['isfirst']}, Length: {item['length']} \n")
        print(f"Output written to {output_file_path}")