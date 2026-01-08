import math

class Utils:
    @staticmethod
    def normalize(v):
        norm = math.sqrt(sum(coord * coord for coord in v))
        return [coord / norm for coord in v] if norm != 0 else v

    @staticmethod
    def transform_to_camera(vertices, E, R):
        transformed = []
        for v in vertices:
            v_shift = [v[i] - E[i] for i in range(3)]
            v_cam = [
                v_shift[0] * R[0][0] + v_shift[1] * R[0][1] + v_shift[2] * R[0][2],
                v_shift[0] * R[1][0] + v_shift[1] * R[1][1] + v_shift[2] * R[1][2],
                v_shift[0] * R[2][0] + v_shift[1] * R[2][1] + v_shift[2] * R[2][2]
            ]
            transformed.append(v_cam)
        return transformed

    @staticmethod
    def perspective_project(v, d=1):
        x, y, z = v
        if z == 0:
            z = 1e-5
        return [-d * x / z, -d * y / z]

    @staticmethod
    def to_pixel(p, scale, tx, ty, height):
        x = int(scale * p[0] + tx)
        y = height - int(scale * p[1] + ty)
        return (x, y)

    @staticmethod
    def darker_color(color, factor=0.5):
        return tuple(max(0, min(255, int(c * factor))) for c in color)