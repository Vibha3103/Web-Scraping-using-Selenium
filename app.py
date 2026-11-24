import pandas as pd
from selenium import webdriver  #allows launching browser
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By  #allows search parameters 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

#1.Configuring chrome options
chrome_options=Options()
chrome_options.add_argument("--incognito")
#we can uncomment the below line when we want it to be executed without opening a visible browser window
#chrome_options.add_argument("--headless=new")

#2.Initializing web driver (Selenium manager handles Chr
# omedriver automatically)
driver = webdriver.Chrome(options=chrome_options)

try:
    #3.Open the target url
    url="https://github.com/collections/machine-learning"
    driver.get(url)
    #implicit_wait gives the dynamic element upto 10 seconds to load
    driver.implicitly_wait(10)

    #4.locate project headings using selenium 
    projects = driver.find_elements(
        By.XPATH, "//h1[@class='h3 lh-condensed']/a"
    )

    #5.Extract project names and URLs
    project_list= []
    for proj in projects:
        project_list.append(
            {"project_name":proj.text,"project_url":proj.get_attribute("href")}
        )

    #6.Convert to Pandas Dataframe and export to csv
    df = pd.DataFrame(project_list)
    df.to_csv("project_list.csv", index=False)
    print(f"Sucess! Saved {len(df)} projects to project_list.csv")

finally:
    driver.quit()

