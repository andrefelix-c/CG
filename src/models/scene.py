from .solids import Cubo, Toro, CanoCurvadoHermite
import copy

class Scene:
    def __init__(self):
        self.setup_scene()

    def aplicar_transformacoes(self, obj, escala=(1,1,1), translacao=(0,0,0)):
        vertices_transformados = []
        for v in obj.vertices:
            # escala
            v_scaled = [
                v[0] * escala[0],
                v[1] * escala[1],
                v[2] * escala[2]
            ]
            # translação
            v_translated = [
                v_scaled[0] + translacao[0],
                v_scaled[1] + translacao[1],
                v_scaled[2] + translacao[2]
            ]
            vertices_transformados.append(v_translated)
        return (vertices_transformados, copy.deepcopy(obj.topo))

    def setup_scene(self):
        self.cubo_original = Cubo(6)
        self.toro_original = Toro(4, 2)
        self.cano_curvado_original = CanoCurvadoHermite(
            P0=[0, 0, 0],
            P1=[6, 6, 4],
            T0=[6, 0, 4],
            T1=[0, 6, 4],
            raio=1,
            espessura=0.3,
            n_curva=20,
            n_secao=10,
            density=0
        ) 
        self.cubo = self.aplicar_transformacoes(
            self.cubo_original,
            escala=(1/3,1/3,1/3),
            translacao=(0, 6, 0)
        )

        self.toro = self.aplicar_transformacoes(
            self.toro_original,
            escala=(0.3, 0.3, 0.3),
            translacao=(2,2,1)
        )

        self.cano_curvado = self.aplicar_transformacoes(
            self.cano_curvado_original,
            escala=(0.5, 0.5, 0.5),
            translacao=(4, 4, 1)
        )