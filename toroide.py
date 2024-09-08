import numpy as np
import utils.utils as util

class Toroide(util.Solido):
    def __init__(self, raio_toroide, raio_central_toroide, ponto_inicial, altura):
        super().__init__()
        self.raio_toroide = raio_toroide
        self.raio_central_toroide = raio_central_toroide
        self.altura = altura
        self.ponto_inicial = ponto_inicial  # Define o ponto inicial aqui

    def gerar_coordenadas(self):
        resolucao_circunferencia = 30  # Número de pontos na circunferência do tubo
        resolucao_toro = 30  # Número de circunferências ao longo do toroide

        # Ângulos para a circunferência do tubo e a volta do toroide
        theta = np.linspace(0, 2 * np.pi, resolucao_circunferencia)
        phi = np.linspace(0, np.pi, resolucao_toro)

        # Criação da malha de pontos (grade de ângulos)
        theta, phi = np.meshgrid(theta, phi)

        # Coordenadas paramétricas para o toroide
        x_var = (self.raio_central_toroide + self.raio_toroide * np.cos(theta)) * np.cos(phi)
        y_var = (self.raio_central_toroide + self.raio_toroide * np.cos(theta)) * np.sin(phi)
        z_var = self.raio_toroide * np.sin(theta)

        # Rotação para colocar o toroide na posição vertical
        x_rot, z_rot = self.rotacao_y(x_var, z_var, np.pi / 2)

        return x_rot + self.ponto_inicial[0], y_var + self.ponto_inicial[1], z_rot + self.ponto_inicial[2]

    def rotacao_y(self, x, z, angulo):
        """Aplica uma rotação em torno do eixo Y."""
        x_rot = x * np.cos(angulo) + z * np.sin(angulo)
        z_rot = -x * np.sin(angulo) + z * np.cos(angulo)
        return x_rot, z_rot

    def gerar_solido(self):
        x_var, y_var, z_var = self.gerar_coordenadas()

        # Obter as dimensões dos dados
        num_rows, num_cols = x_var.shape

        # Percorrer as células da grade e plotar os segmentos de linha
        for i in range(num_rows - 1):
            for j in range(num_cols - 1):
                # Obter as coordenadas dos vértices da célula atual
                v1 = [x_var[i, j], y_var[i, j], z_var[i, j]]
                v2 = [x_var[i, j + 1], y_var[i, j + 1], z_var[i, j + 1]]
                v3 = [x_var[i + 1, j + 1], y_var[i + 1, j + 1], z_var[i + 1, j + 1]]
                v4 = [x_var[i + 1, j], y_var[i + 1, j], z_var[i + 1, j]]

                self.pontosX.extend((v1[0], v2[0], v3[0], v4[0]))
                self.pontosY.extend((v1[1], v2[1], v3[1], v4[1]))
                self.pontosZ.extend((v1[2], v2[2], v3[2], v4[2]))

                posicaov1 = len(self.pontosX) - 4
                posicaov2 = len(self.pontosX) - 3
                posicaov3 = len(self.pontosX) - 2
                posicaov4 = len(self.pontosX) - 1

                # Adicionando arestas
                self.arestas.append([posicaov1, posicaov2])  # Ligação ao longo da circunferência
                self.arestas.append([posicaov2, posicaov3])  # Ligação entre anéis
                self.arestas.append([posicaov3, posicaov4])  # Ligação ao longo da circunferência

    def preencher_faces(self, axes, cor_faces='brown', cor_arestas='black', alpha=0.7):
        # Gerar as coordenadas da superfície do toroide
        x_var, y_var, z_var = self.gerar_coordenadas()

        # Preencher a superfície do toroide com a cor e transparência fornecidas
        axes.plot_surface(x_var, y_var, z_var, color=cor_faces, alpha=alpha)

        # Desenhar as arestas com a cor preta usando plot_wireframe
        axes.plot_wireframe(x_var, y_var, z_var, color=cor_arestas, alpha=1, edgecolor=cor_arestas)

    def preencher_faces_2D(self, axes, pontos_2d, cor_faces, cor_arestas, alpha):
        pass

if __name__ == "__main__":
    # Toroide com raio e altura
    raio_toroide = 0.1
    raio_central_toroide = 0.6
    ponto_inicial_toroide = [1, 0, 0]
    altura_toroide = 0.5
    toroide = Toroide(raio_toroide, raio_central_toroide, ponto_inicial_toroide, altura_toroide)
    toroide.gerar_solido()
    
    axes = util.create_figure()  # Retorna apenas o Axes3D
    toroide.plota_solido(axes)
    
    # Preencher as faces do toroide
    toroide.preencher_faces(axes)
    
    util.show_figure(axes)






#=========== METADE DO TOROIDE===========
'''class Toroide(util.Solido):
    def __init__(self, raio_tubo, raio_central, ponto_inicial):
        self.raio_tubo = raio_tubo  # Raio do tubo
        self.raio_central = raio_central  # Raio da circunferência principal
        super().__init__(ponto_inicial)

    def gerar_coordenadas(self):
        resolucao_circunferencia = 30  # Número de pontos na circunferência do tubo
        resolucao_toro = 50  # Número de circunferências ao longo do toroide

        # Ângulos para a circunferência do tubo
        theta = np.linspace(0, 2 * np.pi, resolucao_circunferencia)
        
        # Ângulos para a volta do toroide - vamos limitar a phi para plotar apenas metade do toroide
        phi = np.linspace(0, np.pi, resolucao_toro)  # De 0 a π (metade do toroide)

        # Criação da malha de pontos (grade de ângulos)
        theta, phi = np.meshgrid(theta, phi)

        # Coordenadas paramétricas para o toroide
        x_var = (self.raio_central + self.raio_tubo * np.cos(theta)) * np.cos(phi)
        y_var = (self.raio_central + self.raio_tubo * np.cos(theta)) * np.sin(phi)
        z_var = self.raio_tubo * np.sin(theta)

        return x_var, y_var, z_var

    def gerar_solido(self):
        x_var, y_var, z_var = self.gerar_coordenadas()

        # Obter as dimensões dos dados
        num_rows, num_cols = x_var.shape

        # Percorrer as células da grade e plotar os segmentos de linha
        for i in range(num_rows - 1):
            for j in range(num_cols - 1):
                # Obter as coordenadas dos vértices da célula atual
                v1 = [x_var[i, j], y_var[i, j], z_var[i, j]]
                v2 = [x_var[i, j + 1], y_var[i, j + 1], z_var[i, j + 1]]
                v3 = [x_var[i + 1, j + 1], y_var[i + 1, j + 1], z_var[i + 1, j + 1]]
                v4 = [x_var[i + 1, j], y_var[i + 1, j], z_var[i + 1, j]]

                self.pontosX.extend((v1[0], v2[0], v3[0], v4[0]))
                self.pontosY.extend((v1[1], v2[1], v3[1], v4[1]))
                self.pontosZ.extend((v1[2], v2[2], v3[2], v4[2]))

                posicaov1 = len(self.pontosX) - 4
                posicaov2 = len(self.pontosX) - 3
                posicaov3 = len(self.pontosX) - 2
                posicaov4 = len(self.pontosX) - 1

                # Adicionando arestas
                self.arestas.append([posicaov1, posicaov2])  # Ligação ao longo da circunferência
                self.arestas.append([posicaov2, posicaov3])  # Ligação entre anéis
                self.arestas.append([posicaov3, posicaov4])  # Ligação ao longo da circunferência

    def preencher_faces(self, axes, cor_faces='green', alpha=0.7):
        # Gerar as coordenadas da superfície do toroide
        x_var, y_var, z_var = self.gerar_coordenadas()

        # Preencher a superfície do toroide com a cor e transparência fornecidas
        axes.plot_surface(x_var, y_var, z_var, color=cor_faces, alpha=alpha, edgecolor='none')

    def preencher_faces_2D(self, axes, pontos_2d, cor_faces, cor_arestas, alpha):
        pass

if __name__ == "__main__":

    # Parâmetros do toroide
    raio_tubo = 0.5
    raio_central = 1.5
    ponto_inicial_toroide = [0, 0, 0]
    
    toroide = Toroide(raio_tubo, raio_central, ponto_inicial_toroide)
    toroide.gerar_solido()

    # Cria e plota o toroide aramado
    axes = util.create_figure()
    toroide.plota_solido(axes)
    toroide.preencher_faces(axes)  # Chama a função para preencher as faces
    util.show_figure(axes)'''







# =========TOROIDE INTEIRO==============
'''class Toroide(util.Solido):
    def __init__(self, raio_tubo, raio_central, ponto_inicial):
        self.raio_tubo = raio_tubo  # Raio do tubo
        self.raio_central = raio_central  # Raio da circunferência principal
        super().__init__(ponto_inicial)

    def gerar_coordenadas(self):
        resolucao_circunferencia = 50  # Número de pontos na circunferência do tubo
        resolucao_toro = 50  # Número de circunferências ao longo do toroide

        # Ângulos para a circunferência do tubo e a volta do toroide
        theta = np.linspace(0, 2 * np.pi, resolucao_circunferencia)
        phi = np.linspace(0, 2 * np.pi, resolucao_toro)

        # Criação da malha de pontos (grade de ângulos)
        theta, phi = np.meshgrid(theta, phi)

        # Coordenadas paramétricas para o toroide
        x_var = (self.raio_central + self.raio_tubo * np.cos(theta)) * np.cos(phi)
        y_var = (self.raio_central + self.raio_tubo * np.cos(theta)) * np.sin(phi)
        z_var = self.raio_tubo * np.sin(theta)

        return x_var, y_var, z_var

    def gerar_solido(self):
        x_var, y_var, z_var = self.gerar_coordenadas()

        # Obter as dimensões dos dados
        num_rows, num_cols = x_var.shape

        # Percorrer as células da grade e plotar os segmentos de linha
        for i in range(num_rows - 1):
            for j in range(num_cols - 1):
                # Obter as coordenadas dos vértices da célula atual
                v1 = [x_var[i, j], y_var[i, j], z_var[i, j]]
                v2 = [x_var[i, j + 1], y_var[i, j + 1], z_var[i, j + 1]]
                v3 = [x_var[i + 1, j + 1], y_var[i + 1, j + 1], z_var[i + 1, j + 1]]
                v4 = [x_var[i + 1, j], y_var[i + 1, j], z_var[i + 1, j]]

                self.pontosX.extend((v1[0], v2[0], v3[0], v4[0]))
                self.pontosY.extend((v1[1], v2[1], v3[1], v4[1]))
                self.pontosZ.extend((v1[2], v2[2], v3[2], v4[2]))

                posicaov1 = len(self.pontosX) - 4
                posicaov2 = len(self.pontosX) - 3
                posicaov3 = len(self.pontosX) - 2
                posicaov4 = len(self.pontosX) - 1

                # Adicionando arestas
                self.arestas.append([posicaov1, posicaov2])  # Ligação ao longo da circunferência
                self.arestas.append([posicaov2, posicaov3])  # Ligação entre anéis
                self.arestas.append([posicaov3, posicaov4])  # Ligação ao longo da circunferência

    def preencher_faces(self, axes, cor_faces='green', alpha=0.7):
        # Gerar as coordenadas da superfície do toroide
        x_var, y_var, z_var = self.gerar_coordenadas()

        # Preencher a superfície do toroide com a cor e transparência fornecidas
        axes.plot_surface(x_var, y_var, z_var, color=cor_faces, alpha=alpha, edgecolor='none')

    def preencher_faces_2D(self, axes, pontos_2d, cor_faces, cor_arestas, alpha):
        pass

if __name__ == "__main__":

    # Parâmetros do toroide
    raio_tubo = 0.5
    raio_central = 1.5
    ponto_inicial_toroide = [0, 0, 0]
    
    toroide = Toroide(raio_tubo, raio_central, ponto_inicial_toroide)
    toroide.gerar_solido()

    # Cria e plota o toroide aramado
    axes = util.create_figure()
    toroide.plota_solido(axes)
    toroide.preencher_faces(axes)  # Chama a função para preencher as faces
    util.show_figure(axes)'''