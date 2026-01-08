from .solids import Cubo, Toro, CanoCurvadoHermite
# , Caixa, Cone, TroncoCone, Linha
import copy

class Scene:
    def __init__(self):
        self.setup_scene() # Ao iniciar a classe chama a função setup_scene()

    def aplicar_transformacoes(self, obj, escala=(1,1,1), translacao=(0,0,0)):
        vertices_transformados = []
        for v in obj.vertices:
            # Aplica escala
            v_scaled = [
                v[0] * escala[0],
                v[1] * escala[1],
                v[2] * escala[2]
            ]
            # Aplica translação
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
        # self.caixa_original = Caixa(2, 2) # Cria uma caixa com lado 2 e altura 2
        # self.cone_original = Cone(1, 6, n=32) # Cria um cone de base 2 e altura 6
        # self.tronco_original = TroncoCone(0.5, 1, 3, n=32) # Cria um tronco de cone de base menos 0,5, base maior 1 e altura 3
        # self.linha_original = Linha() # Cria uma linha de tamanho 3

        
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
        
        # self.caixa = self.aplicar_transformacoes(
        #     self.caixa_original,
        #     escala=(2, 2, 2),
        #     translacao=(0, 0, 0)
        # )

        # self.cone = self.aplicar_transformacoes(
        #     self.cone_original,
        #     escala=(2, 2, 1),
        #     translacao=(8, 2, 0)
        # )

        # self.tronco = self.aplicar_transformacoes(
        #     self.tronco_original,
        #     escala=(2, 2, 1),
        #     translacao=(5, 7, 0)
        # )

        # self.linha = self.aplicar_transformacoes(
        #     self.linha_original,
        #     escala=(1, 1, 6/3),
        #     translacao=(8, 8, 0)
        # )