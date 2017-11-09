from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
import time
import unittest

class LoginTest(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome("/Users/jahancherian/Downloads/chromedriver")
        self.driver.get("https://be.my.ucla.edu/IWE/mygrades.aspx")
        self.f = open("logs.txt", "w")

    def testLogin(self):
        driver = self.driver
        log = self.f
        myuser = "jcherian"
        mypass = "dynamicCorbatoLRUpimpl69"
        user_field_id = "logon"
        pass_field_id = "pass"

        user_field_elem = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_id(user_field_id))
        pass_field_elem = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_id(pass_field_id))
        user_field_elem.clear()
        user_field_elem.send_keys(myuser)
        pass_field_elem.clear()
        pass_field_elem.send_keys(mypass)
        pass_field_elem.send_keys(Keys.RETURN)

        select_field_elem = Select(driver.find_element_by_id("ctl00_StudentTermClassChooser_TermChooser"))
        for option in select_field_elem.options: 
            if option.text == u"Spring":
                option.click()
                time.sleep(15)
                subject_elem = WebDriverWait(driver, 5).until(lambda driver: Select(driver.find_element_by_id("ctl00_StudentTermClassChooser_ClassChooser")))
                for subject in subject_elem.options:
                    print(subject.text)
                    subject.click()
                    time.sleep(15)
                    table = WebDriverWait(driver, 10).until(lambda driver: Select(driver.find_element_by_id("myUCLAGradesGridFoo")))
                    log.write(table.text)
                    log.write('\n')
                break

if __name__ == "__main__":
    unittest.main()
