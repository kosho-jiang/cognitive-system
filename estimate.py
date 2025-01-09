import os
import openai
from openai import OpenAI

client = OpenAI()


OpenAI_API_KEY = os.environ["OPENAI_API_KEY"]

def generate_next_text(api_key, previous_text, next_text_length, isarasuji = False):
    openai.api_key = api_key
    arasuji_path = "testcases/arasuji.txt"

    if isarasuji == False:
        prompt = (
            f"以下は文脈に基づく文章生成です。前の文章を考慮しながら、次の文章をほぼ{next_text_length}文字で作成してください:\n"
            f"前の文章:\n{previous_text}\n"
            "次の文章:\n"
        )
    else:
        with open(arasuji_path, "r", encoding="utf-8") as file:
                arasuji_text = file.read()
        prompt = (
            f"以下は文脈に基づく文章生成です。あ前の文章を考慮しながら、次の文章をほぼ{next_text_length}文字で作成してください:\n"
            f"あらすじ:\n{arasuji_text}\n"  
            f"前の文章:\n{previous_text}\n"
            "次の文章:\n"
        )

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "文章を生成するAIです。"},
                {"role": "user", "content": prompt}
            ],
        )
        content = response.choices[0].message.content
        return content
    
    except Exception as e:
      print(f"Error: {e}")
      return "error"


if __name__ == "__main__":
    previous_text = "これまでの研究では、多くの成果が得られました。特に、データ解析手法の改良によって、精度が大幅に向上しました。"
    next_text_length = 50 

    next_text = generate_next_text(OpenAI_API_KEY, previous_text, next_text_length)
    print("生成された次の文章:", next_text)


"""漫画のコマの衝撃度"""
"""各コマを説明させて、コマごとの衝撃度を測る"""