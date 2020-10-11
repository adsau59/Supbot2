# Models

Data models for the classes used in Supbot

---

## ActionCallback

Optional callback parameter for all Action methods

#### Definition
```python
ActionCallback = Callable[[Action], None]
```

#### Example
```python
def action_callback(action: Action):
    print(action)
```

#### Description

When passed as a parameter in Action method, it is called when action is completed. Can be used to handle cases where the Action was not able to complete successfully.

---

## Action

Represents action to be performed

### Definition
```python
@dataclass
class Action:
    action_id: str
    action_name: ActionName
    callback: ActionCallback
    status: ActionStatus
    data: Tuple

    @property
    def success(self):
        return self.status == ActionStatus.SUCCESS
```

#### Description

Contains details on the action in supbot, maintains a unique id for each action, status represents the current state of the action. It is returned by every action method.