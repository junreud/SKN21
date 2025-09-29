# N-Queen 문제 해결하기
# 핵심: 각 행에 퀸을 하나씩 놓되, 서로 공격하지 않게 배치

def is_safe(queens, row, col):
    """새로운 퀸을 (row, col)에 놓을 수 있는지 확인"""
    for i in range(row):
        # 같은 열에 있는지 확인
        if queens[i] == col:
            return False
        # 대각선에 있는지 확인
        if abs(queens[i] - col) == abs(i - row):
            return False
    return True

def solve_nqueen(N):
    """N-Queen 문제를 백트래킹으로 해결"""
    def backtrack(queens, row):
        if row == N:
            return 1  # 해를 하나 찾음
        
        count = 0
        for col in range(N):
            if is_safe(queens, row, col):
                queens[row] = col
                count += backtrack(queens, row + 1)
        
        return count
    
    queens = [-1] * N  # queens[i] = j는 i번째 행의 j번째 열에 퀸이 있다는 의미
    return backtrack(queens, 0)

# 테스트
N = int(input())
result = solve_nqueen(N)
print(result)

# 시각화를 위한 코드 (N=4일 때 하나의 해 보여주기)
if N <= 8:  # 작은 N에 대해서만 시각화
    def print_one_solution(N):
        def backtrack(queens, row):
            if row == N:
                return True  # 첫 번째 해를 찾으면 종료
            
            for col in range(N):
                if is_safe(queens, row, col):
                    queens[row] = col
                    if backtrack(queens, row + 1):
                        return True
            return False
        
        queens = [-1] * N
        if backtrack(queens, 0):
            print(f"\nN={N}일 때의 한 가지 해:")
            for i in range(N):
                row = ['.' for _ in range(N)]
                row[queens[i]] = 'Q'
                print(' '.join(row))
    
    print_one_solution(N)
