import os
import io
import sys
import time

from pathlib import Path

from selenium import webdriver
from PIL import Image

# Use the following lot for headless environments:
from selenium.webdriver import FirefoxOptions
from selenium.webdriver.common.by import By


def get_driver():
    opts = FirefoxOptions()
    if os.name == 'nt':
        driver = webdriver.Firefox(options=opts)
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
    hrefs = [x.get_attribute("href") for x in articles]
    titles = [x.text for x in articles]

    for href, title in zip(hrefs, titles):
        print(title)
        print(f"Getting {href}")
        driver.get(href)
        # Try and not get Fail2Banned
        time.sleep(10)
        save_name = href.split("/")[-1] + ".webp"
        screencap(driver, f"{archive_dir}/{save_name}")


def main(driver, archive_name):
    try:
        browse(driver, archive_name)
    finally:
        driver.close()
        driver.quit()


if __name__ == "__main__":
    main(get_driver(), sys.argv[1])
