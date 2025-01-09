import os
import openai
from openai import OpenAI

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from estimate import generate_next_text

OpenAI_API_KEY = os.environ["OPENAI_API_KEY"]

client = OpenAI()

"""isbert: boolについて、意味的埋め込みモデルを用いるか、GPTに丸投げするか分岐するフラグ
isbert:True -> sentence-transformersを用いて意味的埋め込みを計算    
isbert:False -> GPT-4o-miniに丸投げして類似度を計算
isarasuji:boolについて、あらすじを用いるかどうかのフラグ
"""

def calculate_similarity(apikey, previous_texts, next_text, next_text_length, isbert, isarasuji=False):
    
    next_text_genrated = generate_next_text(apikey, previous_texts, next_text_length, isarasuji)  
    print("実際の次の文章:", next_text)
    print("生成された文章:", next_text_genrated)

    if isbert:  
        model = SentenceTransformer('sonoisa/sentence-bert-base-ja-mean-tokens-v2')

        embedding1 = model.encode(next_text_genrated)
        embedding2 = model.encode(next_text)

        similarity = cosine_similarity([embedding1], [embedding2])

        return 1-similarity[0][0]  
    
    else:
        prompt = (
        "以下の二つの文章は、予想されたものと実際のものです。独自の方法を用いて類似度を小数点第5位(float型)まで計算してください。出力は数字だけで結構です。\n"
        f"予想された文章:\n{next_text_genrated}\n"
        f"実際の文章:\n{next_text}\n"
        "類似度:\n")

        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "文章を生成するAIです。"},
                    {"role": "user", "content": prompt}
             ],
         )
            content = float(response.choices[0].message.content)
            return 1-content
    
        except Exception as e:
            print(f"Error: {e}")
            return "error"

if __name__ == "__main__":
    previous_text = "これまでの研究では、多くの成果が得られました。特に、データ解析手法の改良によって、精度が大幅に向上しました。"
    next_text = "ボトルネックは機械の性能になってしまったため、次のブレークスルーを待たなければならなそうです。"
    next_text_length = 55
    isbert = False

    similarity = calculate_similarity(OpenAI_API_KEY, previous_text, next_text, next_text_length, isbert)
    print("類似度:", similarity)



