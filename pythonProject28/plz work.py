from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.chrome.service import Service  # Import the Service class
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

def login_to_messenger(email, password):
    driver = webdriver.Chrome()

# Navigate to Messenger login page
    driver.get('https://www.messenger.com/')

    # Wait for the page to load
    time.sleep(3)

    # Wait until the email input is present and visible
    email_input = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, 'email'))
    )

    # Clear and set the email using JavaScript
    driver.execute_script("arguments[0].value = '';", email_input)  # Clear any existing text
    driver.execute_script("arguments[0].value = 'soumi123456123456@gmail.com';", email_input)  # Set the email
    print(f"Email field set to: {email_input.get_attribute('value')}")  # Log the current value

    # Wait a moment before moving to the password field
    time.sleep(0.5)

    # Wait until the password input is present and visible
    password_input = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.NAME, 'pass'))  # Use the name attribute for better reliability
    )

    # Click on the password input field to ensure focus
    password_input.click()
    time.sleep(0.5)  # Small delay to ensure focus

    # Clear and set the password using JavaScript
    driver.execute_script("arguments[0].value = '';", password_input)  # Clear any existing text
    driver.execute_script("arguments[0].value = 'azerty123456123456';", password_input)  # Set the password
    print(f"Password field set to: {password_input.get_attribute('value')}")  # Log the current value

    # Find and click the login button (ensure the selector is correct)
    login_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.NAME, 'login'))  # Update this based on the button element
    )
    login_button.click()

    # Attendre que la page se charge
    time.sleep(8)

    return driver
def delete_conversations(driver):
    time.sleep(5)  # Allow time for the page to load

    # Locate conversation elements
    conversation_elements = driver.find_elements(By.CLASS_NAME, 'x1lliihq')  # Adjust this class name as needed

    for conversation in conversation_elements:
        try:
            # Scroll into view if necessary
            driver.execute_script("arguments[0].scrollIntoView(true);", conversation)

            # Click the specific button represented by the path
            button = conversation.find_element(By.XPATH, ".//path[@d='M12.5 18A2.25 2.25 0 1 1 8 18a2.25 2.25 0 0 1 4.5 0zM20.25 18a2.25 2.25 0 1 1-4.5 0 2.25 2.25 0 0 1 4.5 0zM25.75 20.25a2.25 2.25 0 1 0 0-4.5 2.25 2.25 0 0 0 0 4.5z']")  # Adjust the XPath as necessary
            driver.execute_script("arguments[0].click();", button)  # Click using JavaScript

            time.sleep(1)  # Wait for the options to load

            # Wait for the delete option to be visible and click it
            delete_option = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Supprimer la discussion')]"))
            )
            delete_option.click()

            # Confirm deletion if necessary
            confirm_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Confirmer')]"))  # Adjust this text
            )
            confirm_button.click()

            print("Conversation deleted.")
        except Exception as e:
            print(f"Error while deleting conversation: {e}")

        time.sleep(2)  # Delay between deletions




def main():
    email = "your-email@example.com"  # Replace with your email
    password = "your-password"  # Replace with your password

    driver = login_to_messenger(email, password)
    delete_conversations(driver)
    driver.quit()

if __name__ == "__main__":
    main()
