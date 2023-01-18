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

health = 100
lvlp = 1
exp = 0
power = 5
dang = 1
kills = 0


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
    global playerr, health, lvlp, exp, power, dang, kills
    playerr = 0
    health = 100
    lvlp = 1
    exp = 0
    power = 5
    dang = 1
    kills = 0
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    if 500 < event.pos[0] < 800 and 300 < event.pos[1] < 450:
                        main_game()
                    if 500 < event.pos[0] < 800 and 500 < event.pos[1] < 650:
                        print(1)
                    if 60 < event.pos[0] < 210 and 730 < event.pos[1] < 880:
                        print(1)
                    if 500 < event.pos[0] < 800 and 700 < event.pos[1] < 850:
                        terminate()
        my_font = pygame.font.Font(os.path.join('data', 'retro-land-mayhem.ttf'), 60)
        text1 = my_font.render(f'NECROMANCER GATE', True, (0, 255, 255))
        screen.fill((0, 0, 0))
        pygame.draw.rect(screen, (0, 255, 255), (40, 40, 1200, 860), 10)
        but1 = load_image('play.png')
        screen.blit(but1, (500, 300))
        but2 = load_image('stat.png')
        screen.blit(but2, (500, 500))
        but3 = load_image('exit.png')
        screen.blit(but3, (500, 700))
        but4 = load_image('prof.png')
        screen.blit(but4, (60, 730))
        screen.blit(text1, (300, 100))
        clock.tick(40)
        pygame.display.flip()


def lose_screen():
    running = True
    sp = pygame.sprite.Group()
    curs = load_image("gameover.png")
    gg = pygame.sprite.Sprite(sp)
    gg.image = curs
    gg.rect = gg.image.get_rect()
    gg.rect.x = 0
    gg.rect.y = 0
    al = 0
    my_font = pygame.font.Font(os.path.join('data', 'retro-land-mayhem.ttf'), 40)
    text1 = my_font.render(f'DANGEON:{dang}', True, (0, 255, 255))
    text2 = my_font.render(f'LEVEL:{lvlp}', True, (0, 255, 255))
    text3 = my_font.render(f'KILLS:{kills}', True, (0, 255, 255))
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                start_screen()
        while al < 255:
            gg.image.set_alpha(al + 1)
            al += 1
            sp.draw(screen)
            screen.blit(text1, (550, 600))
            screen.blit(text2, (550, 660))
            screen.blit(text3, (550, 720))
            pygame.display.flip()


def rand_level():
    global exp, dang
    exp += 1
    LevelUp()
    lvl = random.choice(('map.txt', 'map1.txt', 'map2.txt', 'map3.txt', 'map4.txt'))
    if dang % 5 == 0:
        lvl = 'map5.txt'
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
            elif level[y][x] == 'b':
                Tile('empty', x, y)
                new_sk.append(Skeletb(x, y))
    return new_player, new_sk, x, y, x1, y1


tile_images = {
    'wall': load_image('wall.png'),
    'empty': load_image('floor.png'),
    'dark': load_image('dark.png'),
    'portal': load_image('fire.png')
}
sk_image = load_image('skelet.png')
skb_image = load_image('skelet_b.png')
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


class Skeletb(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = skb_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.lf = True


def LevelUp():
    global exp, lvlp, health, power
    if exp >= lvlp * 5:
        exp = 0
        health += 30 * lvlp
        lvlp += 1
        power += 2


def fight():
    global health, lvlp, exp, power, kills, dang
    if dang % 5 == 0:
        return fight_b()
    sk_h = 20
    defend = 0
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    if 300 < event.pos[0] < 450 and 800 < event.pos[1] < 875:
                        sk_h -= random.randint(0, power)
                        health -= random.randint(0, 6 - defend + int(lvlp * 1.5))
                        defend -= 1
                    if 550 < event.pos[0] < 700 and 800 < event.pos[1] < 875:
                        defend = lvlp
                        health -= random.randint(0, 7 - defend)
                        defend -= 1
                    if 800 < event.pos[0] < 950 and 800 < event.pos[1] < 875:
                        if random.randint(0, 3) == 1:
                            return 2
                        health -= random.randint(0, 6 - defend + int(lvlp * 1.5))
                        defend -= 1
                    if defend < 0:
                        defend = 0
        if health <= 0:
            return 0
        if sk_h <= 0:
            kills += 1
            exp += 4
            LevelUp()
            return 1
        my_font = pygame.font.Font(os.path.join('data', 'retro-land-mayhem.ttf'), 30)
        text1 = my_font.render(f'HP:{health}', True, (0, 255, 255))
        text2 = my_font.render(f'LEVEL:{lvlp}', True, (0, 255, 255))
        text3 = my_font.render(f'EXP:{exp}', True, (0, 255, 255))
        text4 = my_font.render(f'POWER:{power}', True, (0, 255, 255))
        text5 = my_font.render(f'SKELET:{sk_h} / 20', True, (0, 255, 255))
        screen.fill((0, 0, 0))
        pygame.draw.rect(screen, (0, 255, 255), (150, 600, 980, 300), 10)
        sk = load_image('skelet-f.png')
        screen.blit(sk, (525, 300))
        but1 = load_image('fight.png')
        screen.blit(but1, (300, 800))
        but2 = load_image('def.png')
        screen.blit(but2, (550, 800))
        but3 = load_image('escape.png')
        screen.blit(but3, (800, 800))
        screen.blit(text1, (200, 620))
        screen.blit(text2, (420, 620))
        screen.blit(text3, (640, 620))
        screen.blit(text4, (860, 620))
        screen.blit(text5, (530, 170))
        clock.tick(40)
        pygame.display.flip()


def fight_b():
    global health, lvlp, exp, power, kills, dang
    sk_h = 10 * lvlp
    defend = 0
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    if 300 < event.pos[0] < 450 and 800 < event.pos[1] < 875:
                        sk_h -= random.randint(0, power)
                        health -= random.randint(0, 8 - defend + int(lvlp * 2))
                        defend -= 1
                    if 550 < event.pos[0] < 700 and 800 < event.pos[1] < 875:
                        defend = lvlp
                        health -= random.randint(0, 9 - defend)
                        defend -= 1
                    if 800 < event.pos[0] < 950 and 800 < event.pos[1] < 875:
                        if random.randint(0, 5) == 1:
                            return 2
                        health -= random.randint(0, 8 - defend + int(lvlp * 2))
                        defend -= 1
                    if defend < 0:
                        defend = 0
        if health <= 0:
            return 0
        if sk_h <= 0:
            kills += 1
            exp += 6 * (dang / 5)
            LevelUp()
            return 1
        my_font = pygame.font.Font(os.path.join('data', 'retro-land-mayhem.ttf'), 30)
        text1 = my_font.render(f'HP:{health}', True, (0, 255, 255))
        text2 = my_font.render(f'LEVEL:{lvlp}', True, (0, 255, 255))
        text3 = my_font.render(f'EXP:{exp}', True, (0, 255, 255))
        text4 = my_font.render(f'POWER:{power}', True, (0, 255, 255))
        text5 = my_font.render(f'SKELET:{sk_h} / {10 * lvlp}', True, (0, 255, 255))
        screen.fill((0, 0, 0))
        pygame.draw.rect(screen, (0, 255, 255), (150, 600, 980, 300), 10)
        sk = load_image('skelet-bf.png')
        screen.blit(sk, (525, 300))
        but1 = load_image('fight.png')
        screen.blit(but1, (300, 800))
        but2 = load_image('def.png')
        screen.blit(but2, (550, 800))
        but3 = load_image('escape.png')
        screen.blit(but3, (800, 800))
        screen.blit(text1, (200, 620))
        screen.blit(text2, (420, 620))
        screen.blit(text3, (640, 620))
        screen.blit(text4, (860, 620))
        screen.blit(text5, (530, 170))
        clock.tick(40)
        pygame.display.flip()


def main_game():
    global playerr, health, lvlp, exp, power, all_sprites, tiles_group, player_group, sk_group, dang
    all_sprites = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    sk_group = pygame.sprite.Group()
    playerr = 0
    health = 100
    lvlp = 1
    exp = 0
    power = 5
    screen.fill((0, 0, 0))
    my_font = pygame.font.Font(os.path.join('data', 'retro-land-mayhem.ttf'), 20)
    level = rand_level()
    player, sk, x, y, x1, y1 = generate_level(level)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                moves = pygame.key.get_pressed()
                if moves[pygame.K_w]:
                    if level[int(player.rect.y / 64) - 1][int(player.rect.x / 64)] == '/':
                        lose_screen()
                    elif level[int(player.rect.y / 64) - 1][int(player.rect.x / 64)] == '$':
                        dang += 1
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
                            res = fight()
                            if res == 1:
                                lt.kill()
                                sk.remove(lt)
                            elif res == 0:
                                lose_screen()

                if moves[pygame.K_s]:
                    if level[int(player.rect.y / 64) + 1][int(player.rect.x / 64)] == '/':
                        lose_screen()
                    elif level[int(player.rect.y / 64) + 1][int(player.rect.x / 64)] == '$':
                        dang += 1
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
                            res = fight()
                            if res == 1:
                                lt.kill()
                                sk.remove(lt)
                            elif res == 0:
                                lose_screen()

                if moves[pygame.K_a]:
                    if level[int(player.rect.y / 64)][int(player.rect.x / 64) - 1] == '/':
                        lose_screen()
                    elif level[int(player.rect.y / 64)][int(player.rect.x / 64) - 1] == '$':
                        dang += 1
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
                            res = fight()
                            if res == 1:
                                lt.kill()
                                sk.remove(lt)
                            elif res == 0:
                                lose_screen()

                if moves[pygame.K_d]:
                    if level[int(player.rect.y / 64)][int(player.rect.x / 64) + 1] == '/':
                        lose_screen()
                    elif level[int(player.rect.y / 64)][int(player.rect.x / 64) + 1] == '$':
                        dang += 1
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
                            res = fight()
                            if res == 1:
                                lt.kill()
                                sk.remove(lt)
                            elif res == 0:
                                lose_screen()

                for lt in sk:
                    xx, yy = random.randint(-1, 1), random.randint(-1, 1)
                    while level[int(lt.rect.y / 64) + yy][int(lt.rect.x / 64) + xx] == '#' or \
                            level[int(lt.rect.y / 64) + yy][int(lt.rect.x / 64) + xx] == '/' or (xx == 0 and yy == 0):
                        xx, yy = random.randint(-1, 1), random.randint(-1, 1)
                    lt.rect.x += xx * 64
                    lt.rect.y += yy * 64
                    if lt.rect.x == player.rect.x and lt.rect.y == player.rect.y:
                        res = fight()
                        if res == 1:
                            lt.kill()
                            sk.remove(lt)
                        elif res == 0:
                            lose_screen()

        text1 = my_font.render(f'HP:{health}', True, (0, 255, 255))
        text2 = my_font.render(f'LEVEL:{lvlp}', True, (0, 255, 255))
        text3 = my_font.render(f'DANGEON:{dang}', True, (0, 255, 255))
        screen.fill((0, 0, 0))
        tiles_group.draw(screen)
        player_group.draw(screen)
        screen.blit(text1, (11, 11))
        screen.blit(text2, (11, 44))
        screen.blit(text3, (11, 77))
        clock.tick(40)
        pygame.display.flip()
    pygame.quit()


start_screen()
