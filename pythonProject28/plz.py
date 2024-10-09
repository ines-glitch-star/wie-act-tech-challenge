from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def initialize_driver():
    driver = webdriver.Chrome()  # Ensure you have the correct WebDriver for your browser version
    return driver

def login_to_messenger(driver, email, password):
    driver.get('https://www.messenger.com/')
    time.sleep(3)

    try:
        email_input = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, 'email'))
        )
        email_input.clear()
        email_input.send_keys(email)

        password_input = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.NAME, 'pass'))
        )
        password_input.clear()
        password_input.send_keys(password)

        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.NAME, 'login'))
        )
        login_button.click()
        time.sleep(5)

    except Exception as e:
        print(f'Error during login: {e}')

def delete_conversation(driver):
    print('Deleting conversation...')
    try:
        # Step 1: Click on the "More options" (three dots) button
        more_options_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[aria-label="Menu"]'))
        )
        more_options_button.click()
        time.sleep(0.25)  # Wait for the menu to open

        # Step 2: Click on "Supprimer la discussion" (Delete Conversation)
        delete_option = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//span[text()="Supprimer la discussion"]'))
        )
        delete_option.click()
        time.sleep(5) # Wait for confirmation dialog to appear

        # Step 3: Confirm the delete action
        confirm_delete_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//em[text()="Supprimer"]'))
        )
        confirm_delete_button.click()
        print("Conversation deleted successfully.")

    except Exception as e:
        print(f'Error while deleting conversation: {e}')


if __name__ == "__main__":
    email = 'soumi123456123456@gmail.com'  # Replace with your email
    password = 'azerty123456123456'  # Replace with your password

    driver = initialize_driver()
    # Log into Messenger
    login_to_messenger(driver, email, password)

    # Call the function to delete a conversation
    delete_conversation(driver)

    driver.quit()  # Close the browser once done
