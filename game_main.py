# ----------- setup ----------- #
import pygame
import random
pygame.init()
WIDTH=550
HEIGHT=800
screen = pygame.display.set_mode((WIDTH, HEIGHT))

from game_classes import *

# ----------- fonts/sounds ----------- #
font1 = pygame.font.SysFont("comicsansms",30)
click = pygame.mixer.Sound('sound_click.wav')

# ----------- pictures ----------- #
background=pygame.image.load("backgroun.jpg")
background=pygame.transform.scale(background,(1420,800))

#start screen
start_background = pygame.image.load("bg_startscreen.png")
start_background=pygame.transform.scale(start_background,(550,800))
button_instructions1= pygame.image.load("button_instructions1.png")
button_instructions1=pygame.transform.scale(button_instructions1,(550,800))
button_start1= pygame.image.load("button_start1.png")
button_start1=pygame.transform.scale(button_start1,(550,800))

#instruction screen
instruction_background = pygame.image.load("bg_instruction.png")
instruction_background=pygame.transform.scale(instruction_background,(550,800))
button_start2= pygame.image.load("button_start2.png")
button_start2=pygame.transform.scale(button_start2,(550,800))

#end screen
end_background = pygame.image.load("bg_endscreen.png")
end_background=pygame.transform.scale(end_background,(550,800))

#in-game
word_compost=pygame.image.load("word_compost.png")
word_compost=pygame.transform.scale(word_compost,(202,43))
word_recycle=pygame.image.load("word_recycle.png")
word_recycle=pygame.transform.scale(word_recycle,(197,43))

pause_button=pygame.image.load("pause.png")
pause_button=pygame.transform.scale(pause_button,(60,65))
play_button=pygame.image.load("play.png")
play_button=pygame.transform.scale(play_button,(60,60))


# ----------- functions ----------- #

def redraw_function():
    screen.fill((0,0,0))
    screen.blit(background, (-300, 0))

    screen.blit(word_compost,(0,0))
    green_score = font1.render(str(green_bin.score), True, (0, 0, 0))
    screen.blit(green_score, (110, 50))

    screen.blit(word_recycle, (350, 0))
    blue_score = font1.render(str(blue_bin.score),True,(0,0,0))
    screen.blit(blue_score,(410,50))

    if paused==False:
        screen.blit(pause_button, (480, 585))
    else:
        screen.blit(play_button, (480, 593))

    blue_bin.draw(screen)
    green_bin.draw(screen)

    for i in garbage_objects:
        i.draw(screen)
        if paused==False:
            i.move_down()

    pygame.display.update()

def start_screen():
    screen.fill((255,255,255))
    screen.blit(start_background, (0, 0))
    (x1,y1)=pygame.mouse.get_pos()
    if x1>25 and x1 < 515 and y1 >200 and y1<270:
        screen.blit(button_instructions1, (0, 0))
    if x1>140 and x1 < 395 and y1 > 305 and y1<375:
        screen.blit(button_start1,(0,0))
    pygame.display.update()

def instruction():
    screen.fill((255,255,255))
    screen.blit(instruction_background, (0, 0))
    (x1, y1) = pygame.mouse.get_pos()
    if x1>170 and x1 < 390 and y1 >710 and y1<780:
        screen.blit(button_start2, (0, 0))
    pygame.display.update()

def end_screen():
    screen.fill((255,255,255))
    screen.blit(end_background, (0, 0))
    total_score=blue_bin.score+green_bin.score
    total_points = font1.render(str(total_score), True, (0, 0, 0))
    screen.blit(total_points, (380, 170))
    pygame.display.update()

# ----------- main ----------- #
pygame.mixer.music.load("sound_background.mp3")
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(loops=-1)

replay = True
while replay:
    garbage_objects = []
    for i in range(0, 20):  # need to make constantly generating until game over
        garbage_objects.append(Garbage(random.randint(0, WIDTH), random.randint(-2000, -5), random.uniform(0.1, 0.5),
                                       random.choice(recyclable_garbage_pictures),0))
        garbage_objects.append(Garbage(random.randint(0, WIDTH), random.randint(-2000, -5), random.uniform(0.1, 0.5),
                                       random.choice(compost_garbage_pictures),0))

    blue_bin = Garbage(90, HEIGHT - 180, 1, blue_bin_pic,0)
    green_bin = Garbage(370, HEIGHT - 180, 1, green_bin_pic,0)

    instructions = False
    pressed = False
    exit_flag = False
    paused = False
    end = False

    while not exit_flag:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_flag = True

        start_screen()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and pressed == False:
                pressed = True
                click.play()
                (cursorX, cursorY) = pygame.mouse.get_pos()
                # if pressed, takes the user to the instruction screen
                if pressed == True and cursorX > 25 and cursorX < 515 and cursorY > 200 and cursorY < 270:
                    instructions = True
                if pressed == True and cursorX > 140 and cursorX < 395 and cursorY > 305 and cursorY < 375:
                    exit_flag = True

            while instructions:
                instruction()

                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        click.play()
                        (cursor2X, cursor2Y) = pygame.mouse.get_pos()
                        if cursor2X > 170 and cursor2X < 380 and cursor2Y > 710 and cursor2Y < 780:
                            instructions = False
                            level_flag = True
                            exit_flag = True

    while exit_flag and not instructions:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_flag = True
        for i in garbage_objects:
            i.collides(blue_bin)
            i.collides(green_bin)

        redraw_function()

        keys = pygame.key.get_pressed()
        # moving blue bin
        if keys[pygame.K_a]:
            blue_bin.move_left()
        if keys[pygame.K_d]:
            blue_bin.move_right()
        # moving green bin
        if keys[pygame.K_LEFT]:
            green_bin.move_left()
        if keys[pygame.K_RIGHT]:
            green_bin.move_right()

        # press p to pause and g to go
        if keys[pygame.K_p]:
            paused = True
        if keys[pygame.K_g]:
            paused = False

        done = True
        for i in garbage_objects:
            if i.y < 800 and i.visable:
                done = False
        if done == True:
            exit_flag = False
            end = True

    while end and not exit_flag:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                exit_flag = True
        end_screen()
        key2 = pygame.key.get_pressed()
        # press q to quit
        if key2[pygame.K_q]:
            end = False
            replay = False

        # press r to replay
        if key2[pygame.K_r]:
            end = False

pygame.quit()
