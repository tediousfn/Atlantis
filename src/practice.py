import pygame

screen_dim = 800

screen = pygame.display.set_mode((screen_dim,screen_dim))


#define variables
clock = pygame.time.Clock()
FPS = 60
move_left = False
move_right = False
move_up = False
move_down = False
GRAVITY = 0.75
COLS = 20
ROWS = 20
tile_size = 40

def bg():
    img = pygame.image.load('bg.jpg')
    screen.blit(img, (0,0))

def grid():
    for x in range(20):
        pygame.draw.line(screen, (0,0,0), (x * 40, 0), (x * 40, screen_dim))
    for y in range(20):
        pygame.draw.line(screen, (0,0,0), (0, y * 40), (screen_dim, y * 40))

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


        # update coordinates
        self.x += self.dx
        self.y += self.dy 
        if self.y > screen_dim - 40:
            self.y = screen_dim - 40
            self.in_air = False

        screen.blit(img, img_rect)
            
#create empty tile list
world_data = []
for row in range(ROWS):
    r = [-1] * COLS
    world_data.append(r)

#create floor
for i in range(COLS):
    world_data[19][i] = 0

for i in range(6,13):
    world_data[17][i] = 0


class World():
    def __init__(self):
        self.tile_list = []

        floor = pygame.image.load('img/tiles/0.png').convert_alpha()

        row_count = 0
        for row in world_data:
            col_count = 0
            for col in row:
                if col == 0:
                    img = floor.get_rect()
                    img.x = col_count * tile_size
                    img.y = row_count * tile_size
                    tile = (floor, img)
                    self.tile_list.append(tile)
                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0],tile[1])
            pygame.draw.rect(screen, (255,255,255), tile[1], -1)


world = World()

x = 100
y = 100

player = Player(x, y)


run = True
while run:
    clock.tick(FPS)

    bg()
    grid()
    world.draw()
    player.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        #keypresses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                move_left = True
            if event.key == pygame.K_RIGHT:
                move_right = True
            if event.key == pygame.K_SPACE:
                player.jumped = True
            
        #key released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                move_left = False
            if event.key == pygame.K_RIGHT:
                move_right = False


    pygame.display.update()
pygame.quit()
