// generate by py2cpp
// original source code: samples/dp.py
#include "py2cpp/py2cpp.hpp"

int dp(std::vector<int> a, std::vector<int> b, int cost=1) {
    min_str = ((len(a) < len(b)) ? (a) : (b));
    max_str = ((len(a) > len(b)) ? (a) : (b));
    min_size = len(min_str);
    max_size = len(max_str);
    states = list();
    temp = list();
    for (auto x : py2cpp::range(min_size + 1)) {
        temp.append(x);
    }
    states.append(temp);
    temp = list();
    for (auto x : py2cpp::range(min_size + 1)) {
        temp.append(0);
    }
    states.append(temp);
    for (auto i : py2cpp::range(1, min_size + 1)) {
        prev = ((i % 2 == 0) ? (1) : (0));
        curr = i % 2;
        states[i % 2][0] = i;
        for (auto j : py2cpp::range(1, max_size + 1)) {
            states[i % 2][j] = min(min(states[prev][j], states[curr][j - 1]) + 1, states[prev][j - 1] + ((max_str[i - 1] == min_str[j - 1]) ? (0) : (cost)));
        }
    }
    return states[min_size % 2][min_size];
}
