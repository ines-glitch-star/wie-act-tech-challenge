import sys
import csv
import re
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton, QLabel, QScrollArea, QFrame
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QTimer
from predic import URLScannerApp  # Import the URL scanner app
import subprocess  # To run test.py and get URL output
from test import extract_and_save_blue_mask, preprocess_image_for_ocr, extract_text_from_image, clean_extracted_text


# Global variable to detect bad words
bad_word_detected = False

class ChatBotUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Friendly Chatbot")
        self.setFixedSize(400, 700)

        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Background frame
        background_frame = QFrame(self)
        background_frame.setStyleSheet("background-color: black")
        main_layout.addWidget(background_frame)

        # Chat area
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.chat_widget = QWidget()
        self.chat_layout = QVBoxLayout(self.chat_widget)
        self.chat_layout.setAlignment(Qt.AlignTop)
        self.chat_widget.setLayout(self.chat_layout)
        self.scroll_area.setWidget(self.chat_widget)
        self.scroll_area.setStyleSheet("background-color: #F4C2C2; border: none;")
        main_layout.addWidget(self.scroll_area)

        # Input field and send button
        input_layout = QHBoxLayout()
        self.text_input = QTextEdit(self)
        self.text_input.setFixedHeight(60)
        self.text_input.setStyleSheet("""
            background-color: #FFFFFF;
            border-radius: 25px;
            padding: 15px;
            font-size: 16px;
        """)
        send_button = QPushButton("Send", self)
        send_button.setStyleSheet("""
            background-color: #F76363;
            color: white;
            border-radius: 25px;
            padding: 18px;
            font-size: 16px;
        """)
        send_button.clicked.connect(self.send_message)
        input_layout.addWidget(self.text_input)
        input_layout.addWidget(send_button)
        main_layout.addLayout(input_layout)

        # Start greeting message
        QTimer.singleShot(1000, self.start_greeting_message)

    def start_greeting_message(self):

        messages = [
            "Hey there! 👋 I sensed something... ✨"
            "Negativity? Pfft. It’s got nothing on you you shoudn't listen to her . 💥",
            "Let’s spread good vibes only! 🎉",
            "Now, how do you feel? 😎"
        ]
        self.delayed_bot_response(messages)



    def check_initial_bad_words_and_links(self):
        file_path = 'C:\\Users\\inesb\\PycharmProjects\\pythonProject28\\extracted_text.txt'
        with open(file_path, 'r', encoding='ISO-8859-1', errors='ignore') as file:
            user_message = file.read()

        if self.check_for_bad_words(user_message):
            self.add_chat_bubble("I see that someone isn't being very nice to you! 😔", "bot")
        elif self.check_for_links(user_message):
            self.add_chat_bubble("Ohh, I see a link was sent to you! 🔗", "bot")
            self.add_chat_bubble("Do you trust that person, or should I analyze it for you?", "bot")
            self.text_input.setPlaceholderText("Type 'yes' to analyze or 'no need' to ignore...")

    def send_message(self):
        user_message = self.text_input.toPlainText().strip()
        if user_message:
            self.add_chat_bubble(user_message, "user")
            self.text_input.clear()
            self.process_bot_message(user_message)

    def process_bot_message(self, user_message):
        if hasattr(self, 'awaiting_url') and self.awaiting_url:
            if self.is_valid_url(user_message):
                self.add_chat_bubble("It is a valid link. I will analyze it for you! 🔗", "bot")
                self.launch_url_scanner(user_message)
                return  # Prevent further message processing once a valid URL is detected
            else:
                self.add_chat_bubble("That doesn't look like a valid URL. Can you provide a valid one? 😊", "bot")
        elif self.check_for_bad_words(user_message):
            self.add_chat_bubble("I see that someone isn't being very nice to you! 😔", "bot")
        elif self.check_for_links(user_message):
            if not hasattr(self, 'awaiting_url'):
                self.add_chat_bubble("Ohh, I see a link was sent to you! 🔗", "bot")
                self.add_chat_bubble("Do you trust that person, or should I analyze it for you?", "bot")
                self.text_input.setPlaceholderText("Type 'yes' to analyze or 'no need' to ignore...")
        elif user_message.lower() == "yes":
            self.add_chat_bubble("Copy and paste the link sent to you:", "bot")
            self.awaiting_url = True  # Now expect a URL in the next message
        else:
            bot_message = self.chatbot_response(user_message)
            self.add_chat_bubble(bot_message, "bot")

    def is_valid_url(self, message):
        import re
        # Simple regex for URL validation
        url_regex = re.compile(r'^(https?|ftp):\/\/[^\s/$.?#].[^\s]*$', re.IGNORECASE)
        return re.match(url_regex, message)

    def launch_url_scanner(self, url):
        self.add_chat_bubble(f"Analyzing the URL: {url} 🔍", "bot")
        self.url_scanner_window = URLScannerApp(url)
        self.url_scanner_window.setWindowModality(Qt.NonModal)  # Allow both windows to be active
        self.url_scanner_window.show()



    def check_for_bad_words(self, text):
        bad_words = ['badword1', 'badword2']
        return any(bad_word in text for bad_word in bad_words)

    def check_for_links(self, text):
        return 'http' in text or 'www' in text

    def add_chat_bubble(self, message, sender):
        bubble_layout = QHBoxLayout()
        bubble_layout.setAlignment(Qt.AlignLeft if sender == "bot" else Qt.AlignRight)

        icon_label = QLabel(self)
        if sender == "bot":
            icon_label.setPixmap(QPixmap("botg.png").scaled(40, 40, Qt.KeepAspectRatio))
        else:
            icon_label.setPixmap(QPixmap("user.png").scaled(40, 40, Qt.KeepAspectRatio))

        text_label = QLabel(message)
        text_label.setWordWrap(True)
        text_label.setStyleSheet(f"""
            background-color: {"#FF5C5C" if sender == "bot" else "#E3A1A1"};
            color: white;
            border-radius: 15px;
            padding: 10px 20px;
            max-width: 600px;
            font-size: 16px;
            margin-bottom: 20px;
        """)

        if sender == "bot":
            bubble_layout.addWidget(icon_label)
            bubble_layout.addWidget(text_label)
        else:
            bubble_layout.addWidget(text_label)
            bubble_layout.addWidget(icon_label)

        self.chat_layout.addLayout(bubble_layout)
        self.chat_widget.adjustSize()
        self.scroll_area.verticalScrollBar().setValue(self.scroll_area.verticalScrollBar().maximum())


# Main application entry point
if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Create and show the chatbot window
    chatbot_window = ChatBotUI()
    chatbot_window.setWindowFlags(chatbot_window.windowFlags() | Qt.WindowStaysOnTopHint)
    chatbot_window.show()

    # Optionally, create and show another widget (like URL scanner)
    # Example: Uncomment to open the URLScannerApp (replace 'example_url' with actual URL)
    # url_scanner_window = URLScannerApp('example_url')
    # url_scanner_window.show()

    sys.exit(app.exec_())


# Load bad words from CSV
def load_bad_words():
    file_path = 'C:\\Users\\inesb\\PycharmProjects\\pythonProject24\\bad_commentsdetection.csv'
    bad_words_list = []
    # Use 'ISO-8859-1' encoding and ignore errors during reading
    with open(file_path, mode='r', encoding='ISO-8859-1', errors='ignore') as file:
        reader = csv.reader(file)
        bad_words_list = [normalize_text(row[0]) for row in reader]  # Normalize bad words
    return bad_words_list


# Normalize Arabic text (removing diacritics and normalizing characters)
def normalize_text(text):
    # Remove diacritics and normalize specific characters
    text = re.sub(r'[ًٌٍَُِّْ]', '', text)  # Remove Arabic diacritics
    text = text.replace("أ", "ا").replace("إ", "ا").replace("آ", "ا")  # Normalize Alif variations
    text = text.replace("ة", "ه")  # Normalize Ta Marbuta
    text = text.replace("ى", "ي")  # Normalize Alif Maqsura
      # Further normalization to decompose characters
    return text


# Function to check for bad words in the text
import re

# Function to check for bad words and links in the text
def check_bad_words(text, bad_words):
    global bad_word_detected
    if not bad_word_detected:
        words = text.split()

        # Check for bad words
        for word in words:
            normalized_word = normalize_text(word)
            if normalized_word in bad_words:
                bad_word_detected = True
                chatbot_app()  # Open chatbot if a bad word is detected
                return True

        # Regex pattern to detect URLs
        url_pattern = r'(https?://\S+|www\.\S+|\S+\.com)'

        # Check for links
        if re.search(url_pattern, text):
            bad_word_detected = True
            chatbot_app()  # Open chatbot if a link is detected
            return True

    return False




# Function to launch the chatbot window
def chatbot_app():
    app = QApplication(sys.argv)
    chatbot = ChatBotUI()
    chatbot.setWindowFlags(chatbot.windowFlags() | Qt.WindowStaysOnTopHint)
    chatbot.show()
    sys.exit(app.exec_())


# Function to read and check the file for bad words
def run_bad_word_check():
    global bad_word_detected
    file_path = 'C:\\Users\\inesb\\PycharmProjects\\pythonProject28\\extracted_text.txt'
    bad_words = load_bad_words()

    if not bad_word_detected:
        # Use 'ISO-8859-1' encoding and ignore errors during reading
        with open(file_path, 'r', encoding='ISO-8859-1', errors='ignore') as file:
            content = file.read()
            if check_bad_words(content, bad_words):
                with open(file_path, 'w') as file:
                    file.write("")
                return True
    return False


# Run the bad word check
run_bad_word_check()
