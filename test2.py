import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
from datetime import datetime, timedelta

# راه‌اندازی مرورگر
driver = webdriver.Chrome()

# لیست ذخیره قیمت‌ها
price_history = []

def save_to_csv():
    """ذخیره داده‌ها در فایل CSV"""
    with open('gold_prices.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Time", "Open", "High", "Low", "Close", "Position"])
        writer.writerows(price_history)

try:
    driver.get("https://www.tradingview.com/")
    sleep(5)

    # ورود به حساب کاربری
    login_button = driver.find_element(By.CSS_SELECTOR, "button[data-name='header-user-menu-sign-in']")
    login_button.click()
    sleep(5)

    iframe = driver.find_element(By.NAME, "Email")
    iframe.click()

    username = driver.find_element(By.NAME, "id_username")
    password = driver.find_element(By.NAME, "id_password")
    username.send_keys("me.anooshi@gmail.com")
    password.send_keys("mobin@nooshi2003")
    password.send_keys(Keys.RETURN)
    
    input('ok? ----------> ')  # منتظر تایید کپچا
    sleep(5)

    gold_select = driver.find_element(By.CSS_SELECTOR, 'div[data-symbol-short="GOLD"]')
    gold_select.click()
    sleep(5)

    driver.switch_to.window(driver.window_handles[1])
    print(driver.current_url)

    def get_price():
        """دریافت قیمت‌های کندل"""
        selecte_name1 = driver.find_element(By.XPATH, '/html/body/div[2]/div/div[5]/div[1]/div[1]/div/div[2]/div[1]/div[2]/div/div[1]/div[1]/div[1]/div[2]/div/div[2]/div[2]')
        selecte_name2 = driver.find_element(By.XPATH, '/html/body/div[2]/div/div[5]/div[1]/div[1]/div/div[2]/div[1]/div[2]/div/div[1]/div[1]/div[1]/div[2]/div/div[3]/div[2]')
        selecte_name3 = driver.find_element(By.XPATH, '/html/body/div[2]/div/div[5]/div[1]/div[1]/div/div[2]/div[1]/div[2]/div/div[1]/div[1]/div[1]/div[2]/div/div[4]/div[2]')
        selecte_name4 = driver.find_element(By.XPATH, '/html/body/div[2]/div/div[5]/div[1]/div[1]/div/div[2]/div[1]/div[2]/div/div[1]/div[1]/div[1]/div[2]/div/div[5]/div[2]')

        open_price = float(selecte_name1.text.replace(',', ''))
        high_price = float(selecte_name2.text.replace(',', ''))
        low_price = float(selecte_name3.text.replace(',', ''))
        close_price = float(selecte_name4.text.replace(',', ''))

        position = 'R' if open_price - close_price >= 0 else 'G'

        return [datetime.now().strftime("%Y-%m-%d %H:%M:%S"), open_price, high_price, low_price, close_price, position]

    def save_last_candle():
        """ذخیره آخرین کندل در لیست و فایل"""
        new_price = get_price()
        price_history.append(new_price)
        save_to_csv()
        print("کندل ذخیره شد:", new_price)

    def generate_45_minute_times(start_hour=2, start_minute=30, num_times=20):
        start_time = datetime(datetime.now().year, datetime.now().month, datetime.now().day, start_hour, start_minute)
        return [start_time + timedelta(minutes=45 * i) for i in range(num_times)]

    def time_to_next_45_minutes():
        now = datetime.now()
        times = generate_45_minute_times()
        for time in times:
            if now < time:
                remaining_time = time - now
                return remaining_time.seconds // 60, remaining_time.seconds % 60
        return None, None

    def is_time_in_range():
        now = datetime.now()
        return (now.hour > 2 or (now.hour == 2 and now.minute >= 30)) or (now.hour < 1 or (now.hour == 1 and now.minute <= 30))

    print("در حال اجرا...")

    while True:
        now = datetime.now()

        if is_time_in_range():
            min_left, sec_left = time_to_next_45_minutes()

            if min_left is not None and sec_left is not None:
                print(f"زمان باقی‌مانده: {min_left} دقیقه و {sec_left} ثانیه")

                if min_left == 0 and sec_left <= 5:
                    print("ذخیره کندل...")
                    save_last_candle()
                
                sleep(10)  # کاهش فشار بر سیستم
            else:
                print("منتظر زمان مناسب...")
                sleep(60)
        else:
            print("خارج از محدوده زمانی مجاز! توقف ۱ ساعته...")
            sleep(3600)

except Exception as e:
    print("خطا:", str(e))

finally:
    driver.quit()
