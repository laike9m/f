# f

Kouhei: Damn, the output of `print` is too long, I can't see all of it in my terminal.

Rikka: Why don't you use `logging` and log to a file?

Kouhei: But I don't need those `print` when I'm finished, they are just for quick debugging.

Rikka: Well, **f** is for you!

## Usage

```python
import f

# This will log to temp.log with mode 'w'
@f
def inner():
    print('Some really really really long stuff....')

# This will log to important.log with mode 'a'
@f('important.log', 'a')
def inner():
    print('Yet another some really really really long stuff....')
```
