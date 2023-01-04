import os
import sys
import pygame
import random

pygame.init()
size = width, height = 1280, 960
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
sk_group = pygame.sprite.Group()
playerr = 0


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["Necromancer gate"]

    fon = pygame.transform.scale(load_image('fon.png'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, True, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(40)


def rand_level():
    lvl = random.choice(('map.txt', 'map1.txt', 'map2.txt', 'map3.txt', 'map4.txt'))
    return load_level(lvl)


def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def generate_level(level):
    global playerr, new_sk
    new_player, x, y = None, None, None
    x1, y1 = 1, 1
    new_sk = []
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '/':
                Tile('dark', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                x1, y1 = x, y
                if playerr == 0:
                    new_player = Player(x, y)
                    playerr = 1
            elif level[y][x] == '$':
                Tile('empty', x, y)
                Tile('portal', x, y)
            elif level[y][x] == 's':
                Tile('empty', x, y)
                new_sk.append(Skelet(x, y))
    return new_player, new_sk, x, y, x1, y1


tile_images = {
    'wall': load_image('wall.png'),
    'empty': load_image('floor.png'),
    'dark': load_image('dark.png'),
    'portal': load_image('fire.png')
}
sk_image = load_image('skelet.png')
player_image = load_image('ggs.png')

tile_width = tile_height = 64


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.lf = True

    def rot(self, s):
        if s == True and self.lf == False:
            self.image = pygame.transform.flip(self.image, True, False)
            self.lf = True
        elif s == False and self.lf == True:
            self.image = pygame.transform.flip(self.image, True, False)
            self.lf = False


class Skelet(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = sk_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.lf = True

    def rot(self, s):
        if s == True and self.lf == False:
            self.image = pygame.transform.flip(self.image, True, False)
            self.lf = True
        elif s == False and self.lf == True:
            self.image = pygame.transform.flip(self.image, True, False)
            self.lf = False


level = rand_level()
player, sk, x, y, x1, y1 = generate_level(level)
start_screen()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            moves = pygame.key.get_pressed()
            if moves[pygame.K_w]:
                if level[int(player.rect.y / 64) - 1][int(player.rect.x / 64)] == '/':
                    pygame.quit()
                elif level[int(player.rect.y / 64) - 1][int(player.rect.x / 64)] == '$':
                    for lt in sk:
                        lt.kill()
                    screen.fill((0, 0, 0))
                    level = rand_level()
                    pl, sk, x, y, player.rect.x, player.rect.y = generate_level(level)
                    player.rect.x *= 64
                    player.rect.y *= 64
                elif not level[int(player.rect.y / 64) - 1][int(player.rect.x / 64)] == '#':
                    player.rect.y -= tile_height
                for lt in sk:
                    if lt.rect.x == player.rect.x and lt.rect.y == player.rect.y:
                        pygame.quit()

            if moves[pygame.K_s]:
                if level[int(player.rect.y / 64) + 1][int(player.rect.x / 64)] == '/':
                    pygame.quit()
                elif level[int(player.rect.y / 64) + 1][int(player.rect.x / 64)] == '$':
                    for lt in sk:
                        lt.kill()
                    screen.fill((0, 0, 0))
                    level = rand_level()
                    pl, sk, x, y, player.rect.x, player.rect.y = generate_level(level)
                    player.rect.x *= 64
                    player.rect.y *= 64
                elif not level[int(player.rect.y / 64) + 1][int(player.rect.x / 64)] == '#':
                    player.rect.y += tile_height
                for lt in sk:
                    if lt.rect.x == player.rect.x and lt.rect.y == player.rect.y:
                        pygame.quit()

            if moves[pygame.K_a]:
                if level[int(player.rect.y / 64)][int(player.rect.x / 64) - 1] == '/':
                    pygame.quit()
                elif level[int(player.rect.y / 64)][int(player.rect.x / 64) - 1] == '$':
                    for lt in sk:
                        lt.kill()
                    screen.fill((0, 0, 0))
                    level = rand_level()
                    pl, sk, x, y, player.rect.x, player.rect.y = generate_level(level)
                    player.rect.x *= 64
                    player.rect.y *= 64
                elif not level[int(player.rect.y / 64)][int(player.rect.x / 64) - 1] == '#':
                    player.rect.x -= tile_width
                    player.rot(True)
                for lt in sk:
                    if lt.rect.x == player.rect.x and lt.rect.y == player.rect.y:
                        pygame.quit()

            if moves[pygame.K_d]:
                if level[int(player.rect.y / 64)][int(player.rect.x / 64) + 1] == '/':
                    pygame.quit()
                elif level[int(player.rect.y / 64)][int(player.rect.x / 64) + 1] == '$':
                    for lt in sk:
                        lt.kill()
                    screen.fill((0, 0, 0))
                    level = rand_level()
                    pl, sk, x, y, player.rect.x, player.rect.y = generate_level(level)
                    player.rect.x *= 64
                    player.rect.y *= 64
                elif not level[int(player.rect.y / 64)][int(player.rect.x / 64) + 1] == '#':
                    player.rect.x += tile_width
                    player.rot(False)
                for lt in sk:
                    if lt.rect.x == player.rect.x and lt.rect.y == player.rect.y:
                        pygame.quit()
            for lt in sk:
                xx, yy = random.randint(-1, 1), random.randint(-1, 1)
                while level[int(lt.rect.y / 64) + yy][int(lt.rect.x / 64) + xx] == '#' or \
                        level[int(lt.rect.y / 64) + yy][int(lt.rect.x / 64) + xx] == '/' or (xx == 0 and yy == 0):
                    xx, yy = random.randint(-1, 1), random.randint(-1, 1)
                lt.rect.x += xx * 64
                lt.rect.y += yy * 64
                if lt.rect.x == player.rect.x and lt.rect.y == player.rect.y:
                    pygame.quit()

    screen.fill((0, 0, 0))
    tiles_group.draw(screen)
    player_group.draw(screen)
    clock.tick(40)
    pygame.display.flip()
pygame.quit()
