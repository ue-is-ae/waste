import sys
import random
import pygame
from pygame.locals import *

def print_text(font, x, y, text, color=(225, 0, 0)):
    imgText = font.render(text, True, color)
    screen.blit(imgText, (x, y))

pygame.init()
screen = pygame.display.set_mode((1024, 768))
pygame.display.set_caption("Bomberman")
font_00 = pygame.font.Font(None, 26)
font_01 = pygame.font.Font(None, 48)
pygame.mouse.set_visible(False)

white = (255, 255, 255)
red = (230, 50, 50)
yellow = (237, 136, 35)
black = (0, 0, 0)

lives = 3
score = 0
high_score = 0
game_over = True
mouse_x = mouse_y = 0
pos_x = 300
pos_y = 460

# 定义炸弹类型
bomb_types = [
    {"color": red, "speed": 7.0, "score": 5},
    {"color": yellow, "speed": 8.0, "score": 10},
    {"color": black, "speed": 9.0, "score": 20}
]

current_bomb = random.choice(bomb_types)
bomb_x = random.randint(0, 1000)
bomb_y = -50
vel_y = current_bomb["speed"]
level = 1

# 游戏循环
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()
        elif event.type == MOUSEMOTION:
            mouse_x, mouse_y = event.pos
            pos_x = mouse_x
        elif event.type == MOUSEBUTTONUP:
            if game_over:
                game_over = False
                lives = 3
                score = 0
                level = 1
                current_bomb = random.choice(bomb_types)
                bomb_x = random.randint(0, 1000)
                bomb_y = -50
                vel_y = current_bomb["speed"]

    keys = pygame.key.get_pressed()
    if keys[K_ESCAPE]:
        sys.exit()

    # 绘制背景颜色
    screen.fill(white)

    if game_over:
        print_text(font_01, 100, 225, "Click to play...")
        print_text(font_01, 100, 300, f"High Score: {high_score}")
    else:
        bomb_y += vel_y
        if bomb_y > 768:
            bomb_x = random.randint(0, 1000)
            bomb_y = -50
            lives -= 1
            current_bomb = random.choice(bomb_types)
            vel_y = current_bomb["speed"]
            if lives == 0:
                game_over = True
                if score > high_score:
                    high_score = score
        elif pos_y < bomb_y + 30 < pos_y + 40 and pos_x - 40 < bomb_x < pos_x + 160:
            score += current_bomb["score"]
            bomb_x = random.randint(0, 1000)
            bomb_y = -50
            current_bomb = random.choice(bomb_types)
            vel_y = current_bomb["speed"]

        # 绘制炸弹方块
        pygame.draw.rect(screen, current_bomb["color"], (bomb_x, int(bomb_y), 50, 50))

        # 确保平台可以移动到屏幕两端
        if pos_x < 0:
            pos_x = 0
        elif pos_x > 904:
            pos_x = 904

        # 绘制平台圆圈
        pygame.draw.circle(screen, black, (pos_x + 50, pos_y + 20), 50)

        # 随着分数增加游戏难度
        if score // 100 + 1 > level:
            level += 1
            for bomb_type in bomb_types:
                bomb_type["speed"] += 1.0

    print_text(font_00, 0, 0, "LIVES: " + str(lives))
    print_text(font_00, 500, 0, "SCORE: " + str(score))
    pygame.display.update()
    pygame.time.delay(10)




