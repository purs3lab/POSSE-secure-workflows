import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

# Load the Excel file into a pandas DataFrame
df = pd.read_excel('top_750_starred_repos.xlsx')

# Initialize Chrome options for WebDriver
options = Options()
options.add_argument("--headless")  # Uncomment if you want the browser to open visibly

# Initialize the Chrome driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Authenticate once
driver.get("https://github.com/login")
time.sleep(2)  # Wait for the login page to load

# Input GitHub username and password
driver.find_element(By.ID, "login_field").send_keys("user_name")
driver.find_element(By.ID, "password").send_keys("password")
driver.find_element(By.ID, "password").send_keys(Keys.RETURN)

# Pause here for manual 2FA
# input("Complete the 2FA/device verification in the browser, then press Enter here to continue...")

# Function to check for the "Report a vulnerability" feature
def check_vulnerability_feature(repository_url):
    driver.get(repository_url)
    time.sleep(2)  # Wait for the page to load
    elements = driver.find_elements(By.CSS_SELECTOR, 'h1[data-view-component="true"].Subhead-heading.Subhead-heading--large')
    return any("Report a vulnerability" in element.text for element in elements)

# List to store the results
vulnerability_feature_enabled = []

# Loop through the DataFrame and check each URL
for index, row in df.iterrows():
    repository_url = row['URL'] + "/security/advisories/new"
    feature_exists = check_vulnerability_feature(repository_url)
    print(f"Feature exists for {repository_url}: {feature_exists}")
    vulnerability_feature_enabled.append(feature_exists)

# Add the results to the DataFrame
df['Vulnerability Feature Enabled'] = vulnerability_feature_enabled

# Write the updated DataFrame to a new Excel file
df.to_excel('chrome_checked.xlsx', index=False)

# Close the WebDriver
driver.quit()

