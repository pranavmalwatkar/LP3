from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def gmail_login():
    # Initialize Chrome WebDriver
    driver = webdriver.Chrome()
    
    try:
        # Navigate to Gmail login page
        driver.get("https://accounts.google.com/")
        
        # Wait for email field and enter email
        email_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "identifier"))
        )
        email_field.send_keys("pranavmalwatkar142@gmail.com")
        
        # Click Next
        driver.find_element(By.ID, "identifierNext").click()
        
        # Wait for password field and enter password
        password_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "Passwd"))
        )
        password_field.send_keys("password1234")
        
        # Click Next to login
        driver.find_element(By.ID, "passwordNext").click()
        
        # Wait for Gmail to load
        time.sleep(5)
        
        print("Successfully logged into Gmail!")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        
    finally:
        # Keep the browser open for 10 seconds to see the result
        time.sleep(10)
        driver.quit()

if __name__ == "__main__":
    gmail_login()