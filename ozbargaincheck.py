#Ozbargain check for 65" OLED
from datetime import datetime
import time
import sys

# Selenium for browser + login
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException
from pushnotifier.exceptions import *
from selenium.webdriver.chrome.options import Options

# Feedparser+ for XML (in use?)
from bs4 import BeautifulSoup

# String for stripping non-ascii
import string

# Pushnotifier for notifications
from pushnotifier import PushNotifier as pn
username = "tyranoc"
password = "75ZHS7NMELV4wxG"
api_key = "E5YR66C3VV75BBV46V75B575B63CVERKFBFFBBKFER"
package_name = "com.ozbargain.app"
devicesTM = ["86wL"] # my Pixel only, must be in array

ozb_user = "kramo"
ozb_pass = "MaSRW7N!gVssWAa"
url_ozb = "https://www.ozbargain.com.au/user/login"

urlRSS = "https://www.ozbargain.com.au/deals/feed"
now = datetime.now()
current_time = now.strftime("%H:%M:%S")
checkedTime = datetime.min
postTime = datetime.min
count = 0

## Mark's Array of arrays of words ["wordA","wordB"]
keywords = [["65","OLED"],["LG","C2","65"],["LG","CS","65"],["SONY","A80K","65"],["Lenovo EDU"]]

def searchKeywords(postK,keywordsK):
    for wordK in keywordsK:
        if(wordK.upper() in postK.title.get_text().upper()):
            continue
        else:
            return False
    return True

## DEFINITIONS FOR MARK
def notifyMark(postM):
    print("OZBARGAIN DEAL FOUND :",postM.title.get_text()[:55],"-",current_time)
    print('\007', end='\r')
    time.sleep(.5)
    print('\007', end='\r')
    time.sleep(.5)
    print('\007', end='\r')
    msg_result = pn.send_notification("TV DEAL FOUND!!" + current_time, post.link.get_text(), devicesTM)

def searchMark(postX):
    for words in keywords:
        if searchKeywords(postX,words):
            notifyMark(postX)
            global count
            count = 0
            return True
        else:
            continue
    return False

## DEFINITIONS FOR OTHERS
def notifyGeneric(postG,devicesG,searchItemG,searchNameG):
    print(searchItemG + " DEAL FOUND FOR " + searchNameG + ": " + postG.title.get_text()[:45] + " - " + current_time)
    msg_result = pn.send_notification(searchItemG + " DEAL FOUND! " + current_time, post.link.get_text(), devicesG)
    pass

def searchGeneric(postY,keywordsY,devicesY,searchItemY,searchNameY):
    for words in keywordsY:
        if searchKeywords(postY,words):
            notifyGeneric(postY,devicesY,searchItemY,searchNameY)
            global count
            count = 0
            return True
        else:
            continue
    return False

##
## ASSIGN VARIABLES FOR OTHERS
## 
def searchOthers(postO):
    searchAaron(postO)
    # Place any other requests
    return True

# Assign details of other people's searches
keywordsAaron = [["WH-1000XM4"],["WH 1000XM4"],["WH1000XM4"],["WH-1000XM5"],["WH 1000XM5"],["WH1000XM5"]]
devicesAaron = ["XLxW"] # old device oQpj
def searchAaron(postX):
    searchGeneric(postX,keywordsAaron,devicesAaron,"HEADPHONE","Aaron")
## END ASSIGNMENTS

# Cleanup title strings
def cleanUp(title):
    cleanedTitle =  ''.join(filter(lambda x: x in string.printable, title))
    cleanedTitle = cleanedTitle.lstrip()
    return cleanedTitle[:55]

# Cleanup time strings
def formatTime(date1):
    return datetime.strptime(date1,'%a, %d %b %Y %H:%M:%S %z').replace(tzinfo=None)

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
delay = 10 # maximum time to wait for page load
sleep_time = 16 # time between cycles
loading_time = 110 # time between 'too long to load'

browser.get(url_ozb)

while(True):
    try:
        myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.ID, "edit-name")))
        elem_user = browser.find_element(By.ID, "edit-name")
        elem_pass = browser.find_element(By.ID, "edit-pass")
        elem_user.send_keys(ozb_user)
        elem_pass.send_keys(ozb_pass, Keys.RETURN)
        time.sleep(5)
        myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.CLASS_NAME, "userinfo")))
        print("Logged in succesfully")
        time.sleep(sleep_time)
        break
    except TimeoutException:
        print("Loading took too much time or unable to login!",current_time)
        time.sleep(loading_time)
    
# First run - get details
while(True):
    try:
        browser.get(urlRSS)
        # Import into BeautifulSoup
        xml_data = browser.find_element(By.TAG_NAME, "body").text
        soup = BeautifulSoup(xml_data,features="xml")
        deals = soup.find_all('item')

        if(len(deals)==0):
            time.sleep(loading_time)
            break
        break
    except WebDriverException:
        time.sleep(loading_time)

abbrevTitle = cleanUp(deals[0].title.get_text())
postTime = formatTime(deals[0].pubDate.get_text())

if(len(sys.argv) == 2 and sys.argv[1] == "A"):
    #do not process current posts
    checkedTime = now
    gapTime = str(now - postTime).split(".")[0].split(":", 1)[1]
    print("Processing from",current_time)
    print(abbrevTitle,"-",gapTime,"ago. Refresh",str(count), end='\r')
else:
    for post in reversed(deals):
        searchMark(post)
        # OTHER PEOPLE'S SEARCHES
        searchOthers(post)
        checkedTime = postTime
    print("Processing from " + current_time)
    gapTime = str(now - postTime).split(".")[0].split(":", 1)[1]
    print(abbrevTitle,"-",gapTime,"ago. Refresh",str(count), end='\r')
time.sleep(sleep_time)

# Looping run, comparing checked-time
while(True):
    # Parse and process feed
    while(True):
        try:
            browser.get(urlRSS)
            break
        except WebDriverException:
            time.sleep(loading_time)
    xml_data = browser.find_element(By.TAG_NAME, "body").text
    # Import into BeautifulSoup
    soup = BeautifulSoup(xml_data,features="xml")
    deals = soup.find_all('item')

    if(len(deals)==0):
        time.sleep(loading_time)
        break

    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    abbrevTitle = cleanUp(deals[0].title.get_text())
    postTime = formatTime(deals[0].pubDate.get_text())
    gapTime = str(now - postTime).split(".")[0].split(":", 1)[1]
    count += 1

    for i,post in enumerate(deals):
        postTime = formatTime(post.pubDate.get_text())
        if(postTime <= checkedTime):
            print(abbrevTitle,"-",gapTime,"ago. Refresh",str(count), end='\r')
            break
        searchMark(post)
        # PERFORM OTHER'S SEARCHES
        searchOthers(post)
    checkedTime = formatTime(deals[0].pubDate.get_text()) # set checked time to most recent post
    time.sleep(sleep_time)