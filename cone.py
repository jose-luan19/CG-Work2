import numpy as np
import utils.utils as util


class Cone(util.Solido):
    def __init__(self, radius, height, num_slices, ponto_inicial):
        self.radius = radius
        self.height = height
        self.num_slices = num_slices
        super().__init__(ponto_inicial)

    def gerar_coordenadas(self):
        # Gera as coordenadas (x, y, z) do cone.

        theta = np.linspace(0, 2 * np.pi, self.num_slices)
        z = np.linspace(0, self.height, self.num_slices)

        x = np.empty((self.num_slices, self.num_slices))
        y = np.empty((self.num_slices, self.num_slices))
        z_2d = np.empty((self.num_slices, self.num_slices))

        # diminuir o tamanho da base do cone ao longo da altura
        for i in range(self.num_slices):
            x[i] = self.ponto_inicial[0] + self.radius * (1 - z[i] / self.height) * np.cos(theta)
            y[i] = self.ponto_inicial[1] + self.radius * (1 - z[i] / self.height) * np.sin(theta)
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

    # Cone
    radius = 1.0
    height = 2 * radius
    num_slices = 10
    ponto_inicial_cone = [0, 0, 0]

    cone = Cone(radius, height, num_slices, ponto_inicial_cone)
    cone.gerar_solido()
    axes = cone.plota_solido(util.create_figure())
    util.show_figure(axes)

