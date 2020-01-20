from supbotserver import model
from supbotserver.controller import idriver

states: model.States = {
    "main": model.GUIState("main"),
    "chat": model.GUIState("chat")
}


def change_state(driver: idriver.IDriver, _from: model.GUIStateWithInfo, _to: model.GUIStateWithInfo) -> model.GUIStateWithInfo:

    if _to.state == states["main"]:

        if _from.state == states["chat"]:
            driver.press_back()

    elif _to.state == states["chat"]:

        if _from == states["main"]:
            driver.click_on_chat(_to.info)
        elif _from == states["chat"] and _from.info != _to.info:
            driver.press_back()
            driver.click_on_chat(_to.info)

    return _to
