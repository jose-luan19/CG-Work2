import numpy as np
import utils.utils as util


class TroncoCone(util.Solido):
    def __init__(self, radius_major, radius_minor, height, num_slices, ponto_inicial):
        self.radius_major = radius_major
        self.radius_minor = radius_minor
        self.height = height
        self.num_slices = num_slices
        super().__init__(ponto_inicial)

    def gerar_coordenadas(self):
        # Gera as coordenadas (x, y, z) do tronco de cone.

        theta = np.linspace(0, 2 * np.pi, self.num_slices)
        z = np.linspace(0, self.height, self.num_slices)

        x = np.empty((self.num_slices, self.num_slices))
        y = np.empty((self.num_slices, self.num_slices))
        z_2d = np.empty((self.num_slices, self.num_slices))

        for i in range(self.num_slices):
            # Calcula o raio da base em cada camada
            radius = self.radius_major - (self.radius_major - self.radius_minor) * ( z[i] / self.height)

            x[i] = self.ponto_inicial[0] + radius * np.cos(theta)
            y[i] = self.ponto_inicial[1] + radius * np.sin(theta)
            z_2d[i] = self.ponto_inicial[2] + z[i]

        return x, y, z_2d

    def gerar_solido(self):
        # Gera os pontos e arestas do cone.

        contador = 0
        x, y, z = self.gerar_coordenadas()
        for i in range(self.num_slices):
            for j in range(len(x[i])):
                self.pontosX.append(x[i][j])
                self.pontosY.append(y[i][j])
                self.pontosZ.append(z[i][j])
                # H
                if j < (len(x[i]) - 1):
                    self.arestas.append([contador, contador + 1])
                contador += 1
            # V
            for circles in range(len(x[i])):
                self.arestas.append([i, i + self.num_slices * circles])


if __name__ == "__main__":

    # Tronco de Cone
    radius_major = 1.5
    radius_minor = 0.5
    height = 2 * radius_major
    num_slices = 30
    ponto_inicial_tronco_cone = [0, 0, 0]

    tronco_cone = TroncoCone(
        radius_major, radius_minor, height, num_slices, ponto_inicial_tronco_cone
    )
    tronco_cone.gerar_solido()
    axes = tronco_cone.plota_solido(util.create_figure())
    util.show_figure(axes)
