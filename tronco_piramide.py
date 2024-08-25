import numpy as np
import matplotlib.pyplot as plt
import utils.utils as util


class Tronco_piramide(util.Solido):
    def __init__(self, aresta_inferior, aresta_superior, altura, ponto_inicial):
        self.aresta_superior = aresta_superior
        self.aresta_inferior = aresta_inferior
        self.altura = altura
        super().__init__(ponto_inicial)
        self.baseInferior = np.array(
            [
                (self.ponto_inicial[0], self.ponto_inicial[1], self.ponto_inicial[2]),
                (
                    self.ponto_inicial[0] + self.aresta_inferior,
                    self.ponto_inicial[1],
                    self.ponto_inicial[2],
                ),
                (
                    self.ponto_inicial[0] + self.aresta_inferior,
                    self.ponto_inicial[1] + self.aresta_inferior,
                    self.ponto_inicial[2],
                ),
                (
                    self.ponto_inicial[0],
                    self.ponto_inicial[1] + self.aresta_inferior,
                    self.ponto_inicial[2],
                ),
            ]
        )
        self.deslocamento = (self.aresta_inferior - self.aresta_superior) / 2
        self.baseSuperior = np.array(
            [
                (
                    self.ponto_inicial[0] + self.deslocamento,
                    self.ponto_inicial[1] + self.deslocamento,
                    self.ponto_inicial[2],
                ),
                (
                    self.ponto_inicial[0] + self.aresta_superior + self.deslocamento,
                    self.ponto_inicial[1] + self.deslocamento,
                    self.ponto_inicial[2],
                ),
                (
                    self.ponto_inicial[0] + self.aresta_superior + self.deslocamento,
                    self.ponto_inicial[1] + self.aresta_superior + self.deslocamento,
                    self.ponto_inicial[2],
                ),
                (
                    self.ponto_inicial[0] + self.deslocamento,
                    self.ponto_inicial[1] + self.aresta_superior + self.deslocamento,
                    self.ponto_inicial[2],
                ),
            ]
        )
        self.bases = [self.baseInferior, self.baseSuperior]

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
                
    def gerar_coordenadas(self):
        # Inicializar as listas x, y, z antes de formar as bases e as arestas
        self.pontosX = [vertex[0] for base in self.bases for vertex in base]
        self.pontosY = [vertex[1] for base in self.bases for vertex in base]
        self.pontosZ = [
            vertex[2] + self.altura * index
            for index, base in enumerate(self.bases)
            for vertex in base
        ]
        self.formarBases()
        self.formarArestasVerticais()

    def gerar_solido(self):
        self.gerar_coordenadas()
        


# Tronco Piramide
tronco = Tronco_piramide(2, 1, 3, (-9, -3, -8))
tronco.gerar_solido()
tronco.plota_solido()


plt.show()
