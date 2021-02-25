import random, pygame
from pygame.constants import K_x
class Cell:
    def __init__(self):
        self.is_bomb = False
        self.is_flag = False
        self.is_qsmark = False
        self.is_open = False
        self.number = 0
        self.x = -1
        self.y = -1
        self.a = -1
        self.b = -1

    def explosion(self):
        pass

    def check_bomb(self):
        return self.is_bomb

    def set_bomb(self):
        self.is_bomb = True

    def set_number(self, number):
        self.number = number

    def add_number(self):
        self.number += 1

    def set_x(self, x):
        self.x = x

    def set_y(self, y):
        self.y = y

    def set_a(self, a):
        self.a = a

    def set_b(self, b):
        self.b = b

    def get_a(self):
        return self.a

    def get_b(self):
        return self.b

    def get_y(self):
        return self.y

    def get_x(self):
        return self.x

    def get_number(self):
        return self.number

    def get_open(self):
        return self.is_open

    def set_open(self):
        self.is_open = True

class Board:
    def __init__(self, width, hight, bombs, beggining):
        self.width = width
        self.hight = hight
        self.bombs = bombs
        self.cell_size = 20
        self.beggining = beggining
        self.font = pygame.font.SysFont('Arial', 10)
        lisst = []
        for a in range(self.width):
            lisst1 = []
            for b in range(self.hight):
                lisst1.append(Cell())
            lisst.append(lisst1)
        self.list_of_cells = lisst
        self.fill_bombs()

    def fill_bombs(self):
        bombs = self.bombs
        while bombs > 0:
            random_hight = random.randrange(self.hight)
            random_width = random.randrange(self.width)
            if not self.list_of_cells[random_width][random_hight].check_bomb():
                self.list_of_cells[random_width][random_hight].set_bomb()
                for a in self.get_near_cells(random_width, random_hight):
                    a.add_number()
                bombs -= 1
        for a in range(self.width):
            for b in range(self.hight):
                self.list_of_cells[a][b].set_a(a)
                self.list_of_cells[a][b].set_b(b)
                self.list_of_cells[a][b].set_x(self.cell_size * a)
                self.list_of_cells[a][b].set_y(self.beggining + (self.cell_size * b))

    def open_area(self, a, b):
        self.list_of_cells[a][b].set_open()
        if self.list_of_cells[a][b].get_number() > 0:
            return
        for i in self.get_near_cells(a, b):
            self.open_area(i.get_a(), i.get_b())


    def left_mouse_click(self, pos):
        a = pos[0] // self.cell_size
        b = (pos[1] - self.beggining) // self.cell_size
        if not self.list_of_cells[a][b].get_open():
            if self.list_of_cells[a][b].check_bomb():
                for i in self.list_of_cells:
                    for j in i:
                        j.explosion()
            else:
                self.open_area(a, b)

    def render(self, screen):
        for a in self.list_of_cells:
            for b in a:
                if b.check_bomb():
                    pygame.draw.rect(screen, "red", (b.get_x(), b.get_y(), self.cell_size, self.cell_size))
                else:
                    if b.get_open():
                        pygame.draw.rect(screen, "white", (b.get_x(), b.get_y(), self.cell_size, self.cell_size))
                    else:
                        pygame.draw.rect(screen, "gray", (b.get_x(), b.get_y(), self.cell_size, self.cell_size))
                    if b.get_number() > 0:
                        screen.blit(self.font.render(str(b.get_number()), True, "black"), (b.get_x(), b.get_y()))

    def check_value(self, x, y):
        if x >= 0 and x <= self.width - 1 and y >= 0 and y <= self.hight - 1:
            return True
        else:
            return False

    def get_near_cells(self, a, b):
        lisst = []
        for counter in range(8):
            if counter == 0:
                x = a - 1
                y = b - 1
            if counter == 1:
                x = a
                y = b - 1
            if counter == 2:
                x = a + 1
                y = b - 1
            if counter == 3:
                x = a + 1
                y = b
            if counter == 4:
                x = a + 1
                y = b + 1
            if counter == 5:
                x = a
                y = b + 1
            if counter == 6:
                x = a - 1
                y = b + 1
            if counter == 7:
                x = a - 1
                y = b
            if self.check_value(x, y):
                lisst.append(self.list_of_cells[x][y])
        return lisst

if __name__ == '__main__':
    pygame.init()
    size = width, height = 500, 500
    screen = pygame.display.set_mode(size)
    board = Board(16, 30, 99, 5)
    #board.set_view(100, 100, 50)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                board.left_mouse_click(event.pos)
        screen.fill("black")
        board.render(screen)
        pygame.display.flip()
    pygame.quit()