#!/bin/env python3
#  coding : utf-8

import os
import re

import requests
import urllib3
from urllib.parse import urljoin

from scrapy.selector import Selector

urllib3.disable_warnings()

DELAY = 0  # time gap between each request
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # path to the current directory
prefic_url = "https://www.javatpoint.com"


def has_dir(dir_path):
    """
    determine if the target directory still exist, if not we create one
    :param dir_path: path to the target directory
    :return:
    """
    dir_path = dir_path.replace(": ", "").replace("*", "").replace("?", "").replace("/", "")
    dir_path = os.path.join(BASE_DIR, dir_path)
    if not os.path.isdir(dir_path):
        os.mkdir(dir_path)

def fetch(url):
    """
    fetch function based on the headers
    :param url:
    :return:  html
    """
    headers = {
        'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 5.1.1; SM-G955F Build/JLS36C)',
        'Connection': 'close',
    }
    url=urljoin(prefic_url,url)
    response = requests.get(url,headers=headers,verify=False)
    return response.text
    
def parse(html,first_dir_path,first=True):
    """
    get info on the page
    :param first_dir_path:path to first level directory
    :param first:if it is under the "Basics of Java" directory, if yes we need to treat it differently
    :return:
    """
    html = Selector(text=html)
    sub_chapters_name = html.xpath('//*[@id="menu"]/div[@class="leftmenu2"]')
    if first:
        sub_chapters_name = sub_chapters_name[:-1]
    else:
        sub_chapters_name=sub_chapters_name[1:-1]
    sub_chapters_url = html.xpath('//*[@id="menu"]/div[@class="leftmenu"]')
    for index,sub_chapter_name in enumerate(sub_chapters_name):
        sub_chapter_name = sub_chapter_name.xpath('.//span/text()').extract_first(default="null")
        sub_chapter_dir_path = os.path.join(first_dir_path, sub_chapter_name)  #path to second level directory
        has_dir(sub_chapter_dir_path)       #create second level direcotry
        urls = sub_chapters_url[index].xpath('./a')
        for url in urls:
            link = url.xpath("./@href").extract_first("")
            title = url.xpath(".//text()").extract_first("")
            sub_chapter_html = fetch(link)
            path = os.path.join(BASE_DIR, sub_chapter_dir_path,title)   #final file directory
            output_to_file(sub_chapter_html,path)
            pass
        
        
def output_to_file(sub_chapter_html, path):
    """
    get the target info to selected files from the last level html
    :param chapter_html:
    :param path:
    :return:
    """
    path = path.replace("*", "").replace("?", "").replace(": ", "").replace("/", "")
    if not os.path.isfile(path):
        html = Selector(text=sub_chapter_html)
        chapter_html = '\n'.join(html.xpath(
            '//div[@id="city"]/table/tr/td/*[not(@id="bottomnext") and not(@id="bottomnextup") and not(@class="nexttopicdiv")]//text()').extract())
        with open(path, "w", encoding="utf8") as f:
            f.write(chapter_html)


if __name__ == '__main__':
    chapters = {                    # Link from the first level html
        "Basics of Java": "java-tutorial",
        "OOPs Concepts": "java-oops-concepts",
        "Java String": "java-string",
        "Java Regex": "java-regex",
        "Exception Handling": "exception-handling-in-java",
        "Java Inner classes": "java-inner-class",
        "Java Multithreading": "multithreading-in-java",
        "Java I/O": "java-io",
        "Java Networking": "java-networking",
        "Java AWT": "java-awt",
        "Java Swing": "java-swing",
        "JavaFX": "javafx-tutorial",
        "Java Applet": "java-applet",
        "Java Reflection": "java-reflection",
        "Java Date": "java-date",
        "Java Conversion": "java-string-to-int",
        "Java Collection": "collections-in-java",
        "Java JDBC": "java-jdbc",
        "Java New Features": "New-features-in-java",
        # "RMI": "RMI",                  
        # "Internationalization": "internationalization-in-java",
        # "Interview Questions": "corejava-interview-questions",
    }
    #put all file under the current java directory
    has_dir("java")
    for chapter_name,src in chapters.items():
        first_dir_path = os.path.join("java",chapter_name)  # path to first level directory
        has_dir(first_dir_path)      # create outer directory 
        html = fetch(src)
        if chapter_name == 'Basics of Java':
            parse(html,first_dir_path=first_dir_path)
        else:
            parse(html,first_dir_path=first_dir_path,first=False)
        