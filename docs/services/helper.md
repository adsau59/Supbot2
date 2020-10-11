# Helper

Used to control supbot services

---

## quit

Flags supbot to turn off

#### Declaration

```python
def quit(self):
```

#### Description

Turns `status` flag false, which allows its internal systems to finish their pending work and finish their work.

---

## wait_for_action

Blocks the thread until the action is executed.

#### Declaration

```python
def wait_for_action(self, action: Action):
```

#### Description

Can be used if result of the action has to be used in the code without using callbacks.

---

## wait_for_finish

Waits for services to finish.

#### Declaration

```python
def wait_for_finish(self):
```

#### Description

Even after quit() is called, it doesn't immediately shut down. So if you want to wait for supbot to turn off completly, this method can be used. You can even use this, if you don't want your main thread to finish while supbot is running on other thread.

---

## is_on

Checks if `quit()` is used

#### Declaration
```python
def is_on(self) -> bool
```

#### Description

Checks for `status` flag, returns True if `status` flag. Used to syncronize other systems of your application to work along with supbot.

---

## has_started

Returns true if Supbot has started

### Declaration

```python
def has_started(self) -> bool:
```
