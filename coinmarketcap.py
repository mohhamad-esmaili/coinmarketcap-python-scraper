from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

DRIVER_PATH = 'chromedriver.exe'
driver = webdriver.Chrome(executable_path=DRIVER_PATH)
driver.get(
    'https://coinmarketcap.com/currencies/radio-caca/'
)

# coin_name = driver.find_elements(By.TAG_NAME, 'h2')[0].text
# coin_name = coin_name.split("\n")
# symbol = coin_name[1]
# coin_name = coin_name[0]
# print(f'coin name: {coin_name} and symbol: {symbol}')
# ------------------------------------------------------------------
# containers = driver.find_elements(
#     By.CLASS_NAME, 'bILTHz')[0].text
# containers = containers.split("\n")
# rank = containers[0]
# isToken = containers[1]
# onwatch = containers[2]
# print(f'{rank} - {isToken} - {onwatch}')
# -------------------------------------------------------------------------
# elems = driver.find_elements_by_xpath("//ul[@class='content']//li//a[@href]")
# for elem in elems:
#     print(elem.get_attribute("href"))
# -------------------------------------------------------------------------


a = ActionChains(driver)

link = driver.find_element_by_xpath(
    "//ul[@class='content']//li//button[@class='link-button']")
link1 = driver.find_element_by_xpath(
    "//ul[@class='content']//li//button[@class='link-button']")

a.move_to_element(link).perform()


try:
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, "//ul[@class='content']//li")))
    my_list = []
    for i in element:
        my_list.append(i.find_element_by_tag_name('a').get_attribute('href'))
        print(my_list)
    # print(element[4].find_element_by_tag_name('a').get_attribute('href'))
except:
    driver.quit()
