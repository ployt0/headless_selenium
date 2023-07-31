import os
import pytest

from selenium import webdriver

# Use the following lot for headless environments:
from selenium.webdriver import FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service


@pytest.fixture
def driver():
    opts = FirefoxOptions()
    if os.name == 'nt':
        # todo This'll need adjusting per user to run locally.
        # Hardcode your firefox path here. like "AppData\Local\Mozilla Firefox\firefox.exe".
        # I don't know what shell you use in Windows.
        opts.binary_location = r"C:\Program Files\Mozilla Firefox\firefox.exe"
        service = Service(r"C:\geckodriver.exe")  # Or wherever you keep it.
        driver = webdriver.Firefox(service=service, options=opts)
    else:
        opts.add_argument("--headless")
        driver = webdriver.Firefox(options=opts)
    return driver


def test_site(driver):
    try:
        driver.implicitly_wait(10)
        driver.get("https://silverbullets.co.uk")
        driver.find_element(By.XPATH, '//article//header/h2/a').click()
        assert driver.find_elements(By.CSS_SELECTOR, "div .col-md-8")[0].text.strip().startswith("Published 20")
    finally:
        driver.close()
        driver.quit()
