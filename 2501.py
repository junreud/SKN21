N, K = map(int, input().split())

list_num = []
for i in range(N):
    if N % (i + 1) == 0:
        list_num.append(i + 1)

print(list_num[K - 1] if K <= len(list_num) else 0)
