n = int(input())  # n일간 일함 (0일~n-1일)
schedule = []
for i in range(n):
    t, p = map(int, input().split())
    schedule.append((t, p))
# schedule = [(3, 10), (5, 20), (1, 10), (1, 20), (2, 15), (4, 40), (2, 200)]
#               0일차     1일차     2일차     3일차     4일차     5일차     6일차

dp = [0] * (n + 1)  # 인덱스 범위 초과 방지를 위해 +1
# dp = [0, 0, 0, 0, 0, 0, 0, 0]
for i in range(n - 1, -1, -1):  # i = n-1, n-2, ..., 0
    t, p = schedule[i]
    if t + i <= n:
        dp[i] = max(p + dp[i + t], dp[i + 1])
    else:
        dp[i] = dp[i + 1]  # 상담 불가능하면 다음 날과 동일

print(dp[0])  # 최대 수익 출력