import pygame
import random
import sys
from enum import Enum
from typing import List, Optional, Tuple


# 게임 설정
WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 900
CARD_WIDTH = 90
CARD_HEIGHT = 126
CARD_SPACING = 15

# 색상 정의 - 현대적이고 세련된 색상 팔레트
BACKGROUND = (25, 42, 56)      # 다크 블루그레이
CARD_WHITE = (248, 250, 252)   # 따뜻한 화이트
CARD_BLACK = (30, 30, 30)      # 소프트 블랙
CARD_RED = (220, 53, 69)       # 생동감있는 레드
CARD_BLUE = (13, 110, 253)     # 밝은 블루
CARD_BACK = (99, 102, 241)     # 인디고 블루
FOUNDATION_BG = (59, 130, 246) # 스카이 블루
TABLEAU_EMPTY = (55, 65, 81)   # 그레이
GREEN_FELT = (16, 78, 139)     # 딥 그린 블루
ACCENT = (34, 197, 94)         # 에메랄드 그린
SHADOW = (0, 0, 0)             # 그림자 (RGB만)
HOVER = (255, 255, 255)        # 호버 효과 (RGB만)
GRADIENT_TOP = (30, 58, 138)   # 그라디언트 상단
GRADIENT_BOTTOM = (29, 78, 216) # 그라디언트 하단


class CardSuit(Enum):
    HEARTS = "♥"
    DIAMONDS = "♦"
    SPADES = "♠"
    CLUBS = "♣"


class Card:
    def __init__(self, value, suit: CardSuit):
        self.value = value
        self.suit = suit
        self.is_face_up = False
        self.rect = pygame.Rect(0, 0, CARD_WIDTH, CARD_HEIGHT)
        
    def __str__(self):
        return f"{self.value}{self.suit.value}"
    
    def get_color(self):
        return CARD_RED if self.suit in [CardSuit.HEARTS, 
                                         CardSuit.DIAMONDS] else CARD_BLACK
    
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
            return int(self.value)
    
    def draw(self, screen, x, y, selected=False, hover=False):
        self.rect.x = x
        self.rect.y = y
        
        # 그림자 효과 (단순화)
        shadow_rect = pygame.Rect(x + 3, y + 3, CARD_WIDTH, CARD_HEIGHT)
        shadow_surface = pygame.Surface((CARD_WIDTH, CARD_HEIGHT))
        shadow_surface.set_alpha(80)
        shadow_surface.fill(SHADOW)
        screen.blit(shadow_surface, shadow_rect)
        
        if self.is_face_up:
            # 카드 앞면 - 둥근 모서리 효과
            card_surface = pygame.Surface((CARD_WIDTH, CARD_HEIGHT))
            card_surface.fill(CARD_WHITE)
            
            # 카드 테두리
            pygame.draw.rect(card_surface, (200, 200, 200), 
                           pygame.Rect(0, 0, CARD_WIDTH, CARD_HEIGHT), 2)
            
            # 선택/호버 효과
            if selected:
                pygame.draw.rect(card_surface, ACCENT, 
                               pygame.Rect(0, 0, CARD_WIDTH, CARD_HEIGHT), 4)
            elif hover:
                overlay = pygame.Surface((CARD_WIDTH, CARD_HEIGHT))
                overlay.set_alpha(50)
                overlay.fill(HOVER)
                card_surface.blit(overlay, (0, 0))
            
            # 카드 텍스트 - 더 큰 폰트와 개선된 배치
            font_large = pygame.font.Font(None, 28)
            font_medium = pygame.font.Font(None, 24)
            font_center = pygame.font.Font(None, 40)
            
            # 메인 값 (왼쪽 위)
            value_text = str(self.value)
            main_text = font_large.render(value_text, True, self.get_color())
            card_surface.blit(main_text, (6, 6))
            
            # 수트 (왼쪽 위, 값 아래)
            suit_symbol = self.suit.value
            suit_text = font_large.render(suit_symbol, True, self.get_color())
            card_surface.blit(suit_text, (6, 30))
            
            # 중앙 대형 수트 - 더 명확하게
            center_suit = font_center.render(suit_symbol, True, self.get_color())
            center_rect = center_suit.get_rect(center=(CARD_WIDTH//2, CARD_HEIGHT//2))
            card_surface.blit(center_suit, center_rect)
            
            # 카드 값도 중앙에 작게 표시
            center_value = font_medium.render(value_text, True, self.get_color())
            value_rect = center_value.get_rect(center=(CARD_WIDTH//2, CARD_HEIGHT//2 - 25))
            card_surface.blit(center_value, value_rect)
            
            # 오른쪽 하단 (뒤집힌 값과 수트)
            small_text = font_medium.render(value_text, True, self.get_color())
            rotated_text = pygame.transform.rotate(small_text, 180)
            card_surface.blit(rotated_text, (CARD_WIDTH - 25, CARD_HEIGHT - 25))
            
            small_suit = font_medium.render(suit_symbol, True, self.get_color())
            rotated_suit = pygame.transform.rotate(small_suit, 180)
            card_surface.blit(rotated_suit, (CARD_WIDTH - 25, CARD_HEIGHT - 45))
            
            screen.blit(card_surface, (x, y))
        else:
            # 카드 뒷면 - 단순한 패턴
            back_surface = pygame.Surface((CARD_WIDTH, CARD_HEIGHT))
            back_surface.fill(CARD_BACK)
            
            # 카드 뒷면 패턴
            pygame.draw.rect(back_surface, CARD_WHITE, 
                           pygame.Rect(10, 10, CARD_WIDTH-20, CARD_HEIGHT-20), 2)
            
            # 다이아몬드 패턴
            center_x, center_y = CARD_WIDTH // 2, CARD_HEIGHT // 2
            diamond_points = [
                (center_x, center_y - 20),
                (center_x + 15, center_y),
                (center_x, center_y + 20),
                (center_x - 15, center_y)
            ]
            pygame.draw.polygon(back_surface, CARD_WHITE, diamond_points)
            
            # 테두리
            pygame.draw.rect(back_surface, CARD_WHITE, 
                           pygame.Rect(0, 0, CARD_WIDTH, CARD_HEIGHT), 2)
            
            screen.blit(back_surface, (x, y))


class SolitaireGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("🃏 Solitaire Game")
        self.clock = pygame.time.Clock()
        
        # 게임 상태
        self.deck = []
        self.waste_pile = []
        self.foundations = {suit: [] for suit in CardSuit}
        self.tableau = [[] for _ in range(7)]
        self.selected_card = None
        self.selected_pile = None
        self.selected_index = None
        
        # UI 요소
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        self.new_game()
    
    def create_deck(self) -> List[Card]:
        """새로운 52장 덱 생성"""
        deck = []
        values = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
        
        for suit in CardSuit:
            for value in values:
                deck.append(Card(value, suit))
        
        random.shuffle(deck)
        return deck
    
    def new_game(self):
        """새 게임 시작"""
        self.deck = self.create_deck()
        self.waste_pile = []
        self.foundations = {suit: [] for suit in CardSuit}
        self.tableau = [[] for _ in range(7)]
        
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
        
        # 선택 상태 초기화
        self.selected_card = None
        self.selected_pile = None
        self.selected_index = None
    
    def draw_card(self):
        """덱에서 카드 뽑기"""
        if self.deck:
            card = self.deck.pop()
            card.is_face_up = True
            self.waste_pile.append(card)
        elif self.waste_pile:
            # 덱이 비었으면 웨이스트를 다시 덱으로
            while self.waste_pile:
                card = self.waste_pile.pop()
                card.is_face_up = False
                self.deck.append(card)
    
    def can_place_on_tableau(self, card: Card, target_pile: List[Card]) -> bool:
        """타블로에 카드를 놓을 수 있는지 확인"""
        if not target_pile:
            return card.get_numeric_value() == 13  # 빈 곳에는 K만
        
        target_card = target_pile[-1]
        return (card.get_color() != target_card.get_color() and
                card.get_numeric_value() == target_card.get_numeric_value() - 1)
    
    def can_move_sequence(self, source_pile, start_index):
        """연속된 카드 시퀀스를 이동할 수 있는지 확인"""
        if start_index >= len(source_pile):
            return False
        
        # 선택된 카드부터 끝까지 유효한 시퀀스인지 확인
        for i in range(start_index, len(source_pile) - 1):
            current_card = source_pile[i]
            next_card = source_pile[i + 1]
            
            # 모든 카드가 앞면이어야 함
            if not current_card.is_face_up or not next_card.is_face_up:
                return False
            
            # 색깔이 교대로 나와야 하고, 숫자가 연속되어야 함
            if (current_card.get_color() == next_card.get_color() or
                current_card.get_numeric_value() != next_card.get_numeric_value() + 1):
                return False
        
        return True
    
    def can_place_on_foundation(self, card: Card, foundation: List[Card]) -> bool:
        """파운데이션에 카드를 놓을 수 있는지 확인"""
        if not foundation:
            return card.get_numeric_value() == 1  # 빈 곳에는 A만
        
        top_card = foundation[-1]
        return (card.suit == top_card.suit and
                card.get_numeric_value() == top_card.get_numeric_value() + 1)
    
    def move_card(self, source_pile, source_index, target_pile):
        """카드 이동"""
        if source_index < len(source_pile):
            card = source_pile.pop(source_index)
            target_pile.append(card)
            
            # 숨겨진 카드 뒤집기
            if source_pile and not source_pile[-1].is_face_up:
                source_pile[-1].is_face_up = True
            
            return True
        return False
    
    def move_multiple_cards(self, source_pile, start_index, target_pile):
        """선택된 카드부터 맨 아래까지 모든 카드를 함께 이동"""
        if start_index >= len(source_pile):
            return False
        
        # 이동하려는 시퀀스가 유효한지 확인
        if not self.can_move_sequence(source_pile, start_index):
            # 유효하지 않은 시퀀스면 맨 위 카드만 이동
            if start_index == len(source_pile) - 1:
                return self.move_card(source_pile, start_index, target_pile)
            return False
        
        # 첫 번째 카드가 타겟에 놓일 수 있는지 확인
        first_card = source_pile[start_index]
        if not self.can_place_on_tableau(first_card, target_pile):
            return False
        
        # 이동할 카드들을 역순으로 제거하고 저장
        cards_to_move = []
        for i in range(len(source_pile) - 1, start_index - 1, -1):
            cards_to_move.append(source_pile.pop(i))
        
        # 역순으로 저장된 카드들을 다시 역순으로 추가 (원래 순서 유지)
        for card in reversed(cards_to_move):
            target_pile.append(card)
        
        # 숨겨진 카드 뒤집기
        if source_pile and not source_pile[-1].is_face_up:
            source_pile[-1].is_face_up = True
        
        return True
    
    def handle_click(self, pos, button=1):
        """마우스 클릭 처리"""
        x, y = pos
        
        # 덱 클릭 (더 큰 클릭 영역)
        deck_rect = pygame.Rect(50, 80, CARD_WIDTH + 10, CARD_HEIGHT + 10)
        if deck_rect.collidepoint(pos):
            self.draw_card()
            return
        
        # 웨이스트 파일 클릭
        waste_rect = pygame.Rect(50 + CARD_WIDTH + 20, 80, CARD_WIDTH, CARD_HEIGHT)
        if waste_rect.collidepoint(pos) and self.waste_pile:
            top_card = self.waste_pile[-1]
            
            # 일반 클릭
            if self.selected_card is None:
                self.selected_card = top_card
                self.selected_pile = self.waste_pile
                self.selected_index = len(self.waste_pile) - 1
                
            return
        
        # 파운데이션 클릭
        foundation_start_x = WINDOW_WIDTH - 400
        for i, suit in enumerate(CardSuit):
            foundation_rect = pygame.Rect(foundation_start_x + i * (CARD_WIDTH + 15), 80, 
                                        CARD_WIDTH, CARD_HEIGHT)
            if foundation_rect.collidepoint(pos):
                if self.selected_card:
                    # 파운데이션으로는 맨 위 카드만 이동 가능
                    if (self.selected_index == len(self.selected_pile) - 1 and
                        self.can_place_on_foundation(self.selected_card, self.foundations[suit])):
                        self.move_card(self.selected_pile, self.selected_index, 
                                     self.foundations[suit])
                        self.selected_card = None
                        self.selected_pile = None
                        self.selected_index = None
                return
        
        # 타블로 클릭 - 역순으로 검사해서 위에 있는 카드부터 클릭 감지
        for col in range(7):
            col_x = 50 + col * (CARD_WIDTH + CARD_SPACING + 10)
            
            # 역순으로 검사 (위에 있는 카드가 우선)
            for row in range(len(self.tableau[col]) - 1, -1, -1):
                card = self.tableau[col][row]
                card_y = 290 + row * 35
                
                # 카드가 앞면이고 클릭 가능한 영역인지 확인
                if card.is_face_up:
                    # 맨 위 카드는 전체 영역, 아래 카드들은 보이는 부분만
                    if row == len(self.tableau[col]) - 1:
                        # 맨 위 카드는 전체 높이
                        card_rect = pygame.Rect(col_x, card_y, CARD_WIDTH, CARD_HEIGHT)
                    else:
                        # 아래 카드들은 35픽셀 높이만 (보이는 부분)
                        card_rect = pygame.Rect(col_x, card_y, CARD_WIDTH, 35)
                    
                    if card_rect.collidepoint(pos):
                        # 뒷면 카드 뒤집기 (맨 위 카드만 가능)
                        if not card.is_face_up and row == len(self.tableau[col]) - 1:
                            card.is_face_up = True
                            return
                        
                        # 앞면 카드 클릭 처리
                        if card.is_face_up:
                            if self.selected_card is None:
                                self.selected_card = card
                                self.selected_pile = self.tableau[col]
                                self.selected_index = row
                            else:
                                # 같은 컬럼의 카드 선택
                                if self.selected_pile == self.tableau[col]:
                                    self.selected_card = card
                                    self.selected_index = row
                                else:
                                    # 다른 컬럼으로 이동 시도
                                    if self.can_place_on_tableau(self.selected_card, self.tableau[col]):
                                        self.move_multiple_cards(self.selected_pile, self.selected_index, 
                                                               self.tableau[col])
                                        self.selected_card = None
                                        self.selected_pile = None
                                        self.selected_index = None
                            return
            
            # 빈 컬럼 클릭
            if not self.tableau[col]:
                empty_rect = pygame.Rect(col_x, 290, CARD_WIDTH, CARD_HEIGHT)
                if empty_rect.collidepoint(pos) and self.selected_card:
                    if self.can_place_on_tableau(self.selected_card, self.tableau[col]):
                        self.move_card(self.selected_pile, self.selected_index, 
                                     self.tableau[col])
                        self.selected_card = None
                        self.selected_pile = None
                        self.selected_index = None
                    return
        
        # 빈 곳 클릭하면 선택 해제
        self.selected_card = None
        self.selected_pile = None
        self.selected_index = None
    
    def draw(self):
        """현대적이고 세련된 화면 그리기"""
        # 단순한 그라디언트 배경 (오류 방지)
        self.screen.fill(BACKGROUND)
        
        # 간단한 배경 패턴 추가
        for y in range(0, WINDOW_HEIGHT, 50):
            alpha = max(0, 20 - (y // 25))
            if alpha > 0:
                pattern_surface = pygame.Surface((WINDOW_WIDTH, 2))
                pattern_surface.set_alpha(alpha)
                pattern_surface.fill(GRADIENT_BOTTOM)
                self.screen.blit(pattern_surface, (0, y))
        
        # 제목 - 더 세련된 타이포그래피
        title_font = pygame.font.Font(None, 48)
        title_shadow = title_font.render("🃏 Solitaire", True, (0, 0, 0))
        title_text = title_font.render("🃏 Solitaire", True, CARD_WHITE)
        self.screen.blit(title_shadow, (22, 12))
        self.screen.blit(title_text, (20, 10))
        
        # 새 게임 버튼
        self.new_game_rect = pygame.Rect(WINDOW_WIDTH - 150, 15, 130, 40)
        pygame.draw.rect(self.screen, ACCENT, self.new_game_rect)
        pygame.draw.rect(self.screen, CARD_WHITE, self.new_game_rect, 2)
        button_font = pygame.font.Font(None, 28)
        button_text = button_font.render("New Game", True, CARD_WHITE)
        button_rect = button_text.get_rect(center=self.new_game_rect.center)
        self.screen.blit(button_text, button_rect)
        
        # 상단 영역 - 덱과 파운데이션
        self.draw_top_area()
        
        # 타블로 영역
        self.draw_tableau()
        
        # 하단 정보
        info_font = pygame.font.Font(None, 24)
        info_text = "Click face-down cards to flip them • Drag cards to move • Press N for new game"
        info_surface = info_font.render(info_text, True, CARD_WHITE)
        info_rect = info_surface.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT - 30))
        self.screen.blit(info_surface, info_rect)
        
        # 승리 화면
        if all(len(foundation) == 13 for foundation in self.foundations.values()):
            self.draw_victory_screen()
    
    def draw_top_area(self):
        """상단 영역 그리기 (덱, 웨이스트, 파운데이션)"""
        # 덱
        deck_x, deck_y = 50, 80
        if self.deck:
            # 덱이 있을 때 - 3D 효과로 여러 카드 표현
            for i in range(3):
                offset = i * 2
                empty_card = Card("", CardSuit.SPADES)
                empty_card.draw(self.screen, deck_x + offset, deck_y + offset)
            
            # 덱 정보
            deck_font = pygame.font.Font(None, 24)
            deck_count = deck_font.render(f"({len(self.deck)})", True, CARD_WHITE)
            self.screen.blit(deck_count, (deck_x + 10, deck_y + CARD_HEIGHT + 5))
        else:
            # 빈 덱 표시
            empty_rect = pygame.Rect(deck_x, deck_y, CARD_WIDTH, CARD_HEIGHT)
            pygame.draw.rect(self.screen, TABLEAU_EMPTY, empty_rect, 3)
            pygame.draw.rect(self.screen, (100, 100, 100), empty_rect, 1)
            
            empty_font = pygame.font.Font(None, 20)
            empty_text = empty_font.render("EMPTY", True, (150, 150, 150))
            empty_rect_text = empty_text.get_rect(center=empty_rect.center)
            self.screen.blit(empty_text, empty_rect_text)
        
        # 웨이스트 파일
        waste_x = deck_x + CARD_WIDTH + 20
        if self.waste_pile:
            self.waste_pile[-1].draw(self.screen, waste_x, deck_y, 
                                   selected=(self.selected_card == self.waste_pile[-1]))
        else:
            waste_rect = pygame.Rect(waste_x, deck_y, CARD_WIDTH, CARD_HEIGHT)
            pygame.draw.rect(self.screen, TABLEAU_EMPTY, waste_rect, 2)
            pygame.draw.rect(self.screen, (80, 80, 80), waste_rect, 1)
        
        # 파운데이션 라벨
        foundation_label = pygame.font.Font(None, 32).render("Foundations", True, CARD_WHITE)
        self.screen.blit(foundation_label, (WINDOW_WIDTH - 400, 50))
        
        # 파운데이션 4개
        foundation_start_x = WINDOW_WIDTH - 400
        for i, (suit, cards) in enumerate(self.foundations.items()):
            foundation_x = foundation_start_x + i * (CARD_WIDTH + 15)
            foundation_y = 80
            
            if cards:
                # 파운데이션에 카드가 있을 때
                cards[-1].draw(self.screen, foundation_x, foundation_y)
                
                # 진행도 표시
                progress = len(cards) / 13
                progress_rect = pygame.Rect(foundation_x, foundation_y + CARD_HEIGHT + 5, 
                                          int(CARD_WIDTH * progress), 4)
                pygame.draw.rect(self.screen, ACCENT, progress_rect)
                pygame.draw.rect(self.screen, (100, 100, 100), 
                               pygame.Rect(foundation_x, foundation_y + CARD_HEIGHT + 5, 
                                         CARD_WIDTH, 4), 1)
            else:
                # 빈 파운데이션
                foundation_rect = pygame.Rect(foundation_x, foundation_y, CARD_WIDTH, CARD_HEIGHT)
                pygame.draw.rect(self.screen, FOUNDATION_BG, foundation_rect)
                pygame.draw.rect(self.screen, CARD_WHITE, foundation_rect, 2)
                
                # 수트 아이콘
                suit_font = pygame.font.Font(None, 36)
                suit_text = suit_font.render(suit.value, True, CARD_WHITE)
                suit_rect = suit_text.get_rect(center=foundation_rect.center)
                self.screen.blit(suit_text, suit_rect)
    
    def draw_tableau(self):
        """타블로 영역 그리기"""
        tableau_label = pygame.font.Font(None, 32).render("Tableau", True, CARD_WHITE)
        self.screen.blit(tableau_label, (50, 250))
        
        for col in range(7):
            col_x = 50 + col * (CARD_WIDTH + CARD_SPACING + 10)
            
            # 컬럼 번호
            col_font = pygame.font.Font(None, 20)
            col_text = col_font.render(f"{col + 1}", True, (200, 200, 200))
            self.screen.blit(col_text, (col_x + CARD_WIDTH//2 - 5, 275))
            
            if not self.tableau[col]:
                # 빈 컬럼 - K만 올 수 있다는 힌트
                empty_rect = pygame.Rect(col_x, 290, CARD_WIDTH, CARD_HEIGHT)
                pygame.draw.rect(self.screen, TABLEAU_EMPTY, empty_rect, 2)
                pygame.draw.rect(self.screen, (60, 60, 60), empty_rect, 1)
                
                hint_font = pygame.font.Font(None, 24)
                hint_text = hint_font.render("K", True, (120, 120, 120))
                hint_rect = hint_text.get_rect(center=empty_rect.center)
                self.screen.blit(hint_text, hint_rect)
            else:
                # 카드들 그리기
                for row, card in enumerate(self.tableau[col]):
                    card_y = 290 + row * 35  # 카드 겹침 간격
                    is_selected = (card == self.selected_card)
                    card.draw(self.screen, col_x, card_y, selected=is_selected)
    
    def draw_victory_screen(self):
        """승리 화면"""
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(150)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        # 승리 메시지
        victory_font = pygame.font.Font(None, 72)
        victory_text = victory_font.render("🎉 VICTORY! 🎉", True, ACCENT)
        victory_rect = victory_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 - 50))
        self.screen.blit(victory_text, victory_rect)
        
        # 부제
        subtitle_font = pygame.font.Font(None, 36)
        subtitle_text = subtitle_font.render("Congratulations! You completed Solitaire!", True, CARD_WHITE)
        subtitle_rect = subtitle_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 10))
        self.screen.blit(subtitle_text, subtitle_rect)
        
        # 새 게임 버튼
        button_font = pygame.font.Font(None, 32)
        button_text = button_font.render("Press N for New Game", True, (200, 200, 200))
        button_rect = button_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 60))
        self.screen.blit(button_text, button_rect)
    
    def run(self):
        """게임 실행"""
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_n:  # N키로 새 게임
                        self.new_game()
                    elif event.key == pygame.K_SPACE:  # 스페이스바로 카드 뽑기
                        self.draw_card()
                    elif event.key == pygame.K_ESCAPE:  # ESC로 선택 해제
                        self.selected_card = None
                        self.selected_pile = None
                        self.selected_index = None
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if hasattr(self, 'new_game_rect') and self.new_game_rect.collidepoint(event.pos):
                        self.new_game()
                    else:
                        self.handle_click(event.pos, event.button)
            
            self.draw()
            pygame.display.flip()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = SolitaireGame()
    game.run()