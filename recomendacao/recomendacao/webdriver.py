from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver
from selenium.common.exceptions import WebDriverException


class ExistingSeleniumSession(RemoteWebDriver):
    def __init__(self, session_id=None, **kwargs):
        if session_id is None:
            raise WebDriverException("Session ID can't be None")
        
        super(ExistingSeleniumSession, self).__init__(**kwargs)
        self.session_id = session_id
