import unittest
from supbot import Supbot

config = {
  "device_name": "71856f60",
  "contact_name": "Adam"
}


class TestSupbot(unittest.TestCase):

    def test_works_properly(self):

        with self.assertLogs(level='DEBUG') as cm:
            with Supbot(config["device_name"]) as supbot:
                supbot.send_message(config["contact_name"], "hi")
            self.assertIn('DEBUG:supbot:sent message hi to {} successfully'.format(config["contact_name"]), cm.output,
                          "log not found")


if __name__ == "__main__":
    unittest.main()
