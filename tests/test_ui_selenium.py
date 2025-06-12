import os
from selenium import webdriver
from selenium.webdriver.common.by import By
import time


def setup_browser():
    """Configure browser differently for local vs CI (GitHub Actions)"""
    options = webdriver.ChromeOptions()

    if os.getenv("CI"):  # Running in GitHub Actions
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        return webdriver.Chrome(options=options)
    else:
        # Local (assumes chromedriver is on PATH)
        return webdriver.Chrome()


def test_invalid_email_shows_error_message():
    driver = setup_browser()
    try:
        driver.get("http://localhost:8000/signup")
        name_input = driver.find_element(By.ID, "name")
        email_input = driver.find_element(By.ID, "email")
        submit_button = driver.find_element(By.TAG_NAME, "button")

        name_input.send_keys("Test User")
        email_input.send_keys("invalid-email")  # not a valid email
        submit_button.click()

        time.sleep(1)  # let the DOM update

        message_div = driver.find_element(By.ID, "message")
        assert message_div.text == ""  # No success message should appear
    finally:
        driver.quit()


def test_blank_password_prevents_submit():
    driver = setup_browser()
    try:
        driver.get("http://localhost:8000/signup")
        name_input = driver.find_element(By.ID, "name")
        email_input = driver.find_element(By.ID, "email")
        submit_button = driver.find_element(By.TAG_NAME, "button")

        name_input.send_keys("Test User")
        email_input.clear()  # leave email blank
        submit_button.click()

        time.sleep(1)
        message_div = driver.find_element(By.ID, "message")
        assert message_div.text == ""  # Should not show success message
    finally:
        driver.quit()


def test_successful_signup_shows_thank_you():
    driver = setup_browser()
    try:
        driver.get("http://localhost:8000/signup")
        name_input = driver.find_element(By.ID, "name")
        email_input = driver.find_element(By.ID, "email")
        submit_button = driver.find_element(By.TAG_NAME, "button")

        name_input.send_keys("Alice Example")
        email_input.send_keys("alice@example.com")
        submit_button.click()

        time.sleep(1)
        message_div = driver.find_element(By.ID, "message")
        assert "Thanks for subscribing" in message_div.text
        assert "Alice Example" in message_div.text
    finally:
        driver.quit()


def test_form_resets_after_submit():
    driver = setup_browser()
    try:
        driver.get("http://localhost:8000/signup")
        name_input = driver.find_element(By.ID, "name")
        email_input = driver.find_element(By.ID, "email")
        submit_button = driver.find_element(By.TAG_NAME, "button")

        name_input.send_keys("Reset Test")
        email_input.send_keys("reset@example.com")
        submit_button.click()

        time.sleep(1)

        # Check that form fields are now empty
        assert name_input.get_attribute("value") == ""
        assert email_input.get_attribute("value") == ""
    finally:
        driver.quit()
