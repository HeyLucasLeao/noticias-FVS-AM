import pandas as pd
import streamlit as st
from PIL import Image
from unidecode import unidecode

def norm_keywords(x):
    dici = {
        'Febre amarela': ['febre amarela'],
        'Cloroquina': ['cloroquina'],
        'Dengue': ['aedes', 'aegypti', 'dengue'],
        'Vacina para Covid-19': ['vacina', 'dose', 'doses', 'vacinas', 'vacinação', 'vacinaram', 'auditoria', 'já completou 30 municípios', 'imunizados', 'imunização'],
        'Pessoas recuperadas': ['recuperados', 'recuperadas', 'neste domingo', 'sexta feira 17 07', 'altas médicas'] ,
        'Cenário epidomiológico': ['epidemiológico', 'epidemiológica', 'nesta sexta feira 19', 'amazonas atualizado', 'variantes', 'variante', 'panorama da covid 19', 'reinfecção', 'boletim', 'covid 19 no amazonas', 'situação da', 'municípios', 'estado', 'atualizados', 'amazonas neste', 'nesta quarta feira', 'restrições', 'wilson lima', 'combate ao', 'investigação ao novo coronavírus', 'medidas', 'monitora', 'monitoramento', 'informações oficiais', 'divulgado', 'cenário da covid-19', 'balanco da covid-19', 'enfrentamento a covid-19', 'enfrentamento à covid-19', 'cenário do novo coronavírus', 'atualização da covid-19', 'dados da pandemia'],
        'Novos casos de Covid-19': ['total de casos', 'número de casos', 'novos casos', 'confirmados', 'casos', 'amazonas contabiliza', 'amazonas chegam', 'ultrapassam', 'novos dados', 'pessoas', 'caso do novo', 'graves do novo', 'caso de covid-19', 'cenários da covid-19', 'panorama da covid-19', 'taxa de transmissão'],
        'Suspeita de Covid-19': ['suspeita', 'suspeito', 'suspeitos', 'dados da covid-19'],
        'Testes a Covid-19': ['testes', 'teste', 'dão negativo', 'dão positivo', 'dá positivo', 'dá negativo', 'detecção de covid-19', 'testagem'],
        'Prevenção a Covid-19': ['prevenção', 'propagação de covid-19', 'epis', 'enfrentamento a covid-19'],
        'Morte por Covid-19': ['mortes por corona virus', 'mortes por covid 19', 'mortes pelo novo corona virus', 'mortes', 'mortos', 'óbitos', 'morte', 'óbito'],
        'Influenza': ['influenza'],
        'Estabelecimentos, eventos & festas clandestinas': ['estabelecimento', 'estabelecimentos', 'festas', 'bar', 'pessoas na zona', 'bares', 'festa', 'festas', 'clandestinas', 'clandestina', 'pessoas nas ruas', 'supermercados', 'supermercado', 'regionais', 'flagradas', 'flagrado', 'fiscalização', 'locais', 'local', 'bebida', 'bebidas', 'pessoas no', 'protocolo', 'escola', 'escolas', 'professores', 'vistoria', 'vistorias', 'transporte', 'não essenciais', 'não essencial', 'ensino privado', 'restaurantes', 'aglomerações', 'funcionamento de serviços', 'evento', 'eventos'],
        'Malária': ['malária', 'mais de 300 pacientes'],
        'Tuberculose': ['tuberculose']
    }
    for key, value in dici.items():
        for y in value:
            if y in x.lower():
                return key
    return " "
    
def traduzir_data(x):
    dici = {'Jan': '01',
    'Fev': '02',
    'Mar': '03',
    'Abr': '04',
    'Mai': '05',
    'Jun': '06',
    'Jul': '07',
    'Ago': '08',
    'Set': '09',
    'Out': '10',
    'Nov': '11',
    'Dez': '12'}

    x = x.split()
    x[1] = dici[x[1]]
    return "-".join(y for y in x)

def make_clickable(link):
    return f'<a target="_blank" href="{link}">>'

def search_words(x, df):
    dataset = df['titulo'].apply(unidecode).copy()
    dataset = [x.lower() for x in dataset]
    x = unidecode(x)
    x = x.lower()
    res = df.index[[pd.Series(x.split()).isin(y.split()).values[0] for y in dataset]].tolist()
    return df.loc[res]


df = pd.read_json(r'C:\Users\heylu\Documents\github\noticias-FVS-AM\scrapping\noticias.json', lines=True)

df['link'] = df['link'].apply(make_clickable)
df['categoria'] = df['titulo'].apply(norm_keywords)
df['data'] = [x[:x.index('-') - 1] for x in df['data']]
df['data'] = df['data'].apply(traduzir_data)
df['data'] = pd.to_datetime(df['data'], format="%d-%m-%Y")
df['data'] = df['data'].dt.date
df.sort_values('data', inplace=True, ascending=False)
df.reset_index(inplace=True)
df.drop(columns='index', inplace=True)
df = df[['data','titulo', 'categoria', 'link']]

img = Image.open(r'C:\Users\heylu\Documents\github\noticias-FVS-AM\stylecloud\stylecloud.png')
st.title('Notícias da Fundação de Vigilância em Saúde do Amazonas (FVS-AM)')
st.image(img,width=None)

inp = st.text_input('Pesquise notícia por palavras no título')
cat = st.multiselect('Categoria',options=df['categoria'].unique())

if cat:
    mask_cat = df['categoria'].isin(cat)
    df = df[mask_cat]

if inp:
    st.write(search_words(inp, df).to_html(escape=False, index=False), unsafe_allow_html=True)
else:
    st.write(df[:10].to_html(escape=False, index=False), unsafe_allow_html=True)

