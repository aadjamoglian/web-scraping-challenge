from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
from bs4 import BeautifulSoup
from pprint import pprint
import requests
import pandas as pd
import time

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)


def scrape_info():
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    time.sleep(5)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    result = soup.find("li", class_="slide")

    # NASA Title

    title_text = result.h3.text
    print(title_text)

    # NASA Summary

    p_text = result.find("div", class_="article_teaser_body").text
    print(p_text)

    url2 = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url2)

    try:
        browser.click_link_by_partial_text('FULL IMAGE')
            
    except ElementDoesNotExist:
        print("Scraping Complete")   
        
    time.sleep(5)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    image_link_short = soup.find("div", class_="fancybox-inner").img['src']
    print(image_link_short)

    # Cover Image full URL

    browser.quit()

    image_link = f"https://www.jpl.nasa.gov{image_link_short}"
    print(image_link)

    twitter_mars = "https://twitter.com/marswxreport?lang=en"

    page = requests.get(twitter_mars)

    soup = BeautifulSoup(page.text, "html.parser")

    # Mars weather

    mars_weather = soup.find("p", class_="TweetTextSize").text
    print(mars_weather)

    mars_table_url = "https://space-facts.com/mars/"

    response = requests.get(mars_table_url)
    soup = BeautifulSoup(response.content,'html.parser')
    table = soup.find('table')

    # Mars table in dataframe

    dfs = pd.read_html(str(table))

    df = dfs[0]

    # df = df.index = ["row_0", "row_1", "row_2", "row_3", "row_4", "row_5", "row_6", "row_7", "row_8"]

    df.columns = ["key", "value"]

    df.set_index("key")

    df = df.to_html()

    # df = df.to_dict("records")

    print(df)


    ### FOR SCRAPE FUNCTION

    hemi_names_list = []
    hemis_image_links = []
    mars_hemis = []

    hemi_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"

    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    browser.visit(hemi_url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    browser.windows[0]
    for i in range(0,4):
        hemi_names_list.append(soup.find_all("h3")[i].text)

    for i in hemi_names_list:
        
        try:
            browser.click_link_by_partial_text(i)

        except ElementDoesNotExist:
            print("Scraping Complete")
            
        time.sleep(5)
        
        try:
            browser.click_link_by_partial_text('Sample')
            
        except ElementDoesNotExist:
            print("Scraping Complete")
            
        time.sleep(5)
            
        browser.windows.current = browser.windows[hemi_names_list.index(i)+1]
        
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        
        hemi_image_link = soup.img['src']
        
        hemis_image_links.append(hemi_image_link)
        
        browser.windows.current = browser.windows[0]
        
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        
        browser.back()
        
        time.sleep(5)   
        
    time.sleep(2)
        
        
    for i in range(0,4):
        mars_hemis.append({"title": hemi_names_list[i], "image_url": hemis_image_links[i]})


    # Store data in a dictionary
    mars_data = {
        "news_title": title_text,
        "news_p": p_text,
        "featured_image_url": image_link,
        "mars_weather": df,
        "hemisphere_image_urls": mars_hemis
    }

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data
