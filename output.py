from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.pdfbase import pdfmetrics

# 入力データ　以下のような構造を持ったリストを想定している
data = [
    {"index": 1, "sentences": "これはテスト文です。", "is_first_line": True, "length": 10, "score": 0.8},
    {"index": 2, "sentences": "もう1つの文です。", "is_first_line": False, "length": 8, "score": 0.4},
]

# HEXをRGBに変換する関数
def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) / 255.0 for i in (0, 2, 4))

# パラメータ設定 　PDF上の文字の座標位置はptという単位で表される。
PAGE_WIDTH, PAGE_HEIGHT = A4  # A4サイズ (210mm x 297mm)
MARGIN = 20 * 2.83465  # mmをptに変換
COLUMN_WIDTH = 25  # 列幅（mm -> pt）
LINE_SPACING = 5  # 行間（pt）文字と文字の間の間隔を調整する。
#スコアとフォントサイズの関係を調節できる。
FONT_MAPPING = {
    0.0: 6,
    0.3: 9,
    0.4: 12,
    0.5: 15,
    0.6: 18,
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
    c = canvas.Canvas(output_file, pagesize=A4)
    c.setFont(FONT_NAME, 10)

    x_offset = PAGE_WIDTH - MARGIN
    y_offset = PAGE_HEIGHT - MARGIN
    column_x = x_offset
    column_y = y_offset

    if isSize:
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
                        column_x = x_offset

    else:
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


if __name__ == "__main__":
    create_pdf(data, "output.pdf",False)
