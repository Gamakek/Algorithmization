def separate(arr):
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2

    left = separate(arr[:mid])
    right = separate(arr[mid:])

    result = []

    for x in left:
        if x < 0:
            result.append(x)

    for x in right:
        if x < 0:
            result.append(x)

    for x in left:
        if x >= 0:
            result.append(x)

    for x in right:
        if x >= 0:
            result.append(x)

    return result


arr = [-1, -7, 1, -2, -8, -9, 6, 3]

print(separate(arr))