import os
import json
from dotenv import load_dotenv
import data.page as page_data

load_dotenv()

def account_credentials():
    return (
        os.getenv('CE_USER'),
        os.getenv('CE_PASS')
    )

def login(username, password):
    page_data.send_keys("//*[@id='username']", username)
    page_data.send_keys("//*[@id='password']", password)
    page_data.press_button("//*[@id='login']")
