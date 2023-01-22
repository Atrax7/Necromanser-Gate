import os
import sys
import time
import pygame
import random
import database

pygame.init()
pygame.mixer.init()
size = 1280, 960
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
sk_group = pygame.sprite.Group()
playerr = 0

sounds = {}

health = 100
lvlp = 1
exp = 0
power = 5
dang = 1
kills = 0
akk = database.DataBase()
pygame.mouse.set_visible(False)


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"ERROR | Файл изображения '{fullname}' не найден!")
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
    playsound('exit.mp3')
    time.sleep(1)
    pygame.quit()
    sys.exit()


def fontrender(text, size=40, pos=(0, 0)):
    if pos != (0, 0):
        screen.blit(pygame.font.Font(os.path.join('data', 'retro-land-mayhem.ttf'), size).render(
            text,
            True, (0, 255, 255)), pos)
    else:
        return pygame.font.Font(os.path.join('data', 'retro-land-mayhem.ttf'), size).render(text, True, (0, 255, 255))


def background():
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (0, 255, 255), (40, 40, 1200, 860), 10)
    fontrender('NECROMANCER GATE', 60, (260, 100))
    pygame.mouse.set_visible(False)
    screen.blit(load_image('curs.png'), pygame.mouse.get_pos())
    pygame.time.Clock().tick(60)


def playsound(name):
    fullname = os.path.join('data', 'sounds', name)
    if not os.path.isfile(fullname):
        print(f"ERROR | Файл звука '{fullname}' не найден!")
        sys.exit()
    else:
        sounds[name] = pygame.mixer.Sound(fullname)
        sounds[name].play()


def akk_profile():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    if 550 < event.pos[0] < 700 and 700 < event.pos[1] < 850:
                        playsound('exit.mp3')
                        start_screen()
        background()
        screen.blit(load_image('ok.png'), (550, 700))
        fontrender(f'{akk.nickname}`s PROFILE', 50, (400, 200))
        fontrender(f'LEVEL: {akk.data[1]} ({akk.data[0]} XP)', pos=(450, 450))
        fontrender(f'KILLS: {akk.data[2]}', pos=(510, 500))
        fontrender(f'FLOOR: {akk.data[3]}', pos=(510, 550))
        pygame.display.flip()


def akk_responce(responce):
    if responce in [2, 3]:
        playsound('success.mp3')
    else:
        playsound('error.mp3')
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    if 550 < event.pos[0] < 700 and 700 < event.pos[1] < 850:
                        if responce in [2, 3]:
                            playsound('button.mp3')
                            akk_profile()
                        else:
                            playsound('exit.mp3')
                            akk_but()
        background()
        screen.blit(load_image('ok.png'), (550, 700))
        if responce in [2, 3]:
            fontrender(f'Welcome, ', pos=(520, 450))
            fontrender(akk.nickname, pos=(560, 500))

        if responce == 2:
            fontrender('LOGIN SUCCESS!', size=50, pos=(400, 250))
        elif responce == 3:
            fontrender('ACCOUNT REGISTERED!', size=50, pos=(300, 250))
        else:
            fontrender('ACCESS DENIED!', size=50, pos=(370, 250))
            if responce == 0:
                fontrender('Invalid username or password!', pos=(250, 450))
            elif responce == 1:
                fontrender('Empty username or password!', pos=(250, 450))
        pygame.display.flip()


def akk_but():
    if akk.nickname:
        akk_profile()
    input_box = pygame.Rect(520, 530, 500, 100)
    input_box1 = pygame.Rect(520, 380, 500, 100)
    color_inactive = pygame.Color(0, 255, 255)
    color_active = pygame.Color(200, 255, 255)
    color_inactive1 = pygame.Color(0, 255, 255)
    color_active1 = pygame.Color(200, 255, 255)
    color = color_inactive
    color1 = color_inactive
    active = False
    active1 = False
    text = ''
    text_1 = ''
    run = False
    while not run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    if 920 < event.pos[0] < 1220 and 730 < event.pos[1] < 880:
                        playsound('exit.mp3')
                        start_screen()
                    if 750 < event.pos[0] < 900 and 730 < event.pos[1] < 880:
                        akk_responce(akk.login(text_1, text))
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive

                if input_box1.collidepoint(event.pos):
                    active1 = not active1
                else:
                    active1 = False
                color1 = color_active1 if active1 else color_inactive1
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        text = ''
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        if len(text) > 11:
                            event.unicode = ''
                        text += event.unicode

                if active1:
                    if event.key == pygame.K_RETURN:
                        text_1 = ''
                    elif event.key == pygame.K_BACKSPACE:
                        text_1 = text_1[:-1]
                    else:
                        if len(text_1) > 11:
                            event.unicode = ''
                        text_1 += event.unicode

        background()
        screen.blit(load_image('exit.png'), (920, 730))
        screen.blit(load_image('ok.png'), (750, 730))
        fontrender('SING IN', 50, (500, 250))
        fontrender(f'USERNAME:', pos=(250, 400))
        fontrender(f'PASSWORD:', pos=(250, 550))
        fontrender(text, pos=(input_box.x + 15, input_box.y + 15))
        fontrender(text_1, pos=(input_box1.x + 15, input_box1.y + 15))
        pygame.draw.rect(screen, color, input_box, 10)
        pygame.draw.rect(screen, color1, input_box1, 10)
        pygame.display.flip()


def top_but():
    global playerr, health, lvlp, exp, power, dang, kills
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    if 920 < event.pos[0] < 1220 and 730 < event.pos[1] < 880:
                        playsound('exit.mp3')
                        return
        top = akk.get_top()

        text3 = fontrender('I       -')
        text4 = fontrender('II      -')
        text5 = fontrender('III     -')
        text6 = fontrender('IV      -')
        text7 = fontrender('V       -')

        if len(top) >= 1:
            text3 = fontrender(f'I      {top[0][0]}  |  {top[0][1]} LVL')

        if len(top) >= 2:
            text4 = fontrender(f'II     {top[1][0]}  |  {top[1][1]} LVL')

        if len(top) >= 3:
            text5 = fontrender(f'III    {top[2][0]}  |  {top[2][1]} LVL')

        if len(top) >= 4:
            text6 = fontrender(f'IV     {top[3][0]}  |  {top[3][1]} LVL')

        if len(top) >= 5:
            text7 = fontrender(f'V      {top[4][0]}  |  {top[4][1]} LVL')
        background()
        screen.blit(load_image('exit.png'), (920, 730))
        fontrender('LEADERBOARD', 50, (400, 200))
        screen.blit(text3, (150, 300))
        screen.blit(text4, (150, 400))
        screen.blit(text5, (150, 500))
        screen.blit(text6, (150, 600))
        screen.blit(text7, (150, 700))
        pygame.display.flip()


def start_screen():
    global playerr, health, lvlp, exp, power, dang, kills
    pygame.display.set_icon(player_image)
    pygame.display.set_caption('Necromancer Gate')
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    if 500 < event.pos[0] < 800 and 300 < event.pos[1] < 450:
                        akk.level = None
                        playsound('start.mp3')
                        time.sleep(1)
                        playerr = 0
                        health = 100
                        lvlp = 1
                        exp = 0
                        power = 5
                        dang = 1
                        kills = 0
                        main_game()
                    if 500 < event.pos[0] < 800 and 500 < event.pos[1] < 650:
                        playsound('button.mp3')
                        top_but()
                    if 60 < event.pos[0] < 210 and 730 < event.pos[1] < 880:
                        playsound('button.mp3')
                        akk_but()
                    if 500 < event.pos[0] < 800 and 700 < event.pos[1] < 850:
                        playsound('exit.mp3')
                        terminate()
        background()
        screen.blit(load_image('play.png'), (480, 300))
        screen.blit(load_image('top.png'), (480, 500))
        screen.blit(load_image('exit.png'), (480, 700))
        screen.blit(load_image('prof.png'), (60, 730))
        pygame.display.flip()


def lose_screen():
    pygame.mixer.music.pause()
    playsound('lose.mp3')
    running = True
    sp = pygame.sprite.Group()
    gg = pygame.sprite.Sprite(sp)
    gg.image = load_image("gameover.png")
    gg.rect = gg.image.get_rect()
    gg.rect.x = 0
    gg.rect.y = 0
    al = 0
    akk.save_result(exp, lvlp, kills, dang)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                playsound('exit.mp3')
                start_screen()
        while al < 255:
            gg.image.set_alpha(al + 1)
            al += 1
            sp.draw(screen)
            fontrender(f'DANGEON: {dang}', pos=(525, 600))
            fontrender(f'LEVEL: {lvlp}', pos=(550, 660))
            fontrender(f'KILLS: {kills}', pos=(550, 720))
            pygame.display.flip()


def rand_level():
    global exp, dang
    pygame.mixer.music.pause()
    exp += 1
    levelUp()
    levels = ['map.txt', 'map1.txt', 'map2.txt', 'map3.txt', 'map4.txt']
    if akk.level and akk.level != 'map5.txt':
        levels.remove(akk.level)
        playsound('nextlevel.mp3')
    levels = tuple(levels)
    lvl = random.choice(levels)
    if dang % 5 == 0:
        pygame.mixer.music.load("data/boss_music.mp3")
        lvl = 'map5.txt'
    else:
        pygame.mixer.music.load("data/castle.mp3")
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.2)
    akk.level = lvl
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
        if s and not self.lf:
            self.image = pygame.transform.flip(self.image, True, False)
            self.lf = True
        elif not s and self.lf:
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


def levelUp():
    global exp, lvlp, health, power
    if exp >= lvlp * 5:
        playsound('levelup.mp3')
        exp = 0
        health += 30 * lvlp
        lvlp += 1
        power += 2
        running = True
        akk.save_result(exp, lvlp, kills, dang)
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                elif event.type == pygame.KEYDOWN or \
                        event.type == pygame.MOUSEBUTTONDOWN:
                    return
            screen.blit(pygame.font.Font(os.path.join('data', 'retro-land-mayhem.ttf'), 80).render(
                f'*LEVEL UP*', True,
                (0, 255, 255)),
                (400, 40))
            clock.tick(60)
            pygame.display.flip()


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
                        playsound('hit.mp3')
                        sk_h -= random.randint(0, power)
                        health -= random.randint(0, 6 - defend + int(lvlp * 1.7))
                        defend -= 1
                    if 550 < event.pos[0] < 700 and 800 < event.pos[1] < 875:
                        playsound('def.mp3')
                        defend = lvlp
                        health -= random.randint(0, 7 - defend + int(lvlp * 1.7))
                        defend -= 1
                    if 800 < event.pos[0] < 950 and 800 < event.pos[1] < 875:
                        if random.randint(0, 3) == 1:
                            playsound('escape.mp3')
                            return 2
                        health -= random.randint(0, 6 - defend + int(lvlp * 1.7))
                        defend -= 1
                    if defend < 0:
                        defend = 0
        if health <= 0:
            return 0
        if sk_h <= 0:
            kills += 1
            exp += 4
            levelUp()
            playsound('kill.mp3')
            return 1
        screen.fill((0, 0, 0))
        pygame.draw.rect(screen, (0, 255, 255), (150, 600, 980, 300), 10)
        screen.blit(load_image('skelet-f.png'), (525, 300))
        screen.blit(load_image('fight.png'), (300, 800))
        screen.blit(load_image('def.png'), (550, 800))
        screen.blit(load_image('escape.png'), (800, 800))
        my_font = pygame.font.Font(os.path.join('data', 'retro-land-mayhem.ttf'), 30)
        screen.blit(my_font.render(f'HP: {health}', True, (0, 255, 255)), (200, 620))
        screen.blit(my_font.render(f'LEVEL: {lvlp}', True, (0, 255, 255)), (420, 620))
        screen.blit(my_font.render(f'EXP: {exp}', True, (0, 255, 255)), (640, 620))
        screen.blit(my_font.render(f'POWER: {power}', True, (0, 255, 255)), (860, 620))
        screen.blit(my_font.render(f'SKELET: {sk_h} / 20', True, (0, 255, 255)), (530, 170))
        pygame.mouse.set_visible(False)
        screen.blit(load_image('curs.png'), pygame.mouse.get_pos())
        clock.tick(60)
        pygame.display.flip()


def fight_b():
    global health, lvlp, exp, power, kills, dang
    sk_h = 10 * lvlp * (dang / 5)
    defend = 0
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    if 300 < event.pos[0] < 450 and 800 < event.pos[1] < 875:
                        playsound('hit_boss.mp3')
                        sk_h -= random.randint(0, power)
                        health -= random.randint(0, 8 - defend + int(lvlp * 2))
                        defend -= 1
                    if 550 < event.pos[0] < 700 and 800 < event.pos[1] < 875:
                        playsound('def.mp3')
                        defend = lvlp
                        health -= random.randint(0, 9 - defend + int(lvlp * 2))
                        defend -= 1
                    if 800 < event.pos[0] < 950 and 800 < event.pos[1] < 875:
                        playsound('escape.mp3')
                        if random.randint(0, 5) == 1:
                            return 2
                        health -= random.randint(0, 8 - defend + int(lvlp * 2))
                        defend -= 1
                    if defend < 0:
                        defend = 0
        if health <= 0:
            playsound('dead_by_boss.mp3')
            return 0
        if sk_h <= 0:
            kills += 1
            exp += 6 * (dang / 5)
            levelUp()
            playsound('kill_boss.mp3')
            return 1
        screen.fill((0, 0, 0))
        pygame.draw.rect(screen, (0, 255, 255), (150, 600, 980, 300), 10)
        screen.blit(load_image('skelet-bf.png'), (525, 300))
        screen.blit(load_image('fight.png'), (300, 800))
        screen.blit(load_image('def.png'), (550, 800))
        screen.blit(load_image('escape.png'), (800, 800))
        my_font = pygame.font.Font(os.path.join('data', 'retro-land-mayhem.ttf'), 30)
        screen.blit(my_font.render(f'HP:{health}', True, (0, 255, 255)), (200, 620))
        screen.blit(my_font.render(f'LEVEL:{lvlp}', True, (0, 255, 255)), (420, 620))
        screen.blit(my_font.render(f'EXP:{exp}', True, (0, 255, 255)), (640, 620))
        screen.blit(my_font.render(f'POWER:{power}', True, (0, 255, 255)), (860, 620))
        screen.blit(my_font.render(f'SKELET:{sk_h} / {10 * lvlp}', True, (0, 255, 255)), (530, 170))
        pygame.mouse.set_visible(False)
        screen.blit(load_image('curs.png'), pygame.mouse.get_pos())
        clock.tick(60)
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
                        playsound('away.mp3')
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

                elif moves[pygame.K_s]:
                    if level[int(player.rect.y / 64) + 1][int(player.rect.x / 64)] == '/':
                        playsound('away.mp3')
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

                elif moves[pygame.K_a]:
                    if level[int(player.rect.y / 64)][int(player.rect.x / 64) - 1] == '/':
                        playsound('away.mp3')
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

                elif moves[pygame.K_d]:
                    if level[int(player.rect.y / 64)][int(player.rect.x / 64) + 1] == '/':
                        playsound('away.mp3')
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
                else:
                    break

                for lt in sk:
                    xx, yy = random.randint(-1, 1), random.randint(-1, 1)
                    while level[int(lt.rect.y / 64) + yy][int(lt.rect.x / 64) + xx] == '#' or \
                            level[int(lt.rect.y / 64) + yy][int(lt.rect.x / 64) + xx] == '/' or (
                            xx == 0 and yy == 0):
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
        screen.fill((0, 0, 0))
        tiles_group.draw(screen)
        player_group.draw(screen)
        screen.blit(my_font.render(f'HP:{health}', True, (0, 255, 255)), (11, 11))
        screen.blit(my_font.render(f'LEVEL:{lvlp}', True, (0, 255, 255)), (11, 44))
        screen.blit(my_font.render(f'DANGEON:{dang}', True, (0, 255, 255)), (11, 77))
        pygame.mouse.set_visible(False)
        cursor = load_image('curs.png')
        screen.blit(cursor, pygame.mouse.get_pos())
        clock.tick(60)
        pygame.display.flip()
    pygame.quit()


start_screen()
