import datetime
import os
import io
import sys

import pytest
from pathlib import Path

from selenium import webdriver
from PIL import Image

# Use the following lot for headless environments:
from selenium.webdriver import FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service


def get_driver():
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


def screencap(driver, save_name):
    screeny = io.BytesIO(driver.get_screenshot_as_png())
    image = Image.open(screeny)
    image.save(save_name)


def browse(driver, archive_dir: str):
    driver.implicitly_wait(10)
    driver.get("https://silverbullets.co.uk")
    articles = driver.find_elements(By.XPATH, '//article//header/h2/a')

    Path(archive_dir).mkdir(parents=True, exist_ok=True)
    screencap(driver, f"{archive_dir}/homepage.webp")
    for artic in articles:
        print(artic.text)

    for artic in articles:
        print(f"Getting {artic.href}")
        driver.get(artic.href)
        save_name = artic.href.split("/")[-1].replace(".md", ".webp")
        screencap(driver, f"{archive_dir}/{save_name}")


def main(driver, archive_name):
    try:
        browse(driver, archive_name)
    finally:
        driver.close()
        driver.quit()


if __name__ == "__main__":
    main(get_driver(), sys.argv[1])