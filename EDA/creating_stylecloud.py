import pandas as pd
import stylecloud

with open('stopwords.txt', 'r', encoding='utf-8') as file:
    stop_words = file.read().split('\n')
stop_words = [x.strip() for x in stop_words]

df = pd.read_json(r'C:\Users\heylu\Documents\github\noticias-FVS-AM\scrapping\noticias.json', lines=True)

txt = ''
for x in df['titulo']:
    txt += x + " "

txt = txt.split()

for word in stop_words:
    while word in txt:
        txt.remove(word)

txt = " ".join(x for x in txt)

with open('stylecloud.txt', 'w', encoding='utf-8') as file:
    file.write(txt)

stylecloud.gen_stylecloud(file_path='stylecloud.txt', 
                          stopwords=stop_words,  
                          gradient='vertical', 
                          size=1920, 
                          icon_name='fas fa-lungs',
                          random_state=42)