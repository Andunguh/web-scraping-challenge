# imports
# Import Splinter, BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
import datetime as dt
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
        "newsParagraph": news_paragraph,
        "featuredImage": scrape_feature_img(browser),
        "facts": scrape_facts_page(browser),
        "hemispheres": scrape_hemispheres(browser),
        "lastUpdated": dt.datetime.now()
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

def scrape_feature_img(browser):

    # Visit the Mars news site

    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find & click full image button

    full_image_link = browser.find_by_tag('button')[1]
    full_image_link.click()

    # Parse the resulting html with soup

    img_html = browser.html
    img_soup = soup(img_html, 'html.parser')
    
    # image url
    
    img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    # Use the base url to create an absolute url

    img_url = f'https://spaceimages-mars.com/{img_url_rel}'

    # return image url

    return img_url




#scrape through the facts page
def scrape_facts_page(browser):

    # Visit URL
    url = 'https://galaxyfacts-mars.com/'
    browser.visit(url)

    # Parse the resulting html with soup

    html = browser.html
    fact_soup = soup(html, 'html.parser')

    # find the facts location

    factsLocation = fact_soup.find('div', class_="diagram mt-4")
    factTable = factsLocation.find('table') # grab the html code for the fact table

    # create an empty string

    facts= ""

    # add text to empty string

    facts += str(factTable)

    return facts




# scrape through the hemispheres pages
def scrape_hemispheres(browser):

    # base url

    base_url = 'https://marshemispheres.com/'

    browser.visit(base_url)

    # Create a list to hold the images and titles.
    hemisphere_image_urls = []

    # set up the loop

    for i in range(4):
        # loop through each of the pages
        # hemisphere info dict
        hemisphereInfo = {}

        # find the elements on each loop to avoid a stale element execption

        browser.find_by_css('a.product-item img')[i].click()

        # next, we find the sample image anchor tag and extract href 

        sample = browser.links.find_by_text('Sample').first
        hemisphereInfo["img_url"] = sample['href']

        # Get hemisphere title

        hemisphereInfo['title'] = browser.find_by_css('h2.title').text

        # append hemisphere object to list

        hemisphere_image_urls.append(hemisphereInfo)

        # we navagate backwards

        browser.back()

    # return  the hemispheres url with the titles
    return hemisphere_image_urls





# set up a flask app

if __name__ == "__main__":
    print(scrape_all())