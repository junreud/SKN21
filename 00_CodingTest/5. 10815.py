import sys
input = sys.stdin.readline

n = int(input())
set_n = set(map(int, input().split()))

m = int(input())
m_list = list(map(int, input().split()))

# 한 줄로 결과 생성 - 더 간결하고 빠름
results = [1 if num in set_n else 0 for num in m_list] # [1, 0, 1, ...]

print(' '.join(map(str, results)))

# m이 아닌 n을 set으로 바꿔야했음. in A 에서 A가 set이면 훨씬 빠름. 찾고자 하는 변수가 set이어야함