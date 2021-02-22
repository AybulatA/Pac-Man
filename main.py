import pygame
from global_names import *
from tools import *
from generate_level import generate_level
from Sprites import Stop


def events():
    global running
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYUP:
            key = event.key
            if key in [UP, DOWN, LEFT, RIGHT]:
                game_obj['Pac-Man'].key_pressed(key)
            elif key == pygame.K_ESCAPE:
                if game_obj['Stop'] is None:
                    game_obj['Stop'] = Stop(10, 11, stop_group, all_sprites)
                    game_parameters['stopped timer'] = pygame.time.get_ticks()
                else:
                    for i in stop_group:
                        i.kill()
                    game_obj['Stop'] = None
                    timer(pygame.time.get_ticks() - game_parameters['stopped timer'],
                          event_id=CHANGE_TO_EVENT_ID[game_parameters['mod']])
        if game_obj['Stop'] is None:
            if event.type == DEFAULT_EVENT_ID:
                if game_parameters['mod'] != FRIGHTENED:
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
            elif event.type == HALF_FRIGHTENED_EVENT_ID:
                game_parameters['mod'] = game_parameters['saved mod']
                game_parameters['ate ghosts'] = -1
                change_frightened(False)
                timer(pygame.time.get_ticks() - game_parameters['stopped timer'])


def change_mod():
    if game_parameters['timer_num'] % 2 == 0:
        game_parameters['mod'] = SCATTER
    else:
        game_parameters['mod'] = CHASE
    change_way()


def draw_rect():
    for i in range(28):
        for j in range(31):
            pygame.draw.rect(screen, (125, 0, 0), (i * CELL_SIZE, j * CELL_SIZE, CELL_SIZE, CELL_SIZE), width=1)


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
        change_frightened(False)

        if mod == GAME_OVER:
            game_parameters['score'] = 0
            game_parameters['saved mod'] = None
            game_parameters['ate ghosts'] = -1
            game_parameters['stopped timer'] = 0

        #reset timers
        pygame.time.set_timer(DEFAULT_EVENT_ID, 0, True)
        pygame.time.set_timer(FRIGHTENED_EVENT_ID, 0, True)
        pygame.time.set_timer(HALF_FRIGHTENED_EVENT_ID, 0, True)

        param = True if mod in [ROUND_OVER, GAME_OVER] else False
        generate_level(game_parameters['map'], new_game=param)
        timer()
    elif mod == STOP:
        pygame.time.wait(500)
        game_parameters['mod'] = FRIGHTENED


def score_update():
    return font_score.render(str(game_parameters['score']), 1, pygame.Color("white"))


def start_screen():
    pygame.mixer.music.load(os.path.join('data/game/music', 'intro.wav'))
    pygame.mixer.music.play()
    im = pygame.transform.scale(load_image('ready!.jpg', key_path='game'),
                                (CELL_SIZE * 7, CELL_SIZE * 1))
    screen.blit(im, (11 * CELL_SIZE, 17 * CELL_SIZE))
    all_sprites.update()
    all_sprites.draw(screen)
    pygame.display.flip()
    while pygame.mixer.music.get_busy():
        pass


if __name__ == '__main__':
    pygame.init()
    size = WIDTH, HEIGHT
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Pac-Man')

    font = pygame.font.SysFont("Arial", 18)
    font_score = pygame.font.SysFont("PerfectDOSVGA437", 36)

    clock = pygame.time.Clock()
    running = True
    load_sprites()
    game_parameters['map'] = load_level('map.txt')
    generate_level(game_parameters['map'])
    start_screen()
    timer()
    #fon = pygame.transform.scale(load_image('field.jpg'), (CELL_SIZE * 28, CELL_SIZE * 31))
    while running:
        check_game_score()
        check_game_status()
        #screen.blit(fon, (0, 0))
        screen.fill(BLACK)
        events()
        screen.blit(update_fps(), (CELL_SIZE * 29, 0))
        screen.blit(score_update(), (CELL_SIZE * 29, CELL_SIZE * 3))
        screen.blit(update_level(), (CELL_SIZE * 29, CELL_SIZE * 4))
        if game_obj['Stop'] is None:
            all_sprites.update()
        all_sprites.draw(screen)
        clock.tick(FPS)
        #draw_rect()
        pygame.display.flip()
        #game_parameters['mod'] = 'frightened'
    pygame.quit()
