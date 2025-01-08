import os
import openai 

from similarity import calculate_similarity    
from read import load_and_split_text_with_length
from estimate import generate_next_text
from output import create_pdf   

text = load_and_split_text_with_length(file_path)
OpenAI_API_KEY = os.environ["OPENAI_API_KEY"]   



if __name__ == "__main__":  
    for i in range(len(text)):
        previous_text_list = [item['sentence'] for item in text[0:i+1]]
        previous_text = '。'.join(previous_text_list)
        next_text_length = text[i+1]['length']
        estimate_text = generate_next_text(OpenAI_API_KEY, previous_text, next_text_length)
