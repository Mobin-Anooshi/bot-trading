from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
from selenium.webdriver.chrome.options import Options
from datetime import datetime, timedelta
import pickle
import requests
import csv
import re





# Log messages
def log_message(message):
    with open("log.txt", "a", encoding="utf-8") as log_file:
        log_file.write(f"{datetime.now()} - {message}\n")



#Headless
chrome_options = Options()
chrome_options.add_argument("--headless")  #  headless
chrome_options.add_argument("--disable-gpu")  # GPU
chrome_options.add_argument("--window-size=1920,1080")
driver = webdriver.Chrome(options=chrome_options)



COOKIE_FILE = "tradingview_cookies.pkl"




def save_cookies():
    """
        Save Cookie
    """
    with open(COOKIE_FILE, "wb") as file:
        pickle.dump(driver.get_cookies(), file)
    log_message("Save cookies")

def load_cookies():
    """
        Load Cookies
    """
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

        btn_menu = driver.find_element(By.CLASS_NAME, 'tv-header__user-menu-button')
        btn_menu.click()
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

        log_message("Login")
        sleep(15)
        save_cookies()

    except:
        log_message('Login')
        sleep(20)

    # Enter Gold Symbol
    log_message('Enter Gold Symbol')
    gold_select = driver.find_element(By.CSS_SELECTOR, f'div[data-symbol-short="XAUUSD"]')
    gold_select.click()
    sleep(15)

    #  Open Gold Chart
    log_message('Click Gold Chart')
    enter_symbol = driver.find_element(By.CLASS_NAME, 'content-D4RPB3ZC')
    enter_symbol.click()

    #  switching the tab
    log_message('switching the tab')
    driver.switch_to.window(driver.window_handles[1])

    # Default price
    last_price = {
        'Open': 0,
        'High': 0,
        'Low': 0,
        'Close': 0,
        'Position': 'G'
    }
except :
    log_message('Error in open chart')


try :

    def get_filename():
        """
            Get CSV file name
        """

        today_date = datetime.now().strftime("%Y-%m-%d")
        return f"candles_{today_date}.csv"

    def create_csv_file():

        """
            Create or Open CSV file
        """

        filename = get_filename()
        with open(filename, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Timestamp", "Open", "High", "Low", "Close", "Position"])


    def round_to_nearest_5_minutes(dt):

        """
            round to nearst 5 minutes and mines 45 minute
        """

        rounded_minute = (dt.minute // 5) * 5
        if dt.minute % 5 >= 3:
            rounded_minute += 5

        if rounded_minute == 60:
            dt += timedelta(hours=1)
            rounded_minute = 0

        rounded_time = dt.replace(minute=rounded_minute, second=0, microsecond=0)
        adjusted_time = rounded_time - timedelta(minutes=45)

        return adjusted_time

    def append_candle_to_csv(candle):

        """
            Append to CSV file
        """

        filename = get_filename()
        with open(filename, mode="a", newline="") as file:
            writer = csv.writer(file)
            current_time = datetime.now()
            rounded_time = round_to_nearest_5_minutes(current_time)
            timestamp = rounded_time.strftime("%Y-%m-%d %H:%M:%S")
            writer.writerow([timestamp, candle["Open"], candle["High"], candle["Low"], candle["Close"], candle["Position"]])



    create_csv_file()


except:
    log_message('Error in CSV files')

try :

    BOT_TOKEN = "7688739598:AAHhxrbE39yYnfeNoPrKb0gjykiDUjfjZ6Q"  #Token
    CHAT_ID = "-1002323662587"  # Chat ID
    TELEGRAM_API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage" # URL


    def send_to_telegram(message):

        """
            Config Telegram Bot
        """

        payload = {
            "chat_id": CHAT_ID,
            "text": message,
            "parse_mode": "HTML",
        }

        try:
            response = requests.post(TELEGRAM_API_URL, data=payload) #Send Message
            if response.status_code == 200:
                log_message('Sent message to Telegram')
            else:
                log_message(("Failed to send Telegram", response.text))
        except Exception as e:
            log_message(("HTTP Error:", e))


    send_to_telegram('Bot started successfully')

except:
    log_message('Telegram Error')

try :

    def get_price():

        """
            Get Price on chart
        """

        select_name1 = driver.find_element(By.XPATH,
                                           '/html/body/div[2]/div/div[5]/div[1]/div[1]/div/div[2]/div[1]/div[2]/div/div[1]/div[1]/div[1]/div[2]/div/div[2]/div[2]')
        select_name2 = driver.find_element(By.XPATH,
                                           '/html/body/div[2]/div/div[5]/div[1]/div[1]/div/div[2]/div[1]/div[2]/div/div[1]/div[1]/div[1]/div[2]/div/div[3]/div[2]')
        select_name3 = driver.find_element(By.XPATH,
                                           '/html/body/div[2]/div/div[5]/div[1]/div[1]/div/div[2]/div[1]/div[2]/div/div[1]/div[1]/div[1]/div[2]/div/div[4]/div[2]')
        select_name4 = driver.find_element(By.XPATH,
                                           '/html/body/div[2]/div/div[5]/div[1]/div[1]/div/div[2]/div[1]/div[2]/div/div[1]/div[1]/div[1]/div[2]/div/div[5]/div[2]')

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
        if candle == last_price:
            log_message('Reloading The Page')
            driver.refresh()

        return candle


except :
    log_message('Cant Get Prices On Chart')

try:

    def get_time_to_end():

        """
            Time to Closed Market
        """

        open_element = driver.find_element(By.XPATH,
                            '/html/body/div[2]/div/div[5]/div[1]/div[1]/div/div[2]/div[1]/div[2]/div/div[1]/div/div[1]/div[1]/div[3]/div/div[1]')
        open_element.click()
        text_numbers = driver.find_element(By.XPATH,
                                   '/html/body/div[6]/div[2]/span/div[1]/div/div/div[1]/div/p/span[2]').text
        numbers = re.findall(r'\d+',text_numbers)
        hour ,minutes = map(int,numbers)
        open_element.click()
        return hour , minutes


    generate_45_list = []

    def generate_45():

        """
            Generate all times for check 45 minutes
        """

        global generate_45_list
        hour,minute = get_time_to_end()
        now = datetime.now().replace(second=0,microsecond=0)
        start_time = now + timedelta(hours=hour, minutes=minute+1)

        return [start_time - timedelta(minutes=45 * i) for i in range(32)]



    def market_closed() :

        """
            Market Closed after checked on site
        """

        global generate_45_list
        open_element = driver.find_element(By.XPATH,
                                           '/html/body/div[2]/div/div[5]/div[1]/div[1]/div/div[2]/div[1]/div[2]/div/div[1]/div/div[1]/div[1]/div[3]/div/div[1]')
        open_element.click()
        text_numbers = driver.find_element(By.XPATH,
                                           '/html/body/div[6]/div[2]/span/div[1]/div/div/div[1]/div/p/span[2]').text
        numbers = re.findall(r'\d+', text_numbers)
        open_element.click()

        if len(numbers) == 1:
            numbers.insert(0,'0')

        timer_sleep = int(numbers[0])*3600 + int(numbers[1])*60 + 180
        log_message(timer_sleep)
        send_to_telegram(f'Market open in {timer_sleep}s ')
        sleep(timer_sleep)
        driver.refresh()
        save_cookies() #Save cookie after 1D
        generate_45_list =[]
        send_to_telegram(f'Open')
        return time_to_next_45_minutes()


    def time_to_next_45_minutes():

        """
            Check Time To Closed Timeframe
        """

        global generate_45_list
        now = datetime.now()

        if len(generate_45_list) == 0:
            times = generate_45()
        else:
            times = generate_45_list

        for time in times:
            if now < time:
                remaining_time = time - now
                return remaining_time.seconds // 60, remaining_time.seconds % 60

        log_message('Can`t give the time')
        return market_closed()

except:
    log_message('Bug in Set Timers')

try:
    def save_last_candle():

        """
            Save Last Candle And After Check Algorithms
        """

        try:
            global last_price
            new_price = get_price()
            append_candle_to_csv(new_price)
            log_message(new_price)
            # Signal
            if last_price:
                if last_price['Position'] == 'R' and new_price['Position'] == 'G' and last_price['Low'] > new_price['Low']:
                    send_to_telegram('Buy Now (45 method)')  # Telegram

            last_price = new_price
        except:
            log_message('Failed to save last_candle ')
except:
    log_message('Bug in Save Candles')


try:
    while True:
        """
            Check Timeline To End 
        """
        mint, sec = time_to_next_45_minutes()
        log_message((mint, sec))

        if mint == 0 and sec <= 3:
            log_message((mint, sec))
            save_last_candle()
            sleep(5)

        elif mint >= 20 and sec > 3:
            log_message('sleep 20m')
            sleep(1200)
            mint, sec = time_to_next_45_minutes()

        elif mint >= 10 and sec > 3:
            log_message('sleep 10m')
            sleep(600)
            mint, sec = time_to_next_45_minutes()


        elif mint >= 1 and sec != 0:
            log_message('sleep 60s')
            sleep(60)
            mint, sec = time_to_next_45_minutes()

        else:
            sleep(2)
            log_message((mint, sec))



except:
    log_message("Die :(")
