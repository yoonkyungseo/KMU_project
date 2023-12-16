import pygame
from player import Player
from bullet import Bullet
from bullet2 import Bullet2
from bullet3 import Bullet3
import random as rnd
import time

def collision(obj1, obj2):
    dist = ((obj1.pos[0] - obj2.pos[0]) ** 2 + (obj1.pos[1] - obj2.pos[1]) ** 2) ** 0.5
    return dist < 20

def draw_text(txt, size, pos, color):
    font = pygame.font.Font("freesansbold.ttf", size)
    r = font.render(txt, True, color)
    screen.blit(r, pos)
   


scores = []
with open("scores.txt","r") as f:
    for line in f:
        scores.append(float(line))
scores.sort(reverse = True)



pygame.init()
WIDTH, HEIGHT = 1000, 800

clock = pygame.time.Clock()
FPS = 60

pygame.display.set_caption("총알 피하기")
screen = pygame.display.set_mode((WIDTH, HEIGHT))

bg_image = pygame.image.load('bg.jpg')
bg_pos1 = -500
bg_pos2 = -500

player = Player(WIDTH/2, HEIGHT/2)

exps = []
exps.append(pygame.image.load("1.png"))
exps.append(pygame.image.load("2.png"))
exps.append(pygame.image.load("3.png"))

bullets = []
for _ in range(3):
    bullets.append(Bullet(0, HEIGHT * rnd.random(), rnd.random()-0.5, rnd.random()-0.5))

bullets2 = []
for _ in range(3):
    bullets2.append(Bullet2(0, HEIGHT * rnd.random(), rnd.random()-0.5, rnd.random()-0.5))

bullets3 = []
for _ in range(3):
    bullets3.append(Bullet3(0, HEIGHT * rnd.random(), rnd.random()-0.5, rnd.random()-0.5))


time_for_adding_bullets = 0
playtime = 0

time.sleep(2)
clock.tick(FPS)

pygame.mixer.music.load('bgm.wav')
pygame.mixer.music.play(-1)

x = 0
running = True
gameover = False

is_saved = False

life = 300

while running:
    
    dt = clock.tick(FPS)

    if gameover == False:
        playtime += dt
        
        time_for_adding_bullets += dt
        if time_for_adding_bullets >= 2000:
            bullets.append(Bullet(0, HEIGHT * rnd.random(), rnd.random()-0.5, rnd.random()-0.5))
            bullets2.append(Bullet2(0, HEIGHT * rnd.random(), rnd.random()-0.5, rnd.random()-0.5))
            bullets3.append(Bullet3(0, HEIGHT * rnd.random(), rnd.random()-0.5, rnd.random()-0.5))
            time_for_adding_bullets -= 2000
        


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.goto(-1, 0)
            elif event.key == pygame.K_RIGHT:
                player.goto(1, 0)
            elif event.key == pygame.K_UP:
                player.goto(0, -1)
            elif event.key == pygame.K_DOWN:
                player.goto(0, 1)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                player.goto(1, 0)
            elif event.key == pygame.K_RIGHT:
                player.goto(-1, 0)
            elif event.key == pygame.K_UP:
                player.goto(0, 1)
            elif event.key == pygame.K_DOWN:
                player.goto(0, -1)

    ## 미션 3 : 배경그림 비행기와 함께 움직이게
    screen.fill((0,0,0)) 
    screen.blit(bg_image, (bg_pos1,bg_pos2))
    bg_pos1 -= dt * player.to[0] * 0.2
    bg_pos2 -= dt * player.to[1] * 0.2

    
    
    ## 미션 6 : 생명력 막대
    pygame.draw.rect(screen, (255, 0, 0), [620, 10, 300, 30])
    pygame.draw.rect(screen, (0, 255, 0), [620, 10, life, 30])
    ## 미션 4 : 비행기가 총알과 여러번 충돌해야 게임 종료
    if life < 0 :
        life = 0
        gameover = True

    player.update(dt, screen)
    

    for b in bullets:
        b.update_and_draw(dt, screen)
    for b2 in bullets2:
        b2.update_and_draw(dt, screen)
    for b3 in bullets3:
        b3.update_and_draw(dt, screen)
    
    player.draw(screen)

    txt = f"Time: {playtime/1000:.1f}, Bullets: {len(bullets)+len(bullets2)+len(bullets3)}"
    draw_text(txt, 32, (10,10), (255, 255, 255))

    ## 미션 1 : 효과음 설정
    explosion_sound = pygame.mixer.Sound('explosion.wav')
    for b in bullets:
        if collision(player, b):
            point1 = 5 
            life -= point1 * 3    ## 미션 8 : 차감되는 생명력 수 다르게
            pygame.mixer.Sound.play(explosion_sound)  ## 미션 1 : 효과음 발생
            screen.blit(exps[0], (210, 100)) ## 미션 2 : 비행기가 총알에 맞았을 때, 그림효과
    for b2 in bullets2:
        if collision(player, b2):
            point2 = 7
            life -= point2 * 3    ## 미션 8 : 차감되는 생명력 수 다르게
            pygame.mixer.Sound.play(explosion_sound)  ## 미션 1 : 효과음 발생
            screen.blit(exps[1], (210, 100))  ## 미션 2 : 비행기가 총알에 맞았을 때, 그림효과
    for b3 in bullets3:
        if collision(player, b3):
            point3 = 3
            life -= point3 * 3    ## 미션 8 : 차감되는 생명력 수 다르게
            pygame.mixer.Sound.play(explosion_sound)  ## 미션 1 : 효과음 발생
            screen.blit(exps[2], (210, 100))  ## 미션 2 : 비행기가 총알에 맞았을 때, 그림효과


    ## 미션6 : 생명력 숫자 표시
    point_txt = f"{int(life/3)}" 
    draw_text(point_txt, 32, (923, 10), (255, 255, 255)) 


    if gameover == True:
        txt = "GAME OVER"
        timeover = playtime/1000
        mytime = f"your time : {timeover}"
        if not is_saved:   ## 미션 9 : 생존 시간 상위 10개를 파일에 기록
            scores.append(timeover)
            scores.sort(reverse = True)
            scores = scores[:10]
            is_saved = True
            print("new scores : ", scores)
            with open("scores.txt","w") as f:
                for s in scores:
                    f.write(f"{s}\n")
        draw_text(txt, 100, (WIDTH/2-300, HEIGHT/2-50), (255, 255, 255))
        ## 미션 11 : 현재 기록이 순위권에 있을 경우 순위를 화면에 출력하고, 생존시간 강조
        if timeover in scores:
            Rank = scores.index(timeover)
            if Rank < 5:
                ranker = f"!! Rank {Rank + 1} !!"
                draw_text(mytime, 30, (WIDTH/2-105, HEIGHT/2+40), (0, 200, 200))  ## 미션 10 : 생존시간 화면에 출력
                draw_text(ranker, 50, (WIDTH/2-110, HEIGHT/2-100), (250, 150, 150))
            else:
                draw_text(mytime, 30, (WIDTH/2-130, HEIGHT/2+40), (255, 255, 255))  ## 미션 10 : 생존시간 화면에 출력
        else:
            draw_text(mytime, 30, (WIDTH/2-130, HEIGHT/2+40), (255, 255, 255))  ## 미션 10 : 생존시간 화면에 출력

    pygame.display.update()


time.sleep(2)
    
    