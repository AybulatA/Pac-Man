import pygame
from global_names import *
from tools import *
from generate_level import generate_level


def events():
    global running
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYUP:
            game_obj['Pac-Man'].key_pressed(event.key)
        elif event.type == DEFAULT_EVENT_ID:
            if game_parameters['mod'] != FRIGHTENED:
                ans = ['Mod changed from', game_parameters['mod'], 'to']
                change_mod()
                ans.append(game_parameters['mod'])
                print(game_parameters['timer_num'])
                print(' '.join(ans))
                timer()
        elif event.type == FRIGHTENED_EVENT_ID:
            game_parameters['mod'] = H_FRIGHTENED
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


def timer(time=None):
    for i in LEVEL_TIME_CHANGE:
        try:
            if str(game_parameters['level']) in i:
                if time is None:
                    time = int(LEVEL_TIME_CHANGE[i][game_parameters['timer_num']] * 1000)
                    game_parameters['timer_num'] += 1
                pygame.time.set_timer(DEFAULT_EVENT_ID, time, True)
                break
        except Exception:
            pass


def draw_score():
    return font.render(str(game_parameters['score']), 1, pygame.Color("white"))


def check_game_score():
    if len(energizers_group) == len(foods_group) == 0 and game_parameters['mod'] != GAME_OVER:
        game_parameters['level'] += 1
        game_parameters['mod'] = ROUND_OVER


def check_game_status():
    mod = game_parameters['mod']
    if mod == ROUND_OVER or mod == ATTEMPT:
        game_parameters['mod'] = SCATTER
        game_parameters['timer_num'] = 0
        change_frightened(False)

        #reset timers
        pygame.time.set_timer(DEFAULT_EVENT_ID, 0, True)
        pygame.time.set_timer(FRIGHTENED_EVENT_ID, 0, True)
        pygame.time.set_timer(HALF_FRIGHTENED_EVENT_ID, 0, True)

        if mod == ROUND_OVER:
            kill_all_sprites()

        param = True if mod == ROUND_OVER else False
        generate_level(game_parameters['map'], new_game=param)
        timer()
    elif mod == GAME_OVER:
        pass
    elif mod == STOP:
        pygame.time.wait(500)
        game_parameters['mod'] = FRIGHTENED


def score_update():
    return font_score.render(str(game_parameters['score']), 1, pygame.Color("white"))


if __name__ == '__main__':
    pygame.init()
    size = WIDTH, HEIGHT
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Pac-Man')

    font = pygame.font.SysFont("Arial", 18)
    font_score = pygame.font.SysFont("PerfectDOSVGA437", 36)

    timer()
    clock = pygame.time.Clock()
    running = True
    #start_screen(screen)
    game_parameters['map'] = load_level('map.txt')
    generate_level(game_parameters['map'])
    print(len(foods_group))
    #fon = pygame.transform.scale(load_image('field.jpg'), (CELL_SIZE * 28, CELL_SIZE * 31))
    while running:
        check_game_score()
        check_game_status()
        #screen.blit(fon, (0, 0))
        screen.fill(BLACK)
        events()
        screen.blit(update_fps(), (CELL_SIZE * 29, 0))
        screen.blit(score_update(), (CELL_SIZE * 29, CELL_SIZE * 3))
        all_sprites.update()
        all_sprites.draw(screen)
        clock.tick(FPS)
        #draw_rect()
        pygame.display.flip()
        #game_parameters['mod'] = 'frightened'
    pygame.quit()
