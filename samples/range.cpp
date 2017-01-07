#include "py2cpp/py2cpp.hpp"

int main() {
    x = 0;
    for (auto i : py2cpp::range(100)) {
        x += i;
    }
    print(x);
    return 0;
}
