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
from appium.webdriver.webelement import WebElement
from appium.webdriver import Remote
import time
from selenium.common.exceptions import NoSuchElementException
from supbot import g, helper


# noinspection PyBroadException
class AppDriver:
    """
    Abstracts appium calls
    """

    def __init__(self, driver: Remote, implicit_wait: int):
        self.driver = driver
        self.implicit_wait = implicit_wait

    @staticmethod
    def create() -> Optional['AppDriver']:
        """
        Initializes appium driver
        """
        try:
            # region input from kwargs
            run_server = not ("no_server" in g.kwargs and g.kwargs["no_server"])

            if "port" in g.kwargs and g.kwargs["port"] is not None:
                port = g.kwargs["port"]
            elif run_server:
                port = str(helper.get_free_tcp_port())
            else:
                port = "4723"

            g.logger.info("Finding android device")

            if "device_name" in g.kwargs and g.kwargs["device_name"] is not None:
                device_name = g.kwargs["device_name"]
            elif "device" in g.kwargs and g.kwargs["device"] is not None:
                device_name = g.kwargs["device"]
            else:
                adb_path = os.path.join(os.environ.get('ANDROID_HOME'), 'platform-tools', "adb.exe")
                ada_output = subprocess.check_output([adb_path, "devices"]).decode('utf-8')
                device_name = re.search(r'^(.+)\tdevice', ada_output, flags=re.MULTILINE).group(1)

            if "implicit_wait" in g.kwargs and g.kwargs["implicit_wait"] is not None:
                implicit_wait = g.kwargs["implicit_wait"]
            else:
                implicit_wait = 5

            # endregion

            if run_server:
                def appium_logging():
                    g.logger.info("launching appium server on {}".format(port))
                    try:
                        appium_process = subprocess.Popen(shlex.split("appium --port {}".format(port)),
                                                          stdout=subprocess.PIPE, shell=True)
                        appium_logs = logging.getLogger('appium')
                        while g.system.status > -1:
                            line = appium_process.stdout.readline().decode('utf-8')
                            appium_logs.debug(line)
                        appium_process.stdout.close()
                        appium_process.kill()
                    except FileNotFoundError:
                        logging.error("Appium not installed")

                threading.Thread(target=appium_logging).start()

            g.logger.info("Connecting to appium with {}".format(device_name))
            desired_caps = {
                "platformName": "Android",
                "udid": device_name,
                "appPackage": "com.whatsapp",
                "appActivity": "com.whatsapp.HomeActivity",
                "noReset": "true",
                "deviceName": "Android Emulator"
            }
            driver = Remote('http://localhost:{}/wd/hub'.format(port), desired_caps)
            driver.implicitly_wait(implicit_wait)
            g.logger.info("driver created")
            return AppDriver(driver, implicit_wait)
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
            element = next(x for x in search if helper.contact_number_equal(x.text, chat_name))
            element.click()
            return True
        except Exception:
            return False

    def type_in_search(self, chat_name: str) -> bool:
        try:
            self.driver.find_element_by_id("com.whatsapp:id/search_src_text").send_keys(chat_name)
            return True
        except NoSuchElementException:
            return False

    def click_search(self) -> bool:
        try:
            self.driver.find_element_by_id("com.whatsapp:id/menuitem_search").click()
            return True
        except:
            return False

    def goto_home(self):
        self.driver.start_activity("com.whatsapp", "com.whatsapp.HomeActivity")

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
        except:
            return False

    def click_on_last_chat_link(self):
        self.driver.find_elements_by_id("com.whatsapp:id/message_text").pop().click()
        return True

    def click_ok(self):
        try:
            ok = self.driver.find_element_by_id("android:id/button1")
            ok.click()
            return True
        except NoSuchElementException:
            return False

    def press_back(self):
        """
        presses the back button, then waits for animation/load to finish
        """
        time.sleep(0.5)
        self.driver.press_keycode(4)

    def press_chat_back(self):
        try:
            self.driver.find_element_by_id("com.whatsapp:id/back").click()
            return True
        except:
            return False

    def press_search_back(self):
        try:
            self.driver.find_element_by_id("com.whatsapp:id/search_back").click()
            return True
        except:
            return False

    def get_new_chat(self) -> Optional[str]:
        """
        Checks for chat item with new message bubble,
        used by new_chat checker (checker system not made yet)
        :return: chat (contact_name) who sent a new chat
        """
        try:
            self.driver.implicitly_wait(1)
            element = self.driver.find_element_by_xpath('//android.widget.TextView[@resource-id='
                                                        '"com.whatsapp:id/conversations_row_message_count"]/../..'
                                                        '//android.widget.TextView[@resource-id="com.whatsapp:id'
                                                        '/conversations_row_contact_name"]')
            return element.text
        except NoSuchElementException:
            return None
        finally:
            self.driver.implicitly_wait(self.implicit_wait)

    def get_new_messages(self) -> Optional[Tuple[str]]:
        """
        checks for all the new messages
        :return: list of messages sent to the bot
        """
        try:
            self.driver.implicitly_wait(1)
            new_bubbles = self.driver.find_elements_by_xpath('//android.widget.TextView[@resource-id='
                                                             '"com.whatsapp:id/unread_divider_tv"]/../..'
                                                             '//following-sibling::android.view.ViewGroup'
                                                             '//android.widget.LinearLayout[@resource-id='
                                                             '"com.whatsapp:id/main_layout"]')

            messages: Tuple[str] = tuple(self.get_message_from_bubble(x) for x in new_bubbles)
            return messages
        except NoSuchElementException:
            return None
        finally:
            self.driver.implicitly_wait(self.implicit_wait)

    def get_message_from_bubble(self, bubble: WebElement) -> str:
        try:
            return bubble.find_element_by_id("com.whatsapp:id/message_text").text
        except:
            return ""

    def get_author_from_bubble(self, bubbles, target_bubble) -> str:
        ...

    def does_any_has_author(self, bubbles) -> bool:
        ...

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

    def scroll_chat(self, reverse=False):
        try:
            elements = self.driver.find_elements_by_id("com.whatsapp:id/conversations_row_contact_name")
            if reverse:
                self.driver.scroll(elements[1], elements[-1], 3000)
            else:
                self.driver.scroll(elements[-1], elements[1], 3000)
            return True
        except:
            return False

    def check(self, id, fast: bool=False):
        try:
            if fast:
                self.driver.implicitly_wait(1)

            return self.driver.find_element_by_id(id) is not None
        except:
            return False
        finally:
            self.driver.implicitly_wait(self.implicit_wait)

    # todo make better architecture for check
    def check_scroll_end(self):
        return self.check("com.whatsapp:id/conversations_row_tip_tv", True)

    def check_scroll_top(self):
        try:
            self.driver.implicitly_wait(1)
            search = self.driver.find_elements_by_id("com.whatsapp:id/conversations_row_contact_name")
            element = next(x for x in search if helper.contact_number_equal(x.text, "!temp"))
            return element is not None
        except:
            return False
        finally:
            self.driver.implicitly_wait(self.implicit_wait)

    def check_for_below_chat(self):
        return self.check("com.whatsapp:id/badge", True)

    def check_fab(self):
        try:
            return self.driver.find_element_by_id("com.whatsapp:id/fab") is not None
        except:
            return False

    def check_search_input(self):
        try:
            return self.driver.find_element_by_id("com.whatsapp:id/search_src_text") is not None
        except:
            return False

    def check_chat(self, chat_name):
        try:
            element = self.driver.find_element_by_id("com.whatsapp:id/conversation_contact_name")
            return helper.contact_number_equal(element.text, chat_name)
        except:
            return False
