import time
import re

from anticaptchaofficial.imagecaptcha import imagecaptcha
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


def SolveCaptcha(driver):
    solver = imagecaptcha()
    solver.set_verbose(1)
    solver.set_key(API_KEY)
    solver.set_soft_id(0)

    captcha_text = solver.solve_and_return_solution("images/captcha.jpeg")
    driver.find_element(By.CSS_SELECTOR, CSS_SELECTOR_TEXT_CAPTCHA_INPUT).send_keys(captcha_text)
    driver.find_element(By.XPATH, "//button[span='Продолжить']").click()


def CheckSolution(driver):
    try:
        error_element = driver.find_element(By.XPATH, "//*[contains(text(), 'Вы указали неправильный код с картинки')]")
        return False
    except:
        return True


def LogInMail(mails_count, driver):
    mails = open("mail.txt")
    for i in range(mails_count):
        driver.execute_script("window.open('');")
    windows = driver.window_handles
    for i, window in zip(mails, windows):
        site_url = "https://account.mail.ru/login"
        mail = i.split(":")[0]
        print(mail)
        password = i.split(":")[1]
        driver.switch_to.window(window)
        driver.get(site_url)
        #WebDriverWait(driver, 90).until((ec.element_to_be_clickable((By.CSS_SELECTOR, CSS_SELECTOR_BUTTON)))).click()
        driver.implicitly_wait(10)
        input_mail = driver.find_element(By.XPATH, "//input[@name='username']")
        input_mail.click()
        input_mail.send_keys(mail)
        input_mail.send_keys(Keys.ENTER)
        driver.implicitly_wait(10)
        time.sleep(2)
        driver.find_element(By.XPATH, "//input[@name='password']").send_keys(password)
        driver.find_element(By.CSS_SELECTOR, CSS_SELECTOR_CONFIRM_PASSWORD).click()
        driver.implicitly_wait(10)
        text_captcha = driver.find_element(By.CSS_SELECTOR, CSS_SELECTOR_TEXT_CAPTCHA)
        captcha_url = text_captcha.get_attribute("src")
        driver.implicitly_wait(10)
        driver.get(captcha_url)
        with open("images/captcha.jpeg", 'wb') as file:
            file.write(driver.find_element(By.TAG_NAME, "img").screenshot_as_png)
        driver.back()

        while not CheckSolution(driver):
            SolveCaptcha(driver)
            time.sleep(2)


options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=options)
mail_phone = FillArray()
LogInMail(1, driver)
