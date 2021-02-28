import random, pygame, os
os.chdir("C:\\Users\\Greg\\Downloads")


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

    def get_bomb(self):
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

    def set_current(self):
        self.is_current = True

    def get_current(self):
        return self.is_current

    def get_flag(self):
        return self.is_flag

    def set_flag(self):
        if not self.is_open:
            if self.is_flag:
                self.is_flag = False
            else:
                self.is_flag = True


class Board:
    def __init__(self, width, hight, bombs, beggining):
        self.width = width
        self.hight = hight
        self.bombs = bombs
        self.cell_size = 20
        self.beggining = beggining
        self.is_exploded = False
        self.smile_location = (self.width * self.cell_size // 2) - 28
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
            if not self.list_of_cells[random_width][random_hight].get_bomb():
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
            if self.list_of_cells[a][b].get_bomb():
                self.list_of_cells[a][b].set_current()
                self.is_exploded = True
            else:
                self.open_area(a, b)

    def right_mouse_click(self, pos):
        a = pos[0] // self.cell_size
        b = (pos[1] - self.beggining) // self.cell_size
        self.list_of_cells[a][b].set_flag()

    def both_mouse_click(self, pos):
        a = pos[0] // self.cell_size
        b = (pos[1] - self.beggining) // self.cell_size
        flag_counter = 0
        if self.list_of_cells[a][b].get_open() and self.list_of_cells[a][b].get_number() > 0:
            for i in self.get_near_cells(a, b):
                if i.get_flag():
                    flag_counter += 1
            if flag_counter == self.list_of_cells[a][b].get_number():
                for i in self.get_near_cells(a, b):
                    if not i.get_open() and not i.get_flag():
                        self.open_area(i.get_a(), i.get_b())

    def render(self, screen):
        pygame.draw.rect(screen, (192, 192, 192, 255), (0, 0, self.width * self.cell_size, 36))
        img = pygame.image.load("data\\normal_smile.png")
        img.convert()
        screen.blit(img, (self.smile_location, 4))
        for a in self.list_of_cells:
            for b in a:
                if b.get_bomb():
                    if self.is_exploded:
                        img = pygame.image.load("data\\dead_smile.png")
                        img.convert()
                        screen.blit(img, (self.smile_location, 4))
                        if b.get_current():
                            img = pygame.image.load("data\\current_bomb.png")
                            img.convert()
                            screen.blit(img, (b.get_x(), b.get_y()))
                        else:
                            img = pygame.image.load("data\\bomb.png")
                            img.convert()
                            screen.blit(img, (b.get_x(), b.get_y()))
                    else:
                        img = pygame.image.load("data\\closed_cell.png")
                        img.convert()
                        screen.blit(img, (b.get_x(), b.get_y()))
                else:
                    if b.get_open():
                        if b.get_number() > 0:
                            img = pygame.image.load(f"data\\number_{b.get_number()}.png")
                            img.convert()
                            screen.blit(img, (b.get_x(), b.get_y()))
                        else:
                            img = pygame.image.load("data\\empty_cell.png")
                            img.convert()
                            screen.blit(img, (b.get_x(), b.get_y()))
                    else:
                        img = pygame.image.load("data\\closed_cell.png")
                        img.convert()
                        screen.blit(img, (b.get_x(), b.get_y()))
                if b.get_flag() and not self.is_exploded:
                    img = pygame.image.load("data\\flag.png")
                    img.convert()
                    screen.blit(img, (b.get_x(), b.get_y()))
                if b.get_flag() and not b.get_bomb() and self.is_exploded:
                    img = pygame.image.load("data\\not_a_bomb.png")
                    img.convert()
                    screen.blit(img, (b.get_x(), b.get_y()))

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
    board = Board(16, 30, 98, 36)
    a = pygame.image.load("data\\icon.ico")
    pygame.display.set_icon(a)
    pygame.display.set_caption("Minesweeper retro")
    running = True
    left_mouse_down = False
    right_mouse_down = False
    while running:
        size = width, height
        screen = pygame.display.set_mode(size)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.pos[1] > 36:
                    if event.button == 1:
                        left_mouse_down = True
                        if right_mouse_down:
                            board.both_mouse_click(event.pos)
                        else:
                            board.left_mouse_click(event.pos)
                    if event.button == 3:
                        right_mouse_down = True
                        if left_mouse_down:
                            board.both_mouse_click(event.pos)
                        else:
                            board.right_mouse_click(event.pos)
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    left_mouse_down = False
                if event.button == 3:
                    right_mouse_down = False
        screen.fill("black")
        board.render(screen)
        pygame.display.flip()
    pygame.quit()