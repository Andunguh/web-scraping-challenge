# imports
# Import Splinter, BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
#import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
from pprint import pprint



# scrape finctions
def scrape_all():

    # Set up Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    
    # the goal is to return a json that has all the necessary data so that it can load to mongodb

    # get the information for the news page
    news_title, news_paragraph = scrape_news(browser)

    # buuild a dict from scrapes
    
    marsData = {
        "newsTitle": news_title,
        "newsParagraph": news_paragraph
    }

    # stop the webdriver
    browser.quit()


    # display output

    return marsData




# scrape the mars news page

def scrape_news(browser):
    # go to the Mars Nasa news site

    url = 'https://redplanetscience.com/'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object
    html = browser.html
    news_soup = soup(html, 'html.parser')

    slide_elem = news_soup.select_one('div.list_text')
    # grabs the title
    news_title = slide_elem.find('div', class_="content_title").get_text()

    # grabs the paragraph
    news_p = slide_elem.find('div', class_="article_teaser_body").get_text()

    # return the title and paragraph

    return news_title, news_p




# scrape through the featured image page




#scrape through the facts page




# scrape through the hemispheres pages


# set up a flask app

if __name__ == "__main__":
    print(scrape_all())