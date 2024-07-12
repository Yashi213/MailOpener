import os
import time

from selenium import webdriver
from twocaptcha import TwoCaptcha
from anticaptchaofficial.hcaptchaproxyless import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

site_url = "https://account.mail.ru/login"
API_KEY = os.getenv('APIKEY_2CAPTCHA', '297c0a0e1d04d927e810ea6887a3d65f')
h_id = "a5f74b19-9e45-40e0-b45d-47ff91b7a6c2"

options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=options)
driver.get(site_url)
driver.switch_to.window(site_url)
driver.switch_to.window(site_url)
