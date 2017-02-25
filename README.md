py2cpp
======

A Python to C++ compiler.

Usage
-----

### Hello world

```
$ cat helloworld.py
def main() -> int:
    print("Hello World!")
    return 0

$ python -m py2cpp helloworld.py
// generate by py2cpp
// original source code: helloworld.py
#include "py2cpp/py2cpp.hpp"

int main() {
    std::cout << "Hello World!" << std::endl;
    return 0;
}
```

### range function

```
$ cat range.py
def main() -> int:
    x = 0
    for i in range(100):
        x += i
    print(x)
    return 0

$ python -m py2cpp range.py
// generate by py2cpp
// original source code: range.py
#include "py2cpp/py2cpp.hpp"

int main() {
    x = 0;
    for (auto i : py2cpp::range(100)) {
        x += i;
    }
    std::cout << x << std::endl;
    return 0;
}
```

### argument annotation

```
$ cat add.py
def add(x: float, y: float) -> float:
    return x + y

def main() -> int:
    print("2.0 + 3.0 =", add(2.0, 3.0))
    return 0

$ python -m py2cpp add.py
// generate by py2cpp
// original source code: add.py
#include "py2cpp/py2cpp.hpp"

double add(double x, double y) {
    return x + y;
}

int main() {
    std::cout << "2.0 + 3.0 =" << add(2.0, 3.0) << std::endl;
    return 0;
}
```
