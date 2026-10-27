import os
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

PROJECT_ROOT = Path(__file__).resolve().parents[1]
BASE_URL = os.environ.get("APP_BASE_URL", "http://127.0.0.1:5000")


@pytest.fixture(scope="session")
def flask_server():
    """Start the Flask app for the test session and stop it afterwards."""
    env = os.environ.copy()
    env["PYTHONUNBUFFERED"] = "1"
    process = subprocess.Popen(
        [sys.executable, str(PROJECT_ROOT / "app.py")],
        cwd=str(PROJECT_ROOT),
        env=env,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    ready = False
    for _ in range(40):
        if process.poll() is not None:
            break
        try:
            with urllib.request.urlopen(BASE_URL, timeout=1) as response:
                if response.status == 200:
                    ready = True
                    break
        except (urllib.error.URLError, TimeoutError, OSError):
            time.sleep(0.5)
    if not ready:
        process.terminate()
        pytest.fail("Flask app did not start at " + BASE_URL)
    yield BASE_URL
    process.terminate()
    try:
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait(timeout=5)


@pytest.fixture
def driver(flask_server):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1280,900")
    browser = webdriver.Chrome(options=options)
    browser.get(flask_server)
    yield browser
    browser.quit()


def alert_text_and_accept(driver):
    alert = WebDriverWait(driver, 5).until(lambda d: d.switch_to.alert)
    message = alert.text
    alert.accept()
    return message


def test_empty_username(driver):
    driver.find_element(By.NAME, "username").clear()
    driver.find_element(By.NAME, "pwd").send_keys("Password123")
    driver.find_element(By.ID, "sb").click()
    assert alert_text_and_accept(driver) == "Username cannot be empty."


def test_empty_password(driver):
    driver.find_element(By.NAME, "username").send_keys("John Doe")
    driver.find_element(By.NAME, "pwd").clear()
    driver.find_element(By.ID, "sb").click()
    assert alert_text_and_accept(driver) == "Password cannot be empty."


def test_short_password(driver):
    driver.find_element(By.NAME, "username").send_keys("Jane")
    driver.find_element(By.NAME, "pwd").send_keys("abc1")
    driver.find_element(By.ID, "sb").click()
    assert alert_text_and_accept(driver) == "Password must be at least 6 characters long, with at least one number and one letter."


def test_valid_registration(driver):
    driver.find_element(By.NAME, "username").send_keys("Alice")
    driver.find_element(By.NAME, "pwd").send_keys("abc123")
    driver.find_element(By.ID, "sb").click()
    WebDriverWait(driver, 5).until(lambda d: "/submit" in d.current_url)
    message = driver.find_element(By.ID, "welcome-message").text
    assert message == "Hello, Alice! Welcome to the website."
