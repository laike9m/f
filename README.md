# f

Kouhei: Damn, the output of `print` is too long, I can't see all of it in my terminal.

Rikka: Why don't you use `logging` and log to a file?

Kouhei: But I don't need those `print` when I'm finished, they are just for quick debugging.

Rikka: Well, **f** is for you!

## Usage

```python
import f


@f    # This will log to tmp.log with mode 'w'
def inner():
    print('Some really really really long stuff....')


# This will log to important.log with mode 'a'
@f(filename='important.log', mode='a')
def inner():
    print('Yet another some really really really long stuff....')
```

# Install
```bash
pip install p2f
```
Originally I was planning to call this package `f`, but without luck, the name has already been taken by another package on pypi. So I name it `p2f`, but when imported and used, it's still `f`. I'm lazy, everyone does.


## FAQ
* What does it do? Will `@f` do anything dangerous?   
All it does is replacing `sys.stdout` with an opened file within your function,
and restore when function ends.

* Why use it? Why not something like `python mymodule.py > tmp.log`?  
`f` gives you **function-level** control over your output. The best thing is, you can just remove the decorator line or comment it out whenever you don't need it.

[![Build Status](https://travis-ci.org/laike9m/f.svg)](https://travis-ci.org/laike9m/f)
