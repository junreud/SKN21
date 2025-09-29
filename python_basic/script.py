import sys
input = sys.stdin.readline

N, K, M = map(int, input().split())

num_list = []
for _ in range(N):
    num = int(input())
    num_list.append(num)

for _ in range(K+M):
    seperate = list(map(int, input().split()))
    
    if seperate[0] == 1:
        num_list[seperate[1]-1] = seperate[2]
    elif seperate[0] == 2:
        start = min(seperate[1], seperate[2]) - 1
        end = max(seperate[1], seperate[2])
        result = sum(num_list[start:end])
        print(result)