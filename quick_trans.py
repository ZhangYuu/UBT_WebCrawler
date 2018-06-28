#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 26 11:19:17 2018

@author: Memo
"""
import requests
import re
from bs4 import BeautifulSoup
from pandas import DataFrame
import pandas

state='alaska'

#alaska

#washitondc

city=''
#url_ori="https://www.quicktransportsolutions.com/carrier/" + state + "/trucking-companies.php"  #almost
url_ori="https://www.quicktransportsolutions.com/carrier/" + state + "/truckingcompanies/trucking-companies.php" #alaska
#url_ori="https://www.quicktransportsolutions.com/carrier/" + state + "/trucking-companies/trucking-companies.php" #mississippi,montana,northdakota,washiton
doc_name=state+".csv"

def check_city(url_ori):
    city_lis=[]
    post_html = requests.post(url_ori)
    print post_html
    if str(post_html)=="<Response [200]>":
        print "correct url"
        html = requests.get(url_ori)
        soup=BeautifulSoup(html.content,'html.parser')
#        city=soup.find_all("td",align="10%")#normal
        city=soup.find_all("td")#alask
#        city=soup.find_all("td",width="10%")#california,oregon,texas
#        city=soup.find_all("td",align="11%")#nebraska
        
        for i in city:
            if " " not in str(i.text.encode('ascii', 'ignore').decode('ascii')).lower():
                city_lis.append(str(i.text.encode('ascii', 'ignore').decode('ascii')).lower())
            else:
                city_lis.append(str(i.text.encode('ascii', 'ignore').decode('ascii')).lower().replace(" ","-"))                
        return city_lis

def check_comp(url_city):
    print url_city
    html = requests.get(url_city)
    soup=BeautifulSoup(html.content,'html.parser')
    comp=soup.find_all("div",itemtype="https://schema.org/Organization")
    #comp=soup.find_all("div",class="well well-sm")
    print comp
    header = ["Company","Phone Number"]
    df=DataFrame(columns=header)
    for com in comp:
#        com_count=[]
#        info = str(com.text.encode('ascii', 'ignore').decode('ascii'))
        name=str(com.find("b").text.encode('ascii', 'ignore').decode('ascii'))
#        address=com.find("span",itemprop="address").text
        try:
            tel=str(com.find("b",itemprop="telephone").text.encode('ascii', 'ignore').decode('ascii'))
        except:
            tel=''
        print tel
        #comp_lis.append(info)
        #comp_lis.append([name,tel])
        df.loc[len(df)]=[name,tel]
    df.to_csv(doc_name, mode='a', header=False)
    return df

city_lis=check_city(url_ori)
print city_lis
for city in city_lis:        
    #URL address here is a liitle bit different
    url_city="https://www.quicktransportsolutions.com/carrier/"+ state +"/truckingcompanies/" + city +".php" # 
#    url_city="https://www.quicktransportsolutions.com/carrier/"+ state +"/" + city +".php" # normal
    com=check_comp(url_city)
#df.to_csv('my_csv.csv', mode='a', header=False)