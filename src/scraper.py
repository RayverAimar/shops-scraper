from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
from config import *
import requests

class GenericScraper(object):
    def __init__(self, product_name, homepage_url) -> None:
        self._product_name = product_name
        self._homepage_url = homepage_url
        self.products = []
    
    def _get_query_url(self, driver : webdriver.Chrome, xpath): 
        driver.get(self._homepage_url)
        WebDriverWait(driver, timeout=TIMEOUT_PER_PAGE).until(EC.presence_of_all_elements_located((By.XPATH, xpath)))
        search_box = driver.find_element(By.XPATH, xpath)
        search_box.send_keys(self._product_name)
        search_box.send_keys(Keys.ENTER)

    def _get_soup(self, xpath):
        options = webdriver.ChromeOptions()
        options.add_argument('--incognito')
        options.add_argument('--start-maximized')
        driver = webdriver.Chrome(options=options)
        self._get_query_url(driver, xpath)
        html = driver.page_source
        driver.quit()
        return BeautifulSoup(html, 'lxml')
    
    def choose_product(self):
        if not self.products:
            print('Please scrape before choose a product.')
            return None
        print(f'Displaying {len(self.products)} products from {self._homepage_url}:')
        for index, product in enumerate(self.products):
            print(f'Product N° {index + 1}:')
            print('\tName:', product.name)
            print('\tPrice:', product.price)
            print('\tUrl:', product.url)
            print()
        index = int(input('Enter the index of one of the products displayed above: ')) - 1
        return self.products[index]

class GenericProduct:
    def __init__(self, name, price, url):
        self.name = name
        self.price = price
        self.url = url

class AmazonScraper(GenericScraper):
    def __init__(self, product_name : str):
        super().__init__(
            product_name=product_name,
            homepage_url='https://www.amazon.com/',
        )

    def scrape(self):
        try:
            soup = self._get_soup('//input[contains(@class, "nav-input nav-progressive-attribute")]')
        except TimeoutException:
            print('Tag wasn\'t found. ERR_CONNECTION_TIMED_OUT.')
            return ERROR
        products = soup.find_all('div', attrs={'class':'sg-col-20-of-24 s-result-item s-asin sg-col-0-of-12 sg-col-16-of-20 sg-col s-widget-spacing-small sg-col-12-of-16'})
        for index, product in enumerate(products):
            try:
                print(f'Scraping product ({index+1}/{len(products)})')
                price = product.find('span', attrs={'class':'a-price'})
                if not price:
                    print('Price not found in current product. Skipping...')
                    continue
                price = price.find('span', attrs={'class':'a-offscreen'}).get_text()
                price = float(price.split('$').pop())
                url = product.find('a', attrs={'class':'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'})
                url = self._homepage_url + url.get('href')
                name = product.find('span', attrs={'class':'a-size-medium a-color-base a-text-normal'}).get_text()
                self.products.append(
                    GenericProduct(name=name,
                            price=price,
                            url=url,
                        )
                )
            except:
                print('Error while parsing product. Skipping...')
                continue
        return SUCCESS
    
    @staticmethod
    def get_price_of_product(url):
        options = webdriver.ChromeOptions()
        options.add_argument('--incognito')
        options.add_argument('--start-maximized')
        driver = webdriver.Chrome(options=options)
        driver.get(url)
        WebDriverWait(driver, timeout=10).until(EC.presence_of_all_elements_located((By.XPATH, "//span[contains(@class, 'a-price a-text-price a-size-medium apexPriceToPay')]")))
        price = driver.find_element(By.XPATH, "//span[contains(@class, 'a-price a-text-price a-size-medium apexPriceToPay')]/span[1]").get_attribute('textContent')
        driver.quit()
        price = price[3:]
        return float(price)

class EbayScraper(GenericScraper):
    def __init__(self, product_name : str):
        super().__init__(
            product_name=product_name,
            homepage_url='https://www.ebay.com',
        )

    def scrape(self):
        try:
            soup = self._get_soup('//input[contains(@class, "gh-tb ui-autocomplete-input")]')
        except TimeoutException:
            print('Tag wasn\'t found. ERR_CONNECTION_TIMED_OUT.')
            return ERROR
        
        products = soup.find_all('li', attrs={'class':'s-item s-item__pl-on-bottom'})
        for index, product in enumerate(products):
            try:
                print(f'Scraping product ({index+1}/{len(products)})')
                name = product.find('div', attrs={'class':'s-item__title'}).get_text()
                url = product.find('a', attrs={'class':'s-item__link'}).get('href')
                price = EbayScraper.get_price_of_product(url)
                self.products.append(
                    GenericProduct(name=name,
                            price=price,
                            url=url,
                    )
                )
            except Exception as e:
                print('Error while parsing product. Skipping...')
                print(e)
                continue
        return SUCCESS
    
    @staticmethod
    def get_price_of_product(url):
        response = requests.get(url)
        if response.status_code != 200:
            return None
        soup = BeautifulSoup(response.text, 'lxml')
        price = soup.find('div', attrs={'class':'x-bin-price__content'}).find('span', attrs={'class':'ux-textspans'})
        if not price:
            return None
        if price.get_text()[:2] != 'US':
            raise TypeError('Error in the currency of the price')
        price = price.get_text()[1:]
        return float(price.split(' ')[1][1:])