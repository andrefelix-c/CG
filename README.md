# Projeto de Renderização 3D em Python

Este é um projeto de renderização 3D escrito em Python que utiliza bibliotecas como `matplotlib` e `PIL` para criar e visualizar objetos 3D, como caixas, cones, troncos de cone e linhas. O projeto inclui funcionalidades para transformar, projetar e rasterizar cenas 3D em diferentes sistemas de coordenadas e resoluções.

## Funcionalidades Principais

- **Criação de Objetos 3D:**
    - Cubo, cano e toro.
    - Definição de vértices, arestas e malhas triangulares.

- **Transformações Geométricas:**
    - Escala, translação e rotação de objetos.
    - Transformação de coordenadas do mundo para o sistema da câmera.

- **Projeção em Perspectiva:**
    - Projeção de objetos 3D em um plano 2D.
    - Visualização de cenas em diferentes sistemas de coordenadas.

- **Renderização e Rasterização:**
    - Plotagem de cenas 3D usando `matplotlib`.
    - Rasterização de cenas em diferentes resoluções usando `PIL`.

- **Visualização Individual e em Grupo:**
    - Visualização de cada sólido individualmente.
    - Visualização de cenas completas com múltiplos objetos.

## Como Usar

1. **Instalação das Dependências:**
    Certifique-se de ter o Python instalado. Instale as bibliotecas necessárias usando o `pip`:
    ```bash
    pip install -r requirements.txt
    ```

2. **Execução do Projeto:**
    Execute o arquivo principal para iniciar a renderização:
    ```bash
    python src/main.py
    ```

3. **Configuração da Cena:**
    - A cena é configurada automaticamente no arquivo scene.py, onde os objetos são criados, transformados e posicionados.
    - Você pode modificar as transformações (escala, translação) diretamente no método setup_scene.

4. **Visualização dos Resultados:**
    - O projeto gera visualizações 3D interativas usando matplotlib.
    - As imagens rasterizadas são salvas na pasta output/ com diferentes resoluções.

## Exemplos de Uso

### Visualização Individual dos Sólidos

Para visualizar cada sólido individualmente em seu estado original (sem transformações), use:
```bash
renderer.plot_individual_solidos()
```

### Visualização da Cena Completa

Para visualizar a cena completa com todos os objetos transformados, use:
```bash
renderer.plot_scene()  # Cena no sistema do mundo
renderer.plot_scene_camera()  # Cena no sistema da câmera
renderer.plot_scene_perspective()  # Projeção em perspectiva 2D
```

### Rasterização da Cena

Para gerar imagens rasterizadas da cena em diferentes resoluções, use:
```bash
renderer.rasterize_at_multiple_resolutions([(144, 144), (360, 360), (720, 720), (1080, 1080)])
```

## Contribuição

Se você quiser contribuir para este projeto, sinta-se à vontade para abrir uma issue ou enviar um pull request.# SolidosComputacaoGrafica
