import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from PIL import Image
from models.scene import Scene
from rendering.utils.math_utils import Utils

class Renderer:
    def __init__(self, scene: Scene):
        # Armazena a cena que contém os objetos transformados e originais
        self.scene = scene
        
        # Cores hexadecimais utilizadas para as faces na visualização 3D do Matplotlib
        self.cores = {
            'cubo': '#d62728',
            'toro': '#2ca02c',
            'cano': '#ff7f0e'
        }
        
        # Cores em formato RGB (0-255) utilizadas no processo de rasterização manual pixel a pixel
        self.cores_rgb = {
            'cubo': (214, 39, 40),
            'toro': (44, 160, 44),
            'cano': (255, 127, 14)
        }
        
        # DEFINIÇÕES DA CÂMERA:
        # eye: Posição (x, y, z) do observador no espaço
        # at: Ponto (x, y, z) para onde a câmera está "olhando"
        # up: Vetor que define a orientação vertical (eixo Y para cima)
        self.eye = [5, -5, 10]
        self.at = [5, 5, 0]
        self.up = [0, 1, 0]

    def _compute_camera_matrix(self, eye, at, up):
        """Calcula a matriz de rotação (R) para transformar para o sistema de câmera."""
        # Calcula a base vetorial UVN (u, v, n) para definir o novo sistema de coordenadas
        n = Utils.normalize([at[i] - eye[i] for i in range(3)])
        u = Utils.normalize([
            n[1] * up[2] - n[2] * up[1],
            n[2] * up[0] - n[0] * up[2],
            n[0] * up[1] - n[1] * up[0]
        ])
        v = [u[1] * n[2] - u[2] * n[1],
             u[2] * n[0] - u[0] * n[2],
             u[0] * n[1] - u[1] * n[0]]
        minus_n = [-n[0], -n[1], -n[2]]
        return [u, v, minus_n]

    def _plot_polyhedron(self, ax, vertices, topology, face_color, edge_color='black', is_mesh=True):
        """Método auxiliar para desenhar malhas triangulares no Matplotlib."""
        if is_mesh:
            # Cria a coleção de polígonos 3D para as faces preenchidas
            mesh = Poly3DCollection([[vertices[int(i)] for i in face] for face in topology],
                                    alpha=0.5, facecolor=face_color)
            ax.add_collection3d(mesh)
            
            # Itera sobre a topologia para desenhar as arestas pretas sobre o sólido
            for face in topology:
                face_indices = [int(idx) for idx in face]
                for i in range(len(face_indices)):
                    idx_atual = face_indices[i % len(face_indices)]
                    idx_proximo = face_indices[(i + 1) % len(face_indices)]
                    x_vals = [vertices[idx_atual][0], vertices[idx_proximo][0]]
                    y_vals = [vertices[idx_atual][1], vertices[idx_proximo][1]]
                    z_vals = [vertices[idx_atual][2], vertices[idx_proximo][2]]
                    ax.plot3D(x_vals, y_vals, z_vals, color=edge_color, linewidth=2)
        else:
            # Caso não seja malha (linhas simples), desenha apenas as conexões
            for edge in topology:
                p0, p1 = vertices[edge[0]], vertices[edge[1]]
                ax.plot3D([p0[0], p1[0]], [p0[1], p1[1]], [p0[2], p1[2]],
                          color=face_color, linewidth=3)

    def _plot_scene_shapes(self, ax, vertices_dict, topology_dict, title, limits, is_3d=True):
        """Configura os eixos e desenha todos os objetos da cena."""
        ax.set_title(title)
        if is_3d:
            for key in ['cubo', 'toro', 'cano']:
                self._plot_polyhedron(ax, vertices_dict[key],
                                      topology_dict[key],
                                      self.cores[key])
            ax.set_xlabel('X')
            ax.set_ylabel('Y')
            ax.set_zlabel('Z')
            ax.set_xlim(limits[0])
            ax.set_ylim(limits[1])
            ax.set_zlim(limits[2])
        else:
            # Visualização 2D para a projeção em perspectiva
            for solid, color in [('cubo', self.cores['cubo']),
                                 ('toro', self.cores['toro']),
                                 ('cano', self.cores['cano'])]:
                for tri in topology_dict[solid]:
                    for i in range(len(tri)):
                        p1 = vertices_dict[solid][tri[i % len(tri)]]
                        p2 = vertices_dict[solid][tri[(i + 1) % len(tri)]]
                        ax.plot([p1[0], p2[0]], [p1[1], p2[1]], color=color, linewidth=2)
            ax.set_xlabel("X'")
            ax.set_ylabel("Y'")
            ax.set_aspect('equal')

    def plot_scene(self, ax=None):
        """Gera a visualização da cena no Sistema de Coordenadas do Mundo."""
        v_cubo, t_cubo = self.scene.cubo
        v_toro, t_toro = self.scene.toro
        v_cano, t_cano = self.scene.cano_curvado

        if ax is None:
            fig = plt.figure(figsize=(10, 8))
            ax = fig.add_subplot(111, projection='3d')
            show = True
        else:
            show = False

        ax.view_init(elev=25, azim=-45)
        vertices = {'cubo': v_cubo, 'toro': v_toro, 'cano': v_cano}
        topologies = {'cubo': t_cubo, 'toro': t_toro, 'cano': t_cano}

        # Define os limites de visualização solicitados (máximo 8)
        self._plot_scene_shapes(ax, vertices, topologies,
                                'Cena Original no Sistema do Mundo',
                                limits=((0, 8), (0, 8), (0, 8)))
        if show:
            plt.tight_layout()
            plt.show()

    def plot_scene_camera(self, ax=None):
        """Transforma e desenha a cena no Sistema de Coordenadas da Câmera."""
        v_cubo, t_cubo = self.scene.cubo
        v_toro, t_toro = self.scene.toro
        v_cano, t_cano = self.scene.cano_curvado

        # Define a origem do mundo para ser marcada na visualização da câmera
        v_origem = [[0, 0, 0]]

        # Calcula a matriz UVN baseada na posição eye, at e up
        R = self._compute_camera_matrix(self.eye, self.at, self.up)

        # Transforma os vértices de todos os objetos para o espaço da câmera
        v_cubo_cam = Utils.transform_to_camera(v_cubo, self.eye, R)
        v_toro_cam = Utils. transform_to_camera(v_toro, self.eye, R)
        v_cano_cam = Utils. transform_to_camera(v_cano, self.eye, R)
        v_origem_cam = Utils.transform_to_camera(v_origem, self.eye, R)

        if ax is None:
            fig = plt.figure(figsize=(10, 8))
            ax = fig.add_subplot(111, projection='3d')
            show = True
        else:
            show = False

        ax.view_init(elev=25, azim=-45)

        # Requisito do trabalho: Marcar a origem do sistema do mundo
        ax.scatter(v_origem_cam[0][0], v_origem_cam[0][1], v_origem_cam[0][2], 
                   color='red', s=100, label='Origem do Mundo (0,0,0)')

        vertices = {'cubo': v_cubo_cam, 'toro': v_toro_cam, 'cano': v_cano_cam}
        topologies = {'cubo': t_cubo, 'toro': t_toro, 'cano': t_cano}

        self._plot_scene_shapes(ax, vertices, topologies,
                                "Cena no Sistema de Coordenadas da Câmera",
                                limits=((-10, 10), (-10, 10), (-15, 5)))
        if show:
            ax.legend() 
            plt.tight_layout()
            plt.show()

    def plot_scene_perspective(self, ax=None):
        """Apresenta a projeção em perspectiva 2D dos sólidos."""
        v_cubo, t_cubo = self.scene.cubo
        v_toro, t_toro = self.scene.toro
        v_cano, t_cano = self.scene.cano_curvado

        R = self._compute_camera_matrix(self.eye, self.at, self.up)

        v_cubo_cam = Utils.transform_to_camera(v_cubo, self.eye, R)
        v_toro_cam = Utils. transform_to_camera(v_toro, self.eye, R)
        v_cano_cam = Utils. transform_to_camera(v_cano, self.eye, R)

        def project_list(v_list, d=1):
            """Projeta uma lista de vértices 3D em coordenadas 2D."""
            proj = []
            for v in v_list:
                # Aplica a fórmula de perspectiva e armazena a profundidade (Z)
                p = Utils.perspective_project(v, d)
                depth = -v[1]
                proj.append((p[0], p[1], depth))
            return proj

        proj_cubo = project_list(v_cubo_cam)
        proj_toro = project_list(v_toro_cam)
        proj_cano = project_list(v_cano_cam)

        if ax is None:
            fig, ax = plt.subplots(figsize=(10, 8))
            show = True
        else:
            show = False

        vertices = {'cubo': proj_cubo, 'toro': proj_toro, 'cano': proj_cano}
        topologies = {'cubo': t_cubo, 'toro': t_toro, 'cano': t_cano}

        # Plota os objetos projetados em um plano 2D
        self._plot_scene_shapes(ax, vertices, topologies,
                                "Projeção em Perspectiva dos Sólidos (2D)",
                                limits=((-10, 10), (-10, 10), None),
                                is_3d=False)
        if show:
            plt.tight_layout()
            plt.show()

    def plot_individual_solidos(self, axes=None):
        """Mostra os sólidos individualmente em sua forma original (Mundo)."""
        originais = {
            'cubo': (self.scene.cubo_original.vertices, self.scene.cubo_original.topo),
            'toro': (self.scene.toro_original.vertices, self.scene.toro_original.topo),
            'cano': (self.scene.cano_curvado_original.vertices, self.scene.cano_curvado_original.topo),
        }

        if axes is None:
            fig, axes = plt.subplots(1, 3, figsize=(18, 6), 
                                     subplot_kw={'projection': '3d'})
            axes = axes.flatten()
            show = True
        else:
            show = False

        def plot_solido(ax, vertices, topo, solido_name, color, is_mesh=True):
            """Configura a proporção e limites para visualização individual do sólido."""
            ax.view_init(elev=25, azim=-45)
            ax.set_title(f"{solido_name} no Mundo")
            
            # Garante que a proporção visual seja correta (caixa quadrada)
            ax.set_box_aspect([1, 1, 1]) 
            
            # Define limites iguais para evitar distorções no Toro
            limit = 7
            ax.set_xlim(-limit, limit)
            ax.set_ylim(-limit, limit)
            ax.set_zlim(-limit, limit)

            self._plot_polyhedron(ax, vertices, topo, color,
                                  edge_color='black', is_mesh=is_mesh)
            ax.set_xlabel("X")
            ax.set_ylabel("Y")
            ax.set_zlabel("Z")

        plot_solido(axes[0], *originais['cubo'], "Cubo", self.cores['cubo'])
        plot_solido(axes[1], *originais['toro'], "Toro", self.cores['toro'])
        plot_solido(axes[2], *originais['cano'], "Cano", self.cores['cano'])

        if show:
            plt.tight_layout()
            plt.show()

    def plot_all_in_grid(self):
        """Gera um painel comparativo com todas as etapas de renderização."""
        fig = plt.figure(figsize=(20, 16))

        # 1. Cena original no sistema do mundo
        ax1 = fig.add_subplot(2, 2, 1, projection='3d')
        self.plot_scene(ax=ax1)

        # 2. Cena transformada para o sistema da câmera
        ax2 = fig.add_subplot(2, 2, 2, projection='3d')
        self.plot_scene_camera(ax=ax2)

        # 3. Projeção 2D matemática
        ax3 = fig.add_subplot(2, 2, 3)
        self.plot_scene_perspective(ax=ax3)

        # 4. Rasterização final pixel a pixel usando PIL
        ax4 = fig.add_subplot(2, 2, 4)
        img = self.rasterize_scene_perspective()
        ax4.imshow(img)
        ax4.axis('off')
        ax4.set_title("Rasterização Perspectiva")

        plt.tight_layout()
        plt.show()

        # Janela secundária para os sólidos originais isolados
        fig2, axes = plt.subplots(2, 2, figsize=(12, 12),
                                  subplot_kw={'projection': '3d'})
        axes = axes.flatten()
        self.plot_individual_solidos(axes=axes)
        plt.tight_layout()
        plt.show()

    def rasterize_scene_perspective(self, resolution=(1080, 1080), d=1):
        """Converte a cena 3D em uma imagem 2D rasterizada com tratamento de visibilidade."""
        width, height = resolution
        cores = self.cores_rgb

        v_cubo, t_cubo = self.scene.cubo
        v_toro, t_toro = self.scene.toro
        v_cano, t_cano = self.scene.cano_curvado

        # Pipeline: Mundo -> Câmera
        R = self._compute_camera_matrix(self.eye, self.at, self.up)
        v_cubo_cam = Utils.transform_to_camera(v_cubo, self.eye, R)
        v_toro_cam = Utils.transform_to_camera(v_toro, self.eye, R)
        v_cano_cam = Utils. transform_to_camera(v_cano, self.eye, R)

        def project_vertices(v_list):
            """Projeta vértices mantendo a coordenada Z para o Z-buffer."""
            proj = []
            for v in v_list:
                p = Utils.perspective_project(v, d)
                depth = -v[2] # Inverte Z para profundidade positiva
                proj.append((p[0], p[1], depth))
            return proj

        proj_cubo = project_vertices(v_cubo_cam)
        proj_toro = project_vertices(v_toro_cam)
        proj_cano = project_vertices(v_cano_cam)

        # Cálculos de escala e translação para centralizar a projeção na imagem final
        all_proj = proj_cubo + proj_toro + proj_cano
        xs = [p[0] for p in all_proj]
        ys = [p[1] for p in all_proj]
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)
        scale = 0.8 * min(width / (max_x - min_x) if (max_x - min_x) != 0 else 1,
                           height / (max_y - min_y) if (max_y - min_y) != 0 else 1)
        tx = (width - scale * (max_x + min_x)) / 2
        ty = (height - scale * (max_y + min_y)) / 2

        img = Image.new('RGB', (width, height), 'white')
        # Z-BUFFER: Matriz para resolver o problema da visibilidade (quem está na frente)
        depth_buffer = [[float('inf')] * width for _ in range(height)]

        def rasterize_triangle(p0, p1, p2, color):
            """Preenche um triângulo pixel a pixel usando coordenadas baricêntricas."""
            # Converte coordenadas da projeção para coordenadas de pixel
            x0, y0 = Utils.to_pixel((p0[0], p0[1]), scale, tx, ty, height)
            x1, y1 = Utils.to_pixel((p1[0], p1[1]), scale, tx, ty, height)
            x2, y2 = Utils.to_pixel((p2[0], p2[1]), scale, tx, ty, height)
            
            # Define a Bounding Box do triângulo para otimizar a varredura
            min_x_tri = max(0, min(x0, x1, x2))
            max_x_tri = min(width - 1, max(x0, x1, x2))
            min_y_tri = max(0, min(y0, y1, y2))
            max_y_tri = min(height - 1, max(y0, y1, y2))
            
            den = ((y1 - y2) * (x0 - x2) + (x2 - x1) * (y0 - y2))
            if den == 0: return
            
            # Varre cada pixel dentro da caixa delimitadora
            for y in range(min_y_tri, max_y_tri + 1):
                for x in range(min_x_tri, max_x_tri + 1):
                    # Calcula pesos baricêntricos para saber se o pixel está no triângulo
                    u_val = ((y1 - y2) * (x - x2) + (x2 - x1) * (y - y2)) / den
                    v_val = ((y2 - y0) * (x - x2) + (x0 - x2) * (y - y2)) / den
                    w_val = 1 - u_val - v_val
                    
                    if u_val >= 0 and v_val >= 0 and w_val >= 0:
                        # Interpola a profundidade (Z) do pixel
                        depth = u_val * p0[2] + v_val * p1[2] + w_val * p2[2]
                        # Teste do Z-buffer: só pinta se for o ponto mais próximo visto até agora
                        if depth < depth_buffer[y][x]:
                            depth_buffer[y][x] = depth
                            img.putpixel((x, y), color)

        # Rasteriza as faces de todos os objetos
        for tri in t_cubo:
            p0, p1, p2 = proj_cubo[tri[0]], proj_cubo[tri[1]], proj_cubo[tri[2]]
            rasterize_triangle(p0, p1, p2, cores['cubo'])
        for tri in t_toro:
            p0, p1, p2 = proj_toro[tri[0]], proj_toro[tri[1]], proj_toro[tri[2]]
            rasterize_triangle(p0, p1, p2, cores['toro'])
        for tri in t_cano:
            p0, p1, p2 = proj_cano[tri[0]], proj_cano[tri[1]], proj_cano[tri[2]]
            rasterize_triangle(p0, p1, p2, cores['cano'])

        def draw_visible_edge(p0, p1, color, tolerance=0.1):
            """Desenha arestas apenas onde elas não estão escondidas por faces (visibilidade)."""
            (x0, y0), d0 = Utils.to_pixel((p0[0], p0[1]), scale, tx, ty, height), p0[2]
            (x1, y1), d1 = Utils.to_pixel((p1[0], p1[1]), scale, tx, ty, height), p1[2]
            dx, dy = x1 - x0, y1 - y0
            steps = max(abs(dx), abs(dy))
            if steps == 0: return
            for i in range(steps + 1):
                t_val = i / steps
                x, y = int(x0 + dx * t_val), int(y0 + dy * t_val)
                depth = d0 + (d1 - d0) * t_val
                if 0 <= x < width and 0 <= y < height:
                    # Compara com o Z-buffer para garantir que a aresta está na superfície
                    if abs(depth_buffer[y][x] - depth) < tolerance:
                        img.putpixel((x, y), color)

        # Desenha as arestas pretas sobre os sólidos rasterizados
        for tri in t_cubo:
            edge_color = Utils.darker_color(cores['cubo'], factor=0.5)
            for i in range(3):
                draw_visible_edge(proj_cubo[tri[i]], proj_cubo[tri[(i+1)%3]], edge_color)
        for tri in t_toro:
            edge_color = Utils.darker_color(cores['toro'], factor=0.5)
            for i in range(3):
                draw_visible_edge(proj_toro[tri[i]], proj_toro[tri[(i+1)%3]], edge_color)
        for tri in t_cano:
            edge_color = Utils.darker_color(cores['cano'], factor=0.5)
            for i in range(3):
                draw_visible_edge(proj_cano[tri[i]], proj_cano[tri[(i+1)%3]], edge_color)

        return img

    def rasterize_at_multiple_resolutions(self, resolutions):
        """Salva a imagem rasterizada nas resoluções especificadas pelo professor."""
        for res in resolutions:
            img = self.rasterize_scene_perspective(resolution=res)
            filename = f"output/raster_perspective_{res[0]}x{res[1]}.png"
            img.save(filename)
            print(f"Imagem salva: {filename}")