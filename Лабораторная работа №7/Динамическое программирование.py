n = int(input())
cost = [int(input()) for _ in range(n)]

INF = 10 ** 9

dp = [[INF] * (n + 2) for _ in range(n + 1)]
parent = [[None] * (n + 2) for _ in range(n + 1)]

dp[0][0] = 0

for i in range(n):
    for coupons in range(n + 1):
        if dp[i][coupons] == INF:
            continue
        price = cost[i]
        if price > 500:
            if dp[i][coupons] + price < dp[i + 1][coupons + 1]:
                dp[i + 1][coupons + 1] = dp[i][coupons] + price
                parent[i + 1][coupons + 1] = (i, coupons, False)
        else:
             if dp[i][coupons] + price < dp[i + 1][coupons]:
                dp[i + 1][coupons] = dp[i][coupons] + price

                parent[i + 1][coupons] = (i, coupons, False)

        if coupons > 0:
            if dp[i][coupons] < dp[i + 1][coupons - 1]:
                dp[i + 1][coupons - 1] = dp[i][coupons]
                parent[i + 1][coupons - 1] = (i, coupons, True)

best_cost = INF
best_coupons = 0

for coupons in range(n + 1):

    if dp[n][coupons] < best_cost:

        best_cost = dp[n][coupons]
        best_coupons = coupons

print(best_cost)

days = []

i = n
coupons = best_coupons

while i > 0:

    pi, pc, used = parent[i][coupons]

    if used:
        days.append(i)

    i = pi
    coupons = pc

days.reverse()

print(len(days))

if days:
    print(*days)