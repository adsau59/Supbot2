from typing import Tuple, Optional
from abc import ABC, abstractmethod

from appium.webdriver import Remote
import time

from selenium.common.exceptions import NoSuchElementException

from supbot import model


class IDriver(ABC):

    @abstractmethod
    def destroy(self):
        pass

    @abstractmethod
    def click_on_chat(self, chat_name: str):
        pass

    @abstractmethod
    def type_and_send(self, message: str):
        pass

    @abstractmethod
    def press_back(self):
        pass

    @abstractmethod
    def get_new_chat(self) -> Optional['model.Chat']:
        pass

    @abstractmethod
    def get_new_messages(self) -> Optional[Tuple[str]]:
        pass


class AppDriver(IDriver):

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

    def click_on_chat(self, chat_name: str) -> bool:
        try:
            element = self.driver.find_element_by_xpath(
                '//android.widget.TextView[contains(@text,"{}")]'.format(chat_name))
            element.click()
            return True
        except NoSuchElementException:
            return False

    def type_and_send(self, message: str):
        try:
            element = self.driver.find_element_by_id('com.whatsapp:id/entry')
            element.send_keys(message)

            element = self.driver.find_element_by_id('com.whatsapp:id/send')
            element.click()
        except NoSuchElementException:
            return False

    def press_back(self):
        self.driver.press_keycode(4)
        time.sleep(1)

    def get_new_chat(self) -> Optional['model.Chat']:
        try:
            element = self.driver.find_element_by_xpath('//android.widget.TextView[@resource-id='
                                                        '"com.whatsapp:id/conversations_row_message_count"]/../..'
                                                        '//android.widget.TextView[@resource-id="com.whatsapp:id'
                                                        '/conversations_row_contact_name"]')
            return model.Chat(element.text)
        except NoSuchElementException:
            return None

    def get_new_messages(self) -> Optional[Tuple[str]]:
        try:
            message_elements = self.driver.find_elements_by_xpath('//android.widget.TextView[@resource-id='
                                                                  '"com.whatsapp:id/unread_divider_tv"]/../..'
                                                                  '//following-sibling::android.view.ViewGroup'
                                                                  '//android.widget.TextView[@resource-id='
                                                                  '"com.whatsapp:id/message_text"]')
            messages: Tuple[str] = tuple(x.text for x in message_elements)
            return messages
        except NoSuchElementException:
            return None
