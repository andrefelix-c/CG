import math

class Cubo:
    def __init__(self, lado):
        self.vertices, self.topo = Cubo.cubo_malha(lado)

    @staticmethod
    def create_cubo(lado):
        vertices = [
            [0, 0, 0],               
            [lado, 0, 0],            
            [lado, lado, 0],         
            [0, lado, 0],            
            [0, 0, lado],            
            [lado, 0, lado],         
            [lado, lado, lado],      
            [0, lado, lado]          
        ]

        edges = [
            (0, 1), (1, 2), (2, 3), (3, 0),
            (4, 5), (5, 6), (6, 7), (7, 4),
            (0, 4), (1, 5), (2, 6), (3, 7)
        ]

        return vertices, edges

    @staticmethod
    def cubo_malha(lado):
        vertices, _ = Cubo.create_cubo(lado)

        triangulos = [
            [0, 2, 1], [0, 3, 2],    
            [4, 5, 6], [4, 6, 7],     
            [0, 1, 5], [0, 5, 4],     
            [3, 7, 6], [3, 6, 2],     
            [0, 4, 7], [0, 7, 3],     
            [1, 2, 6], [1, 6, 5]      
        ]

        return vertices, triangulos

class Toro:
    def __init__(self, R, r, n_u=40, n_v=20):
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

                x = (R + r * cv) * cu
                y = (R + r * cv) * su
                z = r * sv

                vertices.append([x, y, z])

        for i in range(n_u):
            i_next = (i + 1) % n_u
            for j in range(n_v):
                j_next = (j + 1) % n_v

                a = i * n_v + j
                b = i_next * n_v + j
                c = i_next * n_v + j_next
                d = i * n_v + j_next

                triangulos.append([a, b, c])
                triangulos.append([a, c, d])

        return vertices, triangulos

import math

class CanoCurvadoHermite:
    def __init__(self, P0, P1, T0, T1,
                 raio, espessura,
                 n_curva=20, n_secao=16, density=1):

        self.vertices, self.topo = self.cano_malha(
            P0, P1, T0, T1,
            raio, espessura,
            n_curva, n_secao, density
        )

    @staticmethod
    def hermite(P0, P1, T0, T1, t):
        h00 = 2*t**3 - 3*t**2 + 1
        h10 = t**3 - 2*t**2 + t
        h01 = -2*t**3 + 3*t**2
        h11 = t**3 - t**2
        return [
            h00*P0[i] + h10*T0[i] + h01*P1[i] + h11*T1[i]
            for i in range(3)
        ]

    @staticmethod
    def hermite_tangent(P0, P1, T0, T1, t):
        dh00 = 6*t**2 - 6*t
        dh10 = 3*t**2 - 4*t + 1
        dh01 = -6*t**2 + 6*t
        dh11 = 3*t**2 - 2*t
        return [
            dh00*P0[i] + dh10*T0[i] + dh01*P1[i] + dh11*T1[i]
            for i in range(3)
        ]

    @staticmethod
    def cross(a, b):
        return [
            a[1]*b[2] - a[2]*b[1],
            a[2]*b[0] - a[0]*b[2],
            a[0]*b[1] - a[1]*b[0]
        ]

    @staticmethod
    def normalize(v):
        norm = math.sqrt(sum(x*x for x in v))
        if norm == 0:
            return [0, 0, 0]
        return [x / norm for x in v]


    @staticmethod
    def subdivide(vertices, triangles):
        new_vertices = list(vertices)
        edge_midpoints = {}
        new_triangles = []

        def get_midpoint(a, b):
            key = tuple(sorted((a, b)))
            if key not in edge_midpoints:
                va = new_vertices[a]
                vb = new_vertices[b]
                midpoint = [
                    (va[0] + vb[0]) / 2,
                    (va[1] + vb[1]) / 2,
                    (va[2] + vb[2]) / 2
                ]
                edge_midpoints[key] = len(new_vertices)
                new_vertices.append(midpoint)
            return edge_midpoints[key]

        for tri in triangles:
            a, b, c = tri
            ab = get_midpoint(a, b)
            bc = get_midpoint(b, c)
            ca = get_midpoint(c, a)

            new_triangles.append([a, ab, ca])
            new_triangles.append([ab, b, bc])
            new_triangles.append([ca, bc, c])
            new_triangles.append([ab, bc, ca])

        return new_vertices, new_triangles


    @staticmethod
    def cano_malha(P0, P1, T0, T1,
                   raio, espessura,
                   n_curva, n_secao, density):

        vertices = []
        triangles = []
        cls = CanoCurvadoHermite  

        r_ext = raio + espessura
        r_int = raio

        for i in range(n_curva):
            t = i / (n_curva - 1)

            centro = cls.hermite(P0, P1, T0, T1, t)
            tangente = cls.normalize(cls.hermite_tangent(P0, P1, T0, T1, t))

            ref = [0, 0, 1]
            if abs(sum(tangente[k]*ref[k] for k in range(3))) > 0.9:
                ref = [0, 1, 0]

            normal = cls.normalize(cls.cross(tangente, ref))
            binormal = cls.cross(tangente, normal)

            for j in range(n_secao):
                ang = 2 * math.pi * j / n_secao
                c = math.cos(ang)
                s = math.sin(ang)

                vertices.append([
                    centro[k] + r_ext * (c*normal[k] + s*binormal[k])
                    for k in range(3)
                ])

                vertices.append([
                    centro[k] + r_int * (c*normal[k] + s*binormal[k])
                    for k in range(3)
                ])

        for i in range(n_curva - 1):
            for j in range(n_secao):
                j2 = (j + 1) % n_secao

                base_atual = i * n_secao
                base_proxima = (i + 1) * n_secao

                e0, i0 = 2 * (base_atual + j),   2 * (base_atual + j) + 1
                e1, i1 = 2 * (base_atual + j2),  2 * (base_atual + j2) + 1
                e2, i2 = 2 * (base_proxima + j), 2 * (base_proxima + j) + 1
                e3, i3 = 2 * (base_proxima + j2), 2 * (base_proxima + j2) + 1

                triangles.append([e0, e2, e1])
                triangles.append([e1, e2, e3])
                triangles.append([i0, i1, i2])
                triangles.append([i1, i3, i2])
                if i == 0:
                    triangles.append([e0, i1, i0])
                    triangles.append([e0, e1, i1])
                
                if i == n_curva - 2:
                    triangles.append([e2, i2, i3])
                    triangles.append([e2, i3, e3])
                    
        for _ in range(density):
            vertices, triangles = cls.subdivide(vertices, triangles)

        return vertices, triangles