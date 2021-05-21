from subprocess import Popen
from time import sleep
from git import Repo
from os import environ
from time import sleep
import yaml

with open(r'C:\Users\heylu\Documents\github\noticias-FVS-AM\scrapping\config.yml', 'r') as file:
    config = yaml.safe_load(file)

PREFIX_PATH = config['path']['prefix_path']
USER = environ.get('GITHUB_USER')
PASSWORD = environ.get('GITHUB_PASSWORD')
PATH = config['path']['repo_path']
remote = f"https://{USER}:{PASSWORD}@github.com:/noticias-FVS-AM.git"

def atualizar():
    print('atualizando...')
    Popen.wait(Popen('conda run -n noticias-fvs-am scrapy crawl atualizar',
                     cwd=PREFIX_PATH, shell=True), 
                     timeout=360)


def git_push():
    try:
        print('Atualizando dados...')
        repo = Repo(
            path=PATH)
        repo.git.add(PATH, update=True)
        repo.index.commit(f"BOT")
        origin = repo.remote(name='origin')
        origin.push()
    except:
        print('Erro durante tentativa de push.')


atualizar()
print('JSON atualizado.')
sleep(3)
git_push()
print('Push feito com sucesso.')
sleep(15)
