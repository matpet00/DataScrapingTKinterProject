import re
import sys

from datetime import datetime as dt
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException

from time import sleep
class Scraper:
    def __init__(self,page):
        # Initialize the Scraper with a webpage and an empty list to hold cleaned data

        self.page = page
        self.create_session()
        self.cleaned_data =[]

    # Property setter and getter to ensure valid page format
    @property
    def page(self):
        return self._page

    @page.setter
    def page(self, value):
        regex_pattern = r"(https://)?(www\..+)"
        if not re.search(regex_pattern, value):
            raise ValueError('Invalid page format!')
        self._page = value


    # Create a Chrome WebDriver session
    def create_session(self):
        chrome_options = Options()
        chrome_options.add_experimental_option("detach",True)
        service = Service('./Driver/chromedriver.exe')
        self.session = webdriver.Chrome(service=service, options=chrome_options)
        self.session.get(self.page)
        return self.session


    # Get data from the table containing dividend information
    def get_data(self):
        '''gets the data from the table containing dividend information'''

        #trying to access element and waiting for possible page load
        for _ in range(2):
            try:
                content = self.session.find_elements(By.CSS_SELECTOR, 'div.mp-table-body-row-container.mp-table-row.t-static')
            except NoSuchElementException as Exception:
                Sleep(3)
                print(f'Error, element not found {Exception}')
            else:
                self.raw_data = [items.text for items in content]
                self.format_raw_data()



    # Fetch headers for data
    def get_headers(self):
        '''fetch headers for data'''

        for _ in range(2):
            try:
                content = self.session.find_elements(By.CSS_SELECTOR, 'div.mp-table-header-row-container.t-shadow-sticky-anchor')
            except NoSuchElementException as Exception:
                Sleep(3)
                print(f'Error, element not found {Exception}')
            else:
                self.headers = [items.text for items in content]
                self.format_headers()

    # Format headers by splitting, replacing, and deleting specific elements
    def format_headers(self):
        '''Takes care of formating headers to desired format'''
        try:
            headers = self.headers[0].split('\n')
            headers = [data for index, data in enumerate(headers) if index not in (0, 2, 14, 15)]
            headers = [f"{items}_DATE" if items in ('DECLARED', 'EX-DIV', 'PAY') else items for items in headers]
            headers = [items for items in headers if items != 'DATE']
            headers[2] = headers[2].replace(" ", "_")
            headers[-4] = 'LAST_AMOUNT'
            del headers[-1]
            self.headers = headers

        except IndexError:
            print('Could not get the headers!')


     # Format raw data by splitting, replacing, and deleting specific elements
    def format_raw_data(self):
        '''Formating of the raw data to meet desired format'''

        for items in self.raw_data:
            data = items.split('\n')
            data = [data for index, data in enumerate(data) if index not in (1, 14, 15)]
            data = [f"{items}/2023" if "/" in items else items for items in data]
            data = [items for items in data if items not in ('2023','2024')]
            del data[-2]
            self.cleaned_data.append(data)

    def cast_values(self):
        '''Format values to corresponding datatype.'''

        data = self.cleaned_data.copy()

        def cast_value(entry):
            if '%' in entry:
                try:
                    cleaned_value = entry.replace('%', '')
                    return float(cleaned_value)
                except ValueError as Err:
                    print(f"{Err}, returning string...")
                    return entry

            elif '$' in entry and 'Last' in entry:
                cleaned_value = entry.replace('Last', '').replace('$', '')
                return float(cleaned_value)
            elif '$' in entry:
                cleaned_value = entry.replace('$', '')
                return float(cleaned_value)
            elif '/' in entry:
                try:
                    datetime_object = dt.strptime(entry, '%m/%d/%Y')
                    return datetime_object.date()
                except ValueError:
                    print('Cannot convert to date, returning original string...')
                    return entry
            elif entry.isdigit():
                return int(entry)
            else:
                return entry

        self.cleaned_data = [ [cast_value(item) for item in sublist] for sublist in data]



    def check_table_attribute(self):
        element = self.session.find_element(By.CSS_SELECTOR,'div.m-table-page-container.n-section-screen_width.t-flex.t-flex-col.t-relative')
        return element.get_attribute('data-data-state')



    def crawl_tables(self,*, num_pages = 1):
        total_clicks = 0
        while True:
            if total_clicks >= num_pages:
                break
            table_available = self.check_table_attribute()
            if table_available == 'None':
                table_available = 'Loading...'
            print(f"Status of loading up the table on web: {table_available}")

            if table_available != 'loading':
                try:
                    element = self.session.find_element(By.XPATH,'/html/body/main/div[1]/div[2]/div[3]/div[18]/div[32]/div/div[3]/button')

                except NoSuchElementException:
                    print('Element not found!')
                else:
                    self.get_data()
                    self.cast_values()
                    element.click()
                    sleep(10)
                    total_clicks+=1


    def end_session(self):

        self.session.quit()


    def prepare_final_data(self):
        '''combine headers with data that went thru cast values method'''

        result = [ (list(zip(self.headers,items))) for items in self.cleaned_data]
        self.ready_data = result
        return result

if __name__ == '__main__':
    scraper = Scraper('https://www.dividend.com/')
    scraper.get_headers()
    scraper.crawl_tables(num_pages=1)
    print(scraper.prepare_final_data())


















