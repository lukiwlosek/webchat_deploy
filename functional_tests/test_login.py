from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
import time

# mimic the user interaction


class TestLogin(StaticLiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Chrome("functional_tests/chromedriver")

    def tearDown(self):
        self.browser.close()

    def test_wrong_login(self):
        self.browser.get(self.live_server_url)
        # if user enters wrong username and password a list element is shown
        self.browser.find_element_by_id("id_username").send_keys("testing")
        self.browser.find_element_by_css_selector("input[type=password]")
        time.sleep(2)
        self.browser.find_element_by_xpath("//*[@id='Btn']").click()
        time.sleep(5)
        self.assertTrue(self.browser.find_element_by_tag_name("li"))

