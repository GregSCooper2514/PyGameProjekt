import random, pygame, os
os.chdir("C:\\Users\\Greg\\Downloads")
def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image

class Cell:
    def __init__(self):
        self.is_bomb = False
        self.is_flag = False
        self.is_open = False
        self.is_current = False
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

    def set_current(self, par):
        self.is_current = par

    def get_current(self):
        return self.is_current


class Board:
    def __init__(self, width, hight, bombs, beggining):
        self.width = width
        self.hight = hight
        self.bombs = bombs
        self.cell_size = 20
        self.beggining = beggining
        self.is_exploded = False
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
        if self.list_of_cells[a][b].get_open():
            return
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
                self.list_of_cells[a][b].set_current(True)
                self.is_exploded = True
            else:
                self.open_area(a, b)

    def render(self, screen):
        for a in self.list_of_cells:
            for b in a:
                if b.check_bomb():
                    if self.is_exploded:
                        if b.get_current():
                            pygame.draw.rect(screen, "red", (b.get_x(), b.get_y(), self.cell_size, self.cell_size))
                        else:
                            pygame.draw.rect(screen, "white", (b.get_x(), b.get_y(), self.cell_size, self.cell_size))
                        img = pygame.image.load('bomb.png')
                        img.convert()
                        screen.blit(img, (b.get_x(), b.get_y() + 1))
                    else:
                        pygame.draw.rect(screen, (126, 126, 126), (b.get_x(), b.get_y(), self.cell_size, self.cell_size), 0)
                        for i in range(4):
                            pygame.draw.rect(screen, (193, 193, 193), (b.get_x() - i, b.get_y() - i, self.cell_size + 1, self.cell_size + 1), 1)
                else:
                    if b.get_open():
                        pygame.draw.rect(screen, "white", (b.get_x(), b.get_y(), self.cell_size, self.cell_size), 0)
                        for i in range(4):
                            pygame.draw.rect(screen, (193, 193, 193), (b.get_x() - i, b.get_y() - i, self.cell_size + 1, self.cell_size + 1), 1)
                        if b.get_number() > 0:
                            screen.blit(self.font.render(str(b.get_number()), True, "black"), (b.get_x(), b.get_y()))
                    else:
                        pygame.draw.rect(screen, (126, 126, 126), (b.get_x(), b.get_y(), self.cell_size, self.cell_size), 0)
                        for i in range(4):
                            pygame.draw.rect(screen, (193, 193, 193), (b.get_x() - i, b.get_y() - i, self.cell_size + 1, self.cell_size + 1), 1)

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
    size = width, height = 1000, 1000
    screen = pygame.display.set_mode(size)
    board = Board(16, 30, 99, 5)
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