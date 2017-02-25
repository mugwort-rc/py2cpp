// generate by py2cpp
// original source code: samples/add.py
#include "py2cpp/py2cpp.hpp"

double add(double x, double y) {
    return x + y;
}

int main() {
    std::cout << "2.0 + 3.0 =" << add(2.0, 3.0) << std::endl;
    return 0;
}
