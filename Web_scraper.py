# -*- coding: utf-8 -*-
"""
Created on Sun Nov  6 12:43:29 2022

@author: AbishekH
"""

import streamlit as sl
import requests
from bs4 import BeautifulSoup
import webbrowser


#To set the page title and the icon on the web browser
sl.set_page_config(page_title="My first web scraper",page_icon=":expressionless:")

#url = https://unsplash.com/s/photos/{keyword}
#div:"ripi6"=>figure=>img:YVj9w 

main_url = "https://unsplash.com"

sl.image("https://images.unsplash.com/photo-1462143338528-eca9936a4d09")
sl.header("Web Scraper app")

form = sl.form("Search an image")
keyword = form.text_input("Enter keyword")
search = form.form_submit_button("Search")

placeholder=sl.empty()

if keyword:
    
    
    page=requests.get(f"https://unsplash.com/s/photos/{keyword}")
    
    #Check if we are successful in retreiving the page
    sl.write(page.status_code)
    
    #Start the scraping process
    soup=BeautifulSoup(page.content, features="lxml") # Extracts the html info of the page
    rows=soup.find_all("div",class_="ripi6")
    sl.write(str(len(rows))+" rows retrieved")
    
    col1,col2,col3 = placeholder.columns(3)
    
    for index,row in enumerate(rows):
        figures=row.find_all("figure")
        for i in range(3):
            #Instead of scraping the entire set, scrape only the first 3 images in each row
            img_data=figures[i].find("img",class_="YVj9w")
            
            #While img contains the entire image info, we want only the sourceset info 'srcset
            #The srcset itself is quite long and the useful part of this is till the '?' character from the start of the string.
            #So we want to extract only till that. hence split the string based on '?'
            image = img_data['srcset'].split("?")[0]
            
            #Scraping further for downloading. For this we need to access the 'a' item
            #and from that we need to extract the href property - the Hyperreference
            anchor = figures[i].find('a', class_='rEAWd')
            href = anchor['href']
            if not i:
                col1.image(image)
                btn=col1.button("Download",key=str(index)+str(i))
                #The 'key' argument is used to provide a unique key to each download button
                if btn:
                    webbrowser.open_new_tab(main_url+href)
            elif i==1:
                col2.image(image)
                btn=col2.button("Download",key=str(index)+str(i))
                if btn:
                    webbrowser.open_new_tab(main_url+href)
            else:
                col3.image(image)
                btn=col3.button("Download",key=str(index)+str(i))
                if btn:
                    webbrowser.open_new_tab(main_url+href)
        
        