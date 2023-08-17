import time
from linkedIn_constants import LOCATIONS, KEYWORDS, firefoxProfileRootDir
from selenium.webdriver.firefox.options import Options

linkJobUrl = "https://www.linkedin.com/jobs/search/"
jobsPerPage = 25

fast = 2
medium = 3
slow = 10

botSpeed = slow

def browser_options():
    options = Options()
    firefoxProfileRootDir = firefoxProfileRootDir
    options.add_argument("--start-maximized")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-blink-features")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--profile")
    options.add_argument(firefoxProfileRootDir)

    return options

class LinkedinURLGenerator:
    def generate_url_links(self):
        path = []
        for location in LOCATIONS:
            for keyword in KEYWORDS:
                url = linkJobUrl + "?f_AL=true&keywords=" + keyword + "f_JT=F%2CC%2CI" + self.get_location(location) + "&0f_E=2%2C3" + "&f_TPR=r604800" + "&f_SB2=2&" + "&sortBy=DD"
                path.append({"url": url, "keyword": keyword, "location":location})
        return path

    def get_location(self,location):
        if location == "United States":
            return "&geoId=103644278"
        elif location == "Austin, TX":
            return "&geoId=104472865"
        elif location == "Houston, TX":
            return "&geoId=103743442"
        elif location == "Dallas, TX":
            return "&geoId=103743442"
