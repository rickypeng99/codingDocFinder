
# coding: utf-8

# In[1]:


from bs4 import BeautifulSoup
from selenium import webdriver 
from selenium.webdriver.chrome.options import Options
import re 
import urllib
import pandas as pd
options = Options()
options.headless = True
browser = webdriver.Chrome('./chromedriver',options=options)


# In[2]:


title = []
description = []
links = []
Syntax = []
Text = []


# In[4]:


def get_js_soup(url,browser):
    browser.get(url)
    res_html = browser.execute_script('return document.body.innerHTML')
    soup = BeautifulSoup(res_html,'html.parser') #beautiful soup object to be used for parsing html content
    return soup


# In[5]:


dir_url = 'https://doc.bccnsoft.com/docs/cppreference_en/all_c_functions.html'
soup = get_js_soup(dir_url,browser)   


# In[7]:


find = soup.find_all('td',class_='category-table-td')


# In[9]:


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


# In[26]:


web_base = "https://doc.bccnsoft.com/docs/cppreference_en/"


# In[27]:


for link_holder in soup.find_all('td',class_='category-table-td'): 
    try:
        rel_link = link_holder.find('a')['href']
        links.append(web_base + rel_link)
    except:
        continue


# In[52]:


for url in links:
    soupp = get_js_soup(url,browser)  
    try:
        Syntax.append(soupp.find('pre',class_='syntax-box').get_text(separator=' '))
    except:
        Syntax.append(" ")
    Text.append(soupp.getText())


# In[62]:


df = pd.DataFrame({'title':title, 'url':links, 'description':description, 'syntax':Syntax,
                   'text':Text })


# In[63]:


df.to_csv('C_Library.csv', index=False, encoding='utf-8')

