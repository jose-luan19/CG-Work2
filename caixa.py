from matplotlib.patches import Polygon
import numpy as np
import utils.utils as util
from mpl_toolkits.mplot3d.art3d import Poly3DCollection


class Caixa(util.Solido):
    def __init__(self, lado_base_externa, altura_externa, espessura_parede=0.2, espacamento=0.2):
        self.lado_base_externa = lado_base_externa
        self.altura_externa = altura_externa
        self.espessura_parede = espessura_parede
        self.lado_base_interna = lado_base_externa - 2 * espessura_parede  # Define o lado da base interna
        self.altura_interna = altura_externa - 2 * espessura_parede  # Define a altura interna
        self.espaco_entre_caixas = espacamento  # Define o espaçamento entre as caixas
        super().__init__()

    def gerar_coordenadas(self, lado_base, altura, deslocamento_x=0, deslocamento_y=0):
        # Gera as coordenadas (x, y, z) de uma caixa.
        x = np.array([self.ponto_inicial[0] + deslocamento_x, 
                      self.ponto_inicial[0] + deslocamento_x + lado_base,
                      self.ponto_inicial[0] + deslocamento_x + lado_base,
                      self.ponto_inicial[0] + deslocamento_x])
        y = np.array([self.ponto_inicial[1] + deslocamento_y, 
                      self.ponto_inicial[1] + deslocamento_y,
                      self.ponto_inicial[1] + deslocamento_y + lado_base,
                      self.ponto_inicial[1] + deslocamento_y + lado_base])
        z_base = np.array([self.ponto_inicial[2]] * 4)  # Base
        z_topo = np.array([self.ponto_inicial[2] + altura] * 4)  # Topo

        return x, y, z_base, z_topo

    def gerar_solido(self):
        # Calcula o deslocamento necessário para centralizar a caixa interna
        deslocamento_x = (self.lado_base_externa - self.lado_base_interna) / 2
        deslocamento_y = (self.lado_base_externa - self.lado_base_interna) / 2

        # Gera coordenadas para a caixa externa e interna
        x_ext, y_ext, z_base_ext, z_topo_ext = self.gerar_coordenadas(self.lado_base_externa, self.altura_externa)
        x_int, y_int, z_base_int, z_topo_int = self.gerar_coordenadas(
            self.lado_base_interna, self.altura_interna, deslocamento_x, deslocamento_y
        )

        # Adiciona pontos e arestas para a caixa externa
        self.adicionar_pontos_e_arestas(x_ext, y_ext, z_base_ext, z_topo_ext)
        # Adiciona pontos e arestas para a caixa interna
        self.adicionar_pontos_e_arestas(x_int, y_int, z_base_int, z_topo_int)

        # Arestas que conectam a caixa interna e externa
        for i in range(4):
            # Conectando base da caixa externa à base da caixa interna
            self.arestas.append([i, i + 8])
            # Conectando topo da caixa externa ao topo da caixa interna
            self.arestas.append([i + 4, i + 12])

    def adicionar_pontos_e_arestas(self, x, y, z_base, z_topo):
        # Adiciona os pontos e arestas da caixa (base + topo).
        offset = len(self.pontosX)
        # Pontos da base
        for i in range(4):
            self.pontosX.append(x[i])
            self.pontosY.append(y[i])
            self.pontosZ.append(z_base[i])

        # Pontos do topo
        for i in range(4):
            self.pontosX.append(x[i])
            self.pontosY.append(y[i])
            self.pontosZ.append(z_topo[i])

        # Arestas da base
        for i in range(4):
            self.arestas.append([offset + i, offset + (i + 1) % 4])

        # Arestas do topo
        for i in range(4):
            self.arestas.append([offset + i + 4, offset + (i + 1) % 4 + 4])

        # Arestas verticais (ligam base e topo)
        for i in range(4):
            self.arestas.append([offset + i, offset + i + 4])

    def preencher_faces(self, axes, pontos, cor_faces, cor_arestas, alpha):
        # Define as faces da caixa externa e interna.
        faces = [
            [0, 1, 5, 4],  # Face frontal
            [1, 2, 6, 5],  # Face lateral direita
            [2, 3, 7, 6],  # Face traseira
            [3, 0, 4, 7]   # Face lateral esquerda
        ]
        
        # Adiciona as faces da caixa externa
        for face in faces:
            verts = [[pontos[0][i], pontos[1][i], pontos[2][i]] for i in face]
            axes.add_collection3d(Poly3DCollection([verts], facecolors=cor_faces, edgecolors=cor_arestas, alpha=alpha))

        # Adiciona as faces da caixa interna (com vértices deslocados)
        for face in faces:
            verts = [[pontos[0][i + 8], pontos[1][i + 8], pontos[2][i + 8]] for i in face]
            axes.add_collection3d(Poly3DCollection([verts], facecolors=cor_faces, edgecolors=cor_arestas, alpha=alpha))

        # Conecta as faces laterais entre as duas caixas
        for i in range(4):
            verts = [
                [pontos[0][i], pontos[1][i], pontos[2][i]],
                [pontos[0][i + 8], pontos[1][i + 8], pontos[2][i + 8]],
                [pontos[0][(i + 1) % 4 + 8], pontos[1][(i + 1) % 4 + 8], pontos[2][(i + 1) % 4 + 8]],
                [pontos[0][(i + 1) % 4], pontos[1][(i + 1) % 4], pontos[2][(i + 1) % 4]]
            ]
            axes.add_collection3d(Poly3DCollection([verts], facecolors=cor_faces, edgecolors=cor_arestas, linewidths=self.espessura_parede, alpha=alpha))

        # Plota a base interna e a tampa (superior)
        verts_base = [[pontos[0][i + 8], pontos[1][i + 8], pontos[2][i + 8]] for i in range(4)]
        axes.add_collection3d(Poly3DCollection([verts_base], facecolors=cor_faces, edgecolors=cor_arestas, linewidths=self.espessura_parede, alpha=alpha))

        return axes
    
    def preencher_faces_2D(self, axes, pontos_2d, cor_faces, cor_arestas, alpha):
       # Definir as faces como listas de índices dos pontos 2D
        faces = [
            [0, 1, 5, 4],  # Face frontal
            [1, 2, 6, 5],  # Face lateral direita
            [2, 3, 7, 6],  # Face traseira
            [3, 0, 4, 7]   # Face lateral esquerda
        ]
        
        # Iterar sobre cada face e desenhar o polígono correspondente
        for face in faces:
            # Obter os vértices da face
            verts = [[pontos_2d[0][i], pontos_2d[1][i]] for i in face]
            
            # Criar um polígono e adicioná-lo ao gráfico
            poligono = Polygon(verts, closed=True, facecolor=cor_faces, edgecolor=cor_arestas, alpha=alpha)
            axes.add_patch(poligono)

        # Configurar o eixo para que a projeção seja adequadamente exibida
        axes.set_aspect('equal')
        return axes


if __name__ == "__main__":
    # Caixa de madeira aramada com espaçamento
    lado_base_externa = 2.0  # Define o lado da base externa
    altura_externa = 3.0  # Define a altura da caixa externa
    ponto_inicial_caixa = [0, 0, 0]  # Define o ponto inicial da caixa

    caixa = Caixa(lado_base_externa, altura_externa)
    caixa.gerar_solido()

    # Pinta as faces e mostra a caixa
    axes = caixa.plota_solido_com_faces(util.create_figure())
    util.show_figure(axes)