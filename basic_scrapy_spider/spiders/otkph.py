import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time

# Path to chromedriver executable
options = webdriver.ChromeOptions()
options.add_argument('--headless')
service = Service("/usr/local/bin/chromedriver")

driver = webdriver.Chrome(service=service, options=options)

class OtkphSpider(scrapy.Spider):
    name = 'otkph'
    start_urls = ['https://otkph.am/shop/']

    def parse(self, response):
        products = response.css('.woocommerce-LoopProduct-link::attr(href)').extract()

        for index, product in enumerate(products):
            yield scrapy.Request(url=product, callback=self.parseOtkphProduct)

    def parseOtkphProduct(self, response):
        driver.get(response.url)
        
        # Wait for the page to load completely
        time.sleep(5)  # You might want to adjust this delay as necessary

        # List of potential IDs
        potential_ids = [
            "pa_amount",  # The ID you provided
            "pa_dose",  # Add other potential IDs here
            # "yet_another_possible_id"
        ]

        dropdown_found = False

        for potential_id in potential_ids:
            try:
                # Wait for the dropdown to be present
                dropdown_present = EC.presence_of_element_located((By.ID, potential_id))
                WebDriverWait(driver, 5).until(dropdown_present)
                
                # If the dropdown is found, select the first option
                dropdown = driver.find_element(By.ID, potential_id)
                select = Select(dropdown)
                select.select_by_index(1)  # Index 1 corresponds to the first option
                
                # Add a delay to ensure the selection is completed
                time.sleep(2)  # Adjust the delay time as needed

                dropdown_found = True
                print(f"Dropdown with ID {potential_id} found and option selected")
                break  # Exit the loop if a dropdown is found

            except Exception as e:
                print(f"Dropdown with ID {potential_id} not found")

        if not dropdown_found:
            print("No dropdown found with the provided IDs")

        # Continue with further scraping or actions on the page
        # For example, you can extract more data from the page here
