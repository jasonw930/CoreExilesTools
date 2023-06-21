import asyncio
from contextlib import contextmanager
import time
import threading
import socket
import websockets
import os
import json
import itertools
import traceback

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

haul_dests = []
haul_planets = {}
haul_credits = 0
haul_ratio = 0

with open(os.path.join(os.path.expanduser('~'), 'logins.json')) as file:
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


# List of systems in haul_dests to travel to in order
# Each system in haul_dests has a list of planets to deliver to in haul_planets[haul_dests[i]]
# Keep a running total of credits given
# Keep picking up missions as long as the new ratio is higher than the old
# haul_*** is running list of best missions
# best_*** is running best mission
# temp_*** is running best permutation

# haul_dests, haul_planets
# While valid mission exists:
#     best_dests, best_planets, best_fuel_eff, best_credits
#     For every mission:
#         temp_dests, temp_planets, temp_perm_ratio
#         temp_dests = haul_dests + dest
#         temp_planets = haul_planets + planet
#         For every permutation:
#             Find perm ratio
#             Update temp_dests if better
#         Update best_dests, best_planets, best_fuel_eff, best_credits, if better
#     Update haul_dests, haul_planets

def get_haul_mission():
    global haul_dests, haul_planets, haul_credits, haul_ratio
    getting_missions = True
    while getting_missions:
        # Choose Ashar Corporation
        with wait_for_page_load(driver):
            driver.find_element(By.XPATH, "%s[child::td[2][normalize-space()='Ashar Trade Office']]//input[@value='View']" % center_rows).send_keys("\n\n")
        # Enter Ashar Corporation
        with wait_for_page_load(driver):
            driver.find_element(By.XPATH, "%s//input[@value='Enter Ashar Corporation']" % center_rows).send_keys("\n\n")
        # Choose Haul Mission
        with wait_for_page_load(driver):
            cur_system = driver.find_element(By.XPATH, "/html/body/div/div[1]/table/tbody/tr[last()]/td[1]/font/font[2]/strong").text
            cur_cargo_space = int(driver.find_element(By.XPATH, "/html/body/div/div[3]/table/tbody/tr/td[10]").text)

            best_dests = haul_dests[:]
            best_planets = {}
            for d in haul_planets:
                best_planets[d] = haul_planets[d][:]
            best_fuel_eff = 0
            best_row = None
            best_credits = 0

            for row in driver.find_elements(By.XPATH, "%s[descendant::input[@value='Accept']]" % center_rows):
                row_data = row.find_elements(By.TAG_NAME, "td")
                cargo, credits = int(row_data[4].text), int("".join(row_data[5].text.split(",")))
                if cargo > cur_cargo_space:
                    continue
                system, planet = row_data[1].text, row_data[0].text
                if system not in ce_map.systems:
                    continue
                fuel, path = ce_map.dist_and_path(cur_system, system)
                if fuel != int(row_data[3].text):
                    print("*** Path Finding Error ***")

                temp_dests = haul_dests[:] + [system]
                temp_planets = {}
                for d in haul_planets:
                    temp_planets[d] = haul_planets[d][:]
                if system not in temp_planets:
                    temp_planets[system] = []
                temp_planets[system].append(planet)
                temp_perm_ratio = 0

                for perm_dests in itertools.permutations(temp_dests):
                    perm_fuel, perm_credits = ce_map.haul_cost(cur_system, perm_dests, temp_planets, temp_planets[perm_dests[-1]][-1])
                    if (haul_credits + credits - perm_credits) / perm_fuel > temp_perm_ratio:
                        temp_perm_ratio = (haul_credits + credits - perm_credits) / perm_fuel
                        temp_dests = list(perm_dests[:])

                if temp_perm_ratio > best_fuel_eff:
                    best_dests = temp_dests
                    best_planets = temp_planets
                    best_fuel_eff = temp_perm_ratio
                    best_row = row
                    best_credits = haul_credits + credits
                # print(planet, "%.4f" % best_fuel_eff)

            if best_row is None or best_fuel_eff < haul_ratio:
                getting_missions = False
                driver.find_element(By.XPATH, "%s//a[@href='index.php']" % center_rows).send_keys("\n\n")
            else:
                best_row.find_element(By.XPATH, ".//input[@value='Accept']").send_keys("\n\n")
                haul_dests = best_dests
                haul_planets = best_planets
                haul_credits = best_credits
                haul_ratio = best_fuel_eff
                print("--- Haul Info:", "%.4f" % haul_ratio, haul_dests, haul_planets)
        # Exit Ashar Corporation
        if getting_missions:
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
        # current_url = driver.current_url
        try:
            driver.find_element(By.XPATH, "//button[contains(@class,'ce-tools')]")
        except Exception as e:
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
            traceback.print_exc()

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
            traceback.print_exc()


os.system("pkill -f python; pkill -f Python")
threading.Thread(target=tool_loader).start()
threading.Thread(target=tool_listener).start()
threading.Thread(target=command_listener).start()

# TODO: Include tax calculations
# TODO: Random events traveling to location "WARNING - WARNING"


# login()
# while int("".join(driver.find_element(By.XPATH, "/html/body/div/div[3]/table/tbody/tr/td[18]").text.split(","))) > 1000:
#     haul()
# test()
