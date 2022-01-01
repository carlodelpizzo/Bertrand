import pygame
from pygame.locals import *
import random

pygame.init()
clock = pygame.time.Clock()
frame_rate = 30

# Initialize screen
screen_width = 700
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height), RESIZABLE)
# Title
pygame.display.set_caption('Circle')
# Screen colors
black = [0, 0, 0]
white = [255, 255, 255]
red = [255, 0, 0]
green = [0, 255, 0]
blue = [0, 0, 255]
background = black
# Font
font_size = 25
font_face = 'Georgia'
font = pygame.font.SysFont(font_face, font_size)


class Circle:
    def __init__(self, surface, x_pos, y_pos, radius, width=4, color=None, bg_color=None):
        if color is None:
            color = blue
        if bg_color is None:
            bg_color = background
        self.screen = surface
        self.x = x_pos
        self.y = y_pos
        self.r = radius
        self.width = width
        self.color = color
        self.bg_color = bg_color

    def draw(self):
        pygame.draw.circle(self.screen, self.color, (int(self.x), int(self.y)), self.r)
        pygame.draw.circle(self.screen, self.bg_color, (int(self.x), int(self.y)), self.r - self.width)

    def point_inside(self, pos):
        if abs(self.x - pos[0])**2 + abs(self.y - pos[1])**2 <= self.r**2:
            return True
        return False

    def point_on_edge(self, pos):
        if (self.r - self.width)**2 <= abs(self.x - pos[0])**2 + abs(self.y - pos[1])**2 <= self.r**2:
            return True
        return False


def choose_ran_point(circle_obj, on_edge=False):
    # Terrible implementation for on_edge
    ran_x = random.randint(int(circle_obj.x - circle_obj.r), int(circle_obj.x + circle_obj.r))
    ran_y = random.randint(int(circle_obj.y - circle_obj.r), int(circle_obj.y + circle_obj.r))
    if not on_edge and not circle_obj.point_inside((ran_x, ran_y)):
        return choose_ran_point(circle_obj)
    elif on_edge and not circle_obj.point_on_edge((ran_x, ran_y)):
        return choose_ran_point(circle_obj, on_edge=True)
    return ran_x, ran_y


def choose_ran_chord(circle_obj, on_edge=False):
    # I need to extend the two internal points to their respective points on the edge, but I'm struggling
    point1 = choose_ran_point(circle_obj, on_edge=on_edge)
    point2 = choose_ran_point(circle_obj, on_edge=on_edge)

    pygame.draw.line(screen, red, point1, point2)


circle = Circle(screen, screen_width / 2, screen_height / 2, screen_width / 4)
circle.draw()

running = True
while running:
    # screen.fill(black)
    # circle.draw()
    choose_ran_chord(circle, on_edge=True)

    # Event loop
    for event in pygame.event.get():
        keys = pygame.key.get_pressed()
        # Close window
        if event.type == pygame.QUIT:
            running = False
            break

        # Key down events
        elif event.type == pygame.KEYDOWN:
            # Close window shortcut
            if (keys[K_LCTRL] or keys[K_RCTRL]) and keys[K_w]:
                running = False
                break

            elif keys[K_SPACE]:
                screen.fill(black)
                circle.draw()

        # Key up events
        elif event.type == pygame.KEYUP:
            pass

        # Mouse button events
        # mouse_pos = pygame.mouse.get_pos()
        # if event.type == pygame.MOUSEBUTTONDOWN:
        #     pass
        # elif event.type == pygame.MOUSEBUTTONUP:
        #     pass

        # Window resize
        elif event.type == pygame.VIDEORESIZE:
            screen_width = event.w
            screen_height = event.h
            screen = pygame.display.set_mode((screen_width, screen_height), RESIZABLE)

            circle.x = screen_width / 2
            circle.y = screen_height / 2

            screen.fill(black)
            circle.draw()

    clock.tick(frame_rate)
    pygame.display.flip()


pygame.display.quit()
pygame.quit()
