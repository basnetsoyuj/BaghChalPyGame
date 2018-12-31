import pygame

pygame.init()

WHITE=(255,255,255)

DISPLAY_WIDTH=800
DISPLAY_HEIGHT=700

BOARD_SIZE=(472,471)
PIECE_SIZE=59

boardX= ( DISPLAY_WIDTH - BOARD_SIZE[0] ) / 2
boardY= ( DISPLAY_HEIGHT - BOARD_SIZE[1] ) / 2

screen=pygame.display.set_mode((DISPLAY_WIDTH,DISPLAY_HEIGHT))
pygame.display.set_caption('Bagh Chal')
clock = pygame.time.Clock()


board = pygame.image.load("images/board.png")
func=lambda x,y:(round(x/100),round(y/100))
dict_center={(0, 0): (194, 145), (0, 1): (194, 248), (0, 2): (194, 351), (0, 3): (194, 454), (0, 4): (194, 557),
             (1, 0): (297, 145), (1, 1): (297, 248), (1, 2): (297, 351), (1, 3): (297, 454), (1, 4): (297, 557),
             (2, 0): (400, 145), (2, 1): (400, 248), (2, 2): (400, 351), (2, 3): (400, 454), (2, 4): (400, 557),
             (3, 0): (503, 145), (3, 1): (503, 248), (3, 2): (503, 351), (3, 3): (503, 454), (3, 4): (503, 557),
             (4, 0): (606, 145), (4, 1): (606, 248), (4, 2): (606, 351), (4, 3): (606, 454), (4, 4): (606, 557)}


def coordinate_pointing():
    x,y=pygame.mouse.get_pos()
    if boardX+BOARD_SIZE[0]>x>boardX and boardY+BOARD_SIZE[1]>y>boardY :
        rel_x=(x-boardX-30)
        rel_y=(y-boardY-30)
        standardX,standardY=dict_center[func(rel_x,rel_y)]
        if standardX+30>x>standardX-30 and standardY+30>y>standardY-30:
            return func(rel_x,rel_y)
        else:
            return 0
    else:
        return 0

class piece(object):
    def __init__(self,sprite,coordinate):
        self.coordinate=coordinate
        self.sprite=pygame.image.load(f"images/{sprite}")
        self.x,self.y=dict_center[coordinate]
    def draw(self,window):
        window.blit(self.sprite,(self.x-29,self.y-29))
class tiger(piece):
    pass
class goat(piece):
    pass

#defining objects
pieces=[tiger("tiger.png",(x,y))for x in {0,4} for y in {0,4}]

turn=1


board_dict={x.coordinate:x for x in pieces}


dragging=False
gameExit = False

recent_pointer=(0,0)
def gameloop():
    for piece_ in pieces:
        piece_.draw(screen)


while not gameExit:
    clock.tick(60)

    screen.fill(WHITE)
    screen.blit(board,(boardX,boardY))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameExit = True

        elif event.type == pygame.MOUSEBUTTONDOWN:
            recent_pointer = coordinate_pointing()
            dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:

            dragging = False
            latest_pointer=coordinate_pointing()

            if recent_pointer in board_dict:
                piece_ = board_dict[recent_pointer]

                if latest_pointer and (latest_pointer not in board_dict):
                    del board_dict[recent_pointer]
                    board_dict[latest_pointer]=piece_
                    piece_.x, piece_.y=dict_center[latest_pointer]
                    piece_.coordinate=latest_pointer
                else:
                    piece_.x,piece_.y=dict_center[recent_pointer]
        elif event.type == pygame.MOUSEMOTION:
            if dragging:
                try:
                    mousex, mousey = pygame.mouse.get_pos()
                    piece_=board_dict[recent_pointer]
                    piece_.x=mousex
                    piece_.y=mousey
                except:
                    pass
    
    gameloop()
    pygame.display.update()


pygame.quit()
quit()
