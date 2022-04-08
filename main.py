import pygame
import random
import os

FPS = 60
WIDTH = 500
HEIGH = 800

WHITE = (255,255,255)
YELLOW = (255,255,0)
GREEN = (0,255,0)
BLACK = (0,0,0)
#游戏初始化 创建窗口
pygame.init()
pygame.display.set_caption("打飞机")
screen = pygame.display.set_mode((WIDTH,HEIGH))
clock = pygame.time.Clock()
running = True

stone_img = pygame.image.load(os.path.join("img","杀不死的赵某.png")).convert()
player_img = pygame.image.load(os.path.join("img","飞机没耳朵.png")).convert()
bullet_img = pygame.image.load(os.path.join("img","子弹维纳斯.png")).convert()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img,(50,80))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH/2
        self.rect.centery = HEIGH - 100
        self.speedx = 6
        self.speedy = 6
    def update(self):
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_RIGHT]:
            self.rect.x += self.speedx
        if key_pressed[pygame.K_LEFT]:
            self.rect.x -= self.speedx
        if key_pressed[pygame.K_UP]:
            self.rect.y -= self.speedy
        if key_pressed[pygame.K_DOWN]:
            self.rect.y += self.speedy
        
        if self.rect.right > WIDTH:
            self.rect.x = WIDTH -self.rect.width
        if self.rect.x < 0:
            self.rect.x = 0
    
    def shoot(self):
        bullet = Bullet(self.rect.centerx,self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)

class Stone(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(stone_img,(50,80))
        self.image.set_colorkey(BLACK)
        #self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0,WIDTH - self.rect.width)
        self.rect.y = random.randrange(-300,-10)
        self.speedy = random.randrange(1,10)
        self.speedx = random.randrange(-2,2)
    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.y > HEIGH or self.rect.right > WIDTH or self.rect.left < 0:
            self.rect.x = random.randrange(0,WIDTH - self.rect.width)
            self.rect.y = random.randrange(-300,-10)

class Bullet(pygame.sprite.Sprite):
    def __init__(self,x,y):  
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(bullet_img,(20,60))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -10
    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

all_sprites = pygame.sprite.Group()
stones = pygame.sprite.Group()
bullets = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
for i in range(8):
    stone = Stone()
    all_sprites.add(stone)
    stones.add(stone)

#游戏轮询
while running:
    clock.tick(FPS)
# 获取输入
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()
# 更新游戏
    all_sprites.update()
    hits = pygame.sprite.groupcollide(stones,bullets,True,True)
    for hit in hits:
        newStone = Stone()
        all_sprites.add(newStone)
        stones.add(newStone)
    pHit =  pygame.sprite.spritecollide(player,stones,False)
    if pHit:
        running = False
    # 画面渲染
    screen.fill(BLACK)
    all_sprites.draw(screen)
    pygame.display.update()   
pygame.quit()
