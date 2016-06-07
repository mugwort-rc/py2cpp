py2cpp
======

A Python to C++ compiler.

Usage
-----

```
$ cat helloworld.py
def main():
    print("Hello World!")
    return

$ python -m py2cpp helloworld.py
void main() {
    print("Hello World!");
    return;
}
```
