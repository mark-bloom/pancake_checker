## Check Twice ticket availability
## Notification by selection
# A = computer only
# B = mobile only
# other or no input = both

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.firefox.options import Options

from datetime import datetime

from pushnotifier import PushNotifier as pn
username = "tyranoc"
password = "75ZHS7NMELV4wxG"
api_key = "E5YR66C3VV75BBV46V75B575B63CVERKFBFFBBKFER"
package_name = "com.generic.app"

def init_pushnotifier(pnX):
    try:
        pn = pnX.PushNotifier(username, password, package_name, api_key)
        return pn
    except IncorrectCredentialsError:
        print(username + ": Incorrect credentials!")
    except UserNotFoundError:
        print(username + ": User not found!")

pn = init_pushnotifier(pn)

## RUN GENERIC
msg_result = pn.send_notification("Sending you a test notification!", "https://www.ozbargain.com.au/", ["NLLL"])