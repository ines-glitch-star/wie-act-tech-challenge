import sys
import time
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import Qt
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

class URLScannerApp(QtWidgets.QWidget):
    def __init__(self, url):
        super().__init__()

        self.setWindowTitle("URL Scanner")
        self.setGeometry(100, 100, 800, 700)
        self.setStyleSheet("background-color: #FFC0CB;")

        # Layout
        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)

        # Title
        self.title = QtWidgets.QLabel("URL Scanner")
        self.title.setFont(QtGui.QFont("Arial", 28, QtGui.QFont.Bold))
        self.title.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.title)

        # Processing label
        self.processing_label = QtWidgets.QLabel("Please wait, we are processing...")
        self.processing_label.setFont(QtGui.QFont("Arial", 16))
        self.processing_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.processing_label)

        # Progress bar
        self.progress_bar = QtWidgets.QProgressBar(self)
        self.progress_bar.setRange(0, 0)
        self.layout.addWidget(self.progress_bar)

        # Extracted text area
        self.result_area = QtWidgets.QTextBrowser()
        self.result_area.setFontPointSize(18)
        self.result_area.setStyleSheet("background-color: white; border: 1px solid #CCC; padding: 20px;")
        self.layout.addWidget(self.result_area)

        # Start the scanning process with a provided URL
        self.scan_url(url)

    def scan_url(self, url):
        self.thread = ScanThread(url)
        self.thread.result_ready.connect(self.display_result)
        self.thread.start()

    def display_result(self, extracted_text):
        self.processing_label.setVisible(False)
        self.progress_bar.setVisible(False)

        # Check if the URL is safe
        if "Safe" in extracted_text:
            safe_icon = """
            <div style="text-align: center; margin-bottom: 20px;">
                <img src="C:\\Users\\inesb\\PycharmProjects\\pythonProject28\\safe.png" alt="Safe URL" width="500" height="300" />
                <h2 style="color: green;">Safe URL</h2>
            </div>
            """
            extracted_text = extracted_text.replace("safe", "<span style='color: green; font-weight: bold;'>safe</span>")
        else:
            safe_icon = ""

        if "Parked Domain" in extracted_text:
            extracted_text = extracted_text.split("Parked Domain")[0]

        styled_text = f"""
        <style>
            .container {{
                background-color: white;
                border-radius: 20px;
                padding: 25px;
                margin: 20px;
                border: 3px solid #28a745;
                font-size: 22px;
                text-align: center;
                box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);
            }}
            .highlight {{
                color: #FF5733;
                font-weight: bold;
                text-shadow: 1px 1px 5px #FF5733;
            }}
            h3 {{
                color: #333;
                font-size: 26px;
                margin-bottom: 18px;
            }}
        </style>
        {safe_icon}
        <div class="container">
            <div>{extracted_text}</div>
        </div>
        """
        self.result_area.setHtml(styled_text)

class ScanThread(QtCore.QThread):
    result_ready = QtCore.pyqtSignal(str)

    def __init__(self, url):
        super().__init__()
        self.url = url

    def run(self):
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        driver.minimize_window()

        try:
            driver.get("https://www.ipqualityscore.com/threat-feeds/malicious-url-scanner")
            url_input = driver.find_element(By.ID, "url")
            url_input.send_keys(self.url)
            time.sleep(1)
            url_input.send_keys(Keys.RETURN)
            time.sleep(5)

            target_section = driver.find_element(By.CSS_SELECTOR, "body > section.hero.hero-gradient1.valign > div.container.target2 > div:nth-child(1) > div > div.ip-lookup-report-wrapper")
            driver.execute_script("arguments[0].scrollIntoView(true);", target_section)
            time.sleep(1)

            extracted_text = target_section.get_attribute('innerHTML')
            self.result_ready.emit(extracted_text)

        finally:
            driver.quit()


