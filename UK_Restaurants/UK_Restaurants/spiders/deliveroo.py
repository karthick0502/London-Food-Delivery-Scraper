import scrapy
import time
from scrapy_selenium import SeleniumRequest
from scrapy.selector import Selector
from scrapy_selenium import SeleniumRequest
from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class DeliverooSpider(scrapy.Spider):
    name = "deliveroo"
    allowed_domains = ["deliveroo.co.uk"]
    start_urls = ["https://deliveroo.co.uk"]
    custom_headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    scraped_urls = set()  # Set to store unique URLs or identifiers of scraped items

    def scroll_incrementally(self, driver, scroll_pause_time=1, final_wait_time=3):
        """Scrolls the page incrementally in smaller steps based on the total page height and viewport height."""
        last_height = driver.execute_script("return document.body.scrollHeight")
        same_height_counter = 0  # To keep track of how many times the height is the same

        while True:
            # Scroll down by the viewport height
            driver.execute_script("window.scrollBy(0, window.innerHeight);")
            # Wait to load page
            time.sleep(scroll_pause_time)

            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                same_height_counter += 1
                # If height hasn't changed for a few iterations, assume bottom is reached
                if same_height_counter > 5:
                    break
            else:
                same_height_counter = 0  # Reset counter if height changes
                last_height = new_height

        # Final wait at the bottom of the page
        time.sleep(final_wait_time)

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.locations, headers=self.custom_headers)
            # yield SplashRequest(url, callback=self.parse_, args={'wait': 30, 'timeout': 120,
            #                                                      'headers': self.custom_headers})

    def locations(self, response):
        # Extract the link to london location
        london_all_delivery = r"https://deliveroo.co.uk/restaurants/london/st-james's?fulfillment_method=DELIVERY&geohash=gcpvj0e5712f&collection=all-restaurants"
        # yield response.follow(london_all_delivery, callback=self.parse_each, headers=self.custom_headers)
        # yield SplashRequest(london_all_delivery, callback=self.parse_common, endpoint='execute',
        #                     args={'wait': 30,
        #                           'timeout': 90,
        #                           'lua_source': self.scroll_script},
        #                     headers=self.custom_headers)
        # appearance = response.css('div#home-feed-container ul li.HomeFeedGrid-b0432362335be7af:last-child').\
        #     css('div.HomeFeedUICard-b69bd49414a33f36.HomeFeedUICard-5d60bf3bab3dc6f0')
        yield SeleniumRequest(url=london_all_delivery,
                              wait_time=120,
                              callback=self.parse_common,
                              # wait_until=EC.presence_of_element_located((By.CSS_SELECTOR, appearance)),
                              headers=self.custom_headers)

    def parse_common(self, response):
        driver = response.request.meta["driver"]
        # Scroll the page slowly to the bottom
        self.scroll_incrementally(driver, scroll_pause_time=1, final_wait_time=3)

        # get the HTML from the actual driver
        selector = Selector(text=driver.page_source)

        list_of_all_restaurants = selector.css('div#home-feed-container ul li.HomeFeedGrid-b0432362335be7af')
        print('****************************')
        print(len(list_of_all_restaurants))

        for restaurant in list_of_all_restaurants:
            image_url = restaurant.css('div.ccl-a897ba3fd642670d.ccl-92294f995a389ac9::attr(style)').get()
            if image_url:
                image_url = image_url.split('url("')[-1].split('")')[0]
            name = restaurant.css('.ccl-ff5caa8a6f2b96d0.ccl-40ad99f7b47f3781::text').get()
            ratings = restaurant.css('li.HomeFeedUILines-55cd19148e4c15d6 .HomeFeedUILines-d9843e1bd87b0546'
                                     ':nth-child(3) span::text').get()
            minimum_delivery_fare = restaurant.css('li.HomeFeedUILines-55cd19148e4c15d6+* span::text').get()
            restaurant_url = restaurant.css('a::attr(href)').get()

            # Ensure we only yield unique items
            if restaurant_url and restaurant_url not in self.scraped_urls:
                self.scraped_urls.add(restaurant_url)
                yield {
                    'name': name,
                    'ratings': ratings,
                    'delivery_fare': minimum_delivery_fare,
                    'logo': image_url,
                    'url': restaurant_url
                }

    def parse_each(self, response):
        list_of_all_restaurants = response.css('div#home-feed-container ul li.HomeFeedGrid-b0432362335be7af')
        link = list_of_all_restaurants[0].css('a').attrib['href']
        # yield SeleniumRequest(url=self.start_urls[0] + link, wait_time=3, callback=self.parse,
        #                       headers=self.custom_headers)
        # yield SplashRequest(self.start_urls[0] + link, callback=self.parse, headers=self.custom_headers,
        #                     args={'wait': 1})
        for restaurant in list_of_all_restaurants:
            links = restaurant.css('a').attrib['href']
            yield SeleniumRequest(url=self.start_urls[0] + links, wait_time=1, callback=self.parse,
                                  headers=self.custom_headers)

    def parse(self, response):
        # images_url = scrape_image_url(response.url)
        # Extract other data using Scrapy selectors
        headers = response.css('div.MenuHeader-ab8bb00d5a4371e7').css('h1::text').get()
        image_url_style = response.css('div.ccl-a897ba3fd642670d.ccl-92294f995a389ac9').attrib['style']
        # Parse the style attribute to extract the image URL
        image_url = image_url_style.split('url("')[-1].split('")')[0]
        additional_info_tags = response.css('.ccl-45f32b38c5feda86')
        ratings = response.css('.ccl-a5e1512b87ef2079+ .ccl-a5e1512b87ef2079 .ccl-a396bc55704a9c8a span::text').get()
        # react_model = response.css('div.ReactModalPortal::text').getall()
        # Loop through each div tag
        additional_info = []
        for add_info in additional_info_tags:
            # Extract text from the div tag and join them with |
            additional_info.append(''.join(add_info.css('::text').getall()))
        yield {
            'title': headers,
            'image_url': image_url,
            'ratings': ratings,
            'additional_info': additional_info,
            'Business': 'Deliveroo'
        }
