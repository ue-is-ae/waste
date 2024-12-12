import math
import sys
import pygame
from pygame.locals import *

# 初始化
pygame.init()

# 設置窗口
screen = pygame.display.set_mode((600, 500))
pygame.display.set_caption("The Pie Game - Press 1,2,3,4 in Order")
myfont = pygame.font.Font(None, 86)
color = (255, 48, 48)
width = 4
x = 300
y = 250
radius = 200
position = x - radius, y - radius, radius * 2, radius * 2
piece1 = False
piece2 = False
piece3 = False
piece4 = False
score = 0
time_limit = 60  # 遊戲時間限制為60秒
correct_sequence = [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4]
input_index = 0
game_won = False

# 設置計時器
clock = pygame.time.Clock()
start_ticks = pygame.time.get_ticks()

# 遊戲循環
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYUP:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            elif event.key in correct_sequence and not game_won:
                if event.key == correct_sequence[input_index]:
                    input_index += 1
                    score += 1
                    if input_index == 1:
                        piece1 = True
                    elif input_index == 2:
                        piece2 = True
                    elif input_index == 3:
                        piece3 = True
                    elif input_index == 4:
                        piece4 = True
                        game_won = True  # 遊戲勝利
                        input_index = 0  # 重置輸入索引

    screen.fill((0, 0, 0))
    textImage1 = myfont.render("1", True, color)
    screen.blit(textImage1, (x + radius / 2 - 20, y - radius / 2))
    textImage2 = myfont.render("2", True, color)
    screen.blit(textImage2, (x - radius / 2, y - radius / 2))
    textImage3 = myfont.render("3", True, color)
    screen.blit(textImage3, (x - radius / 2, y + radius / 2 - 20))
    textImage4 = myfont.render("4", True, color)
    screen.blit(textImage4, (x + radius / 2 - 20, y + radius / 2 - 20))

    if piece1:
        start_angle = math.radians(0)
        end_angle = math.radians(90)
        pygame.draw.arc(screen, color, position, start_angle, end_angle, width)
        pygame.draw.line(screen, color, (x, y), (x, y - radius), width)
        pygame.draw.line(screen, color, (x, y), (x + radius, y), width)
    if piece2:
        start_angle = math.radians(90)
        end_angle = math.radians(180)
        pygame.draw.arc(screen, color, position, start_angle, end_angle, width)
        pygame.draw.line(screen, color, (x, y), (x, y - radius), width)
        pygame.draw.line(screen, color, (x, y), (x - radius, y), width)
    if piece3:
        start_angle = math.radians(180)
        end_angle = math.radians(270)
        pygame.draw.arc(screen, color, position, start_angle, end_angle, width)
        pygame.draw.line(screen, color, (x, y), (x - radius, y), width)
        pygame.draw.line(screen, color, (x, y), (x, y + radius), width)
    if piece4:
        start_angle = math.radians(270)
        end_angle = math.radians(360)
        pygame.draw.arc(screen, color, position, start_angle, end_angle, width)
        pygame.draw.line(screen, color, (x, y), (x, y + radius), width)
        pygame.draw.line(screen, color, (x, y), (x + radius, y), width)

    if piece1 and piece2 and piece3 and piece4:
        color = (0, 255, 0)

    if game_won:
        win_text = myfont.render("You Win!", True, (0, 255, 0))
        screen.blit(win_text, (200, 200))
        pygame.display.update()
        pygame.time.wait(3000)
        pygame.quit()
        sys.exit()

    # 計時器
    seconds = (pygame.time.get_ticks() - start_ticks) / 1000  # 計算秒數
    time_left = max(0, time_limit - seconds)
    time_text = myfont.render(f"Time: {int(time_left)}", True, (255, 255, 255))
    screen.blit(time_text, (10, 10))

    if time_left <= 0:
        # 遊戲結束
        game_over_text = myfont.render("Game Over", True, (255, 0, 0))
        screen.blit(game_over_text, (150, 200))
        pygame.display.update()
        pygame.time.wait(3000)
        pygame.quit()
        sys.exit()

    # 顯示分數
    score_text = myfont.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 50))

    pygame.display.update()
    clock.tick(60)


