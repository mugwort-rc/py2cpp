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


AST Node
--------

<https://docs.python.jp/3/library/ast.html>

### Supported

#### Modules

* Module

#### Statements

* FunctionDef
* ClassDef
* Return
* Assign
* AugAssign
* For
* While
* If
* Raise
* Expr
* Pass
* Break
* Continue

### Expressions

* BoolOp
* BinOp
* UnaryOp
* Lambda
* IfExp
* Compare
* Call
* Num
* Str
* NameConstant
* Attribute
* Subscript
* Name
* Tuple
* Index
* arguments
* arg
* keyword

### Unsupported yet

```
$ cat unsupported.py
try:
    raise Exception()
except:
    pass

$ python -m py2cpp unsupported.py
// generate by py2cpp
// original source code: unsupported.py
#include "py2cpp/py2cpp.hpp"

// UNSUPPORTED AST NODE: Try
```

#### Modules

* Interactive
* Expression
* Suite

#### Statements

* AsyncFunctionDef
* Delete
* AnnAssign
* AsyncFor
* With
* AsyncWith
* Try
* Assert
* Import
* ImportFrom
* Global
* Nonlocal
* attributes

#### Expressions

* Dict
* Set
* ListComp
* SetComp
* DictComp
* GeneratorExp
* Await
* Yield
* YieldFrom
* FormattedValue
* JoinedStr
* Bytes
* Ellipsis
* Constant
* Starred
* List
* attributes
* expr_context
* slice
* boolop
* operator
* unaryop
* cmpop
* comprehension
* excepthandler
* alias
* withitem
