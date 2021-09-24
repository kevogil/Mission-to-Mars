#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Import Splinter, BeautifulSoup, and Pandas
import pandas as pd
import re

from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup as bs
from time import sleep


# In[2]:


# Path to chromedriver
def init_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser('chrome', **executable_path, headless=False)


# In[3]:


# Set the executable path and initialize the chrome browser in splinter
url = 'https://mars.nasa.gov/news/'
browser = init_browser()


# ## Visit the NASA mars news site

# In[4]:


# Visit the mars nasa news site
browser.visit(url)


# In[5]:


# Convert the browser html to a soup object and then quit the browser
html = browser.html
soup = bs(html, "html.parser")

browser.quit()


# In[6]:


# Print soup
print(soup.prettify)


# In[7]:


# Extract all li items
lists = soup.find_all('li', class_='slide')


# In[8]:


# .find() the content title and save it as `news_title`
news_title = lists[0].find('div', class_='content_title').text
print(news_title)


# In[9]:


# .find() the paragraph text
news_paragraph = lists[0].find('div', class_='article_teaser_body').text
print(news_paragraph)


# ## JPL Space Images Featured Image

# In[10]:


# Set the executable path and initialize the chrome browser in splinter
url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'

browser = init_browser()


# In[11]:


# Visit JPL space images Mars URL 
browser.visit(url)

# Convert the browser html to a soup object
html = browser.html
soup = bs(html, "html.parser")


# In[12]:


# Find and click the full image button
image_href = soup.find('a', attrs={'class': 'showimg fancybox-thumbs'}).get('href')

browser.click_link_by_href(image_href)

featured_image_url = f"https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{image_href}"


# In[13]:


print(featured_image_url)


# In[14]:


browser.quit()


# ## Mars Facts

# In[15]:


# Create a dataframe from the space-facts.com mars page
url = 'https://space-facts.com/mars/'

mars_profile_df = pd.read_html(url)[0]
mars_profile_df


# In[16]:


# clean the dataframe and export to HTML
mars_profile_df.columns=['Attribute', 'Value']
mars_profile_df.set_index('Attribute')


# ## Hemispheres

# In[21]:


# visit the USGS astrogeology page for hemisphere data from Mars
url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

browser = init_browser()
browser.visit(url)

# Convert the browser html to a soup object
html = browser.html
soup = bs(html, "html.parser")


# In[22]:


# First, get a list of all of the hemispheres
hemispheres_soup = soup.find_all('div', class_='description')
print(hemispheres_soup)


# In[23]:


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


# In[24]:


browser.quit()


# In[25]:


# View the hemisphere urls to make sure they look good
hemisphere_urls

