import sys
input = sys.stdin.readline

c = list(map(int, input().split()))

print(sorted(c, reverse=True)[1])

