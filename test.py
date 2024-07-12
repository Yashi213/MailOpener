import os
import time

from selenium import webdriver
from twocaptcha import TwoCaptcha
from anticaptchaofficial.hcaptchaproxyless import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

site_url = "https://2captcha.com/demo/hcaptcha"
API_KEY = os.getenv('APIKEY_2CAPTCHA', '297c0a0e1d04d927e810ea6887a3d65f')
h_id = "a5f74b19-9e45-40e0-b45d-47ff91b7a6c2"

options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=options)
driver.get(site_url)

solver = TwoCaptcha(API_KEY)
result = solver.hcaptcha(
            sitekey='3ceb8624-1970-4e6b-91d5-70317b70b651',
            url=site_url,
        )
code = result['code']


iframe = WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.CSS_SELECTOR,
                                                                        "#root > div._layout_biy5f_1._basicLayout_18ddp_2 > main > div > div > div._content_18ddp_17 > section > div > form > div._captchaWidgetContainer_1f3oo_22 > div > div > iframe")))

driver.execute_script(
        "document.querySelector(" + "'" + '[name="h-captcha-response"]' + "'" + ").innerHTML = " + "'" + code + "'")
driver.execute_script(f'document.querySelector("[data-hcaptcha-response]").setAttribute("data-hcaptcha-response", "{code}");')

driver.find_element(By.CSS_SELECTOR,
                    "#root > div._layout_biy5f_1._basicLayout_18ddp_2 > main > div > div > div._content_18ddp_17 > section > div > form > div._actions_1f3oo_36 > button._actionsItem_1f3oo_41._buttonPrimary_d46vc_44._button_d46vc_1._buttonMd_d46vc_34").click()
time.sleep(10000)