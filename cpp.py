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
prefic_url = "https://www.tutorialspoint.com/cplusplus/"


def has_dir(dir_path):
    """
    determine if the target directory exist, if not we create one
    :param dir_path: path to the target directory
    :return:
    """
    dir_path = dir_path.replace(": ", "").replace("*", "").replace("?", "").replace("/", "")  # eliminate notions such as ':*?/' if using windows
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
    url = urljoin(prefic_url, url)
    response = requests.get(url, headers=headers, verify=False)
    return response.text


def parse_home_page(html):
    """
    get info on the homepage of c++
    :param html:
    :return:
    """
    html = Selector(text=html)
    uls = html.xpath('//div[@class="col-md-2"]/aside/ul')  #url with info of each class, in this case our topic of c++ tutorial
    uls= uls[:3]
    for ul in uls:
        heading = ul.xpath("./li[@class='heading']/text()").extract_first(default="")
        first_dir_path = os.path.join("cpp", heading)
        has_dir(first_dir_path)
        lis= ul.xpath("./li[not(@class)]")
        for li in lis:
            sub_heading = li.xpath('./a/text()').extract_first(default="")
            sub_url = li.xpath('./a/@href').extract_first(default="")
            sub_html = fetch(sub_url)
            sub_path = os.path.join(first_dir_path, sub_heading)
            output_to_file(sub_html,sub_path,first_dir_path)


def output_to_file(sub_chapter_html, path,first_dir):
    """
    fetch info of the target file from the last level of html, meanwhile test if there are other relative links to some useful tutorial pages
    :param chapter_html:
    :param path:
    :return:
    """
    path = path.replace("*", "").replace("?", "").replace(": ", "").replace("/", "").replace(">", "").replace("<", "")
    print(path)
    html = Selector(text=sub_chapter_html)
    if not os.path.isfile(path):
        chapter_html = '\n'.join(html.xpath('//div[@class="content"]/div/*[not(@class="pre-btn") and not(@class="nxt-btn") and not(@class="demo") and not(@class="pre-btn") and not(@class="nxt-btn") and not(@class="bottomgooglead") and not(contains(@class,"print-btn center")) and not(contains(@class,"center-aligned tutorial-menu"))]//text()').extract())    #decode documents under the current page
        chapter_html = re.sub(r'<!--.*?-->',"",chapter_html,flags=re.S|re.M)
        chapter_html=chapter_html.replace("Advertisements","")
        with open(path, "w", encoding="utf8") as f:
            f.write(chapter_html)
    detail_urls = html.xpath('//div[@class="content"]/div/*[not(@class="pre-btn") and not(@class="nxt-btn") and not(@class="demo") and not(@class="pre-btn") and not(@class="nxt-btn") and not(@class="bottomgooglead") and not(contains(@class,"print-btn center")) and not(contains(@class,"center-aligned tutorial-menu"))]//a')    #fetch the link in the current target page, if none then leave it empty
    for detail in detail_urls:
        url = detail.xpath("./@href").extract_first(default="")
        if "cplusplus" in url:
            heading = detail.xpath("./text()").extract_first(default="")
            html = fetch(url)
            detail_path = os.path.join(first_dir, heading)
            output_to_file(html,detail_path,first_dir)
    return []

if __name__ == '__main__':
    #put all files under the current cpp directory
    has_dir("cpp")        #create c++ directory
    html = fetch(url="")  #request hmepage
    parse_home_page(html)   #get info on the pages