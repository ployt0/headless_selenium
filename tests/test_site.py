import pytest
# Use the following lot for headless environments:
from selenium.webdriver.common.by import By

from cap_site import get_driver


@pytest.fixture
def driver():
    return get_driver()


def test_site(driver):
    try:
        driver.implicitly_wait(10)
        driver.get("https://silverbullets.co.uk")
        driver.find_element(By.XPATH, '//article//header/h2/a').click()
        assert driver.find_elements(By.CSS_SELECTOR, "div .col-md-8")[0].text.strip().startswith("Published 20")
    finally:
        driver.close()
        driver.quit()
