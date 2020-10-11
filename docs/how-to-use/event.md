# Event

Run callbacks on event in whatsapp

---

## message_received 

When a text message is received

#### Callback Declaration
```python
def message_received(contact_name: str, message: str):
```

#### Description
When a text message is received this event is triggered. In the event, contact name of the sender is provided along with the message of sent. If there are multiple messages sent by one user, each of those messages will get their own event trigger, so callback will be executed for each one of those messages.

---

## group_message_received 

When a group message is received

#### Callback Declaration
```python
def message_received(group_name: str, contact_name: str, message: str):
```

#### Description
When a group text message is received this event is triggered. In the event, group name, contact name of the sender is provided along with the message of sent. If there are multiple messages sent in the group, each of those messages will get their own event trigger, so callback will be executed for each one of those messages.