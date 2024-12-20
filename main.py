from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd

# Initialize WebDriver
driver = webdriver.Chrome()

# Open the target website
driver.get("https://www.noon.com/uae-en/sports-and-outdoors/exercise-and-fitness/yoga-16328/")
time.sleep(5)  # Allow page to load

# Scroll and load more products
data = []
prev_count = 0

while len(data) < 200:  # Ensure at least 200 products are collected
    # Scroll to the bottom of the page
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)  # Wait for new items to load
    
    # Fetch product elements
    products = driver.find_elements(By.CLASS_NAME, 'sc-57fe1f38-0')
    print(f"Loaded {len(products)} products...")  # Debugging output
    
    # Extract details from new products only
    for product in products[prev_count:]:
        try:
            name = product.find_element(By.CSS_SELECTOR, '[data-qa="product-name"]').get_attribute('title')
        except:
            name = "N/A"
        try:
            sponsored = "yes" if product.find_element(By.CLASS_NAME, 'sc-95ea18ef-24') else "no"
        except:
            sponsored = "no"
        try:
            price = product.find_element(By.CLASS_NAME, 'amount').text
        except:
            price = "N/A"
        try:
            link = product.find_element(By.TAG_NAME, 'a').get_attribute('href')
        except:
            link = "N/A"
        try:
            express = "Yes" if product.find_elements(By.CLASS_NAME, 'sc-d13a0e88-1') else "No"
        except:
            express = "No"
        try:
            delivery = product.find_element(By.CLASS_NAME, 'sc-4d61bf64-5').text
        except:
            delivery = "N/A"

        data.append({
            "Name": name,
            "Price": price,
            "Link": link,
            "Express": express,
            "Delivery_or_rank": delivery,
            "Sponsored": sponsored
        })

    prev_count = len(products)  # Update the count of already processed products

    # Break if no new products are loaded
    if prev_count >= 200:
        break

# Save the data to a CSV file
df = pd.DataFrame(data[:200])  # Limit to the first 200 products
df.to_csv('noon_yoga_products.csv', index=False)
print("Data saved to 'noon_yoga_products.csv'")

# Close the browser
driver.quit()
