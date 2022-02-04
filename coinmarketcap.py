from textwrap import indent
from requests import get
from bs4 import BeautifulSoup
from lib2to3.pgen2 import driver
import re
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
# ------------------------------------------------------------------
telegram_regex = '(https:\/\/(t|tlgrm|telegram)\.me\/)'
twitter_regex = '(https:\/\/twitter.com\/(?![a-zA-Z0-9_]+\/)([a-zA-Z0-9_]+))'
discord_regex = '(https?:\/\/)?(www\.)?(discord\.(gg|io|me|li)|discordapp\.com\/invite)\/.+[a-z]'
reddit_regex = '^http(?:s)?://(?:www\.)?(?:[\w-]+?\.)?reddit.com(/r/|/user/)?(?(1)([\w:]{2,21}))(/comments/)?(?(3)(\w{5,6})(?:/[\w%\\\\-]+)?)?(?(4)/(\w{7}))?/?(\?)?(?(6)(\S+))?(\#)?(?(8)(\S+))?$'
facebook_regex = '(?:(?:http|https):\/\/)?(?:www.)?facebook.com\/(?:(?:\w)*)'
insta_regex = '(?:(?:http|https):\/\/)?(?:www.)?(?:instagram.com|instagr.am|instagr.com)\/(\w+)'
regex_coin = r'/currencies\/*\/[a-z-]*\/$'

list_of_urls = []
list_of_all = []
page = 1

while True:
    try:
        current_page_url = f"https://coinmarketcap.com/coins/?page={page}"
        get_current_page = get(current_page_url)
        soup = BeautifulSoup(get_current_page.content, "html.parser")
        all_coins = soup.find_all("a", class_="cmc-link")

        for link in all_coins:
            if "/currencies/" in link["href"]:
                if re.match(regex_coin, str(link["href"])):
                    fixed_link = "https://coinmarketcap.com" + link["href"]
                    list_of_urls.append(fixed_link)
            if len(list_of_urls) >= 100:
                break
        break
        page = page + 1
    except:
        break


index = 1
DRIVER_PATH = 'chromedriver.exe'
option = webdriver.ChromeOptions()
option.add_argument('headless')
driver = webdriver.Chrome(executable_path=DRIVER_PATH, options=option)
for url in list_of_urls:
    driver.get(
        url
    )
    print(f"-----------------------------{index}/{len(list_of_urls)}")
    # print(f'got in url:::::::::::::::::::{url}')
    get_coin_link = get(url)
    coin_soup = BeautifulSoup(get_coin_link.content, "html.parser")
    coin_name = coin_soup.find("h2", class_="sc-1q9q90x-0 jCInrl h1").contents[0]
    symbol = coin_soup.find("h2", class_="sc-1q9q90x-0 jCInrl h1").contents[1].text

    links = []

    link = driver.find_elements(By.XPATH,
                                "//ul[@class='content']//li//button[@class='link-button']")
    a = ActionChains(driver)
    for i in link:
        a.move_to_element(i).perform()
        try:
            element = WebDriverWait(driver, 3).until(
                EC.presence_of_all_elements_located((By.XPATH, "//ul[@class='content']//li//a")))
            for x in element:
                links.append(x.get_attribute('href'))
            # time.sleep(1)

        except:
            pass

    Coin_Telegram = 'empty'
    insta_regex = 'empty'
    Coin_Twitter = 'empty'
    Coin_Discord = 'empty'
    Coin_Reddit = 'empty'
    Coin_Facebook = 'empty'
    Coin_Instagram = 'empty'
    for item in links:
        if re.match(telegram_regex, item):
            Coin_Telegram = item
            print('telegram found!')
        elif re.match(twitter_regex, item):
            Coin_Twitter = item
            print('twitter found!')
        elif re.match(reddit_regex, item):
            Coin_Reddit = item
            print('Reddit found!')
        elif re.match(discord_regex, item):
            Coin_Discord = item
            print('discord found!')
        elif re.match(facebook_regex, item):
            Coin_Facebook = item
            print('Facebook found!')

        elif re.match(insta_regex, item):
            Coin_Instagram = item
    index = index + 1
    # {coin_link.strip()}
    try:
        csv_string = f"{coin_name.strip()}({symbol}),{url.strip()},{links[0]},{Coin_Telegram.strip()},{Coin_Twitter.strip()},{Coin_Discord.strip()},{Coin_Reddit.strip()},{Coin_Facebook.strip()},{Coin_Instagram.strip()}"
    except:
        csv_string = f"{coin_name.strip()}({symbol}),{url.strip()},empty,{Coin_Telegram.strip()},{Coin_Twitter.strip()},{Coin_Discord.strip()},{Coin_Reddit.strip()},{Coin_Facebook.strip()},{Coin_Instagram.strip()}"

    list_of_all.append(csv_string)


with open("coinmarketcap.csv", "w") as f:
    # This is Information That we want || Headers of CSV File
    f.write(
        "Name,URL,Website,Telegram,Twitter,Discord,Reddit,Facebook,Instagram")
    f.write("\n")
    for item in list_of_all:
        f.write(item)
        f.write("\n")
