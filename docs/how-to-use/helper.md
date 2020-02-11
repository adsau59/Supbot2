# Helper

Used to control supbot services

---

## quit

Flags supbot to turn off

<br/>

#### Declaration

```python
def quit(self):
```

#### Description

Turns `status` flag false, which allows its internal systems to finish their pending work and finish their work.

---

## wait_for_finish

Waits for services to finish.

<br/>

#### Declaration

```python
def wait_for_finish(self):
```

#### Description

Even after quit() is called, it doesn't imediatly shut down. So if you want to wait for supbot to turn off completly, this method can be used. You can even use this, if you don't want your main thread to finish while supbot is running on other thread.

---

## is_on

Checks if `quit()` is used

<br/>

#### Declaration
```python
def is_on(self) -> bool
```

#### Description

Checks for `status` flag, returns True if `status` flag. Used to syncronize other systems of your application to work along with supbot.
