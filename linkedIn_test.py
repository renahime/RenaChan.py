import os, time, sys

from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from make_logger import initialize_logger

logger = initialize_logger()

logger.info("Testing Linkedin Login")

def check_python():
    try:
        if sys.version:
            logger.info("Python is installed")
        else:
            logger.error("Python is not installed, please install Python: https://www.python.org/downloads/")
    except Exception as e:
        logger.error(e)

def check_pip():
    try:
        import pip
        logger.info("Pip is installed")
    except ImportError:
        logger.error("Pip is not installed. Install Pip: https://pip.pypa.io/en/stable/installation/")

def check_selenium():
    try:
        import selenium
        logger.info("Selenium is installed!")
    except ImportError:
        logger.error("Selenium is not installed. Install Selenium: https://pypi.org/project/selenium/")

def check_connection():
    try:
        ip = "no"
        firefox_driver = webdriver.Remote(
            command_executor=f'http://{ip}:4444/wd/hub',
            desired_capabilities={'browserName': 'firefox'}
        )
        firefox_driver.get('https://renahime.github.io/')
        if firefox_driver.execute_script('return document.readyState') != 'complete':
            raise Exception('Page did not load completely')
        firefox_driver.quit()
    except ImportError as e:
        logger.error(e)

def checkSeleniumLinkedIn():

    options = Options()
    options
    options.add_argument("--ignore-certificate-errors")
    options.add_argument('--no-sandbox')
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-blink-features")
    options.add_argument("--disable-blink-features=AutomationControlled")

    browser = webdriver.Chrome(options=options)

    try:
        browser.get("https://renahime.github.io/")
        if (browser.title.index("welcome")>-1):
            logger.info("Selenium and geckodriver are working")
        else:
            logger.error("Please check if selenium and gekodriver are installed")
    except Exception as e:
        logger.error(e)
    try:
        browser.get('https://www.linkedin.com/feed/')
        time.sleep(3)
        if "Feed" in browser.title:
            logger.info('Successfully you are logged in to Linkedin, it is available to use!')
        else:
            logger.error('You are not automatically logged in, please set up your chrome correctly.')
    except Exception as e:
        logger.error(e)
    finally:
        browser.quit()

check_python()
check_pip()
check_selenium()
check_connection()
checkSeleniumLinkedIn()
