import re
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

chrome_options = Options()
# Helps prevent commercial retail sites from blocking automated browsers
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option("useAutomationExtension", False)

driver = webdriver.Chrome(options=chrome_options)

try:
    url = "https://www.1800flowers.com/articles/flower-facts/flower-types"
    driver.get(url)

    # Wait up to 15 seconds until the article headings load
    driver.implicitly_wait(15)

    # Grab all <h2> headings on the page
    headings = driver.find_elements(By.TAG_NAME, "h2")

    flower_list = []
    for heading in headings:
        title_text = heading.text.strip()

        # Match only the numbered flower headings like "1. Rose", "2. Sunflower"
        if re.match(r"^\d+\.\s+", title_text):
            # Grab the first descriptive paragraph following this heading
            try:
                desc_elem = heading.find_element(
                    By.XPATH, "following-sibling::p[1]"
                )
                description = desc_elem.text.strip()
            except Exception:
                description = ""

            flower_list.append(
                {"flower_name": title_text, "description": description}
            )

    df = pd.DataFrame(flower_list)
    df.to_csv("flower_types.csv", index=False, encoding="utf-8-sig")
    print(f"Success! Saved {len(df)} flowers to flower_types.csv")

finally:
    driver.quit()
