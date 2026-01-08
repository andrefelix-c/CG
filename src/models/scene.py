from .solids import Cubo, Toro, CanoCurvadoHermite
import copy

class Scene:
    def __init__(self):
        # Inicializa a cena configurando os objetos e suas posições
        self.setup_scene()

    def aplicar_transformacoes(self, obj, escala=(1,1,1), translacao=(0,0,0)):
        # Aplica transformações lineares aos vértices do objeto
        vertices_transformados = []
        for v in obj.vertices:
            # Para mudar o tamanho, altere os valores de 'escala' em setup_scene
            v_scaled = [v[i] * escala[i] for i in range(3)]
            # Para mudar a posição, altere os valores de 'translacao' em setup_scene
            v_translated = [v_scaled[i] + translacao[i] for i in range(3)]
            vertices_transformados.append(v_translated)
        return (vertices_transformados, copy.deepcopy(obj.topo))

    def setup_scene(self):
        # Definição dos parâmetros originais dos sólidos
        self.cubo_original = Cubo(6)
        self.toro_original = Toro(4, 2)
        
        # Posicionamento no mundo (Limite X, Y, Z <= 8)
        self.cubo = self.aplicar_transformacoes(self.cubo_original, escala=(1/3, 1/3, 1/3), translacao=(0, 6, 0))
        self.toro = self.aplicar_transformacoes(self.toro_original, escala=(0.3, 0.3, 0.3), translacao=(2, 2, 1))
        # Adicione novos objetos aqui seguindo o mesmo padrão