// generate by py2cpp
// original source code: samples/range.py
#include "py2cpp/py2cpp.hpp"

int main() {
    x = 0;
    for (auto i : py2cpp::range(100)) {
        x += i;
    }
    std::cout << x << std::endl;
    return 0;
}
