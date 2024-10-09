import threading
from text_capture import run_text_capture
from check_bad_words import ChatBotUI
import sys
import csv
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt

# Event to stop the capture thread when bad word or URL is detected
stop_capture_event = threading.Event()

# Global variable for bad words detection
bad_word_detected = False

# Function to normalize text (you can enhance this depending on your requirements)
def normalize_text(text):
    return text.lower().strip()

# Function to load bad words from a CSV file
def load_bad_words(file_path):
    bad_words_list = []
    with open(file_path, mode='r', encoding='ISO-8859-1', errors='ignore') as file:
        reader = csv.reader(file)
        bad_words_list = [normalize_text(row[0]) for row in reader]  # Assuming bad words are in the first column
    return bad_words_list

# Function to check for bad words in the given text
def check_for_bad_words(text, bad_words):
    normalized_text = normalize_text(text)
    return any(bad_word in normalized_text for bad_word in bad_words)

# Function to check if the text contains URLs
def check_for_urls(text):
    return 'http' in text or 'www' in text

# Function to check for bad words or URLs and stop capture thread if detected
def check_bad_words_or_urls(text, bad_words):
    global bad_word_detected
    if not bad_word_detected:
        words = text.split()
        for word in words:
            normalized_word = normalize_text(word)
            if normalized_word in bad_words or check_for_urls(normalized_word):
                bad_word_detected = True
                stop_capture_event.set()  # Stop the capture thread
                chatbot_app()  # Open chatbot if a bad word or URL is detected
                return True
    return False

# Function to check bad words and URLs after each screenshot
def run_bad_word_check():
    global bad_word_detected
    file_path = 'C:\\Users\\inesb\\PycharmProjects\\pythonProject28\\extracted_text.txt'
    bad_words = load_bad_words('C:\\path\\to\\your\\bad_words_file.csv')

    if not bad_word_detected:
        with open(file_path, 'r', encoding='ISO-8859-1', errors='ignore') as file:
            content = file.read()
            if check_bad_words_or_urls(content, bad_words):
                with open(file_path, 'w') as file:
                    file.write("")  # Clear the file content
                return True
    return False

# Function to capture text continuously and check for bad words/URLs after each screenshot
def start_text_capture():
    while not stop_capture_event.is_set():
        run_text_capture()  # Capture the screenshot and extract text
        if run_bad_word_check():  # Check for bad words/URLs after each capture
            stop_capture_event.set()  # Stop the capture thread if a bad word or URL is detected

# Function to launch the chatbot window
def chatbot_app():
    app = QApplication(sys.argv)
    chatbot = ChatBotUI()
    chatbot.setWindowFlags(chatbot.windowFlags() | Qt.WindowStaysOnTopHint)
    chatbot.show()
    sys.exit(app.exec_())

# Start the capture thread
capture_thread = threading.Thread(target=start_text_capture)
capture_thread.start()

# Run the bad word check periodically
while not stop_capture_event.is_set():
    run_bad_word_check()
