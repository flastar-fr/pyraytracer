from pygame import Vector3, Vector2, Color

from plane import Plane
from camera import Camera
from triangle import Triangle


CAMERA_WIDTH: float = 0.5
SCREEN_SIZE: Vector2 = Vector2(1280/4, 720/4)
PIXEL_SIZE: Vector2 = Vector2(CAMERA_WIDTH / SCREEN_SIZE.x, CAMERA_WIDTH / SCREEN_SIZE.y)

X_AXIS: Vector3 = Vector3(1, 0, 0)
Y_AXIS: Vector3 = Vector3(0, 1, 0)


def calculate_plane(triangle: Triangle) -> Plane:
    a: Vector3 = triangle.p2 - triangle.p1
    b: Vector3 = triangle.p3 - triangle.p1

    n: Vector3 = a.cross(b)
    k: float = (-n).dot(triangle.p1)

    return Plane(n.x, n.y, n.z, k)


def calculate_ray(pixel: Vector2, rotation: Vector2) -> Vector3:
    center_x: float = SCREEN_SIZE.x / 2.
    center_y: float = SCREEN_SIZE.y / 2

    m: Vector3 = Vector3(
        PIXEL_SIZE.x * (pixel.x - center_x),
        PIXEL_SIZE.y * (pixel.y - center_y),
        1
    )
    m = m.rotate(rotation.x, X_AXIS)
    m = m.rotate(rotation.y, Y_AXIS)
    return m.normalize()


def _calculate_lambda_value(plane: Plane, ray: Vector3, camera: Camera) -> float | None:
    plane_coordinates: Vector3 = Vector3(plane.a, plane.b, plane.c)
    numerator: float = plane_coordinates.dot(camera.coordinates) + plane.k
    divisor: float = plane_coordinates.dot(ray)

    if abs(divisor) < 1e-6:
        return None

    return - numerator / divisor


def intersect_ray_plane(plane: Plane, ray: Vector3, camera: Camera) -> Vector3 | None:
    lambda_value: float | None = _calculate_lambda_value(plane, ray, camera)

    if lambda_value is None:
        return None

    intersection_point: Vector3 = Vector3(
        ray.x * lambda_value + camera.coordinates.x,
        ray.y * lambda_value + camera.coordinates.y,
        ray.z * lambda_value + camera.coordinates.z
    )

    return intersection_point


def _is_point_in_triangle(i: Vector3, t1: Vector3, t2: Vector3, t3: Vector3) -> bool:
    v0 = t3 - t1
    v1 = t2 - t1
    v2 = i - t1

    dot00 = v0.dot(v0)
    dot01 = v0.dot(v1)
    dot02 = v0.dot(v2)
    dot11 = v1.dot(v1)
    dot12 = v1.dot(v2)

    divisor = dot00 * dot11 - dot01 * dot01
    if abs(divisor) < 1e-8:
        return False

    u = (dot11 * dot02 - dot01 * dot12) / divisor
    v = (dot00 * dot12 - dot01 * dot02) / divisor

    eps = 1e-6
    return (u >= -eps) and (v >= -eps) and (u + v <= 1 + eps)


def is_ray_on_triangle(plane: Plane, ray: Vector3, camera: Camera, triangle: Triangle, i: Vector3) -> bool:
    lambda_value = _calculate_lambda_value(plane, ray, camera)
    if lambda_value is None or lambda_value < 0:
        return False

    return _is_point_in_triangle(i, triangle.p1, triangle.p2, triangle.p3)


def get_pixel_color(pixel: Vector2, camera: Camera, triangles: list[Triangle]) -> Color:
    closest_face_distance: float = float("+inf")
    is_intersecting: bool = False
    for triangle in triangles:
        plane: Plane = calculate_plane(triangle)
        ray: Vector3 = calculate_ray(pixel, camera.rotation)
        i: Vector3 = intersect_ray_plane(plane, ray, camera)
        if i is not None and is_ray_on_triangle(plane, ray, camera, triangle, i):
            distance_camera_i: float = camera.coordinates.distance_to(i)
            closest_face_distance: float = min(closest_face_distance, distance_camera_i)
            is_intersecting = True

    if not is_intersecting:
        return Color(0, 0, 0)

    brightness: float = min(1., 1 / closest_face_distance)
    return Color(int(255 * brightness), 0, 0)
