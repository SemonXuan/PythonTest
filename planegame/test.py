# -*- coding: utf-8 -*-
# __author : swu291
# date : 1/2/18 5:39 PM

import pygame
from pygame.locals import *
import time
import random

class Base(object):
    def __init__(self,screen_temp, x, y, image_name):
        self.x = x
        self.y = y
        self.image = pygame.image.load(image_name)
        self.screen = screen_temp

class BasePlane(Base):
    def __init__(self,screen_temp, x, y, image_name):
        Base.__init__(self,screen_temp, x, y, image_name)
        self.bullet_list = [] # 存储发射出去的子弹对象引用

    def display(self):
        self.screen.blit(self.image,(self.x,self.y))

        for bullet in self.bullet_list:
            bullet.display()
            bullet.move()
            if bullet.judge():
                self.bullet_list.remove(bullet)

class HeroPlane(BasePlane):
    def __init__(self,screen_temp):
        BasePlane.__init__(self, screen_temp, 165, 530, "./images/hero.png") # super().__init__()

    def move_left(self):
        self.x -= 5

    def move_right(self):
        self.x += 5

    def fire(self):
        # 创建一个子弹对象
        self.bullet_list.append(Bullet(self.screen, self.x, self.y))

# 敌机的类
class EnemyPlane(BasePlane):
    def __init__(self,screen_temp):
        BasePlane.__init__(self, screen_temp, 0, 0, "./images/enemy.png")  # super().__init__()
        self.direction = "right" # 存储飞机默认的显示方向

    def move(self):
        if self.direction == "right":
            self.x += 5
        elif self.direction == "left":
            self.x -= 5

        if self.x > 315:
            self.direction = "left"
        elif self.x <= 0:
            self.direction = "right"

    def fire(self):
        random_num = random.randint(1,100)
        if random_num == 48 or random_num == 20:
            # 创建一个敌机子弹对象
            self.bullet_list.append(EnemyBullet(self.screen, self.x, self.y))

class BaseBullet(Base):
    def __init__(self,screen_temp, x, y, image_name):
        Base.__init__(self,screen_temp, x, y, image_name)

    def display(self):
        self.screen.blit(self.image,(self.x,self.y))

class Bullet(BaseBullet):
    def __init__(self, screen_temp, x, y):
        BaseBullet.__init__(self, screen_temp, x + 30, y - 30, "./images/bullet.png")

    def move(self):
        self.y -= 5

    def judge(self):
        if self.y < 0:
            return True
        else:
            return False

class EnemyBullet(BaseBullet):
    def __init__(self, screen_temp, x, y):
        BaseBullet.__init__(self, screen_temp, x + 43, y + 66, "./images/enemyBullet.png")

    def move(self):
        self.y += 5

    def judge(self):
        if self.y > 600:
            return True
        else:
            return False

def key_control(hero_temp):
    # 获取时间，比如按键等
    for event in pygame.event.get():

        # 判断是否是点击了退出按钮
        if event.type == QUIT:
            print("exit")
            exit()
        # 判断是否按下了键
        elif event.type == KEYDOWN:
            # 检测按键是否是a或者left
            if event.type == K_a or event.key == K_LEFT:
                print('left')
                hero_temp.move_left()
                hero_temp.fire()
            # 检测按键是否是d或者right
            elif event.type == K_d or event.key == K_RIGHT:
                print('right')
                hero_temp.move_right()
                hero_temp.fire()
            # 检测按键是否是空格键
            elif event.key == K_SPACE:
                print('space')

def main():

    #1. 创建一个窗口，用来显示内容
    screen = pygame.display.set_mode((400,600),0,32)

    #2. 创建一个和窗口大小的图片，用来当背景
    background = pygame.image.load("./images/background.jpg")

    #3. 创建一个飞机对象
    hero = HeroPlane(screen)

    #4. 创建一个敌机对象
    enemy = EnemyPlane(screen)

    #5. 把背景图片放到窗口中显示
    while True:

        #设定需要显示的背景图
        screen.blit(background,(0,0))
        hero.display()
        enemy.display()
        enemy.move() # 调用敌机的移动方法
        enemy.fire()
        #更新需要显示的内容
        pygame.display.update()
        key_control(hero)
        time.sleep(0.01)

if __name__ == "__main__":
    main()

