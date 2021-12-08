password = "e=098787953"











































from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import time

options = Options()
options.binary_location = "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
webdriver_path = 'C:\\chromedriver_win32\\chromedriver.exe'

driver = webdriver.Chrome(executable_path=webdriver_path, options=options)
driver.get("https://mail.npust.edu.tw/")
assert "" in driver.title
acc = driver.find_element_by_name("USERID")
pas = driver.find_element_by_name("PASSWD")
acc.clear()
pas.clear()
acc.send_keys("B10856052")
pas.send_keys(password)
pas.send_keys(Keys.RETURN)
assert "No results found." not in driver.page_source
#driver.close()