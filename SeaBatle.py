from pygame import *
from random import randint, choice

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

margin_up = 55
margin_left = 80
size_cell = 50

win_width = margin_left * 3 + size_cell * 10 * 2
win_height = margin_up * 2 + size_cell * 10

font_size = int(size_cell / 1.5)

game = True
computer_shot = False

clock = time.Clock()

init()

win = display.set_mode((win_width, win_height))
win.fill(WHITE)

display.set_caption("Морской бой")
display.set_icon(image.load("icon.ico"))

font = font.SysFont('Verdana', font_size)


class Ship:
    def __init__(self):
        self.free_blocks = set((x, y) for x in range(1, 11) for y in range(1, 11))
        self.ships = set()
        self.ships_list = self.populate_ships()

    def create_start_block(self, free_blocks):
        horizontal_vertical = randint(0, 1)  # horizontal - 0; vertical - 1
        left_right = choice([-1, 1])
        x, y = choice(tuple(free_blocks))
        return x, y, horizontal_vertical, left_right

    def create_ship(self, num_block, free_block):
        ship_coord = []
        x, y, horizontal_vertical, left_right = self.create_start_block(free_block)
        for i in range(num_block):
            ship_coord += [(x, y)]
            if not horizontal_vertical:
                left_right, x = self.add_block(x, left_right, horizontal_vertical, ship_coord)
            else:
                left_right, y = self.add_block(y, left_right, horizontal_vertical, ship_coord)
        if self.valid_ship(ship_coord):
            return ship_coord
        return self.create_ship(num_block, free_block)

    def add_ship_set(self, ships):
        for el in ships:
            self.ships.add(el)

    def update_ships(self, ships):
        for el in ships:
            for x in range(-1, 2):
                for y in range(-1, 2):
                    if 0 < el[0] + x < 11 and 0 < el[1] + y < 11:
                        self.free_blocks.discard((el[0] + x, el[1] + y))

    def add_block(self, coord, left_right, hor_ver, ship_coord):
        if (coord <= 1 and left_right == -1) or (coord >= 10 and left_right == 1):
            left_right *= -1
            return left_right, ship_coord[0][hor_ver] + left_right
        else:
            return left_right, ship_coord[-1][hor_ver] + left_right

    def valid_ship(self, ship_coord):
        ship = set(ship_coord)
        return ship.issubset(self.free_blocks)

    def populate_ships(self):
        ship_coordinates = []
        for len_ship in range(4, 0, -1):
            for _ in range(5 - len_ship):
                new_ship = self.create_ship(len_ship, self.free_blocks)
                ship_coordinates += [new_ship]
                self.add_ship_set(new_ship)
                self.update_ships(new_ship)
        return ship_coordinates


def print_grid():
    letters = ["А", "Б", "В", "Г", "Д", "Е", "Ж", "З", "И", "К"]
    for i in range(11):
        draw.line(win, BLACK, (margin_left, margin_up + i * size_cell),
                  (margin_left + 10 * size_cell, margin_up + i * size_cell), 2)
        draw.line(win, BLACK, (margin_left + i * size_cell, margin_up),
                  (margin_left + i * size_cell, margin_up + 10 * size_cell), 2)

        draw.line(win, BLACK, (margin_left * 2 + 10 * size_cell, margin_up + i * size_cell),
                  (margin_left * 2 + 10 * size_cell + 10 * size_cell, margin_up + i * size_cell), 2)
        draw.line(win, BLACK, (margin_left * 2 + i * size_cell + 10 * size_cell, margin_up),
                  (margin_left * 2 + i * size_cell + 10 * size_cell, margin_up + 10 * size_cell), 2)
        if i < 10:
            num = font.render(str(i + 1), True, BLACK)
            letter = font.render(letters[i], True, BLACK)

            num_width = num.get_width()
            num_height = num.get_height()

            letter_width = letter.get_width()

            win.blit(num, (margin_left - (size_cell // 2 + num_width // 2),
                           margin_up + i * size_cell + (size_cell // 2 - num_height // 2)))
            win.blit(letter, (margin_left + i * size_cell + (size_cell // 2 - letter_width // 2),
                              margin_up + 10 * size_cell))

            win.blit(num, (margin_left * 2 - (size_cell // 2 + num_width // 2) + 10 * size_cell,
                           margin_up + i * size_cell + (size_cell // 2 - num_height // 2)))
            win.blit(letter, (margin_left * 2 + i * size_cell + (size_cell // 2 - letter_width // 2) + 10 * size_cell,
                              margin_up + 10 * size_cell))


def draw_ships(ship_coordinates):
    for elem in ship_coordinates:
        ship = sorted(elem)
        x_start = ship[0][0]
        y_start = ship[0][1]
        if len(ship) > 1 and ship[0][0] == ship[1][0]:
            ship_width = size_cell
            ship_height = size_cell * len(ship)
        else:
            ship_width = size_cell * len(ship)
            ship_height = size_cell
        x = size_cell * (x_start - 1) + margin_left
        y = size_cell * (y_start - 1) + margin_up
        if ship_coordinates == human.ships_list:
            x += 10 * size_cell + margin_left
        draw.rect(win, BLACK, ((x, y), (ship_width, ship_height)), width=size_cell // 10)


def shoot_computer():
    pass


def check_shoot():
    pass


computer = Ship()
human = Ship()

print_grid()
draw_ships(computer.ships_list)
draw_ships(human.ships_list)
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif not computer_shot and e.type == MOUSEBUTTONDOWN:
            x, y = e.pos()
            if (margin_left <= x <= margin_left + 10 * size_cell) and (margin_up <= y <= margin_up + 10 * size_cell):
                fire_block = ((x - margin_left) // size_cell + 1, (y - margin_up) // size_cell + 1)
            computer_shot = not check_shoot()
    if computer_shot:
        pass
    
    display.update()
    clock.tick(30)
