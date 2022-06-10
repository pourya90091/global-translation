from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from json import dump
import time


original_language = input("select a language: ")
original_text = input("type a text: ")
location = input("set location for json file: ")
time_out = input("set time out (0.5 is recommended): ")

start = time.perf_counter()

if not original_language:
    original_language = "English"
if not original_text:
    original_text = "Hello"
if not location:
    location = "./global_translation.json"
if not time_out:
    time_out = 0.5
else:
    time_out = float(time_out)

global_translation = {}
base_url = "https://translate.google.com"

service = Service(executable_path=ChromeDriverManager().install())

options = Options()
options.add_argument("--headless")

driver = webdriver.Chrome(service=service, options=options)
driver.get(base_url)

Lbtn = driver.find_element("xpath", "//*[@id='yDmH0d']/c-wiz/div/div[2]/c-wiz/div[2]/c-wiz/div[1]/div[1]/c-wiz/div[1]/c-wiz/div[2]/button")
Lbtn.click()
del Lbtn

time.sleep(time_out)

search_original_language = driver.find_element("xpath", "//*[@id='yDmH0d']/c-wiz/div/div[2]/c-wiz/div[2]/c-wiz/div[1]/div[1]/c-wiz/div[2]/c-wiz/div[1]/div/div[2]/input")
search_original_language.send_keys(original_language)
search_original_language.send_keys(Keys.ENTER)
del search_original_language

time.sleep(time_out)

search_original_text = driver.find_element("xpath", "//*[@id='yDmH0d']/c-wiz/div/div[2]/c-wiz/div[2]/c-wiz/div[1]/div[2]/div[3]/c-wiz[1]/span/span/div/textarea")
search_original_text.send_keys(original_text)
del search_original_text

time.sleep(time_out)

Rbtn = driver.find_element("xpath", "//*[@id='yDmH0d']/c-wiz/div/div[2]/c-wiz/div[2]/c-wiz/div[1]/div[1]/c-wiz/div[1]/c-wiz/div[5]/button")
langs = driver.find_elements("xpath", "//*[@id='yDmH0d']/c-wiz/div/div[2]/c-wiz/div[2]/c-wiz/div[1]/div[1]/c-wiz/div[2]/c-wiz/div[2]/div/div[3]/div/div[2]//div[(@class='qSb8Pe' or @class='qSb8Pe RCaXn' or @class='qSb8Pe RCaXn KKjvXb') and @jsname='sgblj' and @tabindex='0']")

n = len(langs)
i = 0
while i < n:
    Rbtn.click()
    time.sleep(time_out)
    langs[i].click()
    time.sleep(time_out)

    lang_code = langs[i].get_attribute("data-language-code")

    try:
        current_translate = driver.find_element("xpath", "//*[@id='yDmH0d']/c-wiz/div/div[2]/c-wiz/div[2]/c-wiz/div[1]/div[2]/div[3]/c-wiz[2]/div[8]/div")
        if current_translate.get_attribute("data-language") == lang_code:
            translated_text = current_translate.find_element("xpath", ".//div[1]/span[1]/span/span").text
        else:
            raise Exception
        global_translation[lang_code] = translated_text
    except:
        time.sleep(time_out)
        continue

    p = ((i + 1) * 100) / n
    progress = f"{str(int(p)).zfill(2)}.{str(round(int((p - int(p)) * 10), 2)).zfill(2)}%"
    print(progress, "translated into", lang_code)
    i += 1

with open(location, "w") as file:
    dump(global_translation, file, indent=4)

end = time.perf_counter()
print(f"\nend in {round(end - start, 2)}s")
