import pygame
import sys
import pygame_gui
import math
import numpy as np
import Utilities as UT
import Minimax
from Tree import TreeNode
import tree_representation
from Heuristic import get_player_scores

k = 4
gameType = True
GAME = UT.GameState(0)
ROW = 6
COLUMN = 7
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 100)
SQUARESIZE = 100
player = 0
AI = 1

pygame.font.init()
pygame.init()


class Button:
    def __init__(self, text, width, height, pos, elevation):
        # Core attributes
        self.pressed = False
        self.elevation = elevation
        self.dynamic_elecation = elevation
        self.original_y_pos = pos[1]

        # top rectangle
        self.top_rect = pygame.Rect(pos, (width, height))
        self.top_color = '#475F77'

        # bottom rectangle
        self.bottom_rect = pygame.Rect(pos, (width, height))
        self.bottom_color = '#000000'
        # text
        self.text_surf = gui_font.render(text, True, '#FFFFFF')
        self.text_rect = self.text_surf.get_rect(center=self.top_rect.center)

    def draw(self):
        # elevation logic
        self.top_rect.y = self.original_y_pos - self.dynamic_elecation
        self.text_rect.center = self.top_rect.center

        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.dynamic_elecation

        pygame.draw.rect(screen, self.bottom_color, self.bottom_rect, border_radius=12)
        pygame.draw.rect(screen, self.top_color, self.top_rect, border_radius=12)
        screen.blit(self.text_surf, self.text_rect)
        self.check_click()

    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            self.top_color = '#D74B4B'
            if pygame.mouse.get_pressed()[0]:
                self.dynamic_elecation = 0
                self.pressed = True
            else:
                self.dynamic_elecation = self.elevation
                if self.pressed == True:
                    print('click')
                    self.pressed = False
        else:
            self.dynamic_elecation = self.elevation
            self.top_color = '#475F77'


def draw_board(board):
    board = np.flip(board, 0)

    for r in range(ROW):
        for c in range(COLUMN):
            pygame.draw.rect(screen, BLUE, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (
            int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), RADIUS)

    for r in range(ROW):
        for c in range(COLUMN):
            if board[r][c] == 1:
                pygame.draw.circle(screen, RED, (
                int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, YELLOW, (
                int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
    pygame.display.update()


turn = 0
pygame.display.set_caption('Connect4 Game')
clock = pygame.time.Clock()
gui_font = pygame.font.SysFont(None, 30)
font = pygame.font.SysFont('arial', 75)

# define font color
fontColor = (255, 255, 255)


def board_is_full(state):
    pieces_num = 0
    for col in range(7):
        pieces_num += (state & (7 << col * 9)) >> col * 9
    if pieces_num == 42:
        return True
    return False

def draw_text(text, font, color, x, y):
    show = font.render(text, True, color)
    screen.blit(show, (x, y))


def draw_menu():
    screen.fill((52, 78, 91))
    draw_text("Connect4 Game", font, fontColor, 80, 100)
    button1.draw()
    button2.draw()


def draw_game():
    turn = 0
    global GAME
    pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
    if event.type == pygame.MOUSEMOTION:
        posx = event.pos[0]
        if turn == 0:
            pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE / 2)), RADIUS)
        else:
            pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE / 2)), RADIUS)
    pygame.display.update()
    if board_is_full(GAME.state):
        ai_score, human_score = get_player_scores(GAME.convert_to_matrix(),2,1)
        s = ""
        if ai_score > human_score:
            s = "AI Wins!"
        elif ai_score < human_score:
            s = "Player Wins!"
        else:
            s = "Tie"
        label = Font.render(f"{s} + Player:Ai = {human_score}:{ai_score}", 2 , YELLOW)
        screen.blit(label, (40, 10))
        pygame.display.update()
        return



    if event.type == pygame.MOUSEBUTTONDOWN:

        # ask for player1 input
        if turn == player:

            posx = event.pos[0]
            col = int(math.floor(posx / SQUARESIZE))

            game = GAME.get_child_state(col, turn)
            if game == None:
                return
            else:
                GAME = UT.GameState(game)

                # check if player 1 wins
        #     if winning_game(board, 1):
        #        label = Font.render("Player1 wins!", 1, RED)
        #       screen.blit(label, (40, 10))
        #      run = False
        #     pygame.display.update()
        draw_board(GAME.convert_to_matrix())

        turn += 1
        turn = turn % 2

        # Ask for player2 input
        if turn == AI:
            root = TreeNode()
            if gameType:
                _, GAME = Minimax.minimax(GAME, 0, True, k, root)
            else:
                _, GAME = Minimax.alphabeta_pruning(GAME, 0, True, k, -math.inf, math.inf, root)
            tree_representation.tree_rep(root, k)

        print(GAME.convert_to_matrix())

        # check if player 2 wins

        #   if winning_game(board, 2):
        #      label = Font.render("Player2 wins!", 2, YELLOW)
        #     screen.blit(label, (40, 10))
        #    pygame.display.update()
        #  run = False
        # board=creat_board()
    # draw_board(board)
    # print_board(board)

    # turn += 1
    # turn = turn % 2
    # pygame.display.update()


button1 = Button('PLAY WITHOUT PRUNING', 260, 130, (220, 400), 5)
button2 = Button('PLAY WITH PRUNING', 260, 130, (220, 250), 5)

width = COLUMN * SQUARESIZE
height = (ROW + 1) * SQUARESIZE

size = (width, height)

RADIUS = int(SQUARESIZE / 2 - 5)

screen = pygame.display.set_mode(size)

draw_board(GAME.convert_to_matrix())
pygame.display.update()

Font = pygame.font.SysFont("monospace", 75)
clock = pygame.time.Clock()
label = pygame_gui.UIManager((width, height))
text_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((250, 550), (200, 50)), manager=label,
                                                 object_id="#main_text_entry")
# print(text_input)
main_menu = True
run = True

while run:
    for event in pygame.event.get():
        if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == "#main_text_entry":
            k = int(event.text)

        if main_menu:
            draw_menu()
            UI_REFRESH_RATE = clock.tick(60)
            label.process_events(event)
            label.update(UI_REFRESH_RATE)
            label.draw_ui(screen)
            # k = int(input("Enter maximum depth"))
            pygame.display.update()

            if button1.pressed == True:
                gameType = True

                main_menu = False

                pygame.display.update()
            elif button2.pressed == True:
                #                global gameType
                gameType = False
                main_menu = False

            pygame.display.update()


        elif event.type == pygame.QUIT:
            run = False

        else:
            draw_board(GAME.convert_to_matrix())
            draw_game()
            pygame.display.update()

    clock.tick(60)
pygame.quit()
sys.exit()
