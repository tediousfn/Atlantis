import pygame, os

pygame.init()

screen_width, screen_height = 800, 800

screen = pygame.display.set_mode((screen_width, screen_height))
screen_temp = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Platformer')

# define variables
clock = pygame.time.Clock()
FPS = 60
TILE_SIZE = 40
scroll_speed_x = 0
scroll_speed_y = 0
scroll_left = False
scroll_right = False
scroll_up = False
scroll_down = False
move_left = False
move_right = False
main_font = pygame.font.SysFont('Bauhaus 93', 40)
GRAVITY = 0.75
reset = False

world_data = []
# load game map
with open('levels/map.txt') as f:
   for line in f:
       world_data.append(list(map(int, line.strip().split(','))))

# load images
floor = pygame.image.load('img/tiles/0.png').convert_alpha()

# background images
bg_1 = pygame.image.load('img/background/0.jpg')
bg_2 = pygame.image.load('img/background/1.jpg')
bg_list = [[bg_1, bg_1], [bg_2, bg_2]]
# assets
img_assets = []
sand_img = pygame.image.load('img/background/4.png').convert_alpha()
fish_img = pygame.image.load('img/background/3.png').convert_alpha()
img_assets.append(sand_img)
img_assets.append(fish_img)

# draw text function
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x,y))

class Background:
    def __init__(self):
        self.x = 0
        self.fish_direction = False

    def draw(self):
        col_1 = 0
        col_2 = 1
        row_1 = 0
        row_2 = 1
        self.x_pos_1 = col_1 * screen_width - scroll_speed_x
        self.x_pos_2 = col_2 * screen_width - scroll_speed_x
        self.y_pos_1 = row_1 * screen_height + scroll_speed_y
        self.y_pos_2 = row_2 * screen_height + scroll_speed_y
        self.sand_pos_y = row_2 * screen_height + 400 + scroll_speed_y

        screen_temp.blit(bg_list[0][0], (self.x_pos_1, self.y_pos_1))
        screen_temp.blit(bg_list[0][1], (self.x_pos_2, self.y_pos_1))
        screen_temp.blit(bg_list[1][0], (self.x_pos_1, self.y_pos_2))
        screen_temp.blit(bg_list[1][1], (self.x_pos_2, self.y_pos_2))
        screen_temp.blit(img_assets[0], (self.x_pos_1, self.sand_pos_y)) #sand 
        screen_temp.blit(img_assets[0], (self.x_pos_2, self.sand_pos_y)) #sand
        if self.fish_direction == False:
            fish_img = img_assets[1]
        if self.fish_direction == True:
            fish_img = pygame.transform.flip(img_assets[1], True, False)
        screen_temp.blit(fish_img, (80 + self.x - scroll_speed_x, 400 + scroll_speed_y))
        if self.fish_direction == False:
            self.x += 1
            if self.x > 319:
                self.fish_direction = True
        elif self.fish_direction == True and 80 + self.x - scroll_speed_x > 0:
            self.x -= 1
            if self.x < 1:
                self.fish_direction = False



def grid():
    for i in range(40):
        pygame.draw.line(screen, (0, 0, 0), (i * TILE_SIZE, 0), (i * TILE_SIZE, screen_height))
    for j in range(40):
        pygame.draw.line(screen, (0, 0, 0), (0, j * TILE_SIZE), (screen_width, j * TILE_SIZE))

# world class

class World:
    def __init__(self, data):
        self.tile_list = []
        self.tile_type = []
        self.sub_list = []
    
        # Automated file append to tile_type list 
        for x in range(17):
            img = pygame.image.load(f'img/tiles/{x}.png').convert_alpha()
            self.tile_type.append(img)

        row_count = 0
        for row in data: 
            col_count = 0 
            for tile in row:
                if tile >= 0 and tile < len(self.tile_type):
                    img = self.tile_type[tile]
                    img_rect = img.get_rect()
                    img_rect.x = TILE_SIZE * col_count
                    img_rect.y = TILE_SIZE * row_count
                    tile = (img, img_rect, col_count, row_count)
                    self.tile_list.append(tile)
                col_count += 1
            row_count += 1
    
    def draw(self, data):
        # tile placement according to row and column digit value
        for tile in self.tile_list:
            tile[1].x = TILE_SIZE * tile[2] - scroll_speed_x
            tile[1].y = TILE_SIZE * tile[3] + scroll_speed_y
            screen.blit(tile[0], tile[1])
            pygame.draw.rect(screen, (255, 255, 255), tile[1], -1)
        

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
        self.vel_y = 0
        self.dx = 0
        self.dy = 0
        self.jumped = False
        self.in_air = False

    def update(self):
        img = pygame.image.load('img/player/idle/0.png').convert_alpha()
        img = pygame.transform.scale(img, (40,40))
        img_rect = img.get_rect()
        img_rect.x = self.x
        img_rect.y = self.y

        if move_right:
            self.dx = 3
        
        if move_left:
            self.dx = -3

        if move_right == False and move_left == False:
            self.dx = 0
        
        if self.jumped and self.in_air == False:
            self.vel_y = -15
            self.in_air = True
            self.jumped = False

        # add gravity
        self.vel_y += 1 
        if self.vel_y > 10:
            self.vel_y = 10
        self.dy = self.vel_y

        #check for collision
        for tile in world.tile_list:
            if tile[1].colliderect(self.x, self.y + self.dy, 40, 40):
                if self.vel_y < 0:
                    self.dy = tile[1].bottom - img_rect.top
                    self.vel_y = 0
                elif self.vel_y >= 0:
                    self.dy = tile[1].top - img_rect.bottom
                    self.vel_y = 0
                    self.in_air = False
            if 40 + tile[1].x >= self.x and self.y == tile[1].y:
                print("y")
                scroll_left = False
            if (40 - tile[1].x < 80 and 40 - tile[1].x > -40 and tile[1].y == self.y):
                print(40 - tile[1].x) 
            
        if reset:
            self.y = 240
        

        # update coordinates
        self.x += self.dx
        self.y += self.dy 
        if self.y > screen_height - 40:
            self.y = screen_height - 40
            self.in_air = False

        screen.blit(img, img_rect)

bg_run = Background()
world = World(world_data)

x = 40
y = 240

player = Player(x, y)

run = True
c = 0 
while run:
    clock.tick(FPS)
    fps = int(clock.get_fps())
    bg_run.draw()
    grid()
    world.draw(world_data)
    screen.blit(screen_temp, (0,0))
    player.update()
    draw_text(f'FPS: {fps}', main_font, (255, 0, 0), 650, 40)
    draw_text(f'X: {player.x}', main_font, (255, 0, 0), 40, 40)
    draw_text(f'Y: {player.y}', main_font, (255, 0, 0), 120, 40)
    
    if scroll_right and bg_run.x_pos_1 > -screen_width: 
        scroll_speed_x += 5
    if scroll_left and bg_run.x_pos_1 < 0: 
        scroll_speed_x -= 5
    if scroll_up and bg_run.y_pos_1 < 0:
        scroll_speed_y += 5
    if scroll_down and bg_run.y_pos_1 > -screen_height:
        scroll_speed_y -= 5
    
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        #keyboard presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                scroll_right = True
                move_right = False
            if event.key == pygame.K_LEFT:
                for tile in world.tile_list:
                    #scroll_left = player.y == tile[1].y and 40 - tile[1].x <= 45
                    if not (40 + tile[1].x >= player.x and player.y == tile[1].y):
                        print('s')
                        scroll_left = True
                    else:
                        scroll_left = False
                #move_left = False
            if event.key == pygame.K_SPACE:
                player.jumped = True
            if event.key == pygame.K_b:
                reset = True
            
            
        
        #keyboard released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                scroll_right = False
                move_right = False
            if event.key == pygame.K_LEFT:
                scroll_left = False
                move_left = False
            if event.key == pygame.K_b:
                reset = False


    pygame.display.update()
        


