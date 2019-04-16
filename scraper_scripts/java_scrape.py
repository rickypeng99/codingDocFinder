import scrapy
from bs4 import BeautifulSoup
import re


class javaSpider(scrapy.Spider):
    name = 'java'

    start_urls = [
        'https://www.tutorialspoint.com/java/'
    ]

    custom_settings = {
        'LOG_LEVEL': 'ERROR'
    }
    #indicating the current index of url
    number = 1

    #saving all urls
    urls = []
    def parse(self, response):
        prefix = 'https://www.tutorialspoint.com/java/'
        soup = BeautifulSoup(response.body, 'html.parser')

        suffices = soup.find_all('a', href = re.compile(r"/java/\w*.htm$"))
        for suffix in suffices:
            url = re.sub('/java/', '', suffix.get('href'))
            #preventing from duplicated websites
            if("Next Page" not in suffix.get_text()):
                javaSpider.urls.append(prefix + url)
        #print(javaSpider.urls)

        yield scrapy.Request(javaSpider.urls[javaSpider.number - 1], callback = self.parse_details)
    
    def parse_details(self, response):
        soup = BeautifulSoup(response.body, 'html.parser')

        paragraph = soup.find('div', class_ = "content")
        innerContent = paragraph.findChild('div', class_ = "col-md-7 middle-col")
        contents = innerContent.find_all(['h1', 'p', 'h2'])
        
        title = str(javaSpider.number) + ". "+ innerContent.find('h1').get_text()
        print("--------------------" + title + "----------------------")
        
        if("/" in title):
            title = re.sub("/", "", title)
        
        f = open("../database_assets/java2/" + title + ".txt", "w+")
        for content in contents:
            f.write(content.get_text() + "\n")
        f.close()
        #disabling asynchronous behavior of yield
        javaSpider.number += 1
        yield scrapy.Request(javaSpider.urls[javaSpider.number - 1], callback = self.parse_details)

    

    

