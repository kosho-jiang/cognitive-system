#改行フラグ・文字数・句点なし改行あり
def load_and_split_text_with_length(file_path: str, delimiter: str = "。") -> list[dict]:
    """
        list[dict]: [{"index": 0, "sentence": "文章1", "is_first_line": True, "length": 5}, ...]
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
        
        lines = text.split("\n")
        result = []
        index = 0

        for line in lines:
            sentences = line.split(delimiter)
            for idx, sentence in enumerate(sentences):
                clean_sentence = sentence.strip()
                if clean_sentence:
                    is_first_line = idx == 0
                    sentence_length = len(clean_sentence)
                    if idx == len(sentences) - 1 and clean_sentence and delimiter not in clean_sentence:
                        result.append({
                            "index": index,
                            "sentence": clean_sentence, 
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