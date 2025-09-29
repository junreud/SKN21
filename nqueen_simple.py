def nqueen_fast(N):
    """최적화된 N-Queen - 배열로 충돌 체크"""

    def solve(row, cols, diag1, diag2):
        if row == N:
            return 1

        count = 0
        for col in range(N):
            # 충돌 체크 - 배열 인덱스로 빠르게 확인
            if cols[col] or diag1[row + col] or diag2[row - col + N - 1]:
                continue

            # 퀸 놓기
            cols[col] = True
            diag1[row + col] = True
            diag2[row - col + N - 1] = True

            count += solve(row + 1, cols, diag1, diag2)

            # 백트래킹 - 퀸 제거
            cols[col] = False
            diag1[row + col] = False
            diag2[row - col + N - 1] = False

        return count

    # 충돌 체크용 배열들
    cols = [False] * N              # 열 체크
    diag1 = [False] * (2 * N - 1)   # 대각선1 체크 (/)
    diag2 = [False] * (2 * N - 1)   # 대각선2 체크 (\)

    return solve(0, cols, diag1, diag2)


# 백준 제출용
N = int(input())
print(nqueen_fast(N))
