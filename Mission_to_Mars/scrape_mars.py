import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup
import time

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def getSoup(url):
    browser = init_browser()

    url = url #"https://mars.nasa.gov/news/"
    browser.visit(url)
    
    time.sleep(5)

    html = browser.html
    browser.quit()
    soup = BeautifulSoup(html, "html.parser")
    
    return soup

def click_around(url):
    
    # Create empty list
    hemisphere_image_urls = []
    
    browser = init_browser()

    url = url #"https://mars.nasa.gov/news/"
    browser.visit(url)
    
    time.sleep(5)
    
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    
    for hemElem in soup.find_all('h3'):
        
        hemDict = {}
        
        hemName = hemElem.get_text().rstrip('Enhanced')

        browser.click_link_by_partial_text(hemName)
        
        time.sleep(1)
        
        html = browser.html
        soup = BeautifulSoup(html, "html.parser")
        
        downloads = soup.find('div',class_='downloads')
        imgURL = downloads.find('a')['href']
        
        hemDict['title'] = hemName 
        hemDict['img_url'] = imgURL
        
        hemisphere_image_urls.append(hemDict)
        
        browser.back()
        
        time.sleep(1)

    browser.quit()
    
    return hemisphere_image_urls

def scrape():

    ##
    ## Mars News
    ##
    
    url = 'https://mars.nasa.gov/news/'
    soup = getSoup(url)

    # Collect all potential news stories
    news = soup.find_all('div',class_='content_title')

    # Get the first story that has a link 
    for story in news:
        if story.find('a'):
            firstNews = story.find('a').get_text()
            break
            
    teaser = soup.find('div',class_='article_teaser_body').get_text()

    ##
    ## JPL Image URL
    ##
    
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    soup = getSoup(url)

    imgLinkSuffix = soup.find("a", class_="button fancybox")['data-fancybox-href']
    featuredImgURL = 'https://www.jpl.nasa.gov' + imgLinkSuffix

    ##
    ## Mars Weather Tweets
    ##
    
    url = 'https://twitter.com/marswxreport?lang=en'
    soup = getSoup(url)

    tweetHolder = soup.find_all('article', role='article')

    # The fifth element of the list of spans should always be the tweet text of the latest tweet
    #
    # Also we need to make sure it's a tweet about weather, which isn't a guarantee.
    # Weather tweets seem to start with "InSight" so we check the first element of the text
    # If it's indeed 'InSight', we set the text to our variable and break the for loop of tweets

    for tweet in tweetHolder:   
        if (tweet.find_all('span')[4].get_text().split(" ")[0] == 'InSight'):
            tweetText = tweet.find_all('span')[4].get_text()
            break

    tweetText = tweetText.replace('\n', ", ")

    ##
    ## Pandas Scraping
    ##

    url = 'https://space-facts.com/mars/'
    tables = pd.read_html(url)
    df = tables[0]

    # Format the table and drop the index name (so it looks better when converted to HTML)
    df = df.rename(columns={0: 'Description', 1:'Value'})\
                .set_index('Description')
    del df.index.name

    # Use pandas built-in method to convert the df to an HTML table
    htmlTable = df.to_html()

    ##
    ## Mars Hemispheres
    ##

    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    hemisphere_image_urls = click_around(url)

    ##
    ## Create dict to be returned to app.py
    ##

    mars_data = {
        'headline': firstNews,
        'teaser': teaser,
        'featuredImage': featuredImgURL,
        'marsWeather': tweetText,
        'marsFacts': htmlTable,
        'hemisphereImages': hemisphere_image_urls
    }

    return mars_data
