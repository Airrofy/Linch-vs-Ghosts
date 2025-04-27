#Создай собственный Шутер!

from pygame import *
from random import*



class GameSprite(sprite.Sprite):
    def __init__(self, s, size, pos, speed):
        super().__init__()
        self.image = transform.scale(image.load(s), (size[0], size[1]))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def update(self, window):
        window.blit(self.image, self.rect)

    def move_up(self):
        self.rect.y -= self.speed

    def move_down(self):
        self.rect.y += self.speed

    def move_left(self):
        self.rect.x -= self.speed

    def move_right(self):
        self.rect.x += self.speed

    def check_collision(self, other_sprite):
        return self.rect.colliderect(other_sprite.rect)



class Player(GameSprite):
    def update(self, window):
        window.blit(self.image, self.rect)
    
        keys_pressed = key.get_pressed()

        if keys_pressed[K_LEFT] and  self.rect.x > 5:
            self.move_left()
        if keys_pressed[K_RIGHT] and  self.rect.x < 595:
            self.move_right()
        if keys_pressed[K_UP] and  self.rect.y > 5:
            self.move_up()
        if keys_pressed[K_DOWN] and  self.rect.y < 395:
            self.move_down()
    def fire(self):
        bullet = Bullet('bullet.png', (20,25),(self.rect.centerx, self.rect.y), 9)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        window.blit(self.image, self.rect)
        self.rect.x -= self.speed
        if self.rect.x < 0:
            self.rect.y = randint(200,height)
            self.rect.x = 800
            global lost
            lost += 1

class Bullet(GameSprite):
    def update(self):
        window.blit(self.image, self.rect)
        self.rect.x += self.speed

bullets = sprite.Group()      


player = Player('Линчикс.jpg',(95,145), (250,300), 6)

clock = time.Clock()
FPS = 30

lost = 0



width,height = 700, 500
window = display.set_mode((width,height))
display.set_caption("Шутер", "rocket.png")
background = transform.scale(image.load("фон.jpg"), (width,height))
is_game = True

enemys = sprite.Group()
for i in range(4):
    enemy = Enemy('Призрак.jpg',(75,110), (800, randint(200,height-150)), randint(1,3))
    enemys.add(enemy)

font.init()
font_stat = font.SysFont('Arial', 32)

score = 0


font.init()
font_stat = font.SysFont('Arial', 32)

score = 0

hp = 5


mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
sound_fire = mixer.Sound('fire.ogg')
mixer.music.set_volume(0.5)
sound_fire.play()

GAME = 0
WIN = 1
LOSE = 2
game_state = GAME

while(is_game):
    for e in event.get():
        if e.type == QUIT:
            is_game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                player.fire()
    if game_state == GAME:
        window.blit(background,(0, 0))
        player.update(window)
        enemys.update()
        enemys.draw(window)
        bullets.draw(window)
        bullets.update()
        sprite_list=sprite.spritecollide(
        player, enemys, False, )

        for i in sprite_list:
            x,y = 800, randint(200,height-150)
            i.rect.x = x
            i.rect.y = y
            player.rect.x, player.rect.y = 250,300
            hp -= 1
        text_score = font_stat.render(f'hp: {hp}', True, (255, 150, 150))
        window.blit(text_score, (5,50))

        collides=sprite.groupcollide(
        enemys, bullets, False, True)
        for i in collides:
            x,y = (800, randint(200,height-150))
            i.rect.x = x
            i.rect.y = y
            score += 1
        text_score = font_stat.render(f'Cчёт: {score}', True, (255, 255, 255))
        window.blit(text_score, (5,5))
        if hp <= 0:
            game_state = LOSE
        if score >= 30:
            game_state = WIN
    elif game_state == LOSE:
        window.fill((0,0,0))
        text_score = font_stat.render('ТЫ ПРОИГРАЛ...', True, (255,80,80))
        window.blit(text_score, (250,220))

        
    elif game_state == WIN:
        window.fill((0,0,0))
        text_score = font_stat.render('ТЫ ВЫЖИЛ, НА ЭТОТ РАЗ..', True, (255,80,80))
        window.blit(text_score, (250,220))

    display.update()
    clock.tick(FPS)