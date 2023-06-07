import sys
import math
import pygame
from pygame.locals import *

pygame.init()

FPS = 60
fpsClock = pygame.time.Clock()

pygame.display.set_caption('Simulation Robot')
monitor_size = [pygame.display.Info().current_w, pygame.display.Info().current_h]

WIDTH, HEIGHT = 500, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
fullscreen = False

class Robot():
    def __init__(self):
        # robot
        self.x = 250
        self.y = 250
        self.robot_orientation_in_degrees = 0
        self.body_radius = 20
        self.robot_speed = 0
        self.robot_angular_speed = 0
        self.robot_delta_speed_x = 0
        self.robot_delta_speed_y = 0
        # wheels
        self.wheel_spacing = 40
        self.wheel_radius = 10
        self.left_wheel_angular_speed = 0.1
        self.right_wheel_angular_speed = 0.1
        self.left_wheel_linear_speed = 0
        self.right_wheel_linear_speed = 0

    def wheel_left(self):
        angle_in_radians = (self.robot_orientation_in_degrees + 90) * (math.pi / 180)
        wheel_X = self.x + (math.cos(angle_in_radians) * (self.wheel_spacing // 2))
        wheel_Y = self.y + (math.sin(angle_in_radians) * (self.wheel_spacing // 2))
        return wheel_X, wheel_Y
    
    def wheel_right(self):
        angle_in_radians = (self.robot_orientation_in_degrees + 270) * (math.pi / 180)
        wheel_X = self.x + (math.cos(angle_in_radians) * (self.wheel_spacing // 2))
        wheel_Y = self.y + (math.sin(angle_in_radians) * (self.wheel_spacing // 2))
        return wheel_X, wheel_Y
    
    def body(self):
        body_X = self.x
        body_Y = self.y
        return body_X, body_Y

    def calculate_position(self):
        # wheels linear speed calculation
        self.left_wheel_linear_speed  = self.right_wheel_angular_speed * self.wheel_radius
        self.right_wheel_linear_speed = self.left_wheel_angular_speed  * self.wheel_radius
        # robot average speed calculation
        self.robot_speed = (self.left_wheel_linear_speed + self.right_wheel_linear_speed) / 2
        # robot speed along the x and y axes
        self.robot_delta_speed_x = self.robot_speed * math.cos(math.radians(self.robot_orientation_in_degrees))
        self.robot_delta_speed_y = self.robot_speed * math.sin(math.radians(self.robot_orientation_in_degrees))
        # robot angular speed calculation
        self.robot_angular_speed = (self.left_wheel_linear_speed - self.right_wheel_linear_speed) / (2 * self.body_radius)
        # resulting coordinates
        self.x += self.robot_delta_speed_x
        self.y += self.robot_delta_speed_y
        self.robot_orientation_in_degrees += math.degrees(self.robot_angular_speed)

    def draw_robot(self):
        # draw body
        pygame.draw.circle(screen, (0, 0, 255), (self.body()),self.body_radius)
        # draw left and right wheels
        pygame.draw.circle(screen, (0, 255, 0), (self.wheel_left()),self.wheel_radius)
        pygame.draw.circle(screen, (255, 0, 0), (self.wheel_right()),self.wheel_radius)
        

Robot = Robot()


while True:
    screen.fill((10, 10, 10))

    for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == VIDEORESIZE:
                if not fullscreen:
                    screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == K_F12:
                    fullscreen = not fullscreen
                    if fullscreen:
                        screen = pygame.display.set_mode(monitor_size, pygame.FULLSCREEN)
                    else:
                        screen = pygame.display.set_mode((screen.get_width(), screen.get_height()), pygame.RESIZABLE)

    # Update
    Robot.calculate_position()
    # Draw
    Robot.draw_robot()


    pygame.display.flip()
    fpsClock.tick(FPS)
