class Plane:
    a: float
    b: float
    c: float
    k: float

    def __init__(self, x: float, y: float, z: float, w: float):
        self.a = x
        self.b = y
        self.c = z
        self.k = w

    def __str__(self):
        return f"Plane(x={self.a}, y={self.b}, z={self.c}, w={self.k})"

    def __repr__(self):
        return self.__str__()
