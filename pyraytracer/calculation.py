from pygame import Vector3, Vector2

from plane import Plane
from camera import Camera
from triangle import Triangle


CAMERA_WIDTH: float = 0.5
SCREEN_SIZE: Vector2 = Vector2(5, 5)
PIXEL_SIZE: Vector2 = Vector2(CAMERA_WIDTH / SCREEN_SIZE.x, CAMERA_WIDTH / SCREEN_SIZE.y)

X_AXIS: Vector3 = Vector3(1, 0, 0)
Y_AXIS: Vector3 = Vector3(0, 1, 0)
Z_AXIS: Vector3 = Vector3(0, 0, 1)


def calculate_planes(triangle: Triangle) -> Plane:
    a: Vector3 = triangle.p2 - triangle.p1
    b: Vector3 = triangle.p3 - triangle.p1

    n: Vector3 = a.cross(b)
    k: float = (-n).dot(triangle.p1)

    return Plane(n.x, n.y, n.z, k)


def calculate_ray(pixel: Vector2, rotation: Vector2) -> Vector3:
    m: Vector3 = Vector3(PIXEL_SIZE.x * (pixel.x - 2), PIXEL_SIZE.y * (pixel.x - 2), 1)
    m = m.rotate(rotation.x, X_AXIS)
    return m.rotate(rotation.y, Y_AXIS)


def calculate_lambda_value(plane: Plane, ray: Vector3, camera: Camera) -> float:
    plane_coordinates: Vector3 = Vector3(plane.a, plane.b, plane.c)
    numerator: float = (plane_coordinates.dot(camera.coordinates) + plane.k)
    divisor: float = plane_coordinates.dot(ray)
    return - numerator / divisor


def intersect_ray_plane(plane: Plane, ray: Vector3, camera: Camera) -> Vector3:
    lambda_value: float = calculate_lambda_value(plane, ray, camera)

    intersection_point: Vector3 = Vector3(
        ray.x * lambda_value + camera.coordinates.x,
        ray.y * lambda_value + camera.coordinates.y,
        ray.z * lambda_value + camera.coordinates.z
    )

    return intersection_point


def is_ray_visible(plane: Plane, ray: Vector3, camera: Camera, triangle: Triangle, i: Vector3) -> bool:
    lambda_value: float = calculate_lambda_value(plane, ray, camera)

    if lambda_value < 0:
        return False


