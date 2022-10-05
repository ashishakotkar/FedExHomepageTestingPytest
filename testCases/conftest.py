import os.path

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

    driver.implicitly_wait(20)
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

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    pytest_html = item.config.pluginmanager.getplugin("html")
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, "extra", [])
    if report.when == "call":
        # always add url to report
        extra.append(pytest_html.extras.url("https://www.fedex.com/en-in/home.html"))
        xfail = hasattr(report, "wasxfail")
        if (report.skipped and xfail) or (report.failed and not xfail):
            # only add additional html on failure
            report_directory = os.path.dirname(item.config.option.htmlpath)
            file_name = report.nodeid.replace("::","_") + ".png"
            destinationFile=os.path.join(report_directory, file_name)
            driver.save_screenshot(destinationFile)
            extra.append(pytest_html.extras.html("<div>Additional HTML</div>"))
        report.extra = extra
        extra.append(pytest_html.extras.text("some string", name="FedEx Homepage Test Automation Report"))
