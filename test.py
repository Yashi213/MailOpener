import os
import time
from bs4 import BeautifulSoup
from anticaptchaofficial.recaptchav2proxyless import recaptchaV2Proxyless
from selenium import webdriver
from twocaptcha import TwoCaptcha
from anticaptchaofficial.hcaptchaproxyless import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

site_url = "https://account.mail.ru/login?fail=1&email=sofiya.vereshchagina.91%40mail.ru&page=https%3A%2F%2Fe.mail.ru%2Fmessages%2Finbox%3Fauthid%3Dlyj3dg7a.8sq%26back%3D1%26dwhsplit%3Ds10273.b1ss12743s%26from%3Dlogin%26show_vkc_promo%3D1%26x-login-auth%3D1%26back%3D1&captcha=1&captcha_type=recaptcha&lang=ru_RU&opener=account&twoSteps=1"
API_KEY = '217950d4b04f418855a5aa146d3d4a07'

options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=options)
driver.get(site_url)

driver.implicitly_wait(10)

time.sleep(10)

script_element = driver.find_element(By.ID, 'state')
script_text = script_element.get_attribute('textContent')
data = json.loads(script_text)
site_key = data.get('config', {}).get('recaptchaSitekey', '')
#site_key = "6LfD3PIbAAAAAJs_eEHvoOl75_83eXSqpPSRFJ_u"

print(site_key)
site_url = driver.current_url
solver = recaptchaV2Proxyless()
solver.set_verbose(1)
solver.set_key(API_KEY)
solver.set_website_url(site_url)
solver.set_website_key(site_key)

g_response = solver.solve_and_return_solution()

print(g_response)
driver.execute_script(f'document.getElementById("g-recaptcha-response").innerHTML = "{g_response}";')

symbols = 'QWERTYUIOPASDFGHJKLZXCVBNM'
for symbol in symbols:
    try:
        resp = driver.execute_script(f"return ___grecaptcha_cfg.clients['0']['{symbol}']['{symbol}']")
        print(resp)
        if 'callback' in resp:
            print("ss")
            driver.execute_script(
                f"___grecaptcha_cfg.clients['0']['{symbol}']['{symbol}']['callback']('{g_response}')")
            print("ss")
        break
    except Exception:
        pass

print("делай")
time.sleep(1000)