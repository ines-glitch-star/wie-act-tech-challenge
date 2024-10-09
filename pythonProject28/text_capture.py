import numpy as np
from PIL import Image, ImageEnhance, ImageOps
import pytesseract
import mss
from screeninfo import get_monitors
from check_bad_words import run_bad_word_check, bad_word_detected
import time
import re
import unicodedata
import cv2 as cv
import os
from datetime import datetime

# Define the Tesseract executable path
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\inesb\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"
screenshot_dir = "C:\\Users\\inesb\\PycharmProjects\\pythonProject28\\screenshots"
last_screenshot_filename = "last_screenshot.png"

# Get the full path for the last screenshot
last_screenshot_path = os.path.join(screenshot_dir, last_screenshot_filename)
# Get screen resolution
def get_screen_resolution():
    for monitor in get_monitors():
        return monitor.width, monitor.height

# Define chatbox region
def get_chatbox_area():
    screen_width, screen_height = get_screen_resolution()
    return {"top": screen_height // 3, "left": screen_width // 2, "width": screen_width // 2, "height": screen_height // 2}

# Preprocess the image for OCR
def preprocess_image(img):
    img = ImageOps.grayscale(img)  # Convert to grayscale
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(2)  # Enhance contrast
    return img

# Detect Facebook message regions dynamically
def detect_message_regions(img_cv):
    gray = cv.cvtColor(img_cv, cv.COLOR_BGR2GRAY)  # Convert to grayscale
    thresh = cv.adaptiveThreshold(gray, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY_INV, 11, 2)  # Adaptive threshold
    contours, _ = cv.findContours(thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)  # Find contours
    message_regions = [cv.boundingRect(contour) for contour in contours if cv.boundingRect(contour)[3] > 30]  # Filter and store valid regions
    return sorted(message_regions, key=lambda r: r[1])  # Sort by vertical position

# Normalize Arabic text
def normalize_text(text):
    text = re.sub(r'[ًٌٍَُِّْ]', '', text)  # Remove diacritics
    text = text.replace("أ", "ا").replace("إ", "ا").replace("آ", "ا").replace("ة", "ه").replace("ى", "ي")
    text = unicodedata.normalize('NFKD', text)  # Normalize other forms
    return text

# Clean invisible characters
def clean_invisible_characters(text):
    return re.sub(r'[\u200e\u200f\u202a-\u202e]', '', text)

# Path for saving extracted text and screenshots
text_file_path = "C:\\Users\\inesb\\PycharmProjects\\pythonProject28\\extracted_text.txt"
screenshot_dir = "C:\\Users\\inesb\\PycharmProjects\\pythonProject28\\screenshots"

# Ensure screenshot directory exists
os.makedirs(screenshot_dir, exist_ok=True)

# Capture and extract messages, save screenshots
def capture_and_extract_messages():
    capture_area = get_chatbox_area()
    with mss.mss() as sct:

        screenshot = sct.grab(capture_area)
        img_cv = np.array(screenshot)  # Convert to OpenCV format

         # Sav the screenshot, overwriting the previous one each time
        cv.imwrite(last_screenshot_path, img_cv)


        # Convert image to HSV and detect text colors
        hsv = cv.cvtColor(img_cv, cv.COLOR_BGR2HSV)
        lower_white, upper_white = np.array([0, 0, 200]), np.array([180, 50, 255])
        lower_black, upper_black = np.array([0, 0, 0]), np.array([180, 255, 100])
        white_mask = cv.inRange(hsv, lower_white, upper_white)
        black_mask = cv.inRange(hsv, lower_black, upper_black)
        combined_mask = cv.bitwise_or(white_mask, black_mask)
        img_cv = cv.bitwise_and(img_cv, img_cv, mask=combined_mask)

        # Detect message regions
        message_regions = detect_message_regions(img_cv)
        for region in message_regions:
            x, y, w, h = region
            message_img = img_cv[y:y + h, x:x + w]
            pil_img = Image.fromarray(message_img)  # Convert to PIL
            pil_img = preprocess_image(pil_img)  # Preprocess for OCR

            # Extract and process text
            extracted_text = pytesseract.image_to_string(pil_img, lang='eng+ara')
            normalized_text = normalize_text(extracted_text)
            cleaned_text = clean_invisible_characters(normalized_text)
            single_line_text = ' '.join(cleaned_text.split())

            # Save extracted text to file
            with open(text_file_path, "a", encoding='utf-8') as file:
                file.write(single_line_text + "\n")

# Main function to continuously capture text and check for bad words
def run_text_capture():
    while not bad_word_detected:
        capture_and_extract_messages()
        run_bad_word_check()
        time.sleep(5)  # Wait 5 seconds before capturing again

# Start the text capture and bad word detection
run_text_capture()
