# Web Scraping

# import splinter and beautiful soup and pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt

def scrape_all():
    # initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)

    # run all scraping funcitons and store in a dictionary
    data = {
        'news_title':news_title,
        'news_paragraph': news_paragraph,
        'featured_image': featured_image(browser),
        'facts': mars_facts(),
        'last_modified': dt.datetime.now(),
        'hemispheres': hemispheres(browser)
    }

    browser.quit()
    return data

# assign URL and instruct browser to visit it
# visit mars nasa news site
def mars_news(browser):

    url = 'https://data-class-mars.s3.amazonaws.com/Mars/index.html'
    browser.visit(url)

    # optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)


    # set up the HTML parser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    #add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
        
    except AttributeError:
        return None,None

    return news_title, news_p


# ### Featured Images

# visit URL
def featured_image(browser):
    url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url)

    # find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()


    # parse the resutling html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # add try except for error handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
        # img_url_rel
    except AttributeError:
        return None


    # use the base URL to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    
    return img_url


# ### import the mars fact table

def mars_facts():
    try:
        # use 'read_html' to scrape the facts table into a df
        df = pd.read_html('https://data-class-mars-facts.s3.amazonaws.com/Mars_Facts/index.html')[0]
    except BaseException:
        return None

    # assign columns and set index of df
    df.columns=['description', 'Mars', 'Earth']
    df.set_index('description', inplace=True)

    # convert df into HTML format, add bootstrap
    return df.to_html(classes='table table-striped')

def hemispheres(browser):

    # 1. Use browser to visit the URL 
    url = 'https://marshemispheres.com/'
    browser.visit(url)

    # 2. Create a list to hold the images and titles.
    hemisphere_image_urls = []

    # 3. Write code to retrieve the image urls and titles for each hemisphere.
    #create for loop to gather the 4 hemispheres
    for i in range(4):

        #create dictionary to hold the title and image of hemisphere
        hemispheres = {}

        #Click the link to go into each hemisphere's subpage
        browser.links.find_by_partial_text("Hemisphere")[i].click()


        #Parse the data from 
        html= browser.html
        hemi_soup = soup(html, 'html.parser')

        #Scrape the data from the hemisphere webpage
        title = hemi_soup.find("h2", class_="title").text
        img_url = hemi_soup.find("a", text="Sample").get("href") 

        #Save the full resolution url 
        # Find the relative image url
        img_url_rel = hemi_soup.find('a', text="Sample").get('href')
        hemispheres['img_url'] = f'https://marshemispheres.com/{img_url_rel}'


        #Save the hemisphere image title
        hemispheres["title"] = title
        hemisphere_image_urls.append(hemispheres) 


        #Broswe back 
        browser.back()
    # 4. Print the list that holds the dictionary of each image url and title.
    return hemisphere_image_urls




if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())

