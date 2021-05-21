from subprocess import Popen
from time import sleep

PREFIX_PATH = r'C:\Users\heylu\Documents\github\noticias-FVS-AM\scrapping'

def atualizar():
    print('atualizando...')
    Popen.wait(Popen('conda run -n noticias-fvs-am scrapy crawl atualizar',
                     cwd=PREFIX_PATH, shell=True), 
                     timeout=360)


atualizar()
print('JSON atualizado.')
sleep(10)

