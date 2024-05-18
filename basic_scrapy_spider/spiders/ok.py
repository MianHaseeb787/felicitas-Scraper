import scrapy
from basic_scrapy_spider.items import QuoteItem
from datetime import date as dt, datetime, timezone
import scrapy
import gspread
import pytz
import json
from google.oauth2 import service_account

scopes = [
    'https://www.googleapis.com/auth/spreadsheets', 
    'https://www.googleapis.com/auth/drive',
    'https://mail.google.com/' 
]
creds = service_account.Credentials.from_service_account_file("credentials.json", scopes=scopes)
client = gspread.authorize(creds)

sheet_id = "15LB8LrV-dXuOoE6oG40i8PhR0iJ9iDZ2MhxQrPCiWks"
sheet = client.open_by_key(sheet_id)

worksheets = sheet.worksheets()


class QuotesSpider(scrapy.Spider):


    name = 'ok'
    # allowed_domains = ['quotes.toscrape.com']
    start_urls = ['https://flcts.eu/products/']


    dataRows = []
    # felicitas_counter = 0

    def parse(self, response):

            products = response.css('.button::attr(href)').extract()
            

            # meta = {"productsLen" : productsLen}

            for index, product in enumerate(products):
                meta = {'index': index}  # Include the index in metadata
                yield scrapy.Request(url=product, callback=self.parsefelicitasProduct, meta=meta)
        
            

    def parsefelicitasProduct(self, response):

        # productsLen = response.meta['productsLen']

        productName = response.css('.entry-title::text').get().strip()
        productPrice = response.css('.elementor-widget-woocommerce-product-price bdi::text').get().strip()
        productPrice = productPrice.replace(',', ".")

        productStock = response.css('.in-stock::text').get()

        if productStock is None:
            productStock = "0"

        print('\n')

        try:
            if 'in stock' in productStock:
                productStock = productStock.replace('in stock', "")
        except Exception as e:
            print(e)

        print(f"product Name : {productName}")
        print(f"product Price : {productPrice}")
        print(f"product Stock : {productStock}")

        data = {
            'Product Name': productName,
            'Price': productPrice,
            'Stock': productStock
        }

        index = response.meta['index']  # Retrieve the index from metadata
        # Ensure that the dataRows list has enough elements
        while len(self.dataRows) <= index:
            self.dataRows.append({})
            
        self.dataRows[index] = data