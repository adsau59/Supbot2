from appium.webdriver import Remote
import time
from supbotserver.controller import idriver


class AppDriver(idriver.IDriver):

    def __init__(self):
        desired_caps = {
            'platformName': 'Android',
            'deviceName': '71856f60',
            'appPackage': 'com.whatsapp',
            'appActivity': 'com.whatsapp.HomeActivity',
            'noReset': 'true'
        }
        self.driver = Remote('http://localhost:4723/wd/hub', desired_caps)

    def destroy(self):
        self.driver.quit()

    def click_on_chat(self, chat_name: str):
        element = self.driver.find_element_by_xpath('//android.widget.TextView[contains(@text,"{}")]'.format(chat_name))
        element.click()

    def type_and_send(self, message: str):
        element = self.driver.find_element_by_id('com.whatsapp:id/entry')
        element.send_keys(message)

        element = self.driver.find_element_by_id('com.whatsapp:id/send')
        element.click()

    def press_back(self):
        self.driver.press_keycode(4)
        time.sleep(1)

    def get_new_chat(self):
        pass
