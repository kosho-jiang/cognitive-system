from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.pdfbase import pdfmetrics

# 入力データ　以下のような構造を持ったリストを想定している
data = [
    {"index": 1, "sentences": "これはテスト文です。", "is_first_line": True, "length": 10, "score": 0.8},
    {"index": 2, "sentences": "もう1つの文です。", "is_first_line": False, "length": 8, "score": 0.4},
]

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
#フォントをこだわりたかったら変更する。ただし、これ以外のやつはダウンロードしないといけないので面倒。
FONT_NAME = "HeiseiKakuGo-W5"

# フォント登録
pdfmetrics.registerFont(UnicodeCIDFont('HeiseiKakuGo-W5'))

# スコアに応じたフォントサイズを決定する関数
def get_font_size(score):
    for threshold, size in sorted(FONT_MAPPING.items()):
        if score <= threshold:
            return size
    return max(FONT_MAPPING.values())

# PDF生成
def create_pdf(data, output_file):
    c = canvas.Canvas(output_file, pagesize=A4)
    c.setFont(FONT_NAME, 10)

    x_offset = PAGE_WIDTH - MARGIN
    y_offset = PAGE_HEIGHT - MARGIN
    column_x = x_offset
    column_y = y_offset

    for entry in data:
        text = entry["sentences"]
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

    c.save()


if __name__ == "__main__":
    create_pdf(data, "output.pdf")
