from lib2to3.pgen2 import driver
from loguru import logger

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

def base_driver(drv_url, service_type, options):
    if options:
        options = options.split(",")
        chr_opt = Options()
        
        for opt in options: 
            chr_opt.add_argument("--"+opt)
    else:
        chr_opt = None

    if service_type == "local":
        service = Service(drv_url)
        service.start()
        service_param = service.service_url

    elif service_type == "remote":
        service_param = drv_url
    
    else:
        pass

    try:
        driver = webdriver.Remote(service_param, options=chr_opt)
    except Exception as e:
        logger.error(e)

    return driver    


def kill_driver(session_id, tg_url):
    driver = webdriver.Remote(command_executor=tg_url, desired_capabilities={})
    driver.session_id = session_id
    driver.quit()