import numpy as np
import utils.utils as util

class Cilindro(util.Solido):
    def __init__(self, raio, altura, ponto_inicial):
        super().__init__()  # Chama o __init__ da classe base sem parâmetros
        self.raio = raio
        self.altura = altura
        self.ponto_inicial = ponto_inicial  # Define o ponto inicial aqui
        
    def gerar_coordenadas(self):
        resolucao = 20  # Resolução do cilindro

        # Criando os pontos para a superfície do cilindro
        theta = np.linspace(0, 2 * np.pi, resolucao)
        z_var = np.linspace(self.ponto_inicial[2], self.ponto_inicial[2] + self.altura, resolucao)
        theta, z_var = np.meshgrid(theta, z_var)
        x_var = self.ponto_inicial[0] + self.raio * np.cos(theta)
        y_var = self.ponto_inicial[1] + self.raio * np.sin(theta)

        return x_var, y_var, z_var
        
    def gerar_solido(self):
        x_var, y_var, z_var = self.gerar_coordenadas()

        # Obter as dimensões dos dados
        num_rows, num_cols = x_var.shape

        # Percorrer as células da grade e plotar os segmentos de linha
        cont = 0
        for i in range(num_rows - 1):
            for j in range(num_cols - 1):
                # Obter as coordenadas dos vértices da célula atual (faz o retângulo e interliga)
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

                # Desenhar o primeiro círculo
                if cont < num_cols - 1:
                    self.arestas.append([posicaov1, posicaov2])  # H
                    cont += 1

                self.arestas.append([posicaov2, posicaov3])  # V
                self.arestas.append([posicaov3, posicaov4])  # H

    def preencher_faces(self, axes, cor_faces='brown', cor_arestas='black', alpha=0.7):
        # Gerar as coordenadas da superfície do cilindro
        x_var, y_var, z_var = self.gerar_coordenadas()
        
        # Preencher a superfície do cilindro
        axes.plot_surface(x_var, y_var, z_var, color=cor_faces, alpha=alpha)
        
        # Desenhar as arestas com a cor preta usando plot_wireframe
        axes.plot_wireframe(x_var, y_var, z_var, color=cor_arestas, alpha=1)

    def preencher_faces_2D(self, axes, pontos_2d, cor_faces, cor_arestas, alpha):
        pass

if __name__ == "__main__":
    # Cilindro com raio e altura
    raio_cilindro = 0.2
    altura_cilindro = 1.0
    ponto_inicial_cilindro = [0, 0, 0]
    cilindro = Cilindro(raio_cilindro, altura_cilindro, ponto_inicial_cilindro)
    cilindro.gerar_solido()
    
    axes = util.create_figure()  # Retorna apenas o Axes3D
    cilindro.plota_solido(axes)
    
    # Preencher as faces do cilindro
    cilindro.preencher_faces(axes)
    
    util.show_figure(axes)
