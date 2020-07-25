import pygame
import Button
pygame.init()

# create screen
HEIGHT = 890
WEIGHT = 1300
screen = pygame.display.set_mode((WEIGHT, HEIGHT))

#title and icon
pygame.display.set_caption("Pac-man")
icon = pygame.image.load("ufo.png")
pygame.display.set_icon(icon)
# background
background = pygame.image.load("background.jpg")
screen.blit(background, (0, 0))
# player
player_x = 370
player_y = 480
running = True


def player():
    screen.blit(icon, (player_x, player_y))


level1 = Button.Button((192, 192, 192), 525, 98, 250, 100, "Level 1")
level2 = Button.Button((192, 192, 192), 525, 296, 250, 100, "Level 2")
level3 = Button.Button((192, 192, 192), 525, 494, 250, 100, "Level 3")
level4 = Button.Button((192, 192, 192), 525, 692, 250, 100, "Level 4")
while running:
    # RGB - red green blue
    #screen.fill((0, 0, 255))
    # quit window
    level1.draw(screen, (0, 0, 0))
    level2.draw(screen, (0, 0, 0))
    level3.draw(screen, (0, 0, 0))
    level4.draw(screen, (0, 0, 0))
    for event in pygame.event.get():
        pos = pygame.mouse.get_pos()
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if level1.isOver(pos):
                # search level 1
                pass
            if level2.isOver(pos):
                # search level 2
                pass
            if level3.isOver(pos):
                # search level 3
                pass
            if level4.isOver(pos):
                # search level 4
                pass
        if event.type == pygame.MOUSEMOTION:
            if level1.isOver(pos):
                level1.color = (255, 255, 255)
            else:
                level1.color = (192, 192, 192)
            if level2.isOver(pos):
                level2.color = (255, 255, 255)
            else:
                level2.color = (192, 192, 192)
            if level3.isOver(pos):
                level3.color = (255, 255, 255)
            else:
                level3.color = (192, 192, 192)
            if level4.isOver(pos):
                level4.color = (255, 255, 255)
            else:
                level4.color = (192, 192, 192)

    pygame.display.update()
pygame.QUIT()
