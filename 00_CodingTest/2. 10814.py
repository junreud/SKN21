import sys

input = sys.stdin.readline
n = int(input())

# 모든 사람 정보를 저장할 리스트
people = []

for i in range(n):
    age, name = input().split()
    people.append(f"{age} {name}")

# 나이를 기준으로 정렬 (안정 정렬로 입력 순서 유지)
print('\n'.join(sorted(people, key=lambda x: int(x.split()[0]))))

"""
join 은 한번의 시스템 호출로 출력하기 때문에
print를 여러번 호출하는 것보다 훨씬 빠릅니다.
''.join(리스트) 를 하면 '' 문자열을 기준으로 리스트의 모든 요소를
합쳐서 하나의 문자열로 만들어 줍니다.
""" 