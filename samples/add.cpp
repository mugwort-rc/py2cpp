#include "py2cpp/py2cpp.hpp"

double add(double x, double y) {
    return x + y;
}

int main() {
    print("2.0 + 3.0 =", add(2.0, 3.0));
    return 0;
}
