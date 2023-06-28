import numpy as np
import matplotlib.pyplot as plt

fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")


# def rotacionar(angle_x, angle_y, angle_z, x, y, z):
#     angle_x = np.radians(angle_x)
#     angle_y = np.radians(angle_y)
#     angle_z = np.radians(angle_z)

#     rotation_x = np.array(
#         [
#             [1, 0, 0],
#             [0, np.cos(angle_x), -np.sin(angle_x)],
#             [0, np.sin(angle_x), np.cos(angle_x)],
#         ]
#     )

#     rotation_y = np.array(
#         [
#             [np.cos(angle_y), 0, np.sin(angle_y)],
#             [0, 1, 0],
#             [-np.sin(angle_y), 0, np.cos(angle_y)],
#         ]
#     )

#     rotation_z = np.array(
#         [
#             [np.cos(angle_z), -np.sin(angle_z), 0],
#             [np.sin(angle_z), np.cos(angle_z), 0],
#             [0, 0, 1],
#         ]
#     )
#     rotated_points = []
#     for i in range(len(x)):
#         point = np.array([x[i], y[i], z[i]])
#         rotated_point = np.dot(
#             rotation_x, np.dot(rotation_y, np.dot(rotation_z, point))
#         )
#         rotated_points.append(rotated_point)

#     return zip(*rotated_points)


# def escalar(sx, sy, sz, x, y, z, ponto_inicial):
#     # Cria matriz de escala
#     matriz_escala = np.array([[sx, 0, 0], [0, sy, 0], [0, 0, sz]])
#     pontos_scaled = matriz_escala.dot([x, y, z])

#     # Ajustar a posição dos pontos escalados
#     pontos_scaled[0] += ponto_inicial[0] * (1 - sx)
#     pontos_scaled[1] += ponto_inicial[1] * (1 - sy)
#     pontos_scaled[2] += ponto_inicial[2] * (1 - sz)
#     return pontos_scaled[0], pontos_scaled[1], pontos_scaled[2]


# def deslocar(dx, dy, dz, x, y, z):
#     T = np.array([[1, 0, 0, dx], [0, 1, 0, dy], [0, 0, 1, dz], [0, 0, 0, 1]])
#     complete_row = np.full((1, len(x)), 1)[0]
#     new_matrix = T.dot([x, y, z, complete_row])
#     x = new_matrix[0]
#     y = new_matrix[1]
#     z = new_matrix[2]
#     return x, y, z


def plotaSolido(pontos, arestas):
    for aresta in arestas:
        x = [pontos[0][aresta[0]], pontos[0][aresta[1]]]
        y = [pontos[1][aresta[0]], pontos[1][aresta[1]]]
        z = [pontos[2][aresta[0]], pontos[2][aresta[1]]]
        ax.plot(x, y, z, "b")


class Tronco_piramide:
    def __init__(self, aresta_inferior, aresta_superior, altura, ponto_inicial):
        self.aresta_superior = aresta_superior
        self.aresta_inferior = aresta_inferior
        self.altura = altura
        self.ponto_inicial = ponto_inicial
        self.x, self.y, self.z, self.arestas = [], [], [], []
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
        for index in range(len(self.x)):
            if contador != 3:
                contador += 1
                self.arestas.append([index, index + 1])
            else:
                self.arestas.append([index, index - 3])
                contador = 0

    def formarArestasVerticais(self):
        for index in range(len(self.x)):
            if index < (len(self.x) - 4):
                self.arestas.append([index, index + 4])

    def gera_tronco(self):
        # Inicializar as listas x, y, z antes de formar as bases e as arestas
        self.x = [vertex[0] for base in self.bases for vertex in base]
        self.y = [vertex[1] for base in self.bases for vertex in base]
        self.z = [
            vertex[2] + self.altura * index
            for index, base in enumerate(self.bases)
            for vertex in base
        ]
        self.formarBases()
        self.formarArestasVerticais()

    # def deslocar_tronco(self, dx, dy, dz):
    #     self.x, self.y, self.z = deslocar(dx, dy, dz, self.x, self.y, self.z)

    # def rotacionar_tronco(self, angle_x, angle_y, angle_z):
    #     self.x, self.y, self.z = rotacionar(
    #         angle_x, angle_y, angle_z, self.x, self.y, self.z
    #     )

    # def escalar_tronco(self, sx, sy, sz):
    #     self.x, self.y, self.z = escalar(
    #         sx, sy, sz, self.x, self.y, self.z, self.ponto_inicial
    #     )

    def plota_tronco(self):
        plotaSolido([self.x, self.y, self.z], self.arestas)


# Tronco Piramide
tronco = Tronco_piramide(2, 1, 3, (-9, -3, -8))
tronco.gera_tronco()
tronco.plota_tronco()

ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")

plt.show()
