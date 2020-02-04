from appium.webdriver import Remote

desired_caps = {
            'platformName': 'Android',
            'deviceName': '71856f60',
            'appPackage': 'com.whatsapp',
            'appActivity': 'com.whatsapp.HomeActivity',
            'noReset': 'true'
        }
driver = Remote('http://localhost:4723/wd/hub', desired_caps)

while True:
    try:
        a = input("?")
        element = driver.find_element_by_xpath(a)
        print(f"tag: {element.tag_name}")
        print(f"clas: {element.get_attribute('class')}")
        print(f"text: {element.text}")

    except Exception as e:
        print(e)
        print("error")
