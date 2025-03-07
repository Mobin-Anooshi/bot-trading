from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
from selenium.webdriver.chrome.options import Options
from datetime import datetime
from datetime import datetime, timedelta






driver = webdriver.Chrome()

try:


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

    driver.switch_to.default_content()



    print("ورود موفقیت‌آمیز!")
    input('ok? ----------> ') # منتظر تایید کپچا
    sleep(5)
    
    
    
    
    gold_select = driver.find_element(By.CSS_SELECTOR,f'div[data-symbol-short="GOLD"]')
    gold_select.click()
    sleep(5)
    eantr_symbol = driver.find_element(By.CLASS_NAME,'content-D4RPB3ZC')
    eantr_symbol.click()
    
    
    driver.switch_to.window(driver.window_handles[1])
    print(driver.current_url)
    last_price = {
        'Open':0,
        'High':0,
        'Low':0,
        'Close':0,
        'Position': 'G'
        }

    
    

    def get_price():
        selecte_name1 = driver.find_element(By.XPATH, '/html/body/div[2]/div/div[5]/div[1]/div[1]/div/div[2]/div[1]/div[2]/div/div[1]/div[1]/div[1]/div[2]/div/div[2]/div[2]')
        selecte_name2 = driver.find_element(By.XPATH, '/html/body/div[2]/div/div[5]/div[1]/div[1]/div/div[2]/div[1]/div[2]/div/div[1]/div[1]/div[1]/div[2]/div/div[3]/div[2]')
        selecte_name3 = driver.find_element(By.XPATH, '/html/body/div[2]/div/div[5]/div[1]/div[1]/div/div[2]/div[1]/div[2]/div/div[1]/div[1]/div[1]/div[2]/div/div[4]/div[2]')
        selecte_name4 = driver.find_element(By.XPATH, '/html/body/div[2]/div/div[5]/div[1]/div[1]/div/div[2]/div[1]/div[2]/div/div[1]/div[1]/div[1]/div[2]/div/div[5]/div[2]')
        p = float(selecte_name1.text.replace(',','')) - float(selecte_name4.text.replace(',',''))
        if p>=0:
            position = 'R'
        else:
            position = 'G'
            
        candel = {
            'Open':float(selecte_name1.text.replace(',','')),
            'High':float(selecte_name2.text.replace(',','')),
            'Low':float(selecte_name3.text.replace(',','')),
            'Close':float(selecte_name4.text.replace(',','')),
            'Position': position
        }
        return candel

    def save_last_candel():
        global last_price
        new_price = get_price()
        if last_price['Position'] == 'G':
            last_price = new_price
        if last_price['Position'] == 'R':
            if new_price['Position'] == 'R':
                last_price = new_price
            if new_price['Position'] == 'G':
                if last_price['Low'] > new_price['Low']:
                    print('BUUUUUUUUUUUUYYYYYYYYYYYYY')
                    last_price = new_price
                else :
                    last_price = new_price
        print(last_price)

    save_last_candel()
        
 
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
        return (now.hour > 2 or (now.hour == 2 and now.minute >= 30)) and (now.hour < 1 or (now.hour == 1 and now.minute <= 30))

    
    # محاسبه زمان باقی‌مانده تا نزدیکترین زمان ۴۵ دقیقه‌ای
    min_left,sec_left = time_to_next_45_minutes()

                
            
    print(f"{min_left,sec_left }")
    save_last_candel(min_left,sec_left) 
        
        
    
    
    
    
    
except :
    print("error")
    
    
