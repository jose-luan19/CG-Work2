import matplotlib.pyplot as plt
import utils.utils as util

class Cubo(util.Solido):
    def __init__(self, raio, ponto_inicial):
        self.raio = raio
        super().__init__(ponto_inicial)
        self.base = [
            self.ponto_inicial,
            (
                self.ponto_inicial[0] + self.raio,
                self.ponto_inicial[1],
                self.ponto_inicial[2],
            ),
            (
                self.ponto_inicial[0] + self.raio,
                self.ponto_inicial[1] + self.raio,
                self.ponto_inicial[2],
            ),
            (
                self.ponto_inicial[0],
                self.ponto_inicial[1] + self.raio,
                self.ponto_inicial[2],
            ),
        ]

    # Faz a base  interligando os pontos
    def formarBases(self):
        contador = 0
        for index in range(len(self.pontosX)):
            if contador != 3:
                contador += 1
                self.arestas.append([index, index + 1])
            else:
                self.arestas.append([index, index - 3])
                contador = 0

    def formarArestasVerticais(self):
        for index in range(len(self.pontosX)):
            if index < (len(self.pontosX) - 4):
                self.arestas.append([index, index + 4])

    #incrementa em z para gerar a base superior
    def gerar_coordenadas(self):
        for bases in range(2):
            for j in range(len(self.base)):
                self.pontosX.append(self.base[j][0])
                self.pontosY.append(self.base[j][1])
                self.pontosZ.append(self.base[j][2] + bases * self.raio)
        self.formarBases()
        self.formarArestasVerticais()

    def gerar_solido(self):
        self.gerar_coordenadas()

# Cubo
raio_cubo = 1
ponto_inicial_cubo = [-6, -8, -7]

cubo = Cubo(raio_cubo, ponto_inicial_cubo)
cubo.gerar_solido()
cubo.plota_solido()

plt.show()
