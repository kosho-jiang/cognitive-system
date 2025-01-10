from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
 
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

# パラメータ設定 　PDF上の文字の座標位置はptという単位で表される。
PAGE_WIDTH, PAGE_HEIGHT = A4  # A4サイズ (210mm x 297mm)
MARGIN = 20 * 2.83465  # mmをptに変換
COLUMN_WIDTH = 25  # 列幅（mm -> pt）
LINE_SPACING = 5  # 行間（pt）文字と文字の間の間隔を調整する。

#スコアとフォントサイズの関係を調節できる。
FONT_MAPPING = {
    0.0: 10,
    0.2: 12,
    0.4: 14,
    0.6: 16,
    0.8: 18,
    1.0: 20,
}
COLOR_MAPPING = {
    0.0: "#F0F0F0",
    0.2: "#C0C0C0",
    0.4: "#808080",
    0.6: "#404040",
    0.8: "#202020",
    1.0: "#000000",
}
#フォントをこだわりたかったら変更する。ただし、これ以外のやつはダウンロードしないといけないので面倒。
FONT_NAME = "HeiseiKakuGo-W5"

# フォント登録
pdfmetrics.registerFont(UnicodeCIDFont('HeiseiKakuGo-W5',isVertical=True))

# HEXをRGBに変換する関数
def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) / 255.0 for i in (0, 2, 4))

# スコアを5分割してカテゴリーを取得する関数
def categorize_scores(scores):
    """
    スコアを小さい順に5分割してカテゴリーを割り当てる。

    引数:
        scores (list[float]): スコアのリスト。

    戻り値:
        list[int]: スコアに対応するカテゴリーリスト（0〜4）。
    """
    sorted_scores = sorted(scores)
    n = len(scores)
    thresholds = [sorted_scores[int(n * i / 5)] for i in range(1, 5)]

    categories = []
    for score in scores:
        if score <= thresholds[0]:
            categories.append(0.2)
        elif score <= thresholds[1]:
            categories.append(0.4)
        elif score <= thresholds[2]:
            categories.append(0.6)
        elif score <= thresholds[3]:
            categories.append(0.8)
        else:
            categories.append(1.0)

    return categories

# スコアに応じたフォントサイズを決定する関数
def get_font_size(score):
    for threshold, size in sorted(FONT_MAPPING.items()):
        if score <= threshold:
            return size
    return max(FONT_MAPPING.values())

# スコアに応じたフォントの色を決定する関数
def get_font_color(score):
    for threshold, hex_color in sorted(COLOR_MAPPING.items()):
        if score <= threshold:
            return hex_to_rgb(hex_color)
    return hex_to_rgb("#000000")

# PDF生成
def create_pdf(data, output_file, isSize):
    if isSize:
        c = canvas.Canvas(output_file, pagesize=A4)
        c.setFont(FONT_NAME, 10)

        x_offset = PAGE_WIDTH - MARGIN
        y_offset = PAGE_HEIGHT - MARGIN
        column_x = x_offset
        column_y = y_offset

        for entry in data:
            text = entry["sentence"]
            score = entry["score"]
            font_size = get_font_size(score)

            c.setFont(FONT_NAME, font_size)
            for char in text:
                c.drawString(column_x, column_y, char)
                column_y -= font_size + LINE_SPACING

                # 次の列に移動する場合
                if column_y < MARGIN:
                    column_y = y_offset
                    column_x -= COLUMN_WIDTH

                    if column_x < MARGIN:
                        c.showPage()
                        c.setFont(FONT_NAME, font_size)
                        column_x = PAGE_WIDTH - MARGIN
                      
            column_y = y_offset
            column_x -= COLUMN_WIDTH
            if column_x < MARGIN:
                c.showPage()
                c.setFont(FONT_NAME, font_size)
                column_x = PAGE_WIDTH - MARGIN

    else:
        c = canvas.Canvas(output_file, pagesize=A4)
        c.setFont(FONT_NAME, 10)

        x_offset = PAGE_WIDTH - MARGIN
        y_offset = PAGE_HEIGHT - MARGIN
        column_x = x_offset
        column_y = y_offset
        
        for entry in data:
            text = entry["sentence"]
            score = entry["score"]
            font_color = get_font_color(score)

            c.setFont(FONT_NAME, 12)  # フォントサイズは固定
            c.setFillColorRGB(*font_color)  # 色を設定
        
            for char in text:
                c.drawString(column_x, column_y, char)
                column_y -= 12 + LINE_SPACING
                
                # 次の列に移動する場合
                if column_y < MARGIN:
                    column_y = y_offset
                    column_x -= COLUMN_WIDTH
                    
                    if column_x < MARGIN:
                        c.showPage()
                        c.setFont(FONT_NAME, 12)
                        c.setFillColorRGB(*font_color)
                        column_x = PAGE_WIDTH - MARGIN
        
    c.save()
    
# スコアリストを読み込む関数
def load_scores(file_path: str, pattern: str) -> list[float]:
    """
    スコアリストを読み込む関数。

    引数:
        file_path (str): スコアリストのファイルパス。
        pattern (str): 使用するスコアセットのパターン名 (例: 'isarasuji=True')。

    戻り値:
        list[float]: 各行に対応するスコアリスト。
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        # 指定されたパターンを見つける
        start = False
        scores = []

        for line in lines:
            if line.strip() == "Pattern: " + pattern:
                start = True
                continue

            if start:
                if line.startswith("  Line"):
                    score = float(line.split("=")[1].strip())
                    scores.append(score)
                elif line.strip() == "":
                    break

        return scores

    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return []

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return []
    
# 統合処理
def main(input_file, score_file, pattern, output_file):
    data = load_and_split_text_with_length(input_file)
    scores = load_scores(score_file, pattern)

    if len(data) != len(scores):
        raise ValueError("Error: The number of sentences and scores do not match.")

    categories = categorize_scores(scores)

    for entry, score in zip(data, categories):
        entry["score"] = score

    create_pdf(data, output_file,False)

# 実行
if __name__ == "__main__":
    input_file = "aruiwa.txt"  # 入力テキストファイル
    output_file = "output_isarasuzi_true_color.pdf"  # 出力PDFファイル
    score_file = "aruiwa_scores_output.txt"  # スコアファイル
    pattern = "isarasuji=True, isbert=False"  # 使用するスコアセット
    main(input_file, score_file, pattern, output_file)
