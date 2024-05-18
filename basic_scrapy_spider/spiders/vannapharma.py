import scrapy
from basic_scrapy_spider.items import QuoteItem
from datetime import date as dt, datetime, timezone
import scrapy
import gspread
import pytz
import json
from google.oauth2 import service_account
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time

options = webdriver.ChromeOptions()
options.add_argument('--headless')
service = Service("/usr/local/bin/chromedriver")

driver = webdriver.Chrome(service=service, options=options)

# scopes = [
#     'https://www.googleapis.com/auth/spreadsheets', 
#     'https://www.googleapis.com/auth/drive',
#     'https://mail.google.com/' 
# ]
# creds = service_account.Credentials.from_service_account_file("credentials.json", scopes=scopes)
# client = gspread.authorize(creds)

# sheet_id = "1tyx1QmOeYv0w9pJ0QpTmvTVR2yRVnWiGlLfBNwz-JRc"
# sheet = client.open_by_key(sheet_id)

# worksheets = sheet.worksheets()


class astrovialsSpider(scrapy.Spider):


    name = 'vannapharma'
    # allowed_domains = ['quotes.toscrape.com']
    start_urls = ['https://otkph.am/shop/']


    dataRows = []

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


    # def closed(self, reason):
    #     print("Closed")


    #     print(self.dataRows)

    #     for i, worksheet in enumerate(worksheets):
            
    #         # worksheet = sheet.get_worksheet(i)

    #         # current_date = dt.today()
    #         # date = current_date.isoformat()

    #         us_eastern = pytz.timezone('US/Eastern')
    #         us_Date = datetime.now(us_eastern).date()

    #         usDateStr = datetime.strftime(us_Date, "%Y-%m-%d")

    #         print(f"usDate time {us_Date}")

    #         # utcDate = datetime.now(timezone.utcoffset())
    #         # print(f"utcDate {utcDate}")
    #         # print(f"tzinfo  {utcDate.tzname()}")

    #         # utcDateStr = datetime.strftime(utcDate, "%Y-%m-%d")
    #         # print(utcDateStr)
            
           
    #         print(f"product is {self.dataRows[i]}")
        

    #         lastRowIndex = len(worksheet.get_all_values())
    #         print(f"last Row index{lastRowIndex}")

    #         if lastRowIndex == 1:
    #             print("in condition 1")
    #             data_to_write = []

    #             product1 = self.dataRows[i] 
    #             print(f"product 1 is {product1}")
                
    #             data_to_write.append([product1.get('Product Name', ''), product1.get('Price', ''), product1.get('Stock', ''), 
    #                                     ])
                
    #             print(f"data_to_write   {data_to_write}")

    #             productName =  product1.get('Product Name', '')
    #             worksheet.update_cell(lastRowIndex+1,1,productName)

    #             productPrice =  product1.get('Price', '')
    #             worksheet.update_cell(lastRowIndex+1,2,productPrice)

    #             stock =  product1.get('Stock', '')
    #             worksheet.update_cell(lastRowIndex+1,3,stock)

    #             # date update
    #             worksheet.update_cell(2,7,usDateStr)
            
    #         else:
    #             lastRowDate = worksheet.cell(lastRowIndex, 7).value
                
    #             # utcDateStr = datetime.strftime(utcDate, "%Y-%m-%d")
    #             if lastRowDate is not None:
    #                 lastRowDate = datetime.strptime(lastRowDate, "%Y-%m-%d").date()

    #             # print(f"tzinfo  {lastRowDate.tzname()}")
    #             # lastRowDate = lastRowDate.replace(tzinfo=timezone.utc)
    #             # print(f"tzinfo  {lastRowDate.tzname()}")

    #                 lastRowDate = datetime.strftime(lastRowDate, "%Y-%m-%d" )

    #             # lastRowDate_utc = lastRowDate.replace(tzinfo=timezone('UTC'))
    #                 print("LLLLASSSTTT")
    #                 print(lastRowDate)
                
                

    #             if lastRowDate == usDateStr:
    #                 print("Same Date as Today")

    #                 # # Write the current stock values to the "Previous Stock" column
    #                 stockValue = worksheet.cell(lastRowIndex,3).value
    #                 worksheet.update_cell(lastRowIndex,4, stockValue)

    #                 # loading A b c

    #                 # data_to_write = []

    #                 product1 = self.dataRows[i]
                    
    #                 # data_to_write.append([product1.get('Product Name', ''), product1.get('Price', ''), product1.get('Stock', ''), 
    #                 #                         ])
                    
                                    
    #                 # print(f"data_to_write   {data_to_write}")

    #                 productName =  product1.get('Product Name', '')
    #                 worksheet.update_cell(lastRowIndex,1,productName)

    #                 productPrice =  product1.get('Price', '')
    #                 worksheet.update_cell(lastRowIndex,2,productPrice)

    #                 stock =  product1.get('Stock', '')
    #                 worksheet.update_cell(lastRowIndex,3,stock)

                
    #                 # range_name = 'A2:C'  
    #                 # request_body = {
    #                 #     'value_input_option': 'USER_ENTERED',  
    #                 #     'data': [
    #                 #         {
    #                 #             'range': range_name,  
    #                 #             'values': data_to_write,  
    #                 #         }
    #                 #     ]
    #                 # }
    #                 # service = discovery.build('sheets', 'v4', credentials=creds)
    #                 # response = service.spreadsheets().values().batchUpdate(spreadsheetId=sheet.id, body=request_body).execute()


    #                 # calc
                    
    #                 previousStock =  worksheet.cell(lastRowIndex,4).value
    #                 if previousStock is not None:
    #                     previousStock = int(previousStock)
    #                     print(f"previous stock {previousStock}")

    #                 else:
    #                     previousStock = 0



        

    #                 stock = self.dataRows[i].get('Stock', '')
    #                 print(f"stock {stock}")

    #                 if stock:
    #                     stock = int(stock)
    #                 else:
    #                     stock = 0

    #                 currentPrice = self.dataRows[i].get('Price', '')
    #                 if currentPrice:
    #                      currentPrice = float(currentPrice)
    #                 else:
    #                     currentPrice = 0

    #                 currentSoldStock = previousStock - stock
    #                 if currentSoldStock < 0:
    #                     currentSoldStock = 0
    #                 print(f"cuurent sold stock ::: {currentSoldStock}")
    #                 # if currentSoldStock < 1:
    #                 #     currentSoldStock = 0

    #                 CurrentRevenue = currentPrice * currentSoldStock

    #                 # adding into sold stock and revenue
    #                 soldStock =  worksheet.cell(lastRowIndex,5).value
    #                 if soldStock is None:
    #                     soldStock = 0
    #                 soldStock = int(soldStock)

                

    #                 updatedSoldStock = soldStock + currentSoldStock

    #                 Revenue =  worksheet.cell(lastRowIndex,6).value
    #                 if Revenue is None:
    #                     Revenue = 0

    #                 Revenue = float(Revenue)

    #                 updatedRevenue = Revenue + CurrentRevenue

    #                 worksheet.update_cell(lastRowIndex,5,updatedSoldStock)
    #                 worksheet.update_cell(lastRowIndex,6,updatedRevenue)



    #             else:
    #                 print("NOOOO")
    #                 print("Date Changed")

    #                 newRow = lastRowIndex + 1
    #                 preStk = worksheet.cell(lastRowIndex,3).value
    #                 worksheet.update_cell(newRow,4, preStk)

    #                 # load a b c g

    #                 # data_to_write = []

    #                 product1 = self.dataRows[i]
                        
    #                 # data_to_write.append([product1.get('Product Name', ''), product1.get('Price', ''), product1.get('Stock', ''), 
    #                 #                             ])
                    
                                    
    #                 # print(f"data_to_write   {data_to_write}")
                    
    #                 productName =  product1.get('Product Name', '')
    #                 worksheet.update_cell(newRow,1,productName)

    #                 productPrice =  product1.get('Price', '')
    #                 worksheet.update_cell(newRow,2,productPrice)

    #                 stock =  product1.get('Stock', '')
    #                 worksheet.update_cell(newRow,3,stock)

    #                 # calcs
    #                 previousStock =  preStk
    #                 if previousStock is not None:
    #                     previousStock = int(previousStock)
    #                     print(f"previous stock {previousStock}")

    #                 else:
    #                     previousStock = 0



        

    #                 stock = self.dataRows[i].get('Stock', '')
    #                 print(f"stock {stock}")

    #                 if stock:
    #                     stock = int(stock)
    #                 else:
    #                     stock = 0

    #                 currentPrice = self.dataRows[i].get('Price', '')
    #                 if currentPrice:
    #                      currentPrice = float(currentPrice)
    #                 else:
    #                     currentPrice = 0

    #                 currentSoldStock = previousStock - stock
    #                 if currentSoldStock < 0:
    #                     currentSoldStock = 0
    #                 print(f"cuurent sold stock ::: {currentSoldStock}")
    #                 # if currentSoldStock < 1:
    #                 #     currentSoldStock = 0

    #                 CurrentRevenue = currentPrice * currentSoldStock

    #                 # adding into sold stock and revenue
    #                 soldStock =  0
    #                 if soldStock is None:
    #                     soldStock = 0
    #                 soldStock = int(soldStock)

                

    #                 updatedSoldStock = soldStock + currentSoldStock

    #                 Revenue =  0
    #                 if Revenue is None:
    #                     Revenue = 0

    #                 Revenue = float(Revenue)

    #                 updatedRevenue = Revenue + CurrentRevenue

    #                 worksheet.update_cell(newRow,5,updatedSoldStock)
    #                 worksheet.update_cell(newRow,6,updatedRevenue)


    #                 # update Date
    #                 worksheet.update_cell(newRow,7, usDateStr)
    