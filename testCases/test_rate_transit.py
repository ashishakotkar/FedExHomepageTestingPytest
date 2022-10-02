import time

import pytest
import json
from pageObjects.RateTransitPage import RateTransitPage
from utilities.readProperties import ReadConfig
from utilities.customLogger import LogGen


# import logging


class TestRateTransitTimes:
    baseURL = ReadConfig.getApplicationURL()

    logger = LogGen.loggen()

    datafile = open("TestData/rate_transit_data.json")
    data = json.load(datafile)

    # setup is method in conftest file that returns driver instance

    @pytest.mark.regression
    def test_001_homepage_title(self, setup):

        self.logger.info("**************Test_001_Verifying Homepage Title*************************")
        expected_title = (self.data["TC1"]["title"])
        self.driver = setup
        self.rtp = RateTransitPage(self.driver)
        self.rtp.clickCloseOnPopup()
        actual_title = self.driver.title
        assert actual_title == expected_title, f'Error.Expected text:{expected_title}, but actual text: {actual_title}'

    # what this test case do?
    @pytest.mark.regression
    def test_002_todays_dt_available_shpdtdrpdwn(self, setup):

        from_address = (self.data["TC2"]["fromAddress"])
        to_address = (self.data["TC2"]["toAddress"])

        self.logger.info("**************test_002_verifyTodaysDtAvailableShpDtDrpdwn*************************")
        self.driver = setup
        self.rtp = RateTransitPage(self.driver)
        self.rtp.enterOrigDestDetails(from_address, to_address)
        print("printing from test case: " + self.rtp.getTodaysDateXpath())

        date_attrib = self.driver.find_element("xpath", (self.rtp.getTodaysDateXpath() + "/parent::*"))
        date_attrib_id = date_attrib.get_attribute('id')
        assert date_attrib_id == "packageShipDate", f"today's date is not available in the dropdown"

    @pytest.mark.regression
    def test_003_tomm_dt_available_shpdtdrpdwn(self, setup):
        from_address = (self.data["TC3"]["fromAddress"])
        to_address = (self.data["TC3"]["toAddress"])

        self.driver = setup
        self.rtp = RateTransitPage(self.driver)
        self.rtp.enterOrigDestDetails(from_address, to_address)
        print("printing from test case: " + self.rtp.getTomorrowDateXpath())

        date_attrib = self.driver.find_element("xpath", self.rtp.getTomorrowDateXpath() + "/parent::*")
        date_attrib_id = date_attrib.get_attribute('id')
        assert date_attrib_id == "packageShipDate", f"tomorrows's date is not available in the dropdown"

    @pytest.mark.regression
    @pytest.mark.sanity
    def test_004_default_additional_cover_btn_val(self, setup):

        from_address = (self.data["TC4"]["fromAddress"])
        to_address = (self.data["TC4"]["toAddress"])
        self.driver = setup
        self.rtp = RateTransitPage(self.driver)
        self.rtp.enterOrigDestDetails(from_address, to_address)
        status = self.rtp.getAddCoverNoRadioBtnStatus()
        assert status, f"'No' radio button is not enabled"

    @pytest.mark.regression
    def test_005_items_in_pkg_dropdown(self, setup):
        # should be out of the test case and called from there
        from_address = (self.data["TC5"]["fromAddress"])
        to_address = (self.data["TC5"]["toAddress"])
        exp_list = (self.data["TC5"]["pkgList"])

        self.driver = setup
        self.rtp = RateTransitPage(self.driver)
        self.rtp.enterOrigDestDetails(from_address, to_address)
        act_list = self.rtp.getItemsInPkgDrpdown()

        assert exp_list == act_list, f'expected list has items: {exp_list}, whereas actual list has items: {act_list} '

    @pytest.mark.regression
    def test_006_wgt_limit_error_envelope(self, setup):
        from_address = (self.data["TC6"]["fromAddress"])
        to_address = (self.data["TC6"]["toAddress"])
        pkg_type = (self.data["TC6"]["pkgType"])
        weight = (self.data["TC6"]["weight"])
        expected_error = (self.data["TC6"]["errorMsg"])

        self.driver = setup
        self.rtp = RateTransitPage(self.driver)
        self.rtp.enterOrigDestDetails(from_address, to_address)
        self.rtp.selPkgType(pkg_type)
        self.rtp.setWgt(weight)

        act_error = self.driver.find_element("xpath", self.rtp.wgt_error_xpath_env).text
        assert expected_error == act_error,"Error is not populated"

    @pytest.mark.regression
    def test_007_rates_applied(self, setup):

        from_address = (self.data["TC7"]["fromAddress"])
        to_address = (self.data["TC7"]["toAddress"])
        pkg_type = (self.data["TC7"]["pkgType"])
        weight = (self.data["TC7"]["weight"])
        expected_rates = (self.data["TC7"]["rates_desc"])
        self.driver = setup
        self.rtp = RateTransitPage(self.driver)
        self.rtp.enterOrigDestDetails(from_address, to_address)
        self.rtp.selPkgType(pkg_type)
        self.rtp.setWgt(weight)
        self.rtp.clickShowRates()
        self.rtp.clickExpandRates()
        actual_rates = self.rtp.getRatesList()
        assert expected_rates == actual_rates,f'rates expected are: {expected_rates}, whereas rates applied are: {actual_rates}'

    @pytest.mark.regression
    def test_008_ln_wd_ht_enabled_for_your_pkg(self, setup):
        from_address = (self.data["TC8"]["fromAddress"])
        to_address = (self.data["TC8"]["toAddress"])
        pkgtype = (self.data["TC8"]["pkgType"])
        self.driver = setup
        self.rtp = RateTransitPage(self.driver)
        self.rtp.enterOrigDestDetails(from_address, to_address)
        self.rtp.selPkgType(pkgtype)

        exp_l = self.driver.find_element("xpath", self.rtp.pkg_length_xpath).get_attribute("formcontrolname")
        exp_w = self.driver.find_element("xpath", self.rtp.pkg_width_xpath).get_attribute("formcontrolname")
        exp_h = self.driver.find_element("xpath", self.rtp.pkg_height_xpath).get_attribute("formcontrolname")

        assert exp_l == "length","length text box is not available"
        assert exp_w == "width","width text box is not available"
        assert exp_h == "height","height text box is not available"



    @pytest.mark.regression
    def test_009_verify_wgt_req_error_msg(self, setup):
        from_address = (self.data["TC9"]["fromAddress"])
        to_address = (self.data["TC9"]["toAddress"])
        pkg_type = (self.data["TC9"]["pkgType"])
        expected_error = (self.data["TC9"]["errorMsg"])
        self.driver = setup
        self.rtp = RateTransitPage(self.driver)
        self.rtp.enterOrigDestDetails(from_address, to_address)
        self.rtp.selPkgType(pkg_type)
        self.rtp.clickAddPkg()
        self.rtp.clickAddPkg()
        actual_error = self.driver.find_element("xpath", self.rtp.wgt_error_xpath_yp).text
        assert expected_error == actual_error,"Error is not populated"