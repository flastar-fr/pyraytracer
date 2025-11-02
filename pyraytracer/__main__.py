import pygame
from pygame import Vector3, Vector2, Color

from camera import Camera
from calculation import get_pixel_color, SCREEN_SIZE
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

camera: Camera = Camera(Vector3(0, -1, -4), Vector2(0, 0))

rect_size: Vector2 = Vector2(1280 / SCREEN_SIZE.x, 720 / SCREEN_SIZE.y)

for pixel_x in range(int(SCREEN_SIZE.x)):
    for pixel_y in range(int(SCREEN_SIZE.y)):
        color: Color = get_pixel_color(Vector2(pixel_x, pixel_y), camera, triangles)
        coordinates: Vector2 = Vector2(rect_size.x * pixel_x, rect_size.y * pixel_y)
        pygame.draw.rect(screen, color, pygame.Rect(coordinates.x, coordinates.y, rect_size.x, rect_size.y))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
