import pygame
from global_names import *
from tools import *
from generate_level import generate_level
from Sprites import Stop, RegulateMusic


def events(intro=False):
    global running
    global intro_screen
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONUP:
            x, y = event.pos
            if 31 * CELL_SIZE > x > 29 * CELL_SIZE and 31 * CELL_SIZE > y > 29 * CELL_SIZE:
                game_obj['RegulateMusic'].change_sound_mode()
        elif event.type == GAME_STARTING_EVENT_ID:
            intro_screen = False
        elif event.type == pygame.KEYUP:
            key = event.key
            if key == pygame.K_ESCAPE:
                if game_obj['Stop'] is None:
                    game_obj['Stop'] = Stop(10, 11, stop_group, all_sprites)
                    game_parameters['stopped timer'] = mod_changed_time()
                    pause_music()
                else:
                    for i in stop_group:
                        i.kill()
                    game_obj['Stop'] = None
                    pygame.mixer.music.unpause()
                    timer(game_parameters['stopped timer'],
                          event_id=CHANGE_TO_EVENT_ID[game_parameters['mod']])
            elif key in [UP, DOWN, LEFT, RIGHT] and intro is False:
                game_obj['Pac-Man'].key_pressed(key)
        if game_obj['Stop'] is None and intro is False:
            if event.type == DEFAULT_EVENT_ID:
                if game_parameters['mod'] not in [FRIGHTENED, H_FRIGHTENED]:
                    ans = ['Mod changed from', game_parameters['mod'], 'to']
                    change_mod()
                    ans.append(game_parameters['mod'])
                    print(game_parameters['timer_num'])
                    print(' '.join(ans))
                    timer()
            elif event.type == FRIGHTENED_EVENT_ID:
                game_parameters['mod'] = H_FRIGHTENED
                time = time_in_frightened_mod()
                pygame.time.set_timer(HALF_FRIGHTENED_EVENT_ID, int(time * 0.5), True)
                game_parameters[H_FRIGHTENED] = True
            elif event.type == HALF_FRIGHTENED_EVENT_ID:
                game_parameters['mod'] = game_parameters['saved mod']
                game_parameters['ate ghosts'] = -1
                change_frightened(False)
                timer(game_parameters['stopped timer'])


def change_mod():
    if game_parameters['timer_num'] % 2 == 0:
        game_parameters['mod'] = SCATTER
    else:
        game_parameters['mod'] = CHASE
    change_way()


def draw_rect():
    for i in range(28):
        for j in range(31):
            pygame.draw.rect(screen, (125, 0, 0), (i * CELL_SIZE, j * CELL_SIZE,
                                                   CELL_SIZE, CELL_SIZE), width=1)


def update_fps():
    fps = str(int(clock.get_fps()))
    fps_text = font.render(fps, 1, pygame.Color("coral"))
    return fps_text


def timer(time=None, event_id=None):
    if time is not None:
        pygame.time.set_timer(event_id if event_id is not None else DEFAULT_EVENT_ID, time, True)
        return None
    for i in LEVEL_TIME_CHANGE:
        if str(game_parameters['level']) in i.split(' '):
            time = int(LEVEL_TIME_CHANGE[i][game_parameters['timer_num']] * 1000)
    if time is None:
        time = int(LEVEL_TIME_CHANGE['infinity'][game_parameters['timer_num']] * 1000)
    pygame.time.set_timer(DEFAULT_EVENT_ID, time, True)
    game_parameters['mod changed time'] = pygame.time.get_ticks()
    game_parameters['timer_num'] += 1


def update_level():
    text = str(game_parameters['level']) + 'UP'
    return font.render(text, 1, pygame.Color("white"))


def check_game_score():
    if len(energizers_group) == len(foods_group) == 0 and game_parameters['mod'] != GAME_OVER:
        game_parameters['level'] += 1
        game_parameters['mod'] = ROUND_OVER


def check_game_status():
    mod = game_parameters['mod']
    if mod in [ROUND_OVER, ATTEMPT, GAME_OVER]:
        game_parameters['mod'] = SCATTER
        game_parameters['timer_num'] = 0
        game_parameters['score per round'] = 0
        game_parameters['mod changed time'] = 0
        change_frightened(False)

        if mod == GAME_OVER:
            game_parameters['score'] = 0
            game_parameters['saved mod'] = None
            game_parameters['ate ghosts'] = -1
            game_parameters['stopped timer'] = 0
        elif mod == ROUND_OVER:
            kill_all_sprites()

        #reset timers
        pygame.time.set_timer(DEFAULT_EVENT_ID, 0, True)
        pygame.time.set_timer(FRIGHTENED_EVENT_ID, 0, True)
        pygame.time.set_timer(HALF_FRIGHTENED_EVENT_ID, 0, True)

        param = True if mod in [ROUND_OVER, GAME_OVER] else False
        generate_level(game_parameters['map'], new_game=param)
        if GAME_OVER == mod:
            start_screen()
            start_background_music()
        timer()


def score_update():
    return font_score.render(str(game_parameters['score']), 1, pygame.Color("white"))


def start_screen():
    global intro_screen
    pygame.mixer.music.load(os.path.join('data/game/music', 'intro.wav'))
    pygame.mixer.music.play()
    if game_parameters['sound on'] is False:
        pygame.mixer.music.pause()
    im = pygame.transform.scale(load_image('ready!.jpg', key_path='game'),
                                (CELL_SIZE * 7, CELL_SIZE * 1))
    all_sprites.update()
    all_sprites.draw(screen)
    pygame.display.flip()
    pygame.time.set_timer(GAME_STARTING_EVENT_ID, 4200, True)
    intro_screen = True
    while intro_screen:
        events(True)
        screen.fill(BLACK)
        screen.blit(im, (11 * CELL_SIZE, 17 * CELL_SIZE))
        game_obj['RegulateMusic'].update()
        all_sprites.draw(screen)
        pygame.display.flip()


def check_music():
    if pygame.mixer.music.get_busy() is False:
        pygame.mixer.music.play()


def start_background_music():
    pygame.mixer.music.load(os.path.join('data/game/music', 'fon.mp3'))
    pygame.mixer.music.play()
    if game_parameters['sound on'] is False or game_obj['Stop'] is not None:
        pygame.mixer.music.pause()


def draw_border():
    pygame.draw.rect(screen, BLUE, (0, 0, CELL_SIZE * 28, CELL_SIZE * 31), width=1)


if __name__ == '__main__':
    pygame.init()
    size = WIDTH, HEIGHT
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Pac-Man')
    pygame.display.set_icon(load_image('pacman.ico', key_path='game'))

    font = pygame.font.SysFont("Comic Sans MS", 32)
    font_score = pygame.font.SysFont("PerfectDOSVGA437", 62)

    clock = pygame.time.Clock()
    running = True
    load_sprites()
    load_musics()
    game_parameters['map'] = load_level('map.txt')
    game_obj['RegulateMusic'] = RegulateMusic(29, 29, all_sprites)
    generate_level(game_parameters['map'])
    start_screen()
    timer()
    start_background_music()
    #fon = pygame.transform.scale(load_image('field.jpg'), (CELL_SIZE * 28, CELL_SIZE * 31))
    while running:
        check_music()
        check_game_score()
        check_game_status()
        #screen.blit(fon, (0, 0))
        screen.fill(BLACK)
        events()
        screen.blit(update_fps(), (CELL_SIZE * 29, 0))
        screen.blit(score_update(), (int(CELL_SIZE * 28.5), CELL_SIZE * 3))
        screen.blit(update_level(), (CELL_SIZE * 29, CELL_SIZE * 5))
        if game_obj['Stop'] is None:
            all_sprites.update()
        all_sprites.draw(screen)
        clock.tick(FPS)
        #draw_rect()
        draw_border()
        pygame.display.flip()
        #game_parameters['mod'] = 'frightened'
    pygame.quit()
