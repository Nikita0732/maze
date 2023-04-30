#создай игру "Лабиринт"
from pygame import *
from pygame import mixer

#создай окно игры
window = display.set_mode((700, 500))
display.set_caption('Лабиринт')
#задай фон сцены
background = transform.scale(image.load('background.jpg'), (700, 500))
mixer.init()
mixer.music.load('jungles.ogg')
mixer.music.play()
money = mixer.Sound('money.ogg')
kick = mixer.Sound('kick.ogg')
#создай 2 спрайта и размести их на сцене
FPS = 60
clock = time.Clock()
x1 = 100
y1 = 300
x2 = 200
y2 = 300
win_width = 700
win_height = 500
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (65, 65))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < win_height - 80:
            self.rect.y += self.speed
class Enemy(GameSprite):
    def update(self):
        if self.rect.x <= 470:
            self.direction = 'right'
        if self.rect.x >= win_width - 85:
            self.direction = 'left'

        if self.direction == 'left':
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed

class Wall(sprite.Sprite):
    def __init__(self, color_1, color_2, color_3, wall_x, wall_y, wall_width, wall_height):
        super().__init__()
        self.color_1 = color_1
        self.color_2 = color_2
        self.color_3 = color_3
        self.width = wall_width
        self.height = wall_height
        self.image = Surface((self.width, self.height))
        self.image.fill((color_1, color_2, color_3))
        self.rect = self.image.get_rect()
        self.rect.x = wall_x
        self.rect.y = wall_y
    def draw_wall(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
font.init()
f1 = font.Font(None, 70)
f2 = font.Font(None, 70)
win = f1.render('YOU WIN!', True, (255, 215, 0))
lose = f2.render('YOU LOSE!', True, (255, 215, 0))
#обработай событие «клик по кнопке "Закрыть окно"»
game = True
finish = False
Player = Player('hero.png', 5, 420, 4)
Monster = Enemy('cyborg.png', 620, 280, 4)
treasure = GameSprite('treasure.png', 580, 420, 0)
w1 = Wall(154, 205, 50, 100, 20, 450, 10)
w2 = Wall(154, 205, 50, 100, 480, 350, 10)
w3 = Wall(154, 205, 50, 100, 20, 10, 380)
w4 = Wall(154, 205, 50, 200, 110 , 10, 370)
while game: 
    for e in event.get():
        if e.type == QUIT:
            game = False
    if finish != True:
        window.blit(background,(0, 0))
        if sprite.collide_rect(Player, treasure):
            finish = True
            window.blit(win, (200, 200))
            money.play()
            
        if sprite.collide_rect(Player, Monster) or sprite.collide_rect(Player, w1) or sprite.collide_rect(Player, w2) or sprite.collide_rect(Player, w3) or sprite.collide_rect(Player, w4):
            window.blit(lose, (200, 200))
            kick.play()
            finish = True
            
        Player.reset()
        Player.update()
        Monster.update()
        w1.draw_wall()
        w2.draw_wall()
        w3.draw_wall()
        w4.draw_wall()
        Monster.reset()
        treasure.reset()
        display.update()
    
    clock.tick(FPS)