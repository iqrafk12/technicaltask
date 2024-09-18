from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys  # To use the Page Down key
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import requests
import pandas as pd

# Set up the Chrome driver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# Navigate to the page
url = 'https://www.fxhash.xyz/explore'
driver.get(url)

# Wait for the initial elements to load
wait = WebDriverWait(driver, 60)
wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'GenerativeTokenCard_anchor__DbGXY')))

# Perform a series of "Page Down" actions with pauses in between to load all items
def page_down_scroll(driver, scroll_pause_time, page_down_attempts=20):
    for attempt in range(page_down_attempts):
        # Simulate pressing the "Page Down" key
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)
        
        # Wait for the new content to load
        time.sleep(scroll_pause_time)
        print(f"Page down {attempt + 1}/{page_down_attempts} complete")

# Scroll down with Page Down key and time.sleep between each scroll
scroll_pause_time = 3 
page_down_scroll(driver, scroll_pause_time, page_down_attempts=500) 

page_source = driver.page_source

soup = BeautifulSoup(page_source, 'html.parser')

generative_art_names = [sketch.get_text() for sketch in soup.find_all('h5', class_="GenerativeTokenCard_title__y4k6B")]
generative_art_links = ['https://www.fxhash.xyz' + link.get('href') for link in soup.find_all('a', class_="GenerativeTokenCard_anchor__DbGXY")]

# Close the driver
driver.quit()
print(f"Generative Arts Names Count: {len(generative_art_names)} & Generaitve Ars Links: {len(generative_art_links)}")
print(f"There are {len(generative_art_names)} links. Checking each link, It will take some time....")

link_status = []
creative_coding_libraries = []
for url in generative_art_links:
  try:
      response = requests.get(url, timeout=5)
      if response.status_code == 200:
          link_status.append(("working"))
          soup = BeautifulSoup(response.content, 'html.parser')
          library = soup.find('div', class_="Clamp_container__xOFme GenerativeDisplay_description__NweHb")
          if library !=None:
            first_part = library.text.split('<br/>')[0].strip()
            # first_part = library.split(',')
            creative_coding_libraries.append(first_part)
          else:
            creative_coding_libraries.append("-")
      else:
          link_status.append("not working")
          creative_coding_libraries.append("-")
  except requests.exceptions.RequestException:
        link_status.append("not working")
        creative_coding_libraries.append("-")


df = pd.DataFrame({
    'Generative Art Name': generative_art_names,
    'Generative Art Link': generative_art_links,
    'Link Status': link_status,
    'Generative Library': creative_coding_libraries
})

# Define the CSV file path
csv_file_path = 'fxhash_data.csv'

# Convert DataFrame to CSV
df.to_csv(csv_file_path, index=False)

print(f"DataFrame has been successfully saved to {csv_file_path}")