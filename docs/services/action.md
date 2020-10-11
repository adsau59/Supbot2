# Action

Perform operations in whatsapp

---

## send_message

Send message to a target contact

#### Declaration

```python
def send_message(self, contact_name: str, message: str, callback: Optional[ActionCallback] = None) -> Action:
```

#### Description

Sends a message to the target contact on whatsapp. `contact_name` represents the name of the target contact if it is saved by a name. If not then phone number should be used, in the exact format shown in whatsapp. Currently supbot doesn't differentiate between groups and personal chat, so you can also use this method to send messages in group too.