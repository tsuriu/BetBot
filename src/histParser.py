from selenium.webdriver.common.by import By
import os

from .modules.misc import datetime_formater
from .modules.scrapper_utils import double_element_parser
from .modules.scrapper_base import base_driver, kill_driver


def init_scrapper(endpoint=None, lookup_class=None):
    srvurl = os.environ.get("SELENIUM_URL")
    options = os.environ.get("SELENIUM_BROWSER_OP")
    service_type = os.environ.get("SELENIUM_SRV_TYPE")

    driver = base_driver(srvurl, service_type, options)
    driver.get("".format(os.environ.get("HISTORY_BASE_URL"),endpoint))

    elements = driver.find_elements(By.CLASS_NAME, lookup_class)

    parsed_elements = globals()[endpoint](elements)

    driver.quit()

    return parsed_elements


def doubles(elements):

    last_entrances = []

    for el in elements:
        bet_id = int(el.get_attribute("data-id"))

        el = el.find_element(By.CLASS_NAME, "sm-box")
        el_html = el.get_attribute("data-bs-content")

        entrance = double_element_parser(el_html)
        entrance["b_id"] = bet_id

        last_entrances.append(entrance)

    return last_entrances


def crashes(elements):    

    last_entrances = []

    for el in elements:
        crash_el = {}

        status = ((el.get_attribute("class")).split(" "))[1]
        datetime_str = (((el.get_attribute("data-bs-original-title")).split(" "))[0::2])[:-1]

        crash_value = el.get_attribute("innerText")

        crash_el["status"] = status
        crash_el["date"] = datetime_str[0]
        crash_el["datetime"] = " ".join(datetime_str)
        crash_el["timestamp"] = datetime_formater(crash_el["datetime"])
        crash_el["crash"] = float(crash_value.replace("X",""))
        crash_el["b_id"] = "".join([status,str(crash_el["timestamp"]),crash_value])

        last_entrances.append(crash_el)

    return last_entrances