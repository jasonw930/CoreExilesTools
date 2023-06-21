import time
import threading
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import selenium.webdriver.support.expected_conditions as expected_conditions
from webdriver_manager.chrome import ChromeDriverManager


driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get('https://play.core-exiles.com/login.php')

def load_client():
    with open('js/client.js', 'r') as client_file:
        client_script = client_file.read()
    
    while True:
        try:
            driver.find_element(By.XPATH, "//button[contains(@class,'ce-tools')]")
        except Exception:
            driver.execute_script(client_script)
        time.sleep(1)

threading.Thread(target=load_client).start()


def send_keys(xpath, keys):
    driver.find_element(By.XPATH, xpath).send_keys(keys)

def press_button(xpath, timeout=5, no_wait=False):
    old_page = driver.find_element(By.TAG_NAME, 'html')
    
    driver.find_element(By.XPATH, xpath).send_keys('\n\n')

    if not no_wait:
        while True:
            try:
                WebDriverWait(driver, timeout).until(expected_conditions.staleness_of(old_page))
                break
            except selenium.common.exceptions.TimeoutException:
                print('*** Timeout')
