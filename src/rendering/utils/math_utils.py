import math

class Utils:
    @staticmethod
    def transform_to_camera(vertices, E, R):
        # Converte coordenadas do mundo para o sistema da câmera (Eye, At, Up)
        # v_shift retira a translação da câmera, R aplica a rotação para alinhar com os eixos UVN
        transformed = []
        for v in vertices:
            v_shift = [v[i] - E[i] for i in range(3)]
            v_cam = [sum(v_shift[j] * R[i][j] for j in range(3)) for i in range(3)]
            transformed.append(v_cam)
        return transformed

    @staticmethod
    def perspective_project(v, d=1):
        # Projeção clássica: divide X e Y por Z para criar o efeito de profundidade
        # Altere 'd' para ajustar a distância focal (zoom)
        x, y, z = v
        if z == 0: z = 1e-5 # Evita divisão por zero
        return [-d * x / z, -d * y / z]

    @staticmethod
    def to_pixel(p, scale, tx, ty, height):
        # Mapeia coordenadas normalizadas (-1 a 1) para pixels da imagem (ex: 0 a 1080)
        x = int(scale * p[0] + tx)
        y = height - int(scale * p[1] + ty) # Inverte Y pois em imagens o (0,0) é o topo
        return (x, y)