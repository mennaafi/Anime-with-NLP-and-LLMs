import scrapy  
from bs4 import BeautifulSoup  

class BlogSpider(scrapy.Spider):  
    name = 'narutospider'  
    start_urls = ['https://naruto.fandom.com/wiki/Special:BrowseData/Jutsu?limit=250&offset=0&_cat=Jutsu']  

    def parse(self, response):  
        for href in response.css('.smw-columnlist-container a::attr(href)').extract():  
            yield scrapy.Request(response.urljoin(href), callback=self.parse_jutsu)  

        for next_page in response.css('a.mw-nextlink::attr(href)').extract():  
            yield response.follow(next_page, self.parse)  

    def parse_jutsu(self, response):  
        jutsu_name = response.css("span.mw-page-title-main::text").get(default='').strip()  

        div_selector = response.css("div.mw-parser-output").get()  
        soup = BeautifulSoup(div_selector, 'html.parser')  

        jutsu_type = ""  
        aside = soup.find('aside')  
        if aside:  
            for cell in aside.find_all('div', {'class': 'pi-data'}):  
                if cell.find('h3'):  
                    cell_name = cell.find('h3').text.strip()  
                    if cell_name == "Classification":  
                        jutsu_type = cell.find('div').text.strip()  
        
        if aside:  
            aside.decompose()  

        jutsu_description = soup.get_text().strip()  
        jutsu_description = jutsu_description.split('Trivia')[0].strip()  

        yield {  
            'jutsu_name': jutsu_name,  
            'jutsu_type': jutsu_type,  
            'jutsu_description': jutsu_description  
        }