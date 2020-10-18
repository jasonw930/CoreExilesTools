import asyncio
from contextlib import contextmanager
import time
import threading
import socket
import websockets
import os
import json

import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import selenium.webdriver.support.expected_conditions as expected_conditions
from webdriver_manager.chrome import ChromeDriverManager

from CoreExilesMap import CoreExilesMap

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get("https://play.core-exiles.com/login.php")
current_url = ""
ce_map = CoreExilesMap()
center_tables = "/html/body/div/div[@align='center']/table/tbody"
center_rows = "/html/body/div/div[@align='center']/table/tbody/tr"
haul_path = []
haul_planet = ""
ashar_nearness = 0
ashar_path = []
ashar_planet = ""
ashar_location = ""

with open(os.path.join(os.path.expanduser('~'), 'logins')) as file:
    logins = json.loads(file.read())
    print(logins.keys())


@contextmanager
def wait_for_page_load(driver, timeout=5):
    # __enter__
    old_page = driver.find_element(By.TAG_NAME, "html")
    yield
    # __exit__
    try:
        WebDriverWait(driver, timeout).until(expected_conditions.staleness_of(old_page))
        # time.sleep(2)
    except selenium.common.exceptions.TimeoutException:
        print("*** Timeout")
        with wait_for_page_load(driver):
            driver.switch_to.active_element.send_keys("\n")


def test():
    driver.get("https://www.google.com/")
    with wait_for_page_load(driver):
        driver.find_element(By.XPATH, "//*[@id='tsf']/div[2]/div[1]/div[1]/div/div[2]/input").send_keys("Test\n")
    with wait_for_page_load(driver):
        results = driver.find_elements(By.XPATH, "//div[@class='g']")
        results[1].find_element(By.XPATH, ".//a").send_keys("i")
        driver.switch_to.active_element.send_keys("\n\n")


def login():
    with wait_for_page_load(driver):
        driver.find_element(By.XPATH, "//*[@id='username']").send_keys(logins['ce_user'])
        driver.find_element(By.XPATH, "//*[@id='password']").send_keys(logins['ce_pass'])
        driver.find_element(By.XPATH, "//*[@id='login']").send_keys("\n\n")


def get_haul_mission():
    global haul_path, haul_planet, ashar_nearness, ashar_path, ashar_planet, ashar_location
    # Choose Ashar Corporation
    with wait_for_page_load(driver):
        driver.find_element(By.XPATH, "%s[child::td[2][normalize-space()='Ashar Trade Office']]//input[@value='View']" % center_rows).send_keys("\n\n")
    # Enter Ashar Corporation
    with wait_for_page_load(driver):
        driver.find_element(By.XPATH, "%s//input[@value='Enter Ashar Corporation']" % center_rows).send_keys("\n\n")
    # Choose Haul Mission
    with wait_for_page_load(driver):
        best_row, best_fuel_eff = None, 0
        cur_system = driver.find_element(By.XPATH, "/html/body/div/div[1]/table/tbody/tr[last()]/td[1]/font/font[2]/strong").text
        cur_cargo_space = int(driver.find_element(By.XPATH, "/html/body/div/div[3]/table/tbody/tr/td[10]").text)
        for row in driver.find_elements(By.XPATH, "%s[descendant::input[@value='Accept']]" % center_rows):
            row_data = row.find_elements(By.TAG_NAME, "td")
            cargo, credits = int(row_data[4].text), int("".join(row_data[5].text.split(",")))
            system, planet = row_data[1].text, row_data[0].text
            if system not in ce_map.systems:
                continue
            fuel, path = ce_map.dist_and_path(cur_system, system)
            if fuel != int(row_data[3].text):
                print("*** Path Finding Error ***")
            fuel += 2
            credits -= 100
            a_nearness, a_dist, a_path, a_planet, a_location, a_cost = ce_map.nearest_ashar(system, planet, planet)
            if a_nearness == 1:
                credits -= a_cost
            elif a_nearness == 2:
                fuel += 1
                credits -= a_cost
            elif a_nearness == 3:
                fuel += 2 + a_dist
                credits -= 50 + a_cost
            if cargo < cur_cargo_space and credits / fuel > best_fuel_eff:
                best_row = row
                best_fuel_eff = credits / fuel
                haul_path, haul_planet = path, planet
                ashar_nearness, ashar_path, ashar_planet, ashar_location = a_nearness, a_path, a_planet, a_location
            print("%.4f" % (credits / fuel), credits, fuel, path, planet, a_path, a_planet, a_location)
        print("--- Haul Info:", "%.4f" % best_fuel_eff, haul_path, haul_planet, ashar_path, ashar_planet, ashar_location)
        best_row.find_element(By.XPATH, ".//input[@value='Accept']").send_keys("\n\n")
    # Exit Ashar Corporation
    with wait_for_page_load(driver):
        driver.find_element(By.XPATH, "%s//input[@value='Exit Office']" % center_rows).send_keys("\n\n")


def travel_to_location(planet, location=""):
    if location == "":
        location = planet
    # Undock
    with wait_for_page_load(driver):
        cur_planet = driver.find_element(By.XPATH, "/html/body/div/div[1]/table/tbody/tr[last()]/td[1]/font/font[1]/strong").text
        if cur_planet == "Jump Gate Nexus":
            driver.find_element(By.XPATH, "%s//input[contains(@value,'Undock in')]" % center_rows).send_keys("\n\n")
        else:
            driver.find_element(By.XPATH, "%s//input[contains(@value,'Undock from')]" % center_rows).send_keys("\n\n")
    # Travel to planet
    cur_planet = driver.find_element(By.XPATH, "/html/body/div/div[1]/table/tbody/tr[last()]/td[1]/font/font[1]/strong").text
    if cur_planet != planet:
        with wait_for_page_load(driver):
            driver.find_element(By.XPATH, "%s//input[@alt='%s']" % (center_rows, planet)).send_keys("\n\n")
    # Dock at planet
    with wait_for_page_load(driver):
        driver.find_element(By.XPATH, "%s//a[@href='dock.php']" % center_rows).send_keys("\n\n")
    # Confirm Dock
    with wait_for_page_load(driver):
        try:
            driver.find_element(By.XPATH, "%s[child::td[1][normalize-space()='%s']]//input[@value='Dock Here']" % (center_rows, location)).send_keys("\n\n")
        except Exception:
            driver.find_element(By.XPATH, "%s//input[@value='Dock Now']" % center_rows).send_keys("\n\n")


def travel_to_system(path):
    # Travel to dest system
    for jump_dest in path:
        print("--- Jumping To:", jump_dest)
        with wait_for_page_load(driver):
            driver.find_element(By.XPATH, "%s[child::td[2][normalize-space()='%s']]//input[@value='Jump']" % (center_rows, jump_dest)).send_keys("\n\n")


def continue_dialogue():
    # Dialogue
    with wait_for_page_load(driver):
        driver.find_element(By.XPATH, "%s//input[@value='Continue']" % center_rows).send_keys("\n\n")


def haul():
    global haul_path, haul_planet, ashar_nearness, ashar_path, ashar_planet, ashar_location
    get_haul_mission()
    travel_to_location("Jump Gate Nexus")
    travel_to_system(haul_path)
    travel_to_location(haul_planet)
    continue_dialogue()
    if ashar_nearness == 1 or ashar_nearness == 2:
        travel_to_location(ashar_planet, ashar_location)
    if ashar_nearness == 3:
        travel_to_location("Jump Gate Nexus")
        travel_to_system(ashar_path)
        travel_to_location(ashar_planet, ashar_location)


def tool_loader():
    global driver, current_url
    while True:
        if driver.current_url != current_url:
            current_url = driver.current_url
            ip = socket.gethostbyname(socket.gethostname())
            js = open("CoreExilesTools.js", "r").read()
            driver.execute_script(f"var ip = \"{ip}\";\n{js}")
        time.sleep(1)


def tool_listener():
    async def server(websocket, path):
        cmd = await websocket.recv()
        if cmd[:4] == "--- ":
            cmd = cmd[4:]
        else:
            return
        print(f"--- Received Command: {cmd}")
        try:
            exec(cmd)
        except Exception as e:
            print(e)

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    start_server = websockets.serve(server, "127.0.0.1", 8765)
    loop.run_until_complete(start_server)
    loop.run_forever()


def command_listener():
    global driver
    while True:
        print("> ", end="")
        line = input()
        code = [line]
        while line != "--":
            print("\n".join(code))
            print("> ", end="")
            line = input()
            if line == "**" and len(code) > 0:
                del code[-1]
            elif line != "**" and line != "--":
                code.append(line)
        # exec("async def func():\n" + code + "\nasyncio.run(func())")
        try:
            exec("\n".join(code))
        except Exception as e:
            print(e)


os.system("pkill -f python; pkill -f Python")
threading.Thread(target=tool_loader).start()
threading.Thread(target=tool_listener).start()
threading.Thread(target=command_listener).start()

# TODO: Add buttons
# TODO: Include tax calculations
# TODO: Random events traveling to location "WARNING - WARNING"
# login()
# while int("".join(driver.find_element(By.XPATH, "/html/body/div/div[3]/table/tbody/tr/td[18]").text.split(","))) > 1000:
#     haul()
# test()
