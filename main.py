import random, pygame
class Cell:
    def __init__(self):
        self.is_bomb = False
        self.is_flag = False
        self.is_qsmark = False
        self.is_open = True
        self.number = 0
        self.x = -1
        self.y = -1
    
    def check_bomb(self):
        return self.is_bomb
    
    def set_bomb(self):
        self.is_bomb = True
    
    def set_number(self, number):
        self.number = number
    
    def set_x(self, x):
        self.x = x
    
    def set_y(self, y):
        self.y = y
    
    def get_y(self):
        return self.y

    def get_x(self):
        return self.x

    def get_number(self):
        return self.number
class Board:
    def __init__(self, width, hight, bombs, beggining):
        self.width = width
        self.hight = hight
        self.bombs = bombs
        self.cell_size = 50
        self.beggining = beggining
        self.font = pygame.font.SysFont('Arial', 40)
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
            celll = self.list_of_cells[random_width][random_hight]
            if not celll.check_bomb():
                celll.set_bomb()
                bombs -= 1
        for a in range(self.width):
            for b in range(self.hight):
                self.list_of_cells[a][b].set_x(self.cell_size * a)
                self.list_of_cells[a][b].set_y(self.beggining + (self.cell_size * b))
                bombs = 0
                if self.list_of_cells[a][b].check_bomb():
                    print("check_bomb", a, b)
                    continue
                if self.check_value(a - 1, b - 1):
                    if self.list_of_cells[a - 1][b - 1].check_bomb(): bombs += 1
                if self.check_value(a, b - 1):
                    if self.list_of_cells[a][b - 1].check_bomb(): bombs += 1
                if self.check_value(a + 1, b - 1):
                    if self.list_of_cells[a + 1][b - 1].check_bomb(): bombs += 1
                if self.check_value(a - 1, b):
                    print("a - 1, b", a, b)
                    print(bombs)
                    if self.list_of_cells[a - 1][b].check_bomb(): bombs += 1
                    print(bombs)
                if self.check_value(a + 1, b):
                    print("a + 1, b", a, b)
                    print(bombs)
                    if self.list_of_cells[a + 1][b].check_bomb(): bombs += 1
                    print(bombs)
                if self.check_value(a - 1, b + 1):
                    if self.list_of_cells[a - 1][b + 1].check_bomb(): bombs += 1
                if self.check_value(a, b + 1):
                    if self.list_of_cells[a][b + 1].check_bomb(): bombs += 1
                if self.check_value(a + 1, b + 1):
                    if self.list_of_cells[a + 1][b + 1].check_bomb(): bombs += 1
            self.list_of_cells[a][b].set_number(bombs)

    def render(self, screen):
        for a in self.list_of_cells:
            for b in a:
                if b.check_bomb():
                    pygame.draw.rect(screen, "red", (b.get_x(), b.get_y(), self.cell_size, self.cell_size))
                else:
                    pygame.draw.rect(screen, "gray", (b.get_x(), b.get_y(), self.cell_size, self.cell_size))
                    screen.blit(self.font.render(str(b.get_number()), True, (255,255,0)), (b.get_x(), b.get_y()))

    def check_value(self, x, y):
        if x >= 0 and x <= self.width - 1 and y >= 0 and y <= self.hight - 1:
            return True
        else:
            return False

if __name__ == '__main__':
    pygame.init()
    size = width, height = 500, 500
    screen = pygame.display.set_mode(size)
    board = Board(2, 2, 1, 5)
    #board.set_view(100, 100, 50)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill("black")
        board.render(screen)
        pygame.display.flip()
    pygame.quit()