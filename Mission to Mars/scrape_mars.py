# Import Splinter, BeautifulSoup, and Pandas
import pandas as pd
import datetime as dt
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup as bs



def scrape():
    # Initiate chromedriver
    chromedriver_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **chromedriver_path, headless=True)

    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in a dictionary
    data_dict = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": jpl_featured_image(browser),
        "facts": mars_facts(),
        "hemispheres": hemispheres(browser),
        "last_modified": dt.datetime.now()
    }

    # Stop webdriver and return data
    browser.quit()
    return data_dict



### NASA Mars News
def mars_news(browser):
    # Visit the Mars NASA news site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    # Convert the browser html to a soup object
    html = browser.html
    soup = bs(html, "html.parser")

    # Print soup
    print(soup.prettify)

    # Extract all li items
    lists = soup.find_all('li', class_='slide')

    # .find() the content title and save it as `news_title`
    news_title = lists[0].find('div', class_='content_title').text
    print(news_title)

    # .find() the paragraph text
    news_paragraph = lists[0].find('div', class_='article_teaser_body').text
    print(news_paragraph)

    return news_title, news_paragraph



### JPL Space Images Featured Image
def jpl_featured_image(browser):
    # Set the executable path and initialize the chrome browser in splinter
    url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'

    # Visit JPL space images Mars URL 
    browser.visit(url)

    # Convert the browser html to a soup object
    html = browser.html
    soup = bs(html, "html.parser")

    # Find and click the full image button
    image_href = soup.find('a', attrs={'class': 'showimg fancybox-thumbs'}).get('href')
    browser.click_link_by_href(image_href)

    featured_image_url = f"https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{image_href}"
    print(featured_image_url)
    return featured_image_url



### Mars Facts
def mars_facts():
    # Create a dataframe from the space-facts.com mars page
    url = 'https://space-facts.com/mars/'

    mars_profile_df = pd.read_html(url)[0]
    mars_profile_df

    # clean the dataframe and export to HTML
    mars_profile_df.columns=['Attribute', 'Value']
    mars_profile_df.set_index('Attribute')

    return mars_profile_df.to_html(classes="table table-striped")



### Hemispheres
def hemispheres(browser):
    # Visit the USGS astrogeology page for hemisphere data from Mars
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    # Convert the browser html to a soup object
    html = browser.html
    soup = bs(html, "html.parser")

    # First, get a list of all of the hemispheres
    hemispheres_soup = soup.find_all('div', class_='description')
    print(hemispheres_soup)

    hemisphere_dict = {}
    hemisphere_urls = []

    # Next, loop through those links, click the link, find the sample anchor, return the href
    for i in hemispheres_soup:
        
        hemisphere_dict = {}
        
        # We have to find the elements on each loop to avoid a stale element exception
        image_href = i.find('a', attrs={'class': 'itemLink product-item'}).get('href')
        image_url = (f"https://astrogeology.usgs.gov{image_href}")
        hemisphere_dict['img_url'] = image_url
        
        # Visit image_url
        browser.visit(image_url)
        
        html = browser.html
        indiv_hemisphere_soup = bs(html, 'html.parser')
        
        # Get Hemisphere title
        hemisphere_dict['title'] = indiv_hemisphere_soup.find('h2', class_='title').text
        
        # Append hemisphere object to list
        hemisphere_urls.append(hemisphere_dict)
        
        # Finally, we navigate backwards with browser.back()
        browser.back()

    return hemisphere_urls

if __name__ == "__main__":
    print(scrape())