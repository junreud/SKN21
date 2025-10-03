import sys

# 빠른 입출력
input = sys.stdin.readline

n = int(input())
numbers = []

for _ in range(n):
    numbers.append(int(input()))

# 정렬
numbers.sort()

# 빠른 출력
print('\n'.join(map(str, numbers)))
