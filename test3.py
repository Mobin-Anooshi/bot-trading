from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
from selenium.webdriver.chrome.options import Options
from datetime import datetime
from datetime import datetime, timedelta
# from DrissionPage import ChromiumPage 
from GoogleRecaptchaBypass.RecaptchaSolver import RecaptchaSolver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC




driver = webdriver.Chrome()




driver.get("https://www.tradingview.com/")


www = driver.find_element(By.CLASS_NAME,'tv-header__user-menu-button')
www.click()
sleep(5)
login_button = driver.find_element(By.CSS_SELECTOR, "button[data-name='header-user-menu-sign-in']")
login_button.click()


sleep(5)


iframe = driver.find_element(By.NAME, "Email")

iframe.click()

username = driver.find_element(By.NAME, "id_username")
password = driver.find_element(By.NAME, "id_password")
username.send_keys("me.anooshi@gmail.com")  # نام کاربری خود را اینجا وارد کنید
password.send_keys("mobin@nooshi2003")  # رمز عبور خود را اینجا وارد کنید
password.send_keys(Keys.RETURN)
sleep(10)
driver.switch_to.default_content() 


wait = WebDriverWait(driver, 10)

solver = RecaptchaSolver(driver)

try:
    solver.solveCaptcha()
except Exception as e:
    print(f"خطا در حل کپچا: {e}")

# ادامه کد بعد از حل کپچا




password.send_keys(Keys.RETURN)


print("ورود موفقیت‌آمیز!")
input('ok? ----------> ') # منتظر تایید کپچا
sleep(5)





gold_select = driver.find_element(By.CSS_SELECTOR,f'div[data-symbol-short="GOLD"]')
gold_select.click()
sleep(5)
eantr_symbol = driver.find_element(By.CLASS_NAME,'content-D4RPB3ZC')
eantr_symbol.click()


    
