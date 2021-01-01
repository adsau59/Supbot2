from logging import Logger
from subprocess import Popen

from supbot.app_driver import AppDriver
from supbot.system import System

logger: Logger
kwargs = None
system: System
driver: AppDriver
appium_process: Popen
