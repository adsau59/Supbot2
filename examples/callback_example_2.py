from supbot import Supbot

contact = "123456789"


def action_callback_with_param(action_id, param2, supbot):
    print(param2)
    action = supbot.get_action(action_id)
    print(action)


def main():
    with Supbot() as supbot:
        var_from_main = "this is to show how you can send variables from other scope to callbacks"
        supbot.send_message(contact, "hi", lambda x: action_callback_with_param(x, var_from_main, supbot))
        supbot.quit()


if __name__ == '__main__':
    main()
