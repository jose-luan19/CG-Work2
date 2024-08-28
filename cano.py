import numpy as np
import utils.utils as util


class Cano(util.Solido):
    def __init__(self, raio, P1, P2, T1, T2, resolucao_curva=20):
        self.raio = raio
        self.P1 = np.array(P1)
        self.P2 = np.array(P2)
        self.T1 = np.array(T1)
        self.T2 = np.array(T2)
        self.resolucao_curva = resolucao_curva
        super().__init__(self.P1)

    def gerar_coordenadas(self):
        # Gerar os pontos ao longo da curva de Hermite
        t = np.linspace(0, 1, self.resolucao_curva)
        h00 = 2 * t**3 - 3 * t**2 + 1
        h10 = t**3 - 2 * t**2 + t
        h01 = -2 * t**3 + 3 * t**2
        h11 = t**3 - t**2

        curva = (
            h00[:, None] * self.P1
            + h10[:, None] * self.T1
            + h01[:, None] * self.P2
            + h11[:, None] * self.T2
        )

        # Gerar as circunferências ao longo dos pontos da curva
        theta = np.linspace(0, 2 * np.pi, self.resolucao_curva)
        x_circ = self.raio * np.cos(theta)
        y_circ = self.raio * np.sin(theta)

        x_var = []
        y_var = []
        z_var = []

        for ponto in curva:
            x_var.append(ponto[0] + x_circ)
            y_var.append(ponto[1] + y_circ)
            z_var.append(np.full_like(x_circ, ponto[2]))

        return np.array(x_var), np.array(y_var), np.array(z_var)

    def gerar_solido(self):
        x_var, y_var, z_var = self.gerar_coordenadas()

        num_rows, num_cols = x_var.shape
        cont = 0
        for i in range(num_rows - 1):
            for j in range(num_cols - 1):
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

                if cont < num_cols - 1:
                    self.arestas.append([posicaov1, posicaov2])  # H
                    cont += 1

                self.arestas.append([posicaov2, posicaov3])  # V
                self.arestas.append([posicaov3, posicaov4])  # H


if __name__ == "__main__":
    # Definindo os parâmetros da curva de Hermite
    P1 = [1, 5, 1]  # Ponto inicial da curva
    P2 = [5, 7, 5]  # Ponto final da curva
    T1 = [1, 1, 0]  # Vetor tangente inicial
    T2 = [0, 1, 2]  # Vetor tangente final
    raio_cano = 2

    # Criando o "cano"
    cano = Cano(raio_cano, P1, P2, T1, T2)
    cano.gerar_solido()

    # Plotando o "cano"
    axes = cano.plota_solido(util.create_figure())
    util.show_figure(axes)
