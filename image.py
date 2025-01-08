import base64
import os
import openai
from openai import OpenAI

client = OpenAI()

OpenAI_API_KEY = os.environ["OPENAI_API_KEY"]

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def image_to_text(image_path: str) -> str:
    try:
        image = encode_image(image_path)
        prompt = (
            f"画像は漫画の一コマです．その内容を小説調で説明する文章を生成してください:\n"
        )
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "文章を生成するAIです。"},
                {"role": "user", "content":[
                    {"type": "text","text": prompt},
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{image}"}}
                ]}
            ]
        )
        content = response.choices[0].message.content
        return content
    except Exception as e:
        return str(e)

if __name__ == "__main__":
    image_path = 'testcases/onepiece.png'  # 適切な画像パスに置き換えてください
    result = image_to_text(image_path)
    print(result)