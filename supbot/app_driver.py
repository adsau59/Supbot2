"""
app_driver.py

provides an interface for the lower level appium calls to other systems of supbot
will be reworked to handle more exceptions
"""
import logging
import os
import re
import shlex
import subprocess
import threading
from typing import Tuple, Optional
from appium.webdriver import Remote
import time
from selenium.common.exceptions import NoSuchElementException
from supbot import model, g


class AppDriver:
    """
    Abstracts appium calls
    """

    def __init__(self, driver: Remote):
        self.driver = driver

    @staticmethod
    def create(device_name: str) -> Optional['AppDriver']:
        """
        Initializes appium driver
        :type device_name: name of the device to be used, if it is none, it uses adb command to fetch it
        """
        try:
            g.logger.info("Finding android device")
            if device_name is None:
                adb_path = os.path.join(os.environ.get('ANDROID_HOME'), 'platform-tools', "adb.exe")
                adb_ouput = subprocess.check_output([adb_path, "devices"]).decode('utf-8')
                device_name = re.search(r'^(.+)\tdevice', adb_ouput, flags=re.MULTILINE).group(1)

            if not g.kwargs["no_server"]:
                def appium_logging():
                    g.logger.info("launching appium server")
                    try:
                        appium_process = subprocess.Popen(shlex.split("appium"), stdout=subprocess.PIPE, shell=True)
                        appium_logs = logging.getLogger('appium')
                        while g.system.status > -1:
                            line = appium_process.stdout.readline().decode('utf-8')
                            appium_logs.debug(line)
                    except FileNotFoundError:
                        logging.error("Appium not installed")

                threading.Thread(target=appium_logging).start()

            g.logger.info("Connecting to appium on {}".format(device_name))
            desired_caps = {
                'platformName': 'Android',
                'deviceName': device_name,
                'appPackage': 'com.whatsapp',
                'appActivity': 'com.whatsapp.HomeActivity',
                'noReset': 'true'
            }
            driver = Remote('http://localhost:4723/wd/hub', desired_caps)
            driver.implicitly_wait(5)
            g.logger.info("driver created")
            return AppDriver(driver)
        except FileNotFoundError:
            logging.error("Device not found; make sure device is connected using `adb devices` command")

    def destroy(self):
        """
        Quits appium drivers
        """
        self.driver.quit()

    def click_on_chat(self, chat_name: str) -> bool:
        """
        Clicks on the chat list item in the app
        :param chat_name: name of the contact
        """
        try:
            search = self.driver.find_elements_by_id("com.whatsapp:id/conversations_row_contact_name")

            # todo instead of equating the number directly, normalize it then compare
            element = next(x for x in search if x.text == chat_name)
            element.click()
            return True
        except Exception:
            return False

    def search_chat(self, chat_name: str) -> bool:
        try:
            self.driver.find_element_by_id("com.whatsapp:id/menuitem_search").click()
            self.driver.find_element_by_id("com.whatsapp:id/search_src_text").send_keys(chat_name)
            return True
        except NoSuchElementException:
            return False

    def chat_via_intent(self, phone_number):
        try:
            self.driver.start_activity("com.whatsapp", "com.whatsapp.Conversation",
                                       intent_action="android.intent.action.SENDTO smsto:{}".format(phone_number))
            return True
        except:
            self.driver.start_activity("com.whatsapp", "com.whatsapp.HomeActivity")
            return False

    def type_and_send(self, message: str):
        """
        Entered text in chat, and presses the send button
        :param message: message to send
        """
        try:
            element = self.driver.find_element_by_id('com.whatsapp:id/entry')
            element.send_keys(message)

            element = self.driver.find_element_by_id('com.whatsapp:id/send')
            element.click()
            return True
        except NoSuchElementException:
            return False

    def click_on_last_chat_link(self):
        self.driver.find_elements_by_id("com.whatsapp:id/message_text").pop().click()
        return True

    def click_ok(self):
        try:
            ok = self.driver.find_element_by_id("android:id/button1")
            ok.click()
            return True
        except  NoSuchElementException:
            return False

    def press_back(self):
        """
        presses the back button, then waits for animation/load to finish
        """
        self.driver.press_keycode(4)

    def get_new_chat(self) -> Optional['model.Chat']:
        """
        Checks for chat item with new message bubble,
        used by new_chat checker (checker system not made yet)
        :return: chat (contact_name) who sent a new chat
        """
        try:
            element = self.driver.find_element_by_xpath('//android.widget.TextView[@resource-id='
                                                        '"com.whatsapp:id/conversations_row_message_count"]/../..'
                                                        '//android.widget.TextView[@resource-id="com.whatsapp:id'
                                                        '/conversations_row_contact_name"]')
            return model.Chat(element.text)
        except NoSuchElementException:
            return None

    def get_new_messages(self) -> Optional[Tuple[str]]:
        """
        checks for all the new messages
        :return: list of messages sent to the bot
        """
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

    def send_image(self, image_loc: str) -> bool:
        try:
            _, ext = os.path.splitext(image_loc)
            os.utime(image_loc, (time.time(), time.time()))
            self.driver.push_file(destination_path="/storage/emulated/0/Supbot/temp" + ext,
                                  source_path=image_loc)
            self.driver.find_element_by_id("com.whatsapp:id/input_attach_button").click()
            self.driver.find_element_by_id("com.whatsapp:id/pickfiletype_gallery").click()
            self.driver.find_element_by_xpath('//android.widget.TextView[@text="Supbot"]').click()
            self.driver.find_element_by_xpath('//android.widget.ImageView').click()
            self.driver.find_element_by_id("com.whatsapp:id/send").click()
            return True
        except:
            return False
