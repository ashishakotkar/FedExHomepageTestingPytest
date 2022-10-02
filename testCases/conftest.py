import pytest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

from utilities.readProperties import ReadConfig
baseURL = ReadConfig.getApplicationURL()


@pytest.fixture()
def setup(browser):
    global driver
    baseURL = ReadConfig.getApplicationURL()
    if browser=='chrome':
        driver=webdriver.Chrome(ChromeDriverManager().install())
        print("Launching chrome browser.........")
    elif browser=='firefox':
        driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
        print("Launching firefox browser.........")

    driver.implicitly_wait(10)
    # open the URL
    driver.get(baseURL)
    driver.maximize_window()
    yield driver
    driver.close()
def pytest_addoption(parser):    # This will get the value from CLI /hooks
    parser.addoption("--browser")

@pytest.fixture()
def browser(request):  # This will return the Browser value to setup method
    return request.config.getoption("--browser")
