import numpy as np
from cone import Cone
import utils.utils as util


class TroncoCone(Cone):
    def __init__(self, raio_maior, raio_menor, altura, num_camadas):
        self.raio_maior = raio_maior
        self.raio_menor = raio_menor
        super().__init__(raio_maior, altura, num_camadas)

    def gerar_coordenadas(self):
        # Gera as coordenadas (x, y, z) do tronco de cone.

        theta = np.linspace(0, 2 * np.pi, self.num_camadas)  # Cria um array de ângulos igualmente espaçados
        z = np.linspace(0, self.altura, self.num_camadas)  # Cria um array de alturas igualmente espaçadas

        x = np.empty((self.num_camadas, self.num_camadas))  # Inicializa um array vazio para as coordenadas x
        y = np.empty((self.num_camadas, self.num_camadas))  # Inicializa um array vazio para as coordenadas y
        z_2d = np.empty((self.num_camadas, self.num_camadas))  # Inicializa um array vazio para as

        for i in range(self.num_camadas):
            # Calcula o raio da base em cada camada, até o raio da base menor
            raio = self.raio_maior - (self.raio_maior - self.raio_menor) * (z[i] / self.altura)

            x[i] = self.ponto_inicial[0] + raio * np.cos(theta)  # Calcula as coordenadas x
            y[i] = self.ponto_inicial[1] + raio * np.sin(theta)  # Calcula as coordenadas y
            z_2d[i] = self.ponto_inicial[2] + z[i]  # Calcula as coordenadas z

        return x, y, z_2d
    


if __name__ == "__main__":

    # Tronco de Cone
    raio_maior = 1.5  # Define o raio maior da base do tronco de cone
    raio_menor = 0.3  # Define o raio menor da base do tronco de cone
    altura = 2 * raio_maior  # Define a altura do tronco de cone como o dobro do raio maior
    num_camadas = 10  # Define o número de camadas para a discretização do tronco de cone
    ponto_inicial = [0, 0, 0]  # Define o ponto inicial do tronco de cone

    tronco_cone = TroncoCone(raio_maior, raio_menor, altura, num_camadas)
    # quantidade de pontos = num_camadas^2 
    # face representa por retangulos
    tronco_cone.gerar_solido()
    axes = tronco_cone.plota_solido_com_faces(util.create_figure())
    # axes = tronco_cone.plota_solido(util.create_figure())
    util.show_figure(axes)
