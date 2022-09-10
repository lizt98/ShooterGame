#Create your own shooter
from pygame import *
from random import randint


background = \
    transform.scale(
        image.load("galaxy.jpg"),    
        (700, 500)
    )

class Character(sprite.Sprite):
    #TODO create init function takes in x, y, width, height, speed
    def __init__ (self, img_file, x, y, width, height, speed):
        super().__init__() #TODO create the sprite.Sprite class first
        self. image = transform.scale(image.load(img_file), (width, height))

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.speed = speed

    def draw(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

#TODO create Player class derived from Character
class Player(Character):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT]:
            self.rect.x -= self.speed
        if keys[K_RIGHT]:
            self.rect.x += self.speed

    def shoot(self):
        #x, y, width, height, speed
        #create a bullet object
        bullet = Bullet("bullet.png", self.rect.centerx, self.rect.top, 15, 40, 2)
        

        #add that object to the group
        bullets.add(bullet) 


#TODO create Enemy class derived from Character class
class Enemy(Character):
    def update(self):
        self.rect.y += self.speed
        global missed
        if self.rect.y > win_height:
            self.rect.y = randint(-10, -1)
            self.rect.x = randint(0, win_width -50)

            missed += 1
        


class Bullet(Character):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()  

    

bullets = sprite.Group()

score = 0

missed = 0

level = 1

win_width = 700
win_height = 500

enemies = sprite.Group()
for i in range(level * 2):
    enemy = Enemy("ufo.png", randint(0, win_width -50), randint(-10, -1), 50, 50, 1)
    enemies.add(enemy)
 

window = display.set_mode((700, 500))
display.set_caption("Shooter Game")

#music
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire = mixer.Sound('fire.ogg')
fire.play()

#width, height, xcor, ycor, color
rocket = Player("rocket.png", 350, 450, 50, 50, 2)
enemy = Enemy("ufo.png", 100, 100, 50, 50, 1)

game = True
finish = False

font.init()
font1 = font.Font(None, 40)
score_txt = font1.render(f"Score:{score}", True, (255, 255, 255))

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                if finish == False:
                    rocket.shoot()
                if finish == True:
                    finish = False
                    missed = 0
                    score = 0
                    level += 1
                    enemies.empty()
                    for i in range(level * 2):
                        enemy = Enemy("ufo.png", randint(0, win_width -50), randint(-10, -1), 50, 50, 1)
                        enemies.add(enemy)

                    

    if not finish:

        window.blit(background,(0, 0)) #draw the background
        window.blit(score_txt, (15, 50))
        missed_txt = font1.render(f"Missed:{missed}", True, (255, 255, 255))
        window.blit(missed_txt, (15, 15))
        rocket.draw()
        enemies.draw(window)
        enemies.update()


        

        bullets.draw(window)
        bullets.update()
        rocket.update()

        

        collisions = sprite.groupcollide(enemies, bullets, True, True)
        for i in collisions:
            #create new Enemy
            enemy = Enemy("ufo.png", randint(0, win_width -50), randint(-10, -1), 50, 50, 1)
            score += 1
            score_txt = font1.render(f"Score:{score}", True, (255, 255, 255))

            #add to group
            enemies.add(enemy)

        if score >= 20:
            win_txt = font1.render("You win!", True, (255, 255, 255))
            window.blit(win_txt, (300, 200))
            finish = True

        if missed >= 20 or sprite.spritecollide(rocket, enemies, True):
            lose_txt = font1.render("You lose!", True, (255, 255, 255))
            window.blit(lose_txt, (300, 200))
            finish = True 

            
    

    display.update()


