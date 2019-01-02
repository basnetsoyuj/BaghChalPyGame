import pygame
pygame.init()

WHITE = (255, 255, 255)
GRAY = (90, 90, 90)

DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 700

BOARD_SIZE = (472, 471)
PIECE_SIZE = 59

boardX = (DISPLAY_WIDTH - BOARD_SIZE[0]) / 2.5
boardY = (DISPLAY_HEIGHT - BOARD_SIZE[1]) / 2

screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
pygame.display.set_caption('Bagh Chal')
clock = pygame.time.Clock()

board_img = pygame.image.load("images/board.png")
tiger_img = pygame.image.load("images/tiger.png")
goat_img = pygame.image.load("images/goat.png")

func = lambda x, y: (round(x / 100), round(y / 100))

goat_coordinate = (int(boardX + BOARD_SIZE[0])+100, 100)

dict_center={}
i=0
for x in range(0,5):
    j=0
    for y in range(0,5):
        dict_center[(x,y)]=(boardX+30+i,boardY+30+j)
        j+=103
    i+=103
dict_center[(-1,-1)]=goat_coordinate

def coordinate_pointing():
    x, y = pygame.mouse.get_pos()
    if boardX + BOARD_SIZE[0] > x > boardX and boardY + BOARD_SIZE[1] > y > boardY:
        rel_x = (x - boardX - 30)
        rel_y = (y - boardY - 30)
        standardX, standardY = dict_center[func(rel_x, rel_y)]
        if standardX + 30 > x > standardX - 30 and standardY + 30 > y > standardY - 30:
            return func(rel_x, rel_y)
        else:
            return 0
    else:

        return (-1,-1)


class Piece(object):
    def __init__(self,coordinate):
        self.coordinate=coordinate
        self.x,self.y=dict_center[coordinate]
    def draw(self,window):
        window.blit(self.sprite,(self.x-29,self.y-29))


class Tiger(Piece):
    sprite = tiger_img

class Goat(Piece):
    sprite = goat_img
class NascentGoat(object):
    sprite = goat_img
    def __init__(self):
        self.coordinate = (-1,-1)
        self.x, self.y = dict_center[self.coordinate]

    def draw(self, window):
        window.blit(self.sprite, (self.x - 29, self.y - 29))



class Board:
    start_pieces = [Tiger((x, y)) for x in {0, 4} for y in {0, 4}]+[NascentGoat() for _ in range(0,20)]

    board_dict = {x.coordinate: x for x in start_pieces}

    def draw(self):
        screen.blit(board_img, (boardX, boardY))

board = Board()

turn = 1



dragging = False
gameExit = False
goats_placed=0

recent_pointer = (0, 0)



def gameloop():
    for piece_ in board.start_pieces:
        piece_.draw(screen)


while not gameExit:
    clock.tick(60)

    screen.fill(WHITE)
    pygame.draw.line(screen,GRAY,(boardX+BOARD_SIZE[0]+10,0),(boardX+BOARD_SIZE[0]+10,DISPLAY_HEIGHT),4)
    board.draw()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameExit = True

        elif event.type == pygame.MOUSEBUTTONDOWN:
            recent_pointer = coordinate_pointing()
            dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:

            dragging = False
            latest_pointer = coordinate_pointing()

            if recent_pointer in board.board_dict:
                piece_ = board.board_dict[recent_pointer]

                if latest_pointer and (latest_pointer not in board.board_dict):
                    if piece_.__class__==NascentGoat:
                        goats_placed+=1
                        if goats_placed==20:
                            del board.board_dict[recent_pointer]
                    else:
                        del board.board_dict[recent_pointer]
                    board.board_dict[latest_pointer] = piece_
                    piece_.x, piece_.y = dict_center[latest_pointer]
                    piece_.coordinate = latest_pointer
                else:
                    piece_.x, piece_.y = dict_center[recent_pointer]
        elif event.type == pygame.MOUSEMOTION:
            if dragging:
                mousex, mousey = pygame.mouse.get_pos()
                try:
                    piece_ = board.board_dict[recent_pointer]
                    piece_.x = mousex
                    piece_.y = mousey
                except:
                    pass
    pygame.draw.circle(screen,GRAY,goat_coordinate,30)
    print(coordinate_pointing())
    gameloop()
    pygame.display.update()

pygame.quit()
quit()
