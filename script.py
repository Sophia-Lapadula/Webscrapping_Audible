#This is the base code for any time we wish to run a bot in selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

#making the but run without Chrome appearing in the screen
options=Options()
options.headless=True
options.add_argument('window-size=1920x1080')
#add the url of the website we wish to srcap
website='https://www.audible.com/adblbestsellers?ref=a_search_t1_navTop_pl0cg1c0r0&pf_rd_p=fe7365e8-61ba-4d50-b524-df73bbd8631f&pf_rd_r=2KPZ8WREYTADZ2HQKYDC'
#Declare the location of your Chrome driver executer
path='/Users/sophi/OneDrive/Documentos/chromedriver.exe'
#Start a drive object by calling the Chrome driver executer
driver=webdriver.Chrome(path,options=options)
#start a session in the website
driver.get(website)
#driver.maximize_window()
#add code here

#dealing with pagination
pagination=driver.find_element_by_xpath('//ul[contains(@class,"pagingElements")]')
pages=pagination.find_elements_by_tag_name('li')
last_page=int(pages[-2].text)
next_page=driver.find_element_by_xpath('//span[contains(@class,"nextButton")]')
next_page.click()

#creating the lists that are going to keep our iteration values
book_title=[]
author=[]
book_lenght=[]

#Creating a while loop to run throught the pages
current_page=1
while current_page<=last_page:
    time.sleep(3)
    #Finding the product list of the current page
    book_list=WebDriverWait(driver,5).until(EC.presence_of_element_located((By.CLASS_NAME,'adbl-impression-container')))
    products=WebDriverWait(book_list,5).until(EC.presence_of_all_elements_located((By.XPATH,'./li')))
    #running throught the pages items
    for product in products:
        book_title.append(product.find_element_by_xpath('.//h3[contains(@class,"bc-heading")]').text)
        book_lenght.append(product.find_element_by_xpath('.//li[contains(@class,"runtimeLabel")]').text)
    #updating current page and clicking in the next one
    current_page+=1
    try:
        next_page=driver.find_element_by_xpath('//span[contains(@class,"nextButton")]')
        next_page.click()
    except:
        pass


driver.quit()

df=pd.DataFrame({'title':book_title,'author':author,'lenght':book_lenght})
df.to_csv('BestSelers.csv',index=False)
