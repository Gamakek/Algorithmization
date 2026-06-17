n = int(input())

square = [0] * 9
used = [False] * 10

square[0] = n
used[n] = True

found = False


def check():
    s = square[0] + square[1] + square[2]

    return (
        square[0] + square[1] + square[2] == s and
        square[3] + square[4] + square[5] == s and
        square[6] + square[7] + square[8] == s and

        square[0] + square[3] + square[6] == s and
        square[1] + square[4] + square[7] == s and
        square[2] + square[5] + square[8] == s and

        square[0] + square[4] + square[8] == s and
        square[2] + square[4] + square[6] == s
    )


def backtrack(pos):
    global found

    if found:
        return

    if pos == 9:
        if check():
            for i in range(0, 9, 3):
                print(square[i], square[i + 1], square[i + 2])
            found = True
        return

    for num in range(1, 10):
        if not used[num]:
            used[num] = True
            square[pos] = num

            backtrack(pos + 1)

            used[num] = False


backtrack(1)

if not found:
    print(-1)