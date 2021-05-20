import pandas as pd
import streamlit as st

pd.set_option('display.max_colwidth', -1)


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
    return float('NaN')

def make_clickable(link):
    # target _blank to open new window
    # extract clickable text to display for your link
    return f'<a target="_blank" href="{link}">>'

# link is the column with hyperlinks
df = pd.read_json(r'C:\Users\heylu\Documents\github\noticias-FVS-AM\scrapping\noticias.json', lines=True)

df['link'] = df['link'].apply(make_clickable)
df['palavra-chave'] = df['titulo'].apply(norm_keywords)
df['data'] = [x[:x.index('-') - 1] for x in df['data']]
df = df[['data','titulo', 'palavra-chave', 'link']]
df = df.to_html(escape=False)


st.write(df, unsafe_allow_html=True)
#st.write(df.to_hml(escape=False, index=False), unsafe_allow_html=True)