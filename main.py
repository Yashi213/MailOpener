import time
import re

from anticaptchaofficial.imagecaptcha import imagecaptcha
from anticaptchaofficial.recaptchav2proxyless import recaptchaV2Proxyless
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains

from anticaptchaofficial.hcaptchaproxyless import *
from twocaptcha import TwoCaptcha
import pandas as pd
import numpy as np
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

API_KEY = '217950d4b04f418855a5aa146d3d4a07'
CSS_SELECTOR_BUTTON = "#mailbox > div.logged-out-one-click.gak__hegm-gzmdja.logged-out-one-click_crossnav > button"
CSS_SELECTOR_TEXT_CAPTCHA = "#app > div > div > form > div.b-panel__content > div > img"
CSS_SELECTOR_TEXT_CAPTCHA_INPUT = "#app > div > div > form > div.b-panel__content > div > div > input"
CSS_SELECTOR_CONFIRM_PASSWORD = "#root > div:nth-child(2) > div > div > div > div > form > div:nth-child(2) > div > div:nth-child(3) > div > div > div.submit-button-wrap > div > button"
site_url = "https://account.mail.ru/login"


def ExcelWriter(ar):
    df = pd.DataFrame(ar)
    df.to_excel('result.xlsx')


def FillArray():
    mails = open("mail.txt")
    phones = open("phones.txt")
    mail_phone = []
    for i in mails:
        mail_phone.append([i.strip().split(":")[0], phones.readline().strip()])
    return mail_phone


def SolveTextCaptcha(driver):
    solver = imagecaptcha()
    solver.set_verbose(1)
    solver.set_key(API_KEY)
    solver.set_soft_id(0)

    captcha_text = solver.solve_and_return_solution("images/captcha.jpeg")
    driver.find_element(By.CSS_SELECTOR, CSS_SELECTOR_TEXT_CAPTCHA_INPUT).send_keys(captcha_text)
    driver.find_element(By.XPATH, "//button[span='Продолжить']").click()


def SolveReCaptcha(driver):
    script_element = driver.find_element(By.ID, 'state')
    script_text = script_element.get_attribute('textContent')
    data = json.loads(script_text)
    site_key = data.get('config', {}).get('recaptchaSitekey', '')

    solver = recaptchaV2Proxyless()
    solver.set_verbose(1)
    solver.set_key(API_KEY)
    solver.set_website_url(site_url)
    solver.set_website_key(site_key)

    g_response = solver.solve_and_return_solution()

    driver.execute_script(f'document.getElementById("g-recaptcha-response").innerHTML = "{g_response}";')

    symbols = 'QWERTYUIOPASDFGHJKLZXCVBNM'
    for symbol in symbols:
        try:
            resp = driver.execute_script(f"return ___grecaptcha_cfg.clients['0']['{symbol}']['{symbol}']")
            if 'callback' in resp:
                driver.execute_script(
                    f"___grecaptcha_cfg.clients['0']['{symbol}']['{symbol}']['callback']('{g_response}')")
            break
        except Exception:
            pass


def CheckSolution(driver):
    try:
        error_element = driver.find_element(By.XPATH, "//*[contains(text(), 'Вы указали неправильный код с картинки')]")
        return False
    except:
        return True


def logIn(driver, mail, password, window):
    try:
        input_mail = driver.find_element(By.XPATH, "//input[@name='username']")
        input_mail.click()
        input_mail.send_keys(mail)
        input_mail.send_keys(Keys.ENTER)

        driver.implicitly_wait(10)
        driver.find_element(By.XPATH, "//input[@name='password']").send_keys(password)
        driver.find_element(By.CSS_SELECTOR, CSS_SELECTOR_CONFIRM_PASSWORD).click()
        print(1)
        return True
    except:
        print(2)
        return False


def LogInMail(driver):
    mails = open("mail.txt").readlines()
    mails_count = len(mails) - 1
    for i in range(mails_count):
        driver.execute_script("window.open('');")
    windows = driver.window_handles
    for i, window in zip(mails, windows):
        mail = i.split(":")[0]
        print(mail)
        password = i.split(":")[1]
        driver.switch_to.window(window)
        driver.get(site_url)
        driver.implicitly_wait(10)
        while logIn(driver, mail, password, window):
            driver.implicitly_wait(10)

        try:
            driver.implicitly_wait(10)
            driver.find_element(By.XPATH, "//button[span='Это я']").click()

            SolveReCaptcha(driver)
            driver.find_element(By.XPATH, "//input[@name='password']").send_keys(password)
        except:
            try:
                text_captcha = driver.find_element(By.CSS_SELECTOR, CSS_SELECTOR_TEXT_CAPTCHA)
                captcha_url = text_captcha.get_attribute("src")
                driver.implicitly_wait(10)
                driver.get(captcha_url)
                with open("images/captcha.jpeg", 'wb') as file:
                    file.write(driver.find_element(By.TAG_NAME, "img").screenshot_as_png)
                driver.back()

                while not CheckSolution(driver):
                    SolveTextCaptcha(driver)
                    time.sleep(2)
            except:
                print("капчу не попросили")


options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=options)
mail_phone = FillArray()
ExcelWriter(mail_phone)
LogInMail(driver)
input("Нажмите Enter, чтобы закрыть браузер и завершить работу...")
driver.quit()

