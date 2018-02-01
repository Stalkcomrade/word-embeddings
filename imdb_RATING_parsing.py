# -*- coding: utf-8 -*-
"""
Created on Fri Jan 12 13:19:35 2018

@author: stlk
"""

#%%


#%%

#### Motivation

## Alternative approach:
### In fact, use of selenium wasn't necessarian: even despite the fact that urls provided
### in archive redirect to the non-existing page. Best approach is to parse urls from the pages
### with errors; afterwards, scrap content from the movie-centric pages: the pages seemed to be
### static

#### disable images, js, css and flash to increase speed up browsing


import re

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import NoSuchElementException

def install_proxy(PROXY_HOST,PROXY_PORT):
        fp = webdriver.FirefoxProfile()
        print(PROXY_PORT)
        print(PROXY_HOST)
        fp.set_preference('permissions.default.image', 2) # images false
        fp.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'False') # flash false
        fp.set_preference("javascript.enabled", 'False') # javascript false
        fp.set_preference("permissions.default.stylesheet", 2) # css false
        fp.set_preference("network.proxy.type", 1)
        fp.set_preference("network.proxy.http",PROXY_HOST)
        fp.set_preference("network.proxy.http_port",int(PROXY_PORT))
        fp.set_preference("network.proxy.https",PROXY_HOST)
        fp.set_preference("network.proxy.https_port",int(PROXY_PORT))
        fp.set_preference("network.proxy.ssl",PROXY_HOST)
        fp.set_preference("network.proxy.ssl_port",int(PROXY_PORT))  
        fp.set_preference("network.proxy.ftp",PROXY_HOST)
        fp.set_preference("network.proxy.ftp_port",int(PROXY_PORT))   
        fp.set_preference("network.proxy.socks",PROXY_HOST)
        fp.set_preference("network.proxy.socks_port",int(PROXY_PORT))   
        fp.set_preference("general.useragent.override","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A")
        fp.update_preferences()
        return webdriver.Firefox(firefox_profile=fp)


def open_browser(PROXY_HOST,PROXY_PORT):
    global driver
    driver = install_proxy(PROXY_HOST,PROXY_PORT)
    driver.get("http://www.imdb.com/")
    
def close_browser():
    driver.close()



### Scrapping list of proxies, if mine IP is blocked 

import pandas as pd
import urllib.request as urllib2

url = "https://free-proxy-list.net/"
req = urllib2.Request(url, headers={'User-Agent' : "Magic Browser"}) 
con = urllib2.urlopen(req)
html = con.read()

dfs = pd.read_html(html, match=".+")
print(dfs[0])
df = dfs[0]
df_sub = df[(df.Anonymity == 'elite proxy') & (df.Https == "yes")]
#df_sub.loc["Used"] = False
df_sub = df_sub.assign(Used = False)



#%%

#### Reading table with commentaries' urls
#### Motivation: I want to evaluate amount of movies presented.

urls_list = open('/home/stlk/Desktop/pwc/data/aclImdb/test/urls_pos.txt', 'r').read().split('\n')
main = pd.DataFrame(data = urls_list, columns = ['urls'])
main['status'] = False
# main.rename(columns = {'Link eLibrary':'Ссылка'}, inplace=True)

#%%

l_pd_main = pd.DataFrame()


#%%

#### Making simple progress bar

import progressbar
import time
from lxml import html


bar = progressbar.ProgressBar(max_value=len(urls_list))


#%%

#### In case of block, function to change proxy

def change_ip(url = "http://www.imdb.com/"):
    try:
        close_browser()
    except:
        pass
    ip = ''.join(df_sub.loc[df_sub["Used"] == False, "IP Address"].sample(n = 1))
    port = list(map(int, df_sub.loc[df_sub["IP Address"] == ip,"Port"].tolist()))
    open_browser(ip, port[0])    
    df_sub.loc[df_sub["IP Address"] == ip, "Used"] = True
    # login()

change_ip()

#%%        

n = 1
path = "/home/stlk/Desktop/pwc/imdb_additional/"
l_pd_main =  pd.read_csv(path + "train/l_pd_main.csv")

l_pd_main = l_pd_main[['director', 'metacritic', 'n_votes', 'paper_name',
                      'rating', 'screenplay', 'source', 'stars']]
l_pd_main = l_pd_main.drop_duplicates(subset = 'paper_name') ## paper_name == movie label

# l_pd_main = pd.DataFrame()
main = pd.read_csv(path + "train/main.csv")

#%%



from bs4 import BeautifulSoup
import codecs
import os
    

#### looping until all is downloaded

while not all(main['status'].tolist()):
    
    first_flag = False
    second_flag = False
    third_flag = False
    
    if n % 1000 == 0: # every 1000 pages change proxy
        change_ip(id)
        
    try:

        id = main.loc[main['status'] == False, 'urls'].sample(n = 1)
        id = ''.join(id.tolist())        
    
        bar.update(sum(main['status']))
        
        driver.implicitly_wait(8)
        driver.get(id)
        
        #### 1
        first_flag = True
        ###
        
        #### set flags  for debugging ####
        
        soup = BeautifulSoup(driver.page_source, "lxml")

        #### prints all the links with corresponding text

        for i in soup.select('.error_attrib'):
            current_movie = "".join(i.text.split(",")[1:len(i.text.split(","))]).strip('\n').strip()
        
        l_pd_main = l_pd_main[pd.notnull(l_pd_main['paper_name'])] # remove rows with empty movies labels in order to escape errors on next line
        l_pd_main.paper_name = l_pd_main.paper_name.apply(
                lambda x: x.strip().replace(u'\xa0', ' '))
        
        #### 2
        second_flag = True
        ###
        
        

        ### If movie's data is already in a data frame - go to next link        
        if not(l_pd_main.paper_name.apply(lambda x: x == current_movie).any()):
            try:
                driver.implicitly_wait(8)
                ### redirect to correct page
                driver.find_element_by_xpath('/html/body/div/div[4]/a').click()
            except NoSuchElementException:
                third_flag = True
                print("Something went wrong, third_flag")
           
            
            
            completeName = os.path.join(path + "train/", "current.html")
            file_object = codecs.open(completeName, "w", "utf-8")
            html = driver.page_source
            file_object.write(html)
            
                
            ### I prefer to use Selenium in python, while, generally, 
            ### rvest for scrapping (xpath supported, in Soup they are not)
            ### That is why for parsing each page I call R script
            import subprocess
            subprocess.call("/usr/bin/Rscript --vanilla " + path + "scrapping_local.R", shell=True)
            l_pd = pd.read_csv(path + "train/current.csv")
            l_pd['source'] = id
       
            ### Write back to file
            l_pd_main = pd.concat([l_pd_main, l_pd], ignore_index=True)
            l_pd_main.to_csv(path + "train/l_pd_main.csv")
            main.loc[main['urls'] == id, 'status'] = True
            main.to_csv(path + "train/main.csv")
            n += 1
            
        else: # if movie's data already presented in pd, check as done
        
            #### Status
            main.loc[main['urls'] == id, 'status'] = True
            
            n += 1
        
    except:
        print('ERROR: Something went completely wrong in %s link' % id)
        print(first_flag, second_flag, third_flag) #### Debugging
        change_ip()