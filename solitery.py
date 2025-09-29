import random

# 카드 수트 정의 (더 깔끔하게)
def create_deck():
    suits = ["♥", "♦", "♠", "♣"]  # heart, diamond, spade, clover
    values = ["A", 2, 3, 4, 5, 6, 7, 8, 9, 10, "J", "Q", "K"]
    
    deck = []
    for suit in suits:
        for value in values:
            deck.append((value, suit, "invisible"))
    
    return deck


def get_card_color(suit):
    """카드 색깔 반환 (빨강 또는 검정)"""
    return "red" if suit in ["♥", "♦"] else "black"


def get_card_value(card):
    """카드의 숫자 값 반환 (A=1, J=11, Q=12, K=13)"""
    value = card[0]
    if value == "A":
        return 1
    elif value == "J":
        return 11
    elif value == "Q":
        return 12
    elif value == "K":
        return 13
    else:
        return value


def can_place_on_tableau(card, target_card):
    """타블로에 카드를 놓을 수 있는지 확인"""
    if target_card is None:  # 빈 컬럼에는 K만 가능
        return get_card_value(card) == 13
    
    # 색깔이 다르고, 숫자가 1 작아야 함
    card_value = get_card_value(card)
    target_value = get_card_value(target_card)
    card_color = get_card_color(card[1])
    target_color = get_card_color(target_card[1])
    
    return (card_color != target_color and 
            card_value == target_value - 1)


def can_place_on_foundation(card, foundation_cards):
    """파운데이션에 카드를 놓을 수 있는지 확인"""
    if not foundation_cards:  # 빈 파운데이션에는 A만 가능
        return get_card_value(card) == 1
    
    # 같은 수트이고 숫자가 1 커야 함
    top_card = foundation_cards[-1]
    return (card[1] == top_card[1] and 
            get_card_value(card) == get_card_value(top_card) + 1)


# 덱 생성 및 섞기
deck = create_deck()
random.shuffle(deck)

# 카드 나누기
board1 = deck[:1]
board2 = deck[1:3]
board3 = deck[3:6]
board4 = deck[6:10]
board5 = deck[10:15]
board6 = deck[15:21]
board7 = deck[21:28]

deck = deck[28:]

# 파운데이션 (완성 더미) - 각 수트별로 A부터 K까지 쌓는 곳
foundations = {"♥": [], "♦": [], "♠": [], "♣": []}

# 게임 시작 - 각 보드의 맨 위 카드를 뒤집기
gamestart = 1
if gamestart:
    if board1:
        board1[-1] = (board1[-1][0], board1[-1][1], "visible")
    if board2:
        board2[-1] = (board2[-1][0], board2[-1][1], "visible")
    if board3:
        board3[-1] = (board3[-1][0], board3[-1][1], "visible")
    if board4:
        board4[-1] = (board4[-1][0], board4[-1][1], "visible")
    if board5:
        board5[-1] = (board5[-1][0], board5[-1][1], "visible")
    if board6:
        board6[-1] = (board6[-1][0], board6[-1][1], "visible")
    if board7:
        board7[-1] = (board7[-1][0], board7[-1][1], "visible")

# 보드들을 리스트로 관리하기 쉽게 정리
boards = [board1, board2, board3, board4, board5, board6, board7]


def print_game():
    print("\n" + "="*60)
    print("🃏 SOLITAIRE GAME 🃏")
    print("="*60)
    
    # 파운데이션 출력
    print("Foundations:")
    for suit, cards in foundations.items():
        if cards:
            top_card = cards[-1]
            print(f"{suit}: {top_card[0]}{top_card[1]}", end="  ")
        else:
            print(f"{suit}: [    ]", end="  ")
    print("\n")
    
    print("Tableau:")
    # 각 컬럼의 카드들 출력
    for i, board in enumerate(boards, 1):
        print(f"Column {i}: ", end="")
        if not board:
            print("[Empty]")
        else:
            for card in board:
                if card[2] == "visible":  # visible 카드
                    print(f"{card[0]}{card[1]}", end=" ")
                else:  # invisible 카드
                    print("🂠", end=" ")
            print()
    
    print(f"\nDeck remaining: {len(deck)} cards")
    print("Commands: 'move <from_col> <to_col>', 'draw', 'quit'")


def move_card(from_col, to_col):
    """카드 이동 함수"""
    if from_col < 1 or from_col > 7 or to_col < 1 or to_col > 7:
        print("Invalid column number! Use 1-7.")
        return False
        
    from_board = boards[from_col - 1]
    to_board = boards[to_col - 1]
    
    if not from_board:
        print("Source column is empty!")
        return False
    
    # 맨 위의 visible 카드만 이동 가능
    if from_board[-1][2] != "visible":
        print("Cannot move hidden card!")
        return False
        
    moving_card = from_board[-1]
    target_card = to_board[-1] if to_board else None
    
    # 이동 가능한지 체크
    if can_place_on_tableau(moving_card, target_card):
        # 카드 이동
        from_board.pop()
        to_board.append(moving_card)
        
        # 이동 후 아래 카드 뒤집기
        if from_board and from_board[-1][2] == "invisible":
            card = from_board[-1]
            from_board[-1] = (card[0], card[1], "visible")
            
        print(f"Moved {moving_card[0]}{moving_card[1]} from column {from_col} to column {to_col}")
        return True
    else:
        print("Invalid move! Check solitaire rules.")
        return False


def main_game_loop():
    """메인 게임 루프"""
    print("Welcome to Solitaire!")
    print("Move cards following solitaire rules:")
    print("- Red on Black, Black on Red")
    print("- Descending order (K, Q, J, 10, 9, ...)")
    print("- Only Kings can go on empty columns")
    
    while True:
        print_game()
        
        # 승리 조건 체크
        if all(len(foundation) == 13 for foundation in foundations.values()):
            print("🎉 Congratulations! You won! 🎉")
            break
            
        command = input("\nEnter command: ").strip().lower()
        
        if command == "quit":
            print("Thanks for playing!")
            break
        elif command == "draw":
            if deck:
                print(f"Drew card: {deck[0][0]}{deck[0][1]}")
            else:
                print("Deck is empty!")
        elif command.startswith("move"):
            try:
                parts = command.split()
                from_col = int(parts[1])
                to_col = int(parts[2])
                move_card(from_col, to_col)
            except (IndexError, ValueError):
                print("Invalid command format! Use: move <from_col> <to_col>")
        else:
            print("Unknown command! Use 'move', 'draw', or 'quit'")


# 게임 시작
if __name__ == "__main__":
    main_game_loop()





