import pygame
from pygame import Vector3, Vector2

from camera import Camera
from calculation import calculate_planes
from triangle import Triangle

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

triangles: list[Triangle] = [
    Triangle(Vector3(-1, 0, 2), Vector3(1, 0, 2), Vector3(0, -1, 3)),
    Triangle(Vector3(-1, 0, 2), Vector3(-1, 0, 4), Vector3(0, -1, 3)),
    Triangle(Vector3(1, 0, 4), Vector3(1, 0, 2), Vector3(0, -1, 3)),
    Triangle(Vector3(1, 0, 4), Vector3(-1, 0, 4), Vector3(0, -1, 3))
]

for triangle in triangles:
    print(calculate_planes(triangle))

camera: Camera = Camera(Vector3(0, 0, 0), Vector2(0, 0))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("black")

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
