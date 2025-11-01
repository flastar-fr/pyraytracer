from pygame import Vector3, Vector2


class Camera:
    coordinates: Vector3
    rotation: Vector2

    def __init__(self, coordinates: Vector3, rotation: Vector2):
        self.coordinates = coordinates
        self.rotation = rotation
