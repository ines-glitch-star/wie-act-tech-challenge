


import pytesseract
from PIL import ImageGrab, ImageOps, ImageEnhance
import cv2 as cv
import pyautogui
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set the path to tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\inesb\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Initialize the Chrome driver
driver = webdriver.Chrome()


from selenium import webdriver
from time import sleep
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import pytesseract
from PIL import ImageGrab, ImageOps, ImageEnhance
import cv2 as cv
import pyautogui
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set the path to tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\inesb\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

# Initialize the Chrome driver
driver = webdriver.Chrome()

# Open Facebook login page

# Open Facebook login page
driver.get('https://www.facebook.com/messages/')

# Locate the email field and input email
driver.find_element(By.XPATH, '//*[@id="email"]').send_keys('soumi123456123456@gmail.com')

# Locate the password field and input password
driver.find_element(By.XPATH, '//*[@id="pass"]').send_keys('azerty123456123456')

# Locate the login button and click it
driver.find_element(By.NAME, 'login').click()

frndId = str(input('Ines Blidi'))
message = str(input('Enter your text message here: '))
# i start navigating to message and click on the friend i wanna messsage
mesgAdd='https://www.facebook.com/messages/t/'
mesgLink=mesgAdd+frndId
driver.get(mesgLink)
sleep (1)
#This is Where I clicked the Send Message '
driver.find_element_by_xpath('//div[@class="_1mf _1mj"]').send_keys(message, Keys.ENTER)
driver.quit()
