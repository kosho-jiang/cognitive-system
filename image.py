import base64
import os
import openai
from openai import OpenAI

client = OpenAI()

OpenAI_API_KEY = os.environ["OPENAI_API_KEY"]

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def image_to_text(api_key, image_path: str) -> str:
    openai.api_key = api_key
    try:
        image = encode_image(image_path)
        prompt = (
            f"画像は漫画の一ページです．その内容を各コマについて小説調で説明する文章を40文字程度生成してください:\n"
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
    text=""
    for i in range(1,21):
        image_path=f"testcases/shanks/shanks_{i}.png"
        tmp = image_to_text(OpenAI_API_KEY,image_path)
        text += tmp
    
    with open("testcases/shanks/shanks_text.txt", "w", encoding="utf-8") as file:
        file.write(text)

    '''
    lines = text.split("\n")
    result = []
    index = 0
    delimiter = "。"
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
    
    for item in result:
        output_file_path = "testcases/shanks/shanks_output.txt"
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            for item in result:
                output_file.write(f"Index: {item['index']}, Sentence: {item['sentence']}, Is First Line: {item['is_first_line']}, Length: {item['length']} \n")
        print(f"Output written to {output_file_path}")
    '''