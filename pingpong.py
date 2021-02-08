import pygame
import random

HEIGHT, WIDTH = 400, 600,
P_W, P_H = 20, 100
BLACK = pygame.Color('black')
GRAY = pygame.Color('gray75')
BS_X = BS_Y = 12
PS = 10
RADIUS = 7

import cv2 as cv
import os

def detectAndDisplay(frame, y):
    #frame_janela = cv.resize(frame, (600, 600))
    frame_janela = frame
    gray_frame = cv.cvtColor(frame_janela, cv.COLOR_BGR2GRAY)
    gray_frame = cv.equalizeHist(gray_frame)

    palms = palm_cascade.detectMultiScale(
        gray_frame,
        1.05,
        15,

    )

    #faces = face_cascade.detectMultiScale(gray_frame)
    for (x,y,w,h) in palms:
        frame = cv.rectangle(frame_janela, (x,y),(x+w,y+h), (0, 255, 0), 4)
        y -= 60
    
    cv.imshow('Camera Laptop', frame_janela)
    print(y)

    return y

face_cascade = cv.CascadeClassifier()
HAAR_PATH = os.path.join(cv.__path__[0], 'data')
face_cascade.load(cv.samples.findFile(os.path.join(HAAR_PATH,'haarcascade_frontalface_alt2.xml')))

palm_cascade = cv.CascadeClassifier()
print(os.path.join(HAAR_PATH,'aGest.xml'))
palm_cascade.load(cv.samples.findFile(os.path.join(HAAR_PATH,'aGest.xml')))

camera = cv.VideoCapture(0)

if not camera.isOpened():
    print('Cannot open camera!')
    exit()



class Ball:
    def __init__(self, x, y, vel_x, vel_y):
        self.x, self.y, self.vel_x, self.vel_y = (x, y, vel_x, vel_y)
        self.radius = RADIUS
        self.hitbox = pygame.Rect((self.x, self.y), (self.radius, self.radius))

class Platform:
    def __init__(self, x, y, vel):
        self.x, self.y, self.vel = (x, y, vel)
        self.hitbox = pygame.Rect((self.x, self.y), (P_W, P_H))

    def move(self, ball):
        if ball.hitbox.centery < self.hitbox.centery and self.hitbox.top - self.vel > 0:
            self.y -= self.vel
        elif ball.hitbox.centery > self.hitbox.centery and self.hitbox.bottom + self.vel < HEIGHT:
            self.y += self.vel
        pygame.Rect((self.x, self.y), (P_W, P_H))

    def draw(self, surface):
        self.hitbox = pygame.Rect((self.x, self.y), (P_W, P_H))
        pygame.draw.rect(surface, GRAY, self.hitbox)

def redraw(surface):
    surface.fill(BLACK)
    plat1.draw(surface)
    plat2.draw(surface)
    pygame.draw.circle(surface, GRAY, (ball.hitbox.centerx, ball.hitbox.centery), ball.radius)
    surface.blit(text, (WIDTH // 2 - text.get_width()//2, 50))
    pygame.display.update()

def reset():
    scoring = [0 ,0]

def score(side):
    scoring[side] += 1
    pygame.time.delay(100)
    if scoring[side] == 5:
        reset()

pygame.init()

surface = pygame.display.set_mode((WIDTH, HEIGHT))

font = pygame.font.SysFont('comicsans',40,True)

platforms = []
plat1 = Platform(5, 35, 10)
plat2 = Platform(WIDTH - 25, HEIGHT - 135, PS)
ball = Ball(20 + 10 + 5, random.randint(10, HEIGHT - 10), BS_X, BS_Y)

clock = pygame.time.Clock()
scoring = [0, 0]
reset()

run = True

while run:

    clock.tick(30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

    ret, frame = camera.read()
    if not ret:
        break
    
    y = detectAndDisplay(frame, plat1.y)
    plat1.y = y
    if cv.waitKey(1) == ord('q'):
        break

#    if keys[pygame.K_UP]:
#        if plat1.hitbox.top - plat1.vel > 0:
#            plat1.y -= plat1.vel

 #   if keys[pygame.K_DOWN]:
 #       if plat1.hitbox.bottom + plat1.vel < HEIGHT:
 #           plat1.y += plat1.vel

    plat2.move(ball)

    if ball.hitbox.right > WIDTH - 7:
        score(False)
        del(ball)
        ball = Ball(20 + 10 + 5, random.randint(10, HEIGHT - 10), BS_X, BS_Y)
    elif ball.hitbox.left < 0:
        score(True)
        del(ball)
        ball = Ball(20 + 10 + 5, random.randint(10, HEIGHT - 10), BS_X, BS_Y)

    if plat1.hitbox.colliderect(ball.hitbox) or plat2.hitbox.colliderect(ball.hitbox):
        ball.vel_x = -ball.vel_x
    if ball.hitbox.bottom > HEIGHT - 7 or ball.hitbox.top < 0:
        ball.vel_y = -ball.vel_y

    ball.hitbox.centerx += ball.vel_x
    ball.hitbox.centery += ball.vel_y

    text = font.render('{} x {}'.format(scoring[0], scoring[1]), -1, (255, 255, 255))

    redraw(surface)

camera.release()
cv.destroyAllWindows()

pygame.quit()
