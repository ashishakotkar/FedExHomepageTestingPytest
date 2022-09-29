import pytest
import json
from pageObjects.RateTransitPage import RateTransitPage
from utilities.readProperties import ReadConfig
from utilities.customLogger import LogGen
# import logging


class Test_Rate_Transit_Times:
    baseURL = ReadConfig.getApplicationURL()
    logger = LogGen.loggen()

    # baseURL = "https://www.fedex.com/en-in/home.html"
    fromAddress = "Chicago, 60612, United States"
    fromPostcode = "60612"
    toAddress = "Warwickshire, CV11 5PA, United Kingdom"
    toPostcode = "CV115PA"

    json_data = open("TestData/rate_transit_data.json")
    json_data1 = json.load(json_data)

    #setup is method in conftest file that returns driver instance
    @pytest.mark.sanity
    def test_001_verifyHomePageTitle(self,setup):

        self.logger.info("**************Test_001_Verifying Homepage Title*************************")

        self.driver = setup
        self.driver.implicitly_wait(10)
        # open the URL
        self.driver.get(self.baseURL)
        self.driver.maximize_window()
        self.rtp = RateTransitPage(self.driver)
        self.rtp.clickCloseOnPopup()
        actual_title = self.driver.title
        expected_title = "FedEx | Express Delivery, Courier & Shipping Services | India"
        if actual_title == expected_title:
            self.driver.close()
            self.logger.info("**************Home page title verification test passed*************************")
            assert True

        else:
            self.driver.save_screenshot(".\\Screenshots\\"+"test_001_verifyHomePageTitle.png")
            self.driver.close()
            self.logger.info("**************Home page title verification test failed*************************")
            assert False


    def test_002_verifyTodaysDtAvailableShpDtDrpdwn(self,setup):
        self.logger.info("**************test_002_verifyTodaysDtAvailableShpDtDrpdwn*************************")

        self.driver = setup
        self.driver.implicitly_wait(10)
        self.driver.get(self.baseURL)
        self.driver.maximize_window()
        self.rtp = RateTransitPage(self.driver)
        self.rtp.enterOrigDestDetails(self.fromAddress, self.fromPostcode, self.toAddress)
        print("printing from test case: "+self.rtp.getTodaysDateXpath())

        if self.driver.find_element("xpath", self.rtp.getTodaysDateXpath()):
            self.driver.close()
            assert True
        else:
            self.driver.save_screenshot(".\\Screenshots\\" + "test_002_verifyTodaysDtAvailableShpDtDrpdwn.png")
            self.driver.close()
            assert False


    def test_003_verifyTommDrAvailableShpDtDrpdwn(self,setup):
        self.driver = setup
        self.driver.implicitly_wait(10)
        self.driver.get(self.baseURL)
        self.driver.maximize_window()
        self.rtp = RateTransitPage(self.driver)
        self.rtp.enterOrigDestDetails(self.fromAddress, self.fromPostcode, self.toAddress)
        print("printing from test case: "+self.rtp.getTomorrowDateXpath())

        if self.driver.find_element("xpath", self.rtp.getTomorrowDateXpath()):
            self.driver.close()
            assert True
        else:
            self.driver.save_screenshot(".\\Screenshots\\" + "test_003_verifyTommDrAvailableShpDtDrpdwn.png")
            self.driver.close()
            assert False

    @pytest.mark.regression
    def test_004_verifyDefaultAdditionalCoverBtnVal(self, setup):
        self.driver = setup
        self.driver.implicitly_wait(10)
        self.driver.get(self.baseURL)
        self.driver.maximize_window()
        self.rtp = RateTransitPage(self.driver)
        self.rtp.enterOrigDestDetails(self.fromAddress, self.fromPostcode, self.toAddress)
        status = self.rtp.getAddCoverNoRadioBtnStatus()
        if not status:
            self.driver.close()
            assert True
        else:
            self.driver.save_screenshot(".\\Screenshots\\" + "test_004_verifyDefaultAdditionalCoverBtnVal.png")
            self.driver.close()
            assert False

    @pytest.mark.regression
    def test_005_verifyItemsInPkgDropdown(self,setup):
        self.driver = setup
        self.driver.implicitly_wait(10)
        self.driver.get(self.baseURL)
        self.driver.maximize_window()
        self.rtp = RateTransitPage(self.driver)
        self.rtp.enterOrigDestDetails(self.fromAddress, self.fromPostcode, self.toAddress)

        my_list = ['Your Packaging\nFedEx 10kg Box\nFedEx 25kg Box\nFedEx Envelope\nFedEx Extra Large Box\nFedEx Large Box\nFedEx Medium Box\nFedEx Pak\nFedEx Small Box\nFedEx Tube']
        act_list = self.rtp.getItemsInPkgDrpdown()

        if my_list == act_list:
            self.driver.close()
            assert True
        else:
            self.driver.save_screenshot(".\\Screenshots\\" + "test_005_verifyItemsInPkgDropdown.png")
            self.driver.close()
            assert False


    @pytest.mark.regression
    def test_006_wgtLimitError(self,setup):
        pkgType = "FedEx Envelope"
        self.driver = setup
        self.driver.implicitly_wait(10)
        self.driver.get(self.baseURL)
        self.driver.maximize_window()
        self.rtp = RateTransitPage(self.driver)
        self.rtp.enterOrigDestDetails(self.fromAddress, self.fromPostcode, self.toAddress)
        self.rtp.selPkgType(pkgType)
        self.rtp.setWgt(2)

        if self.driver.find_element("xpath", self.rtp.max_wgt_error_xpath):
            self.driver.close()
            assert True
        else:
            self.driver.save_screenshot(".\\Screenshots\\" + "test_006_wgtLimitError.png")
            self.driver.close()
            assert False



    @pytest.mark.regression
    def test_007_verifyItemsInPkgDropdown(self, setup):

        pkgtype = 'FedEx 10kg Box'

        self.driver = setup
        self.driver.implicitly_wait(10)
        self.driver.get(self.baseURL)
        self.driver.maximize_window()
        self.rtp = RateTransitPage(self.driver)
        self.rtp.enterOrigDestDetails(self.fromAddress, self.fromPostcode, self.toAddress)
        self.rtp.selPkgType(pkgtype)
        self.rtp.setWgt("5")
        self.rtp.clickShowRates()
        self.rtp.clickExpandRates()
        rates = self.rtp.getRatesList()

        print(rates)

        act_text = rates
        exp_text = ['Base rate', 'Fuel Surcharge', 'FedEx pickup', 'Peak Surcharge', 'Estimated Total']
        if act_text == exp_text:
            self.driver.close()
            assert True
        else:
            self.driver.save_screenshot(".\\Screenshots\\" + "test_007_verifyItemsInPkgDropdown.png")
            self.driver.close()
            assert False


    @pytest.mark.regression
    def test_008_verifyLWHenabledYourPkg(self,setup):
        pkgtype = 'Your Packaging'

        self.driver = setup
        self.driver.implicitly_wait(10)
        self.driver.get(self.baseURL)
        self.driver.maximize_window()
        self.rtp = RateTransitPage(self.driver)
        self.rtp.enterOrigDestDetails(self.fromAddress, self.fromPostcode, self.toAddress)
        self.rtp.selPkgType(pkgtype)

        if self.driver.find_element("xpath",self.rtp.pkg_length_xpath):
            assert True
        if self.driver.find_element("xpath", self.rtp.pkg_width_xpath):
            assert True
        if self.driver.find_element("xpath", self.rtp.pkg_height_xpath):
            assert True
        self.driver.close()

    @pytest.mark.regression
    def test_009_verifyWeightReqError(self, setup):
        pkgtype = 'Your Packaging'

        self.driver = setup
        self.driver.implicitly_wait(10)
        self.driver.get(self.baseURL)
        self.driver.maximize_window()
        self.rtp = RateTransitPage(self.driver)
        self.rtp.enterOrigDestDetails(self.fromAddress, self.fromPostcode, self.toAddress)
        self.rtp.selPkgType(pkgtype)
        self.rtp.clickAddPkg()
        self.rtp.clickAddPkg()

        if self.driver.find_element("xpath", self.rtp.wgt_req_error_xpath):
            self.driver.close()
            assert True
        else:
            self.driver.save_screenshot(".\\Screenshots\\" + "test_009_verifyWeightReqError.png")
            self.driver.close()
            assert False
