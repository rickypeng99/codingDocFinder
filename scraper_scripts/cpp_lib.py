
# coding: utf-8

# In[65]:


from bs4 import BeautifulSoup
from selenium import webdriver 
from selenium.webdriver.chrome.options import Options
import re 
import urllib
import pandas as pd
options = Options()
options.headless = True
browser = webdriver.Chrome('./chromedriver',options=options)


# In[66]:


title = []
description = []
Syntax = []
Text = []
links = []


# In[67]:


def get_js_soup(url,browser):
    browser.get(url)
    res_html = browser.execute_script('return document.body.innerHTML')
    soup = BeautifulSoup(res_html,'html.parser') #beautiful soup object to be used for parsing html content
    return soup


# In[68]:


dir_url = 'https://doc.bccnsoft.com/docs/cppreference_en/all_cpp_functions.html'
soup = get_js_soup(dir_url,browser)   


# In[69]:


find = soup.find_all('td',class_='category-table-td')


# In[71]:


i = 0
while i < len(find):
    a = find[i].get_text(separator=' ')
    a = a.replace("\n","")
    a = a.replace("      "," ")
    title.append(a)
    i += 1
    a = find[i].get_text(separator=' ')
    a = a.replace("\n","")
    a = a.replace("      "," ")
    description.append(a)
    i += 1


# In[83]:


web_base = "https://doc.bccnsoft.com/docs/cppreference_en/"


# In[84]:


for link_holder in soup.find_all('td',class_='category-table-td'): #get list of all <div> of class 'photo nocaption'
    try:
        rel_link = link_holder.find('a')['href']
        if rel_link == "iterators.html":
            continue
        if rel_link == "io_flags.html#format_flags":
            continue
        if rel_link == "complexity.html":
            continue
        links.append(web_base + rel_link)
    except:
        continue


# In[87]:


for url in links:
    soupp = get_js_soup(url,browser)  
    try:
        Syntax.append(soupp.find('pre',class_='syntax-box').get_text(separator=' '))
    except:
        Syntax.append(" ")
    Text.append(soupp.getText())


# In[90]:


df = pd.DataFrame({'title':title, 'url':links, 'description':description, 'syntax':Syntax,
                   'text':Text })


# In[91]:


df.to_csv('Cpp_Library.csv', index=False, encoding='utf-8')

