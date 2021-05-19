# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.

import scrapy
import json
from scrapping.items import ScrappingItem

class MainSpider(scrapy.Spider):
    name = 'noticias'
    std_link = 'https://www.fvs.am.gov.br/noticias'
    urls = []
    for i in range(1, 59 + 1):
        urls.append(std_link + '?page=' + str(i) + '#')
    start_urls = urls

    def parse(self, response):
        item = ScrappingItem()
        std_link = self.std_link
        titulos = response.css('a.link-normal::text').getall()
        datas = response.css('td::text').getall()
        links = response.css('a.link-normal::attr(href)').getall()

        with open('noticias.json', 'a+', encoding='utf-8') as file:

            for i in range(len(titulos)):
                item['titulo'] = titulos[i]
                item['data'] = datas[i]
                item['link'] = std_link + links[i]
                line = json.dumps(dict(item), ensure_ascii=False) + "\n"
                file.write(line)
                yield item

class SubSpider(scrapy.Spider):
    name = 'atualizar'
    std_link = 'https://www.fvs.am.gov.br/noticias'
    urls = []
    for i in range(1, 2):
        urls.append(std_link + '?page=' + str(i) + '#')
    start_urls = urls

    def parse(self, response):
        item = ScrappingItem()
        std_link = self.std_link
        titulos = response.css('a.link-normal::text').getall()
        datas = response.css('td::text').getall()
        links = response.css('a.link-normal::attr(href)').getall()

        with open('noticias.json', 'a+', encoding='utf-8') as file:

            for i in range(len(titulos)):
                item['titulo'] = titulos[i]
                item['data'] = datas[i]
                item['link'] = std_link + links[i]
                if item in file:
                    break
                else:
                    line = json.dumps(dict(item), ensure_ascii=False) + "\n"
                    file.write(line)
                yield item


