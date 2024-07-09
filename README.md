# London Food Delivery Scraper

## Overview
The London Food Delivery Scraper is a Python-based web scraping project designed to extract detailed information from the Deliveroo app for a specific location in London. 

The project utilizes Scrapy, Selenium, and Python to gather and analyze data related to various food delivery options.

## Features
- Scrapes restaurant details including name, address, cuisine type, and rating.
- Extracts menu items and their prices.
- Collects delivery time estimates.
- Easily expandable to other food delivery platforms like JustEat.
- Customizable to different locations.

## Tech Stack
- **Python**: Core programming language.
- **Scrapy**: Web scraping framework.
- **Selenium**: Tool for web browser automation.

## Installation

1. **Clone the repository:**
   ```sh
   git clone 
   cd london-food-delivery-scraper
   ```

2. **Create and activate a virtual environment:**
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

4. **Download the appropriate WebDriver:**
   - For Chrome, download from [here](https://googlechromelabs.github.io/chrome-for-testing/)
   - Make sure to download the WebDriver based on the chrome version you are using it.
   - replace the chromedriver.exe file with your downloaded file and make sure the changes should apply to your settings.py file same here.
     ```sh
     SELENIUM_DRIVER_EXECUTABLE_PATH = <Your chromedriver path>
     ```

## Usage

1. **Run the scraper:**
   ```sh
   scrapy crawl deliveroo_spider --output deliveroo-london.csv
   ```

2. **View the scraped data:**
   - The data will be saved in the `output` folder in CSV format.

## Expanding the Project
I am planning to the expand projects on below,
- **Add new platforms:**
  - To include other food delivery platforms like JustEat, create additional spiders in the `spiders` directory.
  - Update the Scrapy settings to accommodate new platforms.

- **Modify target locations:**
  - Adjust the `TARGET_LOCATION` in the script to scrape data from different areas.

## Contact
For any questions or issues, please contact Karthick Murugan at mkarthick502@gmail.com.
