from models.scene import Scene
from rendering.renderer import Renderer

if __name__ == '__main__':
    # 1. Instancia a lógica da cena (objetos e posições)
    scene = Scene()
    # 2. Instancia o motor de renderização
    renderer = Renderer(scene)

    # 3. Gera visualizações interativas para o relatório
    renderer.plot_individual_solidos() # Mostra sólidos sem transformações
    renderer.plot_scene()             # Mostra cena no sistema do mundo
    renderer.plot_scene_camera()      # Mostra visão da câmera com a origem do mundo destacada

    # 4. Rasterização: Gera os arquivos PNG finais
    # Adicione ou remova tuplas da lista abaixo para gerar novas resoluções
    renderer.rasterize_at_multiple_resolutions([(144,144), (720,720), (1080,1080)])