from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

# Set up Chrome options with headless mode
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# Load the webpage
driver.get(r"https://deliveroo.co.uk/menu/London/marylebone/simple-health-kitchen-baker-st?day=today&geohash=gcpvj0e56cwp&time=ASAP")

url = "https://deliveroo.co.uk/restaurants/london/st-james's?geohash=gcpvj0e5712f"

# Wait for the page to fully load (adjust the sleep time as needed)
import time
time.sleep(5)  # Wait for 5 seconds

# Find the button using the given CSS selector
button = driver.find_element_by_css_selector('.ccl-a5e1512b87ef2079 button')
button.click()

# Wait for the pop-up to appear (adjust wait time as needed)
driver.implicitly_wait(10)

# Get the HTML content of the pop-up
popup_html = driver.page_source

# Parse the page source with BeautifulSoup
soup = BeautifulSoup(popup_html, 'html.parser')

# Find the div elements with the style attribute
div_with_image = soup.find('div', class_='ccl-a897ba3fd642670d ccl-92294f995a389ac9')

# Extract the style attribute
style_attribute = div_with_image['style']

dynamic = soup.find('div', class_='ReactModalPortal')

# Extract the image URL from the style attribute
image_url_start = style_attribute.find('url("') + len('url("')
image_url_end = style_attribute.find('")', image_url_start)
image_url = style_attribute[image_url_start:image_url_end]

print(image_url)

# Quit the Selenium driver
driver.quit()
