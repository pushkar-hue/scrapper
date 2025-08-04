from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

browser = webdriver.Firefox()
browser.get('https://search.earth911.com/?what=Electronics&where=10001&list_filter=all&max_distance=25&family_id=&latitude=&longitude=&country=&province=&city=&sponsor=')

try:
    # Wait for the result items to be present on the page
    
    wait = WebDriverWait(browser, 10)
    elements = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'li.result-item')))

    link_elements = browser.find_elements(By.CSS_SELECTOR, 'li.result-item h2 a')

    url_to_visit = [link.get_attribute('href') for link in link_elements]
    print("URLs to visit:", len(url_to_visit))
    # Visit each URL and extract the required information
    for url in url_to_visit:
        print("Visiting URL:", url)
        browser.get(url)
        print("Page title:", browser.title)
        
        time.sleep(2)
    
    # Loop through each result item found
    #for element in elements:
        # title = element.find_element(By.TAG_NAME, 'h2').text
        
        # address1 = element.find_element(By.CSS_SELECTOR, 'p.address1').text
        # address3 = element.find_element(By.CSS_SELECTOR, 'p.address3').text

        # address = f"{address1}, {address3}"
        # if not address1:
        #     address = address3  # If address1 is empty, use address3 only
        
        # print("Title:", title)
        # print("Address:", address)
        # print("-" * 40)

finally:
    # Ensure the browser closes even if an error occurs
    browser.quit()