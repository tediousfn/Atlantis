import pygame, os, csv

pygame.init()

screen_width, screen_height = 1600, 800

screen = pygame.display.set_mode((screen_width, screen_height))

#define variables
FPS = 60
clock = pygame.time.Clock()
ROWS = 40
COLS = 40
TILE_SIZE = 40
scroll_up = False
scroll_down = False
scroll_speed = 0
speed = 4
save = False
level = 0
lvl_1 = False
lvl_2 = False
cht = False
current_tile = 0
reset = False

#define font
font = pygame.font.SysFont('Futura', 20)

#create empty tile list
world_data = []
for row in range(ROWS):
    r = [-1] * COLS
    world_data.append(r)

#create ground 
for tile in range(COLS):
    world_data[ROWS - 1][tile] = 0

def bg():
    screen.fill((100, 100, 100))

def grid():
    for col in range(COLS):
        pygame.draw.line(screen, (255,255,255), (col * TILE_SIZE, 0 - scroll_speed), (col * TILE_SIZE, screen_height * 2 - scroll_speed))
    for row in range(ROWS):
        pygame.draw.line(screen, (255,255,255), (0, row * TILE_SIZE - scroll_speed), (screen_width, row * TILE_SIZE - scroll_speed))

#load tiles
tile_list = []
for i in range(17):
    img = pygame.image.load(f'img/tiles/{i}.png')
    tile_list.append(img)

def draw_world():
    row_count = 0
    for row in world_data:
        col_count = 0
        for tile in row:
            if tile >= 0 and tile < len(tile_list):
                screen.blit(tile_list[tile], (col_count * TILE_SIZE, row_count * TILE_SIZE - scroll_speed))
            col_count += 1
        row_count += 1

#function for outputting text onto the screen
def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))
    

run = True
while run:
    clock.tick(FPS)
    bg()
    grid()
    draw_world()
    #draw_text(f'LVL: {level}', font, (255, 255, 255), 1500, 30)
    if save:
        ans = input('Want to save? ')
        if ans.lower() == 'y':
            with open(f'level{level}_data.csv', 'w', newline='') as csvfile:
                writer = csv.writer(csvfile, delimiter=',')
                for row in world_data:
                    writer.writerow(row)
        else:
            pass


    if reset:
        for i in range(ROWS - 1):
            for col in range(COLS):
                world_data[i][col] = -1

    pos = pygame.mouse.get_pos()
    x = pos[0] // TILE_SIZE
    y = (pos[1] + scroll_speed) // TILE_SIZE
    
    if pos[0] < screen_width and pos[1] < screen_height:
        #update tile value
        if pygame.mouse.get_pressed()[0] == 1:
            if world_data[y][x] != current_tile:
                world_data[y][x] = current_tile
        if pygame.mouse.get_pressed()[2] == 1:
            world_data[y][x] = -1

    if scroll_up and scroll_speed > 0:
        scroll_speed -= speed
    if scroll_down and scroll_speed < 800:
        scroll_speed += speed

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        #keypresses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                scroll_up = True
            if event.key == pygame.K_DOWN:
                scroll_down = True
            if event.key == pygame.K_t:
                save = True
            if event.key == pygame.K_1:
                current_tile = 0
            if event.key == pygame.K_2:
                current_tile = 1
            if event.key == pygame.K_3:
                current_tile = 2
            if event.key == pygame.K_4:
                current_tile = 3
            if event.key == pygame.K_5:
                current_tile = 4
            if event.key == pygame.K_6:
                current_tile = 5
            if event.key == pygame.K_7:
                current_tile = 6
            if event.key == pygame.K_8:
                current_tile = 7
            if event.key == pygame.K_9:
                current_tile = 8
            if event.key == pygame.K_h:
                current_tile = 9
            if event.key == pygame.K_j:
                current_tile = 10
            if event.key == pygame.K_k:
                current_tile = 11
            if event.key == pygame.K_l:
                current_tile = 12
            if event.key == pygame.K_b:
                current_tile = 13
            if event.key == pygame.K_n:
                current_tile = 14
            if event.key == pygame.K_m:
                current_tile = 15
            if event.key == pygame.K_p:
                current_tile = 16
            if event.key == pygame.K_c:
                reset = True
        
        # key release
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                scroll_up = False
            if event.key == pygame.K_DOWN:
                scroll_down = False
            if event.key == pygame.K_t:
                save = False
            if event.key == pygame.K_c:
                reset = False



    pygame.display.update()

pygame.quit()