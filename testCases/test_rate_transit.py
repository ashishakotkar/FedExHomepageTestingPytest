import pytest
import json
from pageObjects.RateTransitPage import RateTransitPage
from utilities.readProperties import ReadConfig
from utilities.customLogger import LogGen


class TestRateTransitTimes:
    baseURL = ReadConfig.getApplicationURL()

    logger = LogGen.loggen()

    datafile = open("TestData/rate_transit_data.json")
    data = json.load(datafile)

    # setup is method in conftest file that returns driver instance

    # This test case verifies the title of homepage
    @pytest.mark.functional
    def test_001_homepage_title(self, setup):
        self.logger.info("**************Test_001_Verifying Homepage Title*************************")
        expected_title = (self.data["TC1"]["title"])
        self.driver = setup
        self.rtp = RateTransitPage(self.driver)
        self.rtp.clickCloseOnPopup()
        actual_title = self.driver.title
        assert actual_title == expected_title, f'Error.Expected text:{expected_title}, but actual text: {actual_title}'
        self.logger.info("**************Ending Test*************************")
    # Test to verify that current date is available in the ship date dropdown
    @pytest.mark.regression
    def test_002_todays_dt_available_shpdtdrpdwn(self, setup):
        self.logger.info("**************test_002_todays_dt_available_shpdtdrpdwn*************************")
        from_address = (self.data["TC2"]["fromAddress"])
        to_address = (self.data["TC2"]["toAddress"])

        self.driver = setup
        self.rtp = RateTransitPage(self.driver)
        self.rtp.enterOrigDestDetails(from_address, to_address)
        self.logger.info("**************Entered origin destination details*************************")

        # get the dropdown element containing todaay's date
        date_attrib = self.driver.find_element("xpath", (self.rtp.getTodaysDateXpath() + "/parent::*"))
        date_attrib_id = date_attrib.get_attribute('id')
        assert date_attrib_id == "packageShipDate", f"today's date is not available in the dropdown"
        self.logger.info("**************Ending Test*************************")

    # Test to verify that the next day date is available in the ship date dropdown
    @pytest.mark.regression
    def test_003_tomm_dt_available_shpdtdrpdwn(self, setup):
        self.logger.info("**************test_003_tomm_dt_available_shpdtdrpdwn*************************")
        from_address = (self.data["TC3"]["fromAddress"])
        to_address = (self.data["TC3"]["toAddress"])

        self.driver = setup
        self.rtp = RateTransitPage(self.driver)
        self.rtp.enterOrigDestDetails(from_address, to_address)
        self.logger.info("**************Entered origin destination details*************************")

        # get the dropdown element containing tomorrow's date
        date_attrib = self.driver.find_element("xpath", self.rtp.getTomorrowDateXpath() + "/parent::*")
        date_attrib_id = date_attrib.get_attribute('id')
        assert date_attrib_id == "packageShipDate", f"tomorrows's date is not available in the dropdown"
        self.logger.info("**************Ending Test*************************")

    # Test to verify that the radio button for "Need additional cover?" is by default set to 'No'
    @pytest.mark.regression
    @pytest.mark.sanity
    def test_004_default_additional_cover_btn_val(self, setup):
        self.logger.info("**************004_default_additional_cover_btn_val*************************")
        from_address = (self.data["TC4"]["fromAddress"])
        to_address = (self.data["TC4"]["toAddress"])
        self.driver = setup
        self.rtp = RateTransitPage(self.driver)
        self.rtp.enterOrigDestDetails(from_address, to_address)
        self.logger.info("**************Entered origin destination details*************************")
        # getting the boolean value of the radio using isEnabled() method
        status = self.rtp.getAddCoverNoRadioBtnStatus()
        assert status, f"'No' radio button is not enabled"
        self.logger.info("**************Ending Test*************************")

    # Test to verify all the package types are available in the dropdown
    @pytest.mark.regression
    def test_005_items_in_pkg_dropdown(self, setup):
        self.logger.info("**************005_items_in_pkg_dropdown*************************")
        from_address = (self.data["TC5"]["fromAddress"])
        to_address = (self.data["TC5"]["toAddress"])
        exp_list = (self.data["TC5"]["pkgList"])

        self.driver = setup
        self.rtp = RateTransitPage(self.driver)
        self.rtp.enterOrigDestDetails(from_address, to_address)
        self.logger.info("**************Entered origin destination details*************************")

        #to get the elements in the pkg type dropdown as list
        act_list = self.rtp.getItemsInPkgDrpdown()

        assert exp_list == act_list, f'expected list has items: {exp_list}, whereas actual list has items: {act_list}'
        self.logger.info("**************Ending Test*************************")

    # Test to verify that if weight for envelope is exceeded than 0.5 kg throws error
    @pytest.mark.regression
    def test_006_wgt_limit_error_envelope(self, setup):
        self.logger.info("**************006_wgt_limit_error_envelope*************************")
        from_address = (self.data["TC6"]["fromAddress"])
        to_address = (self.data["TC6"]["toAddress"])
        pkg_type = (self.data["TC6"]["pkgType"])
        weight = (self.data["TC6"]["weight"])
        expected_error = (self.data["TC6"]["errorMsg"])

        self.driver = setup
        self.rtp = RateTransitPage(self.driver)
        self.rtp.enterOrigDestDetails(from_address, to_address)
        self.logger.info("**************Entered origin destination details*************************")
        self.rtp.selPkgType(pkg_type)
        self.rtp.setWgt(weight)

        act_error = self.driver.find_element("xpath", self.rtp.wgt_error_xpath_env).text
        assert expected_error == act_error, "Error is not populated"
        self.logger.info("**************Ending Test*************************")

    # Test to verify all the expected rates are applied on the shipment
    @pytest.mark.regression
    def test_007_rates_applied(self, setup):
        self.logger.info("**************test_007_rates_applied*************************")
        from_address = (self.data["TC7"]["fromAddress"])
        to_address = (self.data["TC7"]["toAddress"])
        pkg_type = (self.data["TC7"]["pkgType"])
        weight = (self.data["TC7"]["weight"])
        expected_rates = (self.data["TC7"]["rates_desc"])
        self.driver = setup
        self.rtp = RateTransitPage(self.driver)
        self.rtp.enterOrigDestDetails(from_address, to_address)
        self.logger.info("**************Entered origin destination details*************************")
        self.rtp.selPkgType(pkg_type)
        self.rtp.setWgt(weight)
        self.rtp.clickShowRates()
        self.rtp.clickExpandRates()

        # to get the rates as a list and then asserting them
        actual_rates = self.rtp.getRatesList()
        assert expected_rates == actual_rates, f'rates expected are: {expected_rates}, whereas rates applied are: {actual_rates}'
        self.logger.info("**************Ending Test*************************")

    # Test to verify that length, width, height fields are enabled when 'Your Packaging' is selected
    @pytest.mark.regression
    def test_008_ln_wd_ht_enabled_for_your_pkg(self, setup):
        self.logger.info("**************test_008_ln_wd_ht_enabled_for_your_pkg*************************")
        from_address = (self.data["TC8"]["fromAddress"])
        to_address = (self.data["TC8"]["toAddress"])
        pkgtype = (self.data["TC8"]["pkgType"])
        self.driver = setup
        self.rtp = RateTransitPage(self.driver)
        self.rtp.enterOrigDestDetails(from_address, to_address)
        self.logger.info("**************Entered origin destination details*************************")
        self.rtp.selPkgType(pkgtype)

        exp_l = self.driver.find_element("xpath", self.rtp.pkg_length_xpath).get_attribute("formcontrolname")
        exp_w = self.driver.find_element("xpath", self.rtp.pkg_width_xpath).get_attribute("formcontrolname")
        exp_h = self.driver.find_element("xpath", self.rtp.pkg_height_xpath).get_attribute("formcontrolname")

        assert exp_l == "length", "length text box is not available"
        assert exp_w == "width", "width text box is not available"
        assert exp_h == "height", "height text box is not available"
        self.logger.info("**************Ending Test*************************")

    # Test to verify 'Weight is required' error when it is missed to enter
    @pytest.mark.regression
    def test_009_verify_wgt_req_error_msg(self, setup):
        self.logger.info("**************009_verify_wgt_req_error_msg*************************")
        from_address = (self.data["TC9"]["fromAddress"])
        to_address = (self.data["TC9"]["toAddress"])
        pkg_type = (self.data["TC9"]["pkgType"])
        expected_error = (self.data["TC9"]["errorMsg"])
        self.driver = setup
        self.rtp = RateTransitPage(self.driver)
        self.rtp.enterOrigDestDetails(from_address, to_address)
        self.logger.info("**************Entered origin destination details*************************")
        self.rtp.selPkgType(pkg_type)
        self.rtp.clickAddPkg()
        self.rtp.clickAddPkg()
        actual_error = self.driver.find_element("xpath", self.rtp.wgt_error_xpath_yp).text
        assert expected_error == actual_error, "Error is not populated"
        self.logger.info("**************Ending Test*************************")

    # Test to verify all the expected links are available in the shipping dropdown
    @pytest.mark.regression
    def test_010_verify_links_shipping_dropdown(self, setup):
        self.logger.info("**************010_verify_links_shipping_dropdown*************************")
        expected_list = (self.data["TC10"]["drp_dwn_list"])
        self.driver = setup
        self.rtp = RateTransitPage(self.driver)
        self.rtp.clickCloseOnPopup()
        self.rtp.clickShippingDropdown()

        # adding the elements text in the shipping dropdown to the list
        actual_list = [element.text for element in
                       self.driver.find_elements("xpath", self.rtp.shipping_dropdown_elements_xpath)]
        assert expected_list == actual_list, "Expected list and actual list do not match"
        self.logger.info("**************Ending Test*************************")

    # Test to verify all the expected links are available in 'Account dropdown'
    @pytest.mark.regression
    def test_011_verify_links_account_dropdown(self, setup):
        self.logger.info("**************test_011_verify_links_account_dropdown*************************")
        expected_list = (self.data["TC11"]["drp_dwn_list"])
        self.driver = setup
        self.rtp = RateTransitPage(self.driver)
        self.rtp.clickCloseOnPopup()
        self.rtp.clickAccountDropdown()

        # adding the elements text in the account dropdown to the list
        actual_list = [element.text for element in
                       self.driver.find_elements("xpath", self.rtp.account_dropdown_elements_xpath)]
        print("Below are the values in dropdown: ")
        print(actual_list)
        assert expected_list == actual_list, "Expected list and actual list do not match"
        self.logger.info("**************Ending Test*************************")

    # Test to verify expected currency type is applied for rates calculation
    @pytest.mark.regression
    def test_0012_rate_currency(self, setup):
        self.logger.info("**************test_0012_rate_currency_service*************************")
        from_address = (self.data["TC12"]["fromAddress"])
        to_address = (self.data["TC12"]["toAddress"])
        pkg_type = (self.data["TC12"]["pkgType"])
        weight = (self.data["TC12"]["weight"])
        expected_curr = (self.data["TC12"]["currency"])

        self.driver = setup
        self.rtp = RateTransitPage(self.driver)
        self.rtp.enterOrigDestDetails(from_address, to_address)
        self.logger.info("**************Entered origin destination details*************************")
        self.rtp.selPkgType(pkg_type)
        self.rtp.setWgt(weight)
        self.rtp.clickShowRates()
        self.logger.info("**************Clicked on show rates button*************************")
        currency_txt_actual = self.driver.find_element("xpath", self.rtp.amount_shown_xpath).text
        assert expected_curr == currency_txt_actual
        self.logger.info("**************Ending Test*************************")
