import math

class Cubo:
    def __init__(self, lado):
        # Gera a malha do cubo baseada no tamanho da aresta (lado)
        self.vertices, self.topo = Cubo.cubo_malha(lado)

    @staticmethod
    def create_cubo(lado):
        # Define os 8 vértices espaciais do cubo
        vertices = [
            [0, 0, 0], [lado, 0, 0], [lado, lado, 0], [0, lado, 0],
            [0, 0, lado], [lado, 0, lado], [lado, lado, lado], [0, lado, lado]
        ]
        # Define as conexões (arestas) entre os vértices
        edges = [
            (0, 1), (1, 2), (2, 3), (3, 0), (4, 5), (5, 6), 
            (6, 7), (7, 4), (0, 4), (1, 5), (2, 6), (3, 7)
        ]
        return vertices, edges

    @staticmethod
    def cubo_malha(lado):
        vertices, _ = Cubo.create_cubo(lado)
        # Define a topologia usando triângulos (2 por face) para permitir a rasterização
        triangulos = [
            [0, 2, 1], [0, 3, 2], [4, 5, 6], [4, 6, 7], [0, 1, 5], [0, 5, 4],
            [3, 7, 6], [3, 6, 2], [0, 4, 7], [0, 7, 3], [1, 2, 6], [1, 6, 5]
        ]
        return vertices, triangulos

class Toro:
    def __init__(self, R, r, n_u=40, n_v=20):
        # R = Raio maior (do centro ao tubo), r = Raio menor (espessura do tubo)
        # n_u e n_v controlam a resolução da malha (número de divisões)
        self.vertices, self.topo = self.gerar_malha(R, r, n_u, n_v)

    @staticmethod
    def gerar_malha(R, r, n_u, n_v):
        vertices = []
        triangulos = []
        for i in range(n_u):
            u = 2 * math.pi * i / n_u
            cu, su = math.cos(u), math.sin(u)
            for j in range(n_v):
                v = 2 * math.pi * j / n_v
                cv, sv = math.cos(v), math.sin(v)
                # Equação paramétrica do toro para converter ângulos em coordenadas X, Y, Z
                x = (R + r * cv) * cu
                y = (R + r * cv) * su
                z = r * sv
                vertices.append([x, y, z])
        # Conecta os vértices gerados em triângulos, fechando o anel (módulo n_u/n_v)
        for i in range(n_u):
            i_next = (i + 1) % n_u
            for j in range(n_v):
                j_next = (j + 1) % n_v
                a, b, c, d = i*n_v+j, i_next*n_v+j, i_next*n_v+j_next, i*n_v+j_next
                triangulos.extend([[a, b, c], [a, c, d]])
        return vertices, triangulos

class CanoCurvadoHermite:
    def __init__(self, P0, P1, T0, T1, raio, espessura, n_curva=20, n_secao=16, density=1):
        # P = Pontos (início/fim), T = Tangentes (direção da curva nos pontos)
        # n_curva define quantos anéis existem ao longo do cano
        self.vertices, self.topo = self.cano_malha(P0, P1, T0, T1, raio, espessura, n_curva, n_secao, density)

    @staticmethod
    def hermite(P0, P1, T0, T1, t):
        # Polinômios de Hermite para calcular a posição exata na curva no tempo 't' (0 a 1)
        h00 = 2*t**3 - 3*t**2 + 1
        h10 = t**3 - 2*t**2 + t
        h01 = -2*t**3 + 3*t**2
        h11 = t**3 - t**2
        return [h00*P0[i] + h10*T0[i] + h01*P1[i] + h11*T1[i] for i in range(3)]

    @staticmethod
    def cano_malha(P0, P1, T0, T1, raio, espessura, n_curva, n_secao, density):
        vertices = []
        triangles = []
        r_ext, r_int = raio + espessura, raio
        # Gera a geometria do cano criando anéis duplos (interno e externo) ao longo da curva
        for i in range(n_curva):
            t = i / (n_curva - 1)
            centro = CanoCurvadoHermite.hermite(P0, P1, T0, T1, t)
            # (Lógica de Normal/Binormal omitida para brevidade, mas essencial para orientar os anéis)
            # ... geração de vértices e triângulos para paredes internas, externas e tampas ...
        return vertices, triangles