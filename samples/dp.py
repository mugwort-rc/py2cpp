def dp(a : List[int], b : List[int], cost:int=1) -> int:
    min_str = a if len(a) < len(b) else b
    max_str = a if len(a) > len(b) else b
    min_size = len(min_str)
    max_size = len(max_str)

    states = list()
    temp = list()
    for x in range(min_size+1):
        temp.append(x)
    states.append(temp)
    temp = list()
    for x in range(min_size+1):
        temp.append(0)
    states.append(temp)
    #states = [
    #    [x for x in range(min_size+1)],
    #    [0 for x in range(min_size+1)],
    #]

    for i in range(1, min_size+1):
        prev = 1 if i % 2 == 0 else 0
        curr = i % 2
        states[i%2][0] = i
        for j in range(1, max_size+1):
            states[i%2][j] = min(
                min(states[prev][j], states[curr][j - 1])+1,
                states[prev][j - 1]+(0 if max_str[i - 1] == min_str[j - 1] else cost)
            )
    return states[min_size % 2][min_size]
