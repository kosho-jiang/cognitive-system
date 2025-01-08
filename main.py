import os
import openai 

from similarity import calculate_similarity    
from read import load_and_split_text_with_length
from estimate import generate_next_text
from output import create_pdf   

text = load_and_split_text_with_length("testcases/usakusai.txt")
OpenAI_API_KEY = os.environ["OPENAI_API_KEY"]   

if __name__ == "__main__":  
    scoresum = 0
    for i in range(len(text)):
        if i == len(text) - 1:
            break

        else:
            previous_text_list = [item['sentence'] for item in text[0:i+1]]
            previous_text = '。'.join(previous_text_list)
            next_text_length = text[i+1]['length']            

            similarity = calculate_similarity(OpenAI_API_KEY, text[i]['sentence'], text[i+1]['sentence'], next_text_length, True)
            print(similarity)
            text[i+1]['score'] = similarity
            scoresum += similarity
            i = i + 1     

        text[0]['score'] = scoresum/len(text)   

    print(text)

    create_pdf(text, "output.pdf")
