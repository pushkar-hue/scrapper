from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv

browser = webdriver.Firefox()
browser.get('https://search.earth911.com/?what=Electronics&where=10001&list_filter=all&max_distance=25&family_id=&latitude=&longitude=&country=&province=&city=&sponsor=')

def clean_data(text):
    """Removes non-ASCII characters from a string."""
    return text.encode('ascii', 'ignore').decode('ascii').strip()

try:
    # Wait for the result items to be present on the page
    
    wait = WebDriverWait(browser, 10)
    elements = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'li.result-item')))

    link_elements = browser.find_elements(By.CSS_SELECTOR, 'li.result-item h2 a')

    url_to_visit = [link.get_attribute('href') for link in link_elements]
    print("URLs to visit:", len(url_to_visit))
    # Visit each URL and extract the required information
    extracted_data = []
    for url in url_to_visit:
        print("Visiting URL:", url)
        browser.get(url)
        data = {}

        full_header = browser.find_element(By.CSS_SELECTOR, '.back-to').text
        cleaned_header = full_header.replace("Back", "").strip()
        buisness_name = cleaned_header.split(' - ')[0].strip()

        last_updated = browser.find_element(By.CSS_SELECTOR, 'span.last-verified').text

        first_line_address = browser.find_element(By.CSS_SELECTOR, 'p.addr:nth-child(2)').text
        second_line_address = browser.find_element(By.CSS_SELECTOR, 'p.addr:nth-child(3)').text
        address = f"{first_line_address}, {second_line_address}"

        material_elements = browser.find_elements(By.CSS_SELECTOR, 'span.material.no-link')

        if not first_line_address:
            address = second_line_address  # Fallback if first line is empty

        data['buisness_name'] = clean_data(buisness_name)
        data['last_updated'] = clean_data(last_updated.replace("Back", "").strip())
        data['address'] = clean_data(address)
        data['materials_accepted'] = [clean_data(material.text) for material in material_elements]

        print("Page title:", browser.title)
        extracted_data.append(data)
        time.sleep(2)
    
    if extracted_data:
        with open('extracted_data.csv', 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['buisness_name', 'last_updated', 'address', 'materials_accepted'])
            writer.writeheader()
            writer.writerows(extracted_data)
        print("Data saved successfully to extracted_data.csv")

        for data in extracted_data:
            print("Business Name:", data['buisness_name'])
            print("Last Updated:", data['last_updated'])
            print("Address:", data['address'])
            print("Materials Accepted:", ", ".join(data['materials_accepted']))
            print("-" * 40)

finally:
    # Ensure the browser closes even if an error occurs
    browser.quit()