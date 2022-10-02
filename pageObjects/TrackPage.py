import time
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common import keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from datetime import datetime, timedelta
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains


class TrackPage:
    pop_up_close_xpath = "//a[text()='X']"
    button_track_putple_xpath = "//*[@aria-label='Get Tracking Information']"
    button_track_orange_xpath = "//button[@type='submit' and @id='btnSingleTrack']"
    textbox_trk_id_xpath = "//input[@id='trackingnumber']"
    message_duplicate_xpath = "//div/h1[@class='wtrk_header']"
    link_trk_no_xpath = "//a[contains(text(),'111111111111')]"
    dup_rows_xpath = "//table/tbody/tr"
    table_column_headers_xpath = "//table/thead/tr/th"

    # Initializing the driver using the constructor
    # the driver is passed from test cases class to page object class
    # this diver is then used to perform action on the above elements
    def __init__(self, driver):
        self.driver = driver

    def setFromAddress(self, FromAddress):
        self.driver.find_element("xpath", self.textbox_origin_xpath).clear()
        self.driver.find_element("xpath", self.textbox_origin_xpath).send_keys(FromAddress)

    def setToAddress(self, toAddress):
        self.driver.find_element("xpath", self.textbox_dest_xpath).clear()
        self.driver.find_element("xpath", self.textbox_dest_xpath).send_keys(toAddress)

    def clickSuggestionFrom(self, fromAddress):
        WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//strong[.='"+fromAddress+"']"))).click()
        # self.driver.find_element("//span[.='Chicago, IL 60612, United States']")


    def clickSuggestionTo(self):
        WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//span[@class='fdx-u-font-size--default']"))).click()

    def clickRateTransitBtn(self):
        self.driver.find_element("xpath", self.button_rate_transit_times_xpath).click()

    def clickCloseOnPopup(self):
        self.driver.find_element("xpath", self.pop_up_close_xpath).click()

    def clickContinueBtn(self):
        WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, self.continue_button_xpath))).click()

    def getTextOfShpResiChkBox(self):
        text1 = self.driver.find_element("xpath", self.ship_to_resi_chkbox_xpath).text
        print("printing value of text1: " + text1)
        return text1

    def getAddCoverNoRadioBtnStatus(self):
        status = self.driver.find_element("xpath", self.add_cover_no_radio_btn_xpath).is_selected()
        return status

    def getItemsInPkgDrpdown(self):
        pkg_options = [element.text for element in self.driver.find_elements("xpath", self.pkg_dropdown_xpath)]
        return pkg_options

    def setWgt(self, wgt):
        self.driver.find_element("xpath", self.wgt_per_pkg_xpath).clear()
        self.driver.find_element("xpath", self.wgt_per_pkg_xpath).send_keys(wgt)

    def clickShowRates(self):
        WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, self.show_rates_btn_xpath))).click()

    def clickExpandRates(self):
        WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, self.expand_rates_btn_xpath))).click()

    def getRatesList(self):
        rates_list = [element.text for element in self.driver.find_elements("xpath", self.rates_list_xpath)]
        return rates_list

    def selPkgType(self, pkgType):
        select = Select(self.driver.find_element("xpath", self.pkg_dropdown_xpath))
        select.select_by_visible_text(pkgType)

    def clickAddPkg(self):
        WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, self.add_pkg_link_xpath))).click()

    def clickShpResiChkBox(self):
        WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, self.ship_to_resi_chkbox_xpath))).click()

    def getTodaysDateXpath(self):
        # Get today's date
        presentday = datetime.now()
        # # strftime() is to format date according to
        # # the need by converting them to string
        today = presentday.strftime('X%d %B, %Y').replace('X0','X').replace('X','')
        return "//*[contains(text(),'" + today + "')]"

    def getTomorrowDateXpath(self):
        # Get today's date
        presentday = datetime.now()  # or presentday = datetime.today()
        # # strftime() is to format date according to
        # # the need by converting them to string
        today = presentday.strftime('%d %B,%Y')
        # Get Tomorrow
        nextday = presentday + timedelta(1)
        tomorrow = nextday.strftime('X%d %B, %Y').replace('X0','X').replace('X','')
        return "//*[contains(text(),'" + tomorrow + "')]"

    def enterOrigDestDetails(self, fromAddress, toAddress):
        # self.rtp = RateTransitPage(self.driver)
        self.clickCloseOnPopup()
        # self.clickUkEngChkBox()
        # self.clickAcceptCookies()
        self.clickRateTransitBtn()
        self.setFromAddress(fromAddress)
        self.clickSuggestionFrom(fromAddress)
        time.sleep(3)
        self.setToAddress(toAddress)
        self.clickSuggestionTo()

    def clickUkEngChkBox(self):
        WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, self.uk_eng_btn_xpath))).click()

    def clickAcceptCookies(self):
        WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, self.accept_cookies_btn_xpath))).click()

    def clickTrackButton(self):
        self.driver.find_element("xpath", self.track_button_xpath).click()
