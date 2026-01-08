from models.scene import Scene
from rendering.renderer import Renderer

if __name__ == '__main__':
    scene = Scene()
    renderer = Renderer(scene)

    renderer.plot_individual_solidos()

    renderer.plot_scene()
    renderer.plot_scene_camera()
    renderer.plot_scene_perspective()
    renderer.rasterize_at_multiple_resolutions([(144,144), (360,360), (720,720), (1080,1080)])