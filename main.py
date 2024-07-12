import time
import re
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
PATH_MAIL = "/html/body/div[1]/div[2]/div/div/div/div[2]/div/form/div[2]/div[2]/div[1]/div/div/div/div/div/div[1]/div/input"
CSS_SELECTOR_PASSWORD = ("#root > div > div > div > div.wrapper-0-2-5 > div > form > div:nth-child(2) > div > "
                         "div.login-row.password.fill-icon > div > div > div > div > div > input")


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


def SolveCaptcha(h_id):
    solver = hCaptchaProxyless()
    solver.set_verbose(1)
    solver.set_key(API_KEY)
    solver.set_website_url(
        "https://id.rambler.ru/login-20/login?rname=head&session=false&back=https%3A%2F%2Fwww.rambler.ru%2F&param=popup&iframeOrigin=https%3A%2F%2Fwww.rambler.ru#startTime=1720530029957")
    solver.set_website_key(h_id)
    solver.set_soft_id(0)

    g_response = solver.solve_and_return_solution()
    return g_response


def LogInMail():
    mails = open("mail.txt")
    for i in mails:
        site_url = "https://account.mail.ru/login"
        mail = i.split(":")[0]
        print(mail)
        password = i.split(":")[1]
        options = webdriver.ChromeOptions()
        driver = webdriver.Chrome(options=options)
        driver.get(site_url)
        #WebDriverWait(driver, 90).until((ec.element_to_be_clickable((By.CSS_SELECTOR, CSS_SELECTOR_BUTTON)))).click()
        driver.implicitly_wait(10)
        input_mail = driver.find_element(By.XPATH, "//input[@name='username']")
        input_mail.click()
        input_mail.send_keys(mail)
        input_mail.send_keys(Keys.ENTER)
        driver.implicitly_wait(10)
        driver.find_element(By.XPATH, "//input[@name='password']").send_keys(password)
        driver.find_element(By.XPATH, "//input[@name='password']").send_keys(Keys.ENTER)
        time.sleep(100)
        try:
            capt = driver.find_element(By.XPATH,
                                       "/html/body/div[1]/div/div/div/div/div/div/div[1]/form/section[3]/div/div/div[1]/div/div/iframe")
            h_id = capt.get_attribute("src")
            print(h_id)
            h_id = re.search(r"sitekey\s*=\s*([^\s]*)", h_id).group(1).split("&")[0]

            print(h_id)
            result = SolveCaptcha(h_id)
        except:
            print("Капчу не попросили")

        driver.execute_script(
            f'document.querySelector("[data-hcaptcha-response]").setAttribute("data-hcaptcha-response", "{result}");')
        salt = driver.execute_script(
            "return document.querySelector('[data-hcaptcha-response]').getAttribute('data-hcaptcha-widget-id')")
        driver.execute_script(
            "document.querySelector(" + "'" + '[name="h-captcha-response"]' + "'" + ").innerHTML = " + "'" + result + "'")
        time.sleep(10)
        driver.find_element(By.CSS_SELECTOR,
                            "#__next > div > div > div > div > div > div > div.styles_leftColumn__k_O3r.styles_narrow__6JuTY > form > button").click()
        time.sleep(10000)


arr = np.array([[1, 2], [3, 4]])
ExcelWriter(arr)
mail_phone = FillArray()
LogInMail()
