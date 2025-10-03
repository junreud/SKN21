import sys
input = sys.stdin.readline

n = int(input())
coords = list(map(int, input().split()))

# 1단계: 중복 제거 후 정렬
unique_coords = sorted(set(coords))

# 2단계: 각 값에 대해 압축된 좌표를 딕셔너리로 매핑
# 정렬된 순서대로 0, 1, 2, ... 인덱스를 부여
coord_map = {value: index for index, value in enumerate(unique_coords)}

# 3단계: 원본 배열의 각 값을 압축된 값으로 변환
results = [coord_map[coord] for coord in coords]

print(' '.join(map(str, results)))
