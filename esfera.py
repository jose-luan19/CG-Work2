import numpy as np
import utils.utils as util

class Esfera(util.Solido):
    def __init__(self, raio, ponto_inicial):
        self.raio = raio
        super().__init__(ponto_inicial)

    def gerar_coordenadas(self):
        num_pontos = 10
        t_incremento = 2 * np.pi / num_pontos
        p_incremento = np.pi / num_pontos
        theta = 0.0
        phi = 0.0

        # Percorre Horizontalmente ( L -> O )
        for _ in range(num_pontos + 1):
            phi = 0.0
            # Percorre Verticalmente ( N -> S )
            for _ in range(num_pontos + 1):
                self.pontosX.append(
                    self.ponto_inicial[0] + self.raio * np.cos(theta) * np.sin(phi)
                )
                self.pontosY.append(
                    self.ponto_inicial[1] + self.raio * np.sin(theta) * np.sin(phi)
                )
                self.pontosZ.append(self.ponto_inicial[2] + self.raio * np.cos(phi))

                phi += p_incremento
            theta += t_incremento

    def gerar_solido(self):
        self.gerar_coordenadas()
        num_pontos = 10

        # Traça as arestas da esfera
        for i in range(num_pontos):
            for j in range(num_pontos):
                self.arestas.append(
                    [i * (num_pontos + 1) + j, i * (num_pontos + 1) + j + 1]
                )
                self.arestas.append(
                    [j * (num_pontos + 1) + i, (j + 1) * (num_pontos + 1) + i]
                )

if __name__ == "__main__":
    # Esfera
    # Cria um objeto Esfera com raio 1 e ponto inicial (0, 0, 0)
    esfera = Esfera(1, (7, -2, -6))

    # Plota a esfera original
    esfera.gerar_solido()
    axes = esfera.plota_solido(util.create_figure())
    util.show_figure(axes)


