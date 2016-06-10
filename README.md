py2cpp
======

A Python to C++ compiler.

Usage
-----

```
$ cat helloworld.py
def main():
    """
    :rtype: int
    """
    print("Hello World!")
    return 0

$ python -m py2cpp helloworld.py
int main() {
    print("Hello World!");
    return 0;
}
```
