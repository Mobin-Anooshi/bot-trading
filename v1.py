from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
from selenium.webdriver.chrome.options import Options
from datetime import datetime, timedelta
import pickle
import requests
import csv


def log_message(message):
    with open("log.txt", "a", encoding="utf-8") as log_file:
        log_file.write(f"{datetime.now()} - {message}\n")

chrome_options = Options()
chrome_options.add_argument("--headless")  #  headless
chrome_options.add_argument("--disable-gpu")  # GPU
chrome_options.add_argument("--window-size=1920,1080")
driver = webdriver.Chrome(options=chrome_options)



COOKIE_FILE = "tradingview_cookies.pkl"


def save_cookies():
    """ذخیره کوکی‌های لاگین در فایل"""
    with open(COOKIE_FILE, "wb") as file:
        pickle.dump(driver.get_cookies(), file)
    log_message("Save cookies")

def load_cookies():
    """بارگذاری کوکی‌های ذخیره‌شده"""
    try:
        with open(COOKIE_FILE, "rb") as file:
            cookies = pickle.load(file)
            for cookie in cookies:
                driver.add_cookie(cookie)
        log_message("Set cookies")
    except FileNotFoundError:
        log_message("Cookies Not found")

try:


    driver.get("https://www.tradingview.com/")
    
    load_cookies()
    driver.refresh() 
    try:
        www = driver.find_element(By.CLASS_NAME,'tv-header__user-menu-button')
        www.click()
        sleep(5)
        login_button = driver.find_element(By.CSS_SELECTOR, "button[data-name='header-user-menu-sign-in']")
        login_button.click()
        

        sleep(5)


        iframe = driver.find_element(By.NAME, "Email")
        iframe.click()

        # login
        username = driver.find_element(By.NAME, "id_username")
        password = driver.find_element(By.NAME, "id_password")
        username.send_keys("me.anooshi@gmail.com")  # username
        password.send_keys("mobin@nooshi2003")  # password
        password.send_keys(Keys.RETURN)

        driver.switch_to.default_content()


        ###################################### Delete #############################
        log_message("Login")
        sleep(15)
        save_cookies()
        
    except :
        log_message('Login')
        sleep(20)
    
    
    #  انتخاب سیمبل طلا 
    log_message('Enter XAUUSD in Dashbord')
    gold_select = driver.find_element(By.CSS_SELECTOR,f'div[data-symbol-short="XAUUSD"]')
    gold_select.click()
    sleep(15)
    
    #  وارد شذن به طلا 
    log_message('Click XAUUSD Chart')
    eantr_symbol = driver.find_element(By.CLASS_NAME,'content-D4RPB3ZC')
    eantr_symbol.click()
    
    # سوییچ کردن تب 
    log_message('switching the tab')
    driver.switch_to.window(driver.window_handles[1])

    #Defualt price
    last_price = {
        'Open':0,
        'High':0,
        'Low':0,
        'Close':0,
        'Position': 'G'
        }
    
    
    # Save CSV
    def get_filename():
        today_date = datetime.now().strftime("%Y-%m-%d")
        return f"candles_{today_date}.csv"    
    
    def round_to_nearest_5_minutes(dt):
        rounded_minute = (dt.minute // 5) * 5
        if dt.minute % 5 >= 3:
            rounded_minute += 5

        if rounded_minute == 60:
            dt += timedelta(hours=1)
            rounded_minute = 0

        rounded_time = dt.replace(minute=rounded_minute, second=0, microsecond=0)

        adjusted_time = rounded_time - timedelta(minutes=45)

        return adjusted_time

    def create_csv_file():
        filename = get_filename()
        with open(filename, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Timestamp", "Open", "High", "Low", "Close", "Position"])
    
    def append_candle_to_csv(candle):
        filename = get_filename()
        with open(filename, mode="a", newline="") as file:
            writer = csv.writer(file)
            current_time = datetime.now()
            rounded_time = round_to_nearest_5_minutes(current_time)
            timestamp = rounded_time.strftime("%Y-%m-%d %H:%M:%S")
            writer.writerow([timestamp, candle["Open"], candle["High"], candle["Low"], candle["Close"], candle["Position"]])


    create_csv_file()

    
    
    
    
    # Telgram channel
    
    BOT_TOKEN = "7688739598:AAHhxrbE39yYnfeNoPrKb0gjykiDUjfjZ6Q"  # توکن جدید ربات تلگرام را اینجا وارد کنید
    CHAT_ID = "-1002323662587"  # شناسه چت تلگرام را وارد کنید
    TELEGRAM_API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    
    def send_to_telegram(message):
        
        payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "HTML",
        }
        
        try:
            response = requests.post(TELEGRAM_API_URL, data=payload)
            if response.status_code == 200:
                log_message('Sent message to Telegram')
            else:
                log_message("Faild to send Telegram", response.text)
        except Exception as e:
            log_message(("HTTP Error:", e))
    
    
    send_to_telegram('Bot started successfully')

    #get price in chart
    def get_price():

        select_name1 = driver.find_element(By.XPATH, '/html/body/div[2]/div/div[5]/div[1]/div[1]/div/div[2]/div[1]/div[2]/div/div[1]/div[1]/div[1]/div[2]/div/div[2]/div[2]')
        select_name2 = driver.find_element(By.XPATH, '/html/body/div[2]/div/div[5]/div[1]/div[1]/div/div[2]/div[1]/div[2]/div/div[1]/div[1]/div[1]/div[2]/div/div[3]/div[2]')
        select_name3 = driver.find_element(By.XPATH, '/html/body/div[2]/div/div[5]/div[1]/div[1]/div/div[2]/div[1]/div[2]/div/div[1]/div[1]/div[1]/div[2]/div/div[4]/div[2]')
        select_name4 = driver.find_element(By.XPATH, '/html/body/div[2]/div/div[5]/div[1]/div[1]/div/div[2]/div[1]/div[2]/div/div[1]/div[1]/div[1]/div[2]/div/div[5]/div[2]')
        
        
        open_price = float(select_name1.text.replace(',', ''))
        high_price = float(select_name2.text.replace(',', ''))
        low_price = float(select_name3.text.replace(',', ''))
        close_price = float(select_name4.text.replace(',', ''))
        
        
        position = 'R' if open_price - close_price >= 0 else 'G'
        
        candle = {
            'Open': open_price,
            'High': high_price,
            'Low': low_price,
            'Close': close_price,
            'Position': position
        }
        if candle == last_price :
            log_message('Two candles being equal *************************')
            driver.refresh()

        

        return candle 
        
    # save last candle info
    def save_last_candle():
        try:
            global last_price
            new_price = get_price()
            append_candle_to_csv(new_price)
            log_message(new_price)
            # signal
            if last_price:
                if last_price['Position'] == 'R' and new_price['Position'] == 'G' and last_price['Low'] > new_price['Low']:
                    send_to_telegram('Buy Now (45 method)')# Telegram
            
            last_price = new_price
        except :
            log_message('Failed to save last_candle ')
        # 276

    # save_last_candle()
    def generate_45_minute_times(start_hour=1, start_minute=15, num_times=31):
        start_time = datetime(datetime.now().year, datetime.now().month, datetime.now().day, start_hour, start_minute)
        return [start_time + timedelta(minutes=45 * i) for i in range(num_times)]


    #set 45 timers
    def time_to_next_45_minutes():
        now = datetime.now()
        times = generate_45_minute_times()
        for time in times:
            if now < time:
                remaining_time = time - now
                return remaining_time.seconds // 60, remaining_time.seconds % 60
        log_message('Can`t give the time')
        return None, None
    
    
    def should_run():
        now = datetime.now()
        current_hour = now.hour
        current_minute = now.minute

        # اگر بین ساعت ۱:۳۰ تا ۲:۳۰ بامداد است، برنامه متوقف شود
        if current_hour == 0 and current_minute >= 45:
            return False
        if current_hour == 2 and current_minute < 15:
            return False
        
        return True
    

    #loop
    while True :

        if should_run():

            mint,secn = time_to_next_45_minutes()
            log_message((mint,secn))
            
            if mint ==0 and secn <=3:
                log_message((mint,secn))
                save_last_candle()
                sleep(5)
                
            elif mint >= 20 and secn >3 :
                log_message('sleep 20m')
                sleep(1200)
                mint,secn = time_to_next_45_minutes()
                
            elif mint >= 10 and secn > 3:
                log_message('sleep 10m')
                sleep(600)
                mint,secn = time_to_next_45_minutes()
                
            elif mint >= 1 and secn != 0  :
                log_message('sleep 60s')
                sleep(60)
                mint,secn = time_to_next_45_minutes()
                
            else:
                sleep(2)
                log_message((mint,secn))
                
        else :
            log_message('Sleeping')
            sleep(1800)    
        
except :
    log_message("Die :(")
    
    
