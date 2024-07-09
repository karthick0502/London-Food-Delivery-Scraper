import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

# url = r"https://deliveroo.co.uk/menu/London/marylebone/simple-health-kitchen-baker-st?day=today&geohash=gcpvj0e56cwp&time=ASAP"


def scrape_image_url(url):
    # Set up Chrome options with headless mode
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Load the webpage
    driver.get(url)

    time.sleep(5)  # Wait for 5 seconds

    # Get the page source after dynamic content is loaded
    page_source = driver.page_source

    # Parse the page source with BeautifulSoup
    soup = BeautifulSoup(page_source, 'html.parser')

    # Find the div elements with the style attribute
    div_with_image = soup.find('div', class_='ccl-a897ba3fd642670d ccl-92294f995a389ac9')

    # Extract the style attribute
    style_attribute = div_with_image['style']

    # Extract the image URL from the style attribute
    image_url_start = style_attribute.find('url("') + len('url("')
    image_url_end = style_attribute.find('")', image_url_start)
    image_url = style_attribute[image_url_start:image_url_end]

    # Quit the Selenium driver
    driver.quit()

    return image_url

# print(scrape_image_url(url))