# How to use

Overview of interfacing with Supbot

---

Supbot encapsulates all its functionality into `Supbot` class. In order to use supbot's services you will have to create its instance. Even after you create the instance it need to start its services so that it becomes useable. It does that using `__enter__()` method. Also, it need to destroy its internal states before you stop using supbot, which it does using `__exit__()` method.

So instead of using those methods directly, you can use `with - as` statement to create a scope in which supbot can be used without any worries.

```python
with Supbot() as supbot:
	supbot.send_message("Adam", "hi!");
```

---

## Services

There are two main sub-catagories of services that supbot provides which are, `Action`, `Events`, and `Helper`.

### Action

Actions are services which allows the developer to perform operations in whatsapp, like sending a message, anything which is initiated by the developer is an Action. Check out [Action](../services/action.md) to learn more.

### Event

Events are services which allows the developer to run code when an event occours in whatsapp, like reciving a message. Supbot provides event listeners so that you can register your own callback methods to be executed when an event occours. Check out [Event](../services/event.md) to learn more.

### Helper Services

Other than the above to main types of services, supbot also provides some helper methods. Check out [Helper](../services/helper.md) to learn more.

---

## Example

```python
from supbot import Supbot


def repeat_message(contact_name, message):
    supbot.send_message(contact_name, message)


with Supbot(message_received=repeat_message) as supbot:
    supbot.wait_for_finish()
```

Lets look at the getting started example, to understand each type of service much better. The code written below re-sends the message sent to the bot back. We will break down each part of the code, in order to understand how supbot API is used

```python
from supbot import Supbot
``` 
imports `Supbot` class which will be used to create its instance later on.

```python
def repeat_message(contact_name, message):
```
This is a function which is going to be used as an event callback.

```python
supbot.send_message(contact_name, message)
```
Over here we are using an `Action` service. `send_message` service just sends the message to the target contact. Over here we are getting the contact name from the event and we are directly passing it to the `Action`.

```python
with ... as supbot:
```
In order to use supbot we need to create an instance for it, and for it to make its services usable, it need to initialize itself, which is done using `with - as` statement.

```python
Supbot(message_received=repeat_message)
```
Constructor of supbot takes in the callback methods for events you want to use. Over here we are assigning the `repeat_message` method to `message_received` Event, so that when `message_received` Event occours, `repeat_message` method is called.

```python
 supbot.wait_for_finish()
```
This is a `Helper` service which allows the main thread to sleep till supbot is turned off. This is used so that the program doesn't quit.
