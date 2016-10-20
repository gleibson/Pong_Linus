#!/usr/bin/python
#-*- coding: utf-8 -*-
import sys 
import pygame
from pygame.locals import*
pygame.init()

print 'Are you want to play pong in FullScreen?'
print 'Type Y and press Enter'
print 'for No just press enter'

#reusing code from link http://docs.python.org/2/faq/library#how-do-i-get-a-single-keypress-at-a-time

import termios, fcntl, os
fd = sys.stdin.fileno()
oldterm = termios.tcgetattr(fd)
newattr = termios.tcgetattr(fd)
newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
termios.tcsetattr(fd, termios.TCSANOW, newattr)
oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)
fcntl.fcntl(fd, fcntl.F_SETFL, oldflags | os.O_NONBLOCK)


choice = False

try:
    while not choice:
        try:
            full_screen = sys.stdin.read(1)
            full_screen = (full_screen).lower()
            choice = True
        except IOError: pass

finally:
    termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
    fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)

#full_screen = raw_input('Your Awnser: ')
#full_screen = (full_screen).lower()

if full_screen == 'y':
    size = width, high = 0,0

else: 
    size = width, high = 500,420

black = 0,0,0
white = 255, 255, 255
scenario = pygame.display.set_mode(size)
clock = pygame.time.Clock()
size = width, high = scenario.get_size()
result_left = result_right = 0

#font
font = pygame.font.Font("8bit_font/8-BIT WONDER.TTF", width/7)
font_msg = pygame.font.Font(None, width/10)
font_smaller = pygame.font.Font(None, width/20)
victory_txt = font_msg.render('Winner', 1, white)
end_txt = font_msg.render('press f to quit game', 1, white)
continue_txt1 = font_smaller.render('or any other', 1,  white)
continue_txt2 = font_smaller.render('press to continue', 1, white)

#character

class character(pygame.sprite.Sprite):
   def __init__(self, w_character, h_character):
       pygame.sprite.Sprite.__init__(self)
       self.w_character = w_character
       self.h_character = h_character
       self.image = pygame.Surface([self.w_character, self.h_character])
       self.image.fill(white)
       self.rect = self.image.get_rect()

ball = character(width/40, high/40)
coordinates_ball = [width/2, high/2]
velocity_ball = [1,1]

racket_left = character(width/40, high/10)
coordinates_racket_left = [width/25, high/2]

racket_right = character(width/40, high/10)
coordinates_racket_right = [width/25, high/2]

velocity_racket = [high/420,high/420]

characters = pygame.sprite.Group()

characters.add(ball)
characters.add(racket_left)
characters.add(racket_right)

while 1: 
    print
    print 'infinite loop'
    print  
    print 'Coordinates of ball: x =' str(coordinates_ball[0]) + ', y = ' str(coordinates_ball[1]) 
    print 'Coordinates of racket: x =' str(coordinates_racket[0]) + ', y = ' str(coordinates_racket[1]) 
    print 'Velocity of ball: x =' str(velocity_ball[0]) + ', y = ' str(velocity_ball[1])
    print 'width =' str(width) + ', high = ' str(high) 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

#moviment ball
    ball.rect.center = (coordinates_ball[0], coordinates_ball[1])
    coordinates_ball[0] = coordinates_ball[0] + velocity_ball[0]
    coordinates_ball[1] = coordinates_ball[1] + velocity_ball[1]
    
    if coordinates_ball[0] > width or coordinates_ball[0] < 0:
        print 'Ball changed of the direction on X'
        velocity_ball[0] = -velocity_ball[0]
        pygame.mixer.Sound('usr/share/pyshared/pygame/examples/data/boom.wav').play()
        if velocity_ball[0] >0:
           result_left +=1 
        else:
           result_right +=1
        velocity_ball[0] = -velocity_ball[0]
        coordinates_ball[0] = width/2

    if coordinates_ball[1] > high or coordinates_ball[1] < 0:
        print 'Ball changed of the direction on Y'
        velocity_ball[1] = -velocity_ball[1]
        pygame.mixer.Sound('user/share/pyshared/pygame/example/data/Pop.wav').play()
    
    characters.draw(scenario)
    pygame.display.flip()

#moviment racket 
    key = pygame.key.get_pressed()
    
    racket_right.rect.center = (coordinates_racket_right[0], coordinates_racket_right[1])
    if (key[K_UP]):
       print ' key up pressed'
       coordinates_racket_right[1] = coordinates_racket_right[1] - velocity_racket[1]
    elif (key[K_DOWN]):
       print 'Key down pressed'
       coordinates_racket_left[1]= coordinates_racket_right[1] + velocity_racket[1]

    racket_left.rect.center = (coordinates_racket_left[0], coordinates_racket_left[1])
    if (key[K_a]):
       print ' key A pressed' 
       coordinates_racket_left[1] = coordinates_racket_right[1] - velocity_racket[1]
    elif(key[K_z]):
       coordinates_racket_left[1] = coordinates_racket_left[1] + velocity_racket[1]

#colision
    if pygame.sprite.collide_rect(ball, racket_left) or pygame.sprite.collide_rect(ball, racket_right) == True :
       print 'Detected one colision between the ball and racket'
       pygame.mixer.Sound('usr/lib/libreoffice/share/gallery/sounds/laser.wav').play()
       velocity_ball[0] = -velocity_ball[0]
    if velocity_ball[0] >0:
       coordinates_ball[0] = coordinates_ball[0] + width/80
    if velocity_ball[0] <0:
       coordinates_ball[0] = coordinates_ball[0] - width/80
#draw line

    y = high / 200
    trace = high / 50
    increase = high /30
    while y <= high:
       pygame.draw.line(scenario, white, (width/2,0), (width/2, high), width/200)
       y += increase
#result 
    result_left_txt = font.render(str(result_left), 1, white)
    result_right_txt = font.render(str(result_right), 1, white)
    scenario.blit(result_left_txt, (width/2 - width/5, high/20))
    scenario.blit(result_right_txt, (width/2 - width/10, high/20))
    if result_left >= 10  or result_right >= 10:
       pygame.mixer.Sound('usr/lib/libreoffice/share/gallery/sounds/romans.wav').play()
       if result_left > result_right:
          scenario.blit(victory_txt, (width/10, high/4))
       else:
          scenario.blit(victory_txt, (width/2 + width/10, high/4))
       scenario.blit(end_txt,( width/2 + width/30, high/2 + high/20))
       scenario.blit(continue_txt1,( width/2 + width/30, high/2 + high/6))
       scenario.blit(continue_txt2,( width/2 + width/30, high/2 + high/5))
       pygame.display.flip()
       result_left = result_right = 0
       answer = False
       while not answer:
           for event in pygame.event.get():
               press = pygame.key.get_pressed()
           if (key[K_f]):
               print 'Key f pressed'
           elif event.type == KEYDOWN:
               print 'Other key pressed'
               answer = True 

#raw_input("Press Enter to continue"


scenario.fill(black)
pygame.draw.line(scenario, white, (width/2,0), (width/2, high), width/200)
pygame.display.flip()
clock.tick(60)
