# 浏览器的类型（chrome,ie,firefox,edge,opera）
# 浏览器的启动参数（无头化，最大化，尺寸化）
# 浏览器的属性（显示尺寸,隐式等待/页面加载/js执行时间）

from selenium.webdriver import *
from typing import Type,Union


class BrowserTypeError(Exception):

    def __init__(self, _type):
        self._type = _type

    def __str__(self):
        return f'unsupported browser type: {self._type}'


class BROWSER:

    CHROME_DRIVER_PATH = '../drivers/chrome_driver.exe'
    EDGE_DRIVER_PATH = '../drivers/edge_driver.exe'
    FIREFOX_DRIVER_PATH = '../drivers/gecko_driver.exe'
    IE_DRIVER_PATH = '../drivers/IEDriverServer.exe'
    OPERA_DRIVER_PATH = '../drivers/opera_driver.exe'

    WINDOWS_SIZE = (1024, 768)

    IMP_TIME = 30

    PAGE_LOAD_TIME = 20

    SCRIPT_TIME_OUT = 20

    HEADLESS = True

    def __init__(self, browser_type: Type[Union[Firefox, Chrome, Ie, Edge, Opera]] = Chrome,
                 option_type: Type[Union[FirefoxOptions, ChromeOptions, IeOptions]] = ChromeOptions,
                 driver_path: str = CHROME_DRIVER_PATH):
        if not issubclass(browser_type, (Firefox, Chrome, Ie, Edge, Opera)):
            raise BrowserTypeError(browser_type)
        if not issubclass(option_type, (FirefoxOptions, ChromeOptions, IeOptions)):
            raise BrowserTypeError(option_type)
        if not isinstance(driver_path, str):
            raise TypeError
        self._path = driver_path
        self._browser = browser_type
        self._option = option_type

    @property
    def options(self):
        """
        浏览器特定的操作，在子类中实现
        :return:
        """
        return

    @property
    def browser(self):
        """
        启动浏览器，返回浏览器实例
        :return:
        """
        return


class CHROME(BROWSER):

    OPTION_MARK = True

    METHOD_MARK = True

    HEADLESS = False

    IMP_TIME = 30

    PAGE_LOAD_TIME = 30

    SCRIPT_TIME_OUT = 30

    WINDOWS_SIZE = (1920, 900)

    START_MAX = '--start-maximized'

    EXP = {
        'excludeSwitches': ['enable-automation'],
        'mobileEmulation': {'deviceName': 'iPhone 6'}
    }

    @property
    def options(self):
        if self.OPTION_MARK:
            chrome_option = self._option()
            chrome_option.add_argument(self.START_MAX)
            for k, v in self.EXP.items():
                chrome_option.add_experimental_option(k, v)
            chrome_option.headless = self.HEADLESS
            return chrome_option
        return None

    @property
    def browser(self):
        if self.options:
            chrome = self._browser(self._path, options=self.options)
        else:
            chrome = self._browser(self._path)

        if self.METHOD_MARK:
            chrome.implicitly_wait(self.IMP_TIME)
            chrome.set_script_timeout(self.SCRIPT_TIME_OUT)
            chrome.set_page_load_timeout(self.PAGE_LOAD_TIME)
            # chrome.set_window_size(*self.WINDOWS_SIZE)
        return chrome


with CHROME().browser as _chrome:
    _chrome.get('http://127.0.0.1/zentao/user-login.html')
    from time import sleep
    sleep(3)


class IE(BROWSER):

    CLEAN_SESSION = True

    def __init__(self):
        super(IE, self).__init__(
            browser_type=Ie,
            option_type=IeOptions,
            driver_path=super().IE_DRIVER_PATH
        )

    @property
    def options(self):
        ie_option = self._option()
        ie_option.ensure_clean_session = self.CLEAN_SESSION
        return ie_option

    @property
    def browser(self):
        ie = self._browser(self._path, options=self.options)
        ie.implicitly_wait(self.IMP_TIME)
        ie.set_page_load_timeout(self.PAGE_LOAD_TIME)
        ie.set_script_timeout(self.SCRIPT_TIME_OUT)
        ie.maximize_window()
        return ie


with IE().browser as _ie:
    _ie.get('http://127.0.0.1/zentao/user-login.html')
    from time import sleep
    sleep(5)