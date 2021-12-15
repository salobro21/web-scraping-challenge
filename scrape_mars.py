from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

def scrape_data():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    url = 'https://redplanetscience.com/'  
    browser.visit(url)

    for x in range(1):
        html = browser.html
        soup = bs(html, 'html.parser')
    
        container = soup.find('section', class_='image_and_description_container')
    
        news_title = container.find('div', class_='content_title').text
        news_p = container.find('div', class_='article_teaser_body').text

        mars_news = {
            "news_title": news_title,
            "news_paragraph": news_p
        }

        print(mars_news)

    url = 'https://spaceimages-mars.com/'
    browser.visit(url) 

    for x in range(1):
        html = browser.html
        soup = bs(html, 'html.parser')
    
        container = soup.find('div', class_='floating_text_area')
    
        browser.links.find_by_partial_text('FULL IMAGE').click()
    
        box = container.find('a', class_='showimg fancybox-thumbs')
    
        featured_image_url = box['href']
        featured_image_url = url + featured_image_url

        jpl_feat_image = {
            "feat_image_url": featured_image_url
        }
        
        print(jpl_feat_image)

    url = 'https://galaxyfacts-mars.com/'

    tables = pd.read_html(url)

    mars_earth_df = tables[0]
    mars_earth_df = mars_earth_df.rename(columns = mars_earth_df.iloc[0])
    mars_earth_df = mars_earth_df.set_index("Mars - Earth Comparison")
    mars_earth_df = mars_earth_df.iloc[1:]
    
    print(mars_earth_df)

    html_table = mars_earth_df.to_html(index_names=False, justify="center", border = 0, classes=["table", "table-striped", "table-bordered", "table-hover"])

    url = 'https://marshemispheres.com/'

    browser.visit(url)

    html = browser.html
    soup = bs(html, 'html.parser')
    
    hemisphere_image_urls = []
    
    descriptions = soup.find_all('h3', limit=4)

    for title in descriptions:

        browser.links.find_by_partial_text(title.text).click()

        html = browser.html
        soup = bs(html, 'html.parser')

        downloads = soup.find('div', class_='downloads')

        img_list = downloads.find('li')

        img_url = img_list.a['href']

        img_url = url + img_url

        dictionary = {
            "title": title.text,
            "img_url": img_url
            }

        hemisphere_image_urls.append(dictionary) 

        browser.back()

        print(hemisphere_image_urls)

    browser.quit()

    mars_data = {
        "mars_news": mars_news,
        "jpl_feat_image": jpl_feat_image,
        "mars_facts": html_table,
        "hemisphere_image_urls": hemisphere_image_urls
    }

    return mars_data

