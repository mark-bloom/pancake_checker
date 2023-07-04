# Check pancake parlour to notify of <5 degrees
from datetime import datetime
from enum import Enum
import time

# Selenium for browser + login
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
from pushnotifier.exceptions import *
from selenium.webdriver.chrome.options import Options

# Regex for stripping number out of temperature
import re

# Pushnotifier for notifications
from pushnotifier import PushNotifier as pn
username = "tyranoc"
password = "75ZHS7NMELV4wxG"
api_key = "E5YR66C3VV75BBV46V75B575B63CVERKFBFFBBKFER"
package_name = "com.pancakes.app"
devices = ["86wL"] # my Pixel only, must be in array

url_pancakes = "https://www.winterparlour.com.au/live-temp-update/"

StateEnum = Enum('StateEnum', ['MONITORING','BELOW','NEAR'])

# Initial configuration

program_state = StateEnum.MONITORING
temp_below = False
previous_temp = 0
current_temp = 0

now = datetime.now()
current_time = now.strftime("%H:%M:%S")
current_date = now.strftime("%A %d/%m/%Y")

def notifyPancakes():
    message = "It's " + str(current_temp) + " degrees at " + current_time + " " + current_date + ". Get some pancakes!"
    print(message)
    msg_result = pn.send_notification(message, url_pancakes, devices)

def init_pushnotifier(pnX):
    try:
        pn = pnX.PushNotifier(username, password, package_name, api_key)
        return pn
    except IncorrectCredentialsError:
        print(username,": Incorrect credentials!")
        exit()
    except UserNotFoundError:
        print(username,": User not found!")
        exit()

# Setup options for Chrome
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

# Initialise pushnotifier
pn = init_pushnotifier(pn)

# Initialise browser
browser = webdriver.Chrome(options=chrome_options)
delay = 15 # maximum time to wait for page load
time_for_run = 12

###CHANGE TO 180 AFTER ENUM
sleep_time = 180 - time_for_run # time between cycles
below_time = 600 - time_for_run # time when below 5 degrees
near_time = 45 - time_for_run # time when waiting for update
success_sleep = 3600 - time_for_run # Wait 1 hour if below before starting to check again

# First run - get details
while(True):
    try:
        browser.get(url_pancakes)
        temp_text = browser.find_element(By.ID, "temp").text
        if temp_text:
            break
    except WebDriverException:
        time.sleep(sleep_time)

#print("Processing from",current_time,"on",current_date)
# Get current temperature digits, decimal, digits
current_temp = float(re.findall("^\d*\.?\d?",temp_text)[0])

if current_temp <= 5.0:
    notifyPancakes()
    temp_below = True
    time.sleep(success_sleep)
else:
    print("Pancake temperature is",str(current_temp)+"° at",current_time,"on",current_date)
    
previous_temp = current_temp
time.sleep(sleep_time)

# Looping run, comparing checked-time
while(True):
    # Parse and process feed
    while(True):
        try:
            browser.get(url_pancakes)
            break
        except WebDriverException:
            time.sleep(sleep_time)
    temp_text = browser.find_element(By.ID, "temp").text
    
    current_temp = float(re.findall("^\d*\.*\d*",temp_text)[0])

    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    current_date = now.strftime("%A %d/%m/%Y")

    changed_temp = (previous_temp != current_temp)

    if changed_temp:
        print("Pancake temperature is",str(current_temp)+"° at",current_time,"on",current_date)
        last_time_change = now
        previous_temp = current_temp

    match program_state:
        case StateEnum.MONITORING:
            if current_temp <= 5.0:
                notifyPancakes()
                program_state = StateEnum.BELOW
                time.sleep(success_sleep)
                continue
            else:
                duration = (now - last_time_change).total_seconds()
                if (duration > 1200): # If 20 minutes since last change
                    program_state = StateEnum.NEAR
                time.sleep(sleep_time)
                continue
        case StateEnum.BELOW:
            if current_temp > 5.0:
                program_state = StateEnum.MONITORING
            time.sleep(below_time)
            continue
        case StateEnum.NEAR:
            if current_temp <= 5.0:
                notifyPancakes()
                program_state = StateEnum.BELOW
                time.sleep(success_sleep)
                continue
            elif changed_temp:
                program_state = StateEnum.MONITORING
            time.sleep(near_time)
            continue

    # if reached, no match?
    time.sleep(sleep_time)