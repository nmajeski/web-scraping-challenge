# Dependencies
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd

def init_browser():
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    return Browser('chrome', **executable_path, headless=False)

def scrape():    
    browser = init_browser()
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    news_title = None
    news_p = None
    is_visible = browser.is_element_visible_by_css('ul.item_list', wait_time=10)
    if is_visible:
        try:
            slides = browser.find_by_css('li.slide')
            image_and_description_container = slides[0].find_by_css('div.image_and_description_container')
            list_text = image_and_description_container.find_by_css('div.list_text')
            news_title = list_text.find_by_css('a').text
            print(f"Found news title: {news_title}")
            news_p = list_text.find_by_css('div.article_teaser_body').text
            print(f"Found news paragraph: {news_p}")
        except:
            print("Error finding the news title and/or news paragraph...")
    else:
        print("Could not find any top news.")

    featured_image_domain = 'https://www.jpl.nasa.gov'
    featured_image_url = None
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    is_visible = browser.is_element_visible_by_css('article.carousel_item', wait_time=10)
    if is_visible:
        try:
            carousel_item = browser.find_by_css('article.carousel_item')
            background_image_str = carousel_item['style']
            url_ending_start_index = background_image_str.find('"') + 1
            url_ending_end_index = background_image_str.rfind('"')
            background_image_url_ending = background_image_str[url_ending_start_index:url_ending_end_index]
            featured_image_url = featured_image_domain + background_image_url_ending
            print(f"Found featured image URL {featured_image_url}.")
        except:
            print("Error finding feature image URL...")
    else:
        print("Could not find a feature image.")

    mars_weather = None
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)

    is_visible = browser.is_element_visible_by_css('div.css-901oao.r-hkyrab.r-1qd0xha.r-a023e6.r-16dba41.r-ad9z0x.r-bcqeeo.r-bnwqim.r-qvutc0', wait_time=10)
    if is_visible:
        try:
            tweet = browser.find_by_css('div.css-901oao.r-hkyrab.r-1qd0xha.r-a023e6.r-16dba41.r-ad9z0x.r-bcqeeo.r-bnwqim.r-qvutc0')
            mars_weather = tweet.text
            print(f"Found mars weather tweet: {mars_weather}")
        except:
            print("Error finding Mars weather tweet...")
    else:
        print("Could not find the tweets for Mars weather.")

    url = 'https://space-facts.com/mars/'
    tables = pd.read_html(url)
    df = tables[0]
    df.columns = ['', 'Data']
    df = df.set_index('')
    html_str = df.to_html()
    print(f"Table HTML string:\n{html_str}")

    hemisphere_image_urls = None
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    is_visible = browser.is_element_visible_by_css("div.collapsible.results", wait_time=10)
    if is_visible:
        try:
            results = browser.find_by_css("div.collapsible.results")
            items = results.find_by_tag('div.item')
            item0 = items[0]
            item_link0 = item0.find_by_css('div.description a')
            title0 = item_link0.find_by_tag('h3').text
            url0 = item_link0['href']
            item1 = items[1]
            item_link1 = item1.find_by_css('div.description a')
            title1 = item_link1.find_by_tag('h3').text
            url1 = item_link1['href']
            item2 = items[2]
            item_link2 = item2.find_by_css('div.description a')
            title2 = item_link2.find_by_tag('h3').text
            url2 = item_link2['href']
            item3 = items[3]
            item_link3 = item3.find_by_css('div.description a')
            title3 = item_link3.find_by_tag('h3').text
            url3 = item_link3['href']
            browser.visit(url0)
            link0 = browser.find_by_text("Original")["href"]
            browser.visit(url1)
            link1 = browser.find_by_text("Original")["href"]
            browser.visit(url2)
            link2 = browser.find_by_text("Original")["href"]
            browser.visit(url3)
            link3 = browser.find_by_text("Original")["href"]
            hemisphere_image_urls = [
                {"title": title0, "img_url": link0},
                {"title": title1, "img_url": link1},
                {"title": title2, "img_url": link2},
                {"title": title3, "img_url": link3}
            ]
            print(f"Found hemisphere titles and image URLs: {hemisphere_image_urls}")
        except:
            print("Error occurred while finding hemipshere titles and links...")
    else:
        print("Could not find the hemisphere title and image links.")

    return {"news_title": news_title, "news_p": news_p, "featured_image_url": featured_image_url, "mars_weather": mars_weather, "html_str": html_str, "hemisphere_image_urls": hemisphere_image_urls}