import time,math,random,os
import platform
from .linkedIn_utils import browser_options, LinkedinURLGenerator
import renachan.managers.models as models
from .database_helpers import add_to_database

from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver.firefox.options import Options


class Linkedin_Bot:
    def __init__(self):
        self.driver=webdriver.Firefox(options=browser_options())

    def generate_urls(self):
        url_obj = LinkedinURLGenerator.generate_url_links()

        for obj in url_obj:
            query = bot.db.query(models.LinkedInUrls).filter_by(url=obj["url"]).first()
