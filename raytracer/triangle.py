from pygame import Vector3


class Triangle:
    p1: Vector3
    p2: Vector3
    p3: Vector3

    def __init__(self, p1: Vector3, p2: Vector3, p3: Vector3):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3