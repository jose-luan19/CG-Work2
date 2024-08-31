import numpy as np
import utils.utils as util


class Cone(util.Solido):
    def __init__(self, raio, altura, num_camadas, ponto_inicial):
        self.raio = raio
        self.altura = altura
        self.num_camadas = num_camadas
        super().__init__(ponto_inicial)

    def gerar_coordenadas(self):
        # Gera as coordenadas (x, y, z) do cone.
        
        theta = np.linspace(0, 2 * np.pi, self.num_camadas) # Cria um array de alturas igualmente espaçadas
        z = np.linspace(0, self.altura, self.num_camadas) # Cria um array de alturas igualmente espaçadas

        x = np.empty((self.num_camadas, self.num_camadas)) # Inicializa um array vazio para as coordenadas x
        y = np.empty((self.num_camadas, self.num_camadas)) # Inicializa um array vazio para as coordenadas y
        z_2d = np.empty((self.num_camadas, self.num_camadas)) # Inicializa um array vazio para as coordenadas z

        # diminuir o tamanho da base do cone ao longo da altura
        for i in range(self.num_camadas):
            # Calcula o raio da base em cada camada, até 0 que é a ponta do conte
            raio = self.raio * (1 - z[i] / self.altura)
            
            x[i] = self.ponto_inicial[0] + raio * np.cos(theta)  # Calcula as coordenadas x
            y[i] = self.ponto_inicial[1] + raio * np.sin(theta)  # Calcula as coordenadas y
            z_2d[i] = self.ponto_inicial[2] + z[i]  # Calcula as coordenadas z

        return x, y, z_2d

    def gerar_solido(self):
        # Gera os pontos e arestas do cone.

        contador = 0
        x, y, z = self.gerar_coordenadas()
        
        for i in range(self.num_camadas):
            for j in range(len(x[i])):
                self.pontosX.append(x[i][j]) # Adiciona as coordenadas x aos pontos do cone
                self.pontosY.append(y[i][j]) # Adiciona as coordenadas y aos pontos do cone
                self.pontosZ.append(z[i][j]) # Adiciona as coordenadas z aos pontos do cone
                # H
                if j < (len(x[i]) - 1):
                    self.arestas.append([contador, contador + 1]) # Adiciona arestas horizontais
                contador += 1
            # V
            for circles in range(len(x[i])):
                self.arestas.append([i, i + self.num_camadas * circles]) # Adiciona arestas verticais

if __name__ == "__main__":

    # Cone
    raio = 1.0  # Define o raio do cone
    altura = 2 * raio  # Define a altura do cone como o dobro do raio
    num_camadas = 10  # Define o número de camadas para a discretização do cone
    ponto_inicial_cone = [0, 0, 0]  # Define o ponto inicial do cone

    cone = Cone(raio, altura, num_camadas, ponto_inicial_cone)
    # quantidade de pontos = num_camadas^2 
    # face representa por retangulos
    cone.gerar_solido()
    axes = cone.plota_solido(util.create_figure())
    util.show_figure(axes)

