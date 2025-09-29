import tkinter as tk
from tkinter import ttk, messagebox
import random
from typing import List, Tuple, Optional


class Card:
    """카드 클래스"""
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit
        self.is_face_up = False
        
    def __repr__(self):
        return f"{self.value}{self.suit}"
    
    def get_color(self):
        return "red" if self.suit in ["♥", "♦"] else "black"
    
    def get_numeric_value(self):
        if self.value == "A":
            return 1
        elif self.value == "J":
            return 11
        elif self.value == "Q":
            return 12
        elif self.value == "K":
            return 13
        else:
            return self.value


class SolitaireGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🃏 Solitaire Game")
        self.root.geometry("1200x800")
        self.root.configure(bg="#0d7377")
        
        # 게임 상태
        self.deck = []
        self.waste_pile = []
        self.foundations = {"♥": [], "♦": [], "♠": [], "♣": []}
        self.tableau = [[] for _ in range(7)]
        self.selected_card = None
        self.selected_location = None
        
        # GUI 요소들을 저장할 딕셔너리
        self.card_buttons = {}
        self.foundation_frames = {}
        self.tableau_frames = []
        
        self.setup_game()
        self.create_widgets()
        self.update_display()
        
    def create_deck(self):
        """새로운 덱 생성"""
        suits = ["♥", "♦", "♠", "♣"]
        values = ["A", 2, 3, 4, 5, 6, 7, 8, 9, 10, "J", "Q", "K"]
        
        deck = []
        for suit in suits:
            for value in values:
                deck.append(Card(value, suit))
        
        random.shuffle(deck)
        return deck
    
    def setup_game(self):
        """게임 초기 설정"""
        self.deck = self.create_deck()
        
        # 타블로에 카드 배치
        card_index = 0
        for col in range(7):
            for row in range(col + 1):
                if card_index < len(self.deck):
                    card = self.deck[card_index]
                    if row == col:  # 맨 위 카드만 뒤집기
                        card.is_face_up = True
                    self.tableau[col].append(card)
                    card_index += 1
        
        # 나머지 카드는 덱으로
        self.deck = self.deck[card_index:]
        
    def create_widgets(self):
        """GUI 위젯 생성"""
        # 메인 프레임
        main_frame = tk.Frame(self.root, bg="#0d7377")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 상단 영역 (덱, 웨이스트 파일, 파운데이션)
        top_frame = tk.Frame(main_frame, bg="#0d7377")
        top_frame.pack(fill=tk.X, pady=(0, 20))
        
        # 덱과 웨이스트 파일
        deck_frame = tk.Frame(top_frame, bg="#0d7377")
        deck_frame.pack(side=tk.LEFT)
        
        self.deck_button = tk.Button(
            deck_frame, text="🂠\nDECK", font=("Arial", 12, "bold"),
            width=8, height=4, command=self.draw_card,
            bg="#14a085", fg="white", relief=tk.RAISED
        )
        self.deck_button.pack(side=tk.LEFT, padx=5)
        
        self.waste_button = tk.Button(
            deck_frame, text="[ ]\nWASTE", font=("Arial", 12),
            width=8, height=4, state=tk.DISABLED,
            bg="#2c3e50", fg="white", relief=tk.SUNKEN
        )
        self.waste_button.pack(side=tk.LEFT, padx=5)
        
        # 파운데이션
        foundation_frame = tk.Frame(top_frame, bg="#0d7377")
        foundation_frame.pack(side=tk.RIGHT)
        
        foundation_label = tk.Label(
            foundation_frame, text="Foundations", font=("Arial", 14, "bold"),
            bg="#0d7377", fg="white"
        )
        foundation_label.pack()
        
        foundations_container = tk.Frame(foundation_frame, bg="#0d7377")
        foundations_container.pack()
        
        for suit in ["♥", "♦", "♠", "♣"]:
            frame = tk.Frame(foundations_container, bg="#2c3e50", relief=tk.SUNKEN, bd=2)
            frame.pack(side=tk.LEFT, padx=5)
            
            label = tk.Label(
                frame, text=f"{suit}\n[ ]", font=("Arial", 16),
                width=6, height=3, bg="#2c3e50", fg="white"
            )
            label.pack(padx=5, pady=5)
            label.bind("<Button-1>", lambda e, s=suit: self.foundation_clicked(s))
            
            self.foundation_frames[suit] = label
        
        # 타블로 영역
        tableau_frame = tk.Frame(main_frame, bg="#0d7377")
        tableau_frame.pack(fill=tk.BOTH, expand=True)
        
        # 컬럼 라벨
        columns_label = tk.Label(
            tableau_frame, text="Tableau Columns", font=("Arial", 14, "bold"),
            bg="#0d7377", fg="white"
        )
        columns_label.pack(pady=(0, 10))
        
        # 7개 컬럼 생성
        columns_container = tk.Frame(tableau_frame, bg="#0d7377")
        columns_container.pack(fill=tk.BOTH, expand=True)
        
        for i in range(7):
            col_frame = tk.Frame(columns_container, bg="#0d7377")
            col_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
            
            col_label = tk.Label(
                col_frame, text=f"Col {i+1}", font=("Arial", 12, "bold"),
                bg="#0d7377", fg="white"
            )
            col_label.pack()
            
            # 카드들이 들어갈 프레임
            cards_frame = tk.Frame(col_frame, bg="#14a085", relief=tk.SUNKEN, bd=2, height=400)
            cards_frame.pack(fill=tk.BOTH, expand=True, pady=5)
            cards_frame.pack_propagate(False)
            
            self.tableau_frames.append(cards_frame)
        
        # 하단 버튼들
        button_frame = tk.Frame(main_frame, bg="#0d7377")
        button_frame.pack(fill=tk.X, pady=(20, 0))
        
        new_game_btn = tk.Button(
            button_frame, text="🎮 New Game", font=("Arial", 12, "bold"),
            command=self.new_game, bg="#e74c3c", fg="white", padx=20
        )
        new_game_btn.pack(side=tk.LEFT)
        
        quit_btn = tk.Button(
            button_frame, text="❌ Quit", font=("Arial", 12, "bold"),
            command=self.root.quit, bg="#34495e", fg="white", padx=20
        )
        quit_btn.pack(side=tk.RIGHT)
        
        # 게임 정보
        info_label = tk.Label(
            button_frame, text="Click cards to select and move • Draw cards from deck • Build foundations A-K",
            font=("Arial", 10), bg="#0d7377", fg="white"
        )
        info_label.pack(expand=True)
    
    def update_display(self):
        """화면 업데이트"""
        # 덱 버튼 업데이트
        if self.deck:
            self.deck_button.config(text=f"🂠\nDECK\n({len(self.deck)})")
        else:
            self.deck_button.config(text="🂠\nEMPTY", state=tk.DISABLED)
        
        # 웨이스트 파일 업데이트
        if self.waste_pile:
            top_card = self.waste_pile[-1]
            self.waste_button.config(
                text=f"{top_card}\nWASTE", state=tk.NORMAL,
                command=lambda: self.card_clicked('waste', len(self.waste_pile)-1)
            )
        
        # 파운데이션 업데이트
        for suit, cards in self.foundations.items():
            if cards:
                top_card = cards[-1]
                self.foundation_frames[suit].config(text=f"{suit}\n{top_card}")
            else:
                self.foundation_frames[suit].config(text=f"{suit}\n[ ]")
        
        # 타블로 업데이트
        for col_idx, column in enumerate(self.tableau):
            frame = self.tableau_frames[col_idx]
            
            # 기존 버튼들 제거
            for widget in frame.winfo_children():
                widget.destroy()
            
            # 새로운 카드 버튼들 생성
            for card_idx, card in enumerate(column):
                if card.is_face_up:
                    color = "red" if card.get_color() == "red" else "black"
                    text = str(card)
                    bg_color = "white"
                else:
                    text = "🂠"
                    color = "blue"
                    bg_color = "#3498db"
                
                btn = tk.Button(
                    frame, text=text, font=("Arial", 10, "bold"),
                    fg=color, bg=bg_color, width=4, height=1,
                    command=lambda c=col_idx, i=card_idx: self.card_clicked('tableau', c, i)
                )
                btn.pack(pady=1)
        
        # 승리 조건 체크
        if all(len(foundation) == 13 for foundation in self.foundations.values()):
            messagebox.showinfo("🎉 Congratulations!", "You won the game! 🎉")
    
    def draw_card(self):
        """덱에서 카드 뽑기"""
        if self.deck:
            card = self.deck.pop()
            card.is_face_up = True
            self.waste_pile.append(card)
            self.update_display()
    
    def card_clicked(self, location, col_idx, card_idx=None):
        """카드 클릭 처리"""
        if self.selected_card is None:
            # 카드 선택
            if location == 'tableau' and card_idx is not None:
                column = self.tableau[col_idx]
                if card_idx < len(column) and column[card_idx].is_face_up:
                    self.selected_card = column[card_idx]
                    self.selected_location = ('tableau', col_idx, card_idx)
                    print(f"Selected: {self.selected_card}")
            elif location == 'waste':
                if self.waste_pile:
                    self.selected_card = self.waste_pile[-1]
                    self.selected_location = ('waste', len(self.waste_pile)-1)
                    print(f"Selected: {self.selected_card}")
        else:
            # 카드 이동
            self.move_card_to(location, col_idx, card_idx)
    
    def move_card_to(self, target_location, target_col, target_card_idx=None):
        """선택된 카드를 목표 위치로 이동"""
        if not self.selected_card or not self.selected_location:
            return
        
        moved = False
        
        if target_location == 'tableau':
            moved = self.move_to_tableau(target_col)
        elif target_location == 'foundation':
            moved = self.move_to_foundation(target_col)
        
        if moved:
            self.reveal_hidden_cards()
            self.selected_card = None
            self.selected_location = None
            self.update_display()
        else:
            messagebox.showwarning("Invalid Move", "Cannot move card there!")
            self.selected_card = None
            self.selected_location = None
    
    def move_to_tableau(self, target_col):
        """타블로로 카드 이동"""
        target_column = self.tableau[target_col]
        
        # 빈 컬럼인 경우
        if not target_column:
            if self.selected_card.get_numeric_value() == 13:  # K만 가능
                return self.execute_move(target_col)
            return False
        
        # 마지막 카드와 비교
        target_card = target_column[-1]
        if (self.selected_card.get_color() != target_card.get_color() and
            self.selected_card.get_numeric_value() == target_card.get_numeric_value() - 1):
            return self.execute_move(target_col)
        
        return False
    
    def move_to_foundation(self, foundation_suit):
        """파운데이션으로 카드 이동"""
        foundation = self.foundations[foundation_suit]
        
        # 같은 수트인지 확인
        if self.selected_card.suit != foundation_suit:
            return False
        
        # 빈 파운데이션에는 A만
        if not foundation:
            if self.selected_card.get_numeric_value() == 1:
                return self.execute_foundation_move(foundation_suit)
            return False
        
        # 순서대로 쌓기
        if self.selected_card.get_numeric_value() == foundation[-1].get_numeric_value() + 1:
            return self.execute_foundation_move(foundation_suit)
        
        return False
    
    def execute_move(self, target_col):
        """실제 이동 실행 (타블로)"""
        source_location = self.selected_location
        
        if source_location[0] == 'tableau':
            source_col = source_location[1]
            self.tableau[source_col].pop()
        elif source_location[0] == 'waste':
            self.waste_pile.pop()
        
        self.tableau[target_col].append(self.selected_card)
        return True
    
    def execute_foundation_move(self, foundation_suit):
        """실제 이동 실행 (파운데이션)"""
        source_location = self.selected_location
        
        if source_location[0] == 'tableau':
            source_col = source_location[1]
            self.tableau[source_col].pop()
        elif source_location[0] == 'waste':
            self.waste_pile.pop()
        
        self.foundations[foundation_suit].append(self.selected_card)
        return True
    
    def reveal_hidden_cards(self):
        """숨겨진 카드 뒤집기"""
        for column in self.tableau:
            if column and not column[-1].is_face_up:
                column[-1].is_face_up = True
    
    def foundation_clicked(self, suit):
        """파운데이션 클릭 처리"""
        if self.selected_card:
            self.move_card_to('foundation', suit)
        
    def new_game(self):
        """새 게임 시작"""
        # 게임 상태 초기화
        self.deck = []
        self.waste_pile = []
        self.foundations = {"♥": [], "♦": [], "♠": [], "♣": []}
        self.tableau = [[] for _ in range(7)]
        self.selected_card = None
        self.selected_location = None
        
        # 게임 설정 및 화면 업데이트
        self.setup_game()
        self.update_display()
        
    def run(self):
        """게임 실행"""
        self.root.mainloop()


if __name__ == "__main__":
    game = SolitaireGUI()
    game.run()