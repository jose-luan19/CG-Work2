import numpy as np
import utils.utils as util
from mpl_toolkits.mplot3d.art3d import Poly3DCollection


class CaixaAramada(util.Solido):
    def __init__(self, lado_base_externa, altura_externa, espessura_parede, ponto_inicial, espacamento=0.1):
        self.lado_base_externa = lado_base_externa
        self.altura_externa = altura_externa
        self.espessura_parede = espessura_parede
        self.lado_base_interna = lado_base_externa - 2 * espessura_parede  # Define o lado da base interna
        self.altura_interna = altura_externa - 2 * espessura_parede  # Define a altura interna
        self.espaco_entre_caixas = espacamento  # Define o espaçamento entre as caixas
        super().__init__(ponto_inicial)

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
            pass


if __name__ == "__main__":
    # Caixa de madeira aramada com espaçamento
    lado_base_externa = 2.0  # Define o lado da base externa
    altura_externa = 3.0  # Define a altura da caixa externa
    espessura_parede = 0.2  # Define a espessura das paredes e arestas
    ponto_inicial_caixa = [0, 0, 0]  # Define o ponto inicial da caixa
    espacamento = 0.2  # Define o espaçamento entre as caixas

    caixa_aramada = CaixaAramada(lado_base_externa, altura_externa, espessura_parede, ponto_inicial_caixa, espacamento)
    caixa_aramada.gerar_solido()
    
    # Define as cores e alpha
    cor_faces = "brown"
    cor_arestas = "black"
    alpha = 0.6

    # Pinta as faces e mostra a caixa
    axes = caixa_aramada.plota_solido_com_faces(util.create_figure(), cor_faces=cor_faces, cor_arestas=cor_arestas, alpha=alpha)
    util.show_figure(axes)












'''class CaixaSemTampa(util.Solido):
    def __init__(self, lado_base, altura, ponto_inicial):
        self.lado_base = lado_base
        self.altura = altura
        super().__init__(ponto_inicial)

    def gerar_coordenadas(self):
        # Gera as coordenadas (x, y, z) da caixa.
        x = np.array([self.ponto_inicial[0], self.ponto_inicial[0] + self.lado_base,
                      self.ponto_inicial[0] + self.lado_base, self.ponto_inicial[0]])
        y = np.array([self.ponto_inicial[1], self.ponto_inicial[1],
                      self.ponto_inicial[1] + self.lado_base, self.ponto_inicial[1] + self.lado_base])
        z_base = np.array([self.ponto_inicial[2]] * 4)  # Base
        z_topo = np.array([self.ponto_inicial[2] + self.altura] * 4)  # Topo

        return x, y, z_base, z_topo

    def gerar_solido(self):
        # Gera os pontos e arestas da caixa.
        x, y, z_base, z_topo = self.gerar_coordenadas()
        
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
            self.arestas.append([i, (i + 1) % 4])

        # Arestas do topo
        for i in range(4):
            self.arestas.append([i + 4, (i + 1) % 4 + 4])

        # Arestas verticais (ligam base e topo)
        for i in range(4):
            self.arestas.append([i, i + 4])

    def preencher_faces(self, axes, pontos, cor_faces, cor_arestas, alpha):
        # Preenche as faces da caixa.
        for i in range(4):
            verts = [
                [pontos[0][i], pontos[1][i], pontos[2][i]],  # Base
                [pontos[0][(i + 1) % 4], pontos[1][(i + 1) % 4], pontos[2][(i + 1) % 4]],  # Base
                [pontos[0][(i + 1) % 4 + 4], pontos[1][(i + 1) % 4 + 4], pontos[2][(i + 1) % 4 + 4]],  # Topo
                [pontos[0][i + 4], pontos[1][i + 4], pontos[2][i + 4]]  # Topo
            ]
            axes.add_collection3d(Poly3DCollection([verts], facecolors=cor_faces, edgecolors=cor_arestas, alpha=alpha))
        
        # Preenche a face da base
        base_verts = [
            [pontos[0][i], pontos[1][i], pontos[2][i]] for i in range(4)
        ]
        axes.add_collection3d(Poly3DCollection([base_verts], facecolors=cor_faces, edgecolors=cor_arestas, alpha=alpha))

        return axes


if __name__ == "__main__":

    # Caixa sem tampa
    lado_base = 1.0  # Define o lado da base quadrada
    altura = 2.0  # Define a altura da caixa
    ponto_inicial_caixa = [0, 0, 0]  # Define o ponto inicial da caixa

    caixa = CaixaSemTampa(lado_base, altura, ponto_inicial_caixa)
    caixa.gerar_solido()
    axes = caixa.plota_solido_com_faces(util.create_figure())
    util.show_figure(axes)'''
