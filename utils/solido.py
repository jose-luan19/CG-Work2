from abc import ABC, abstractmethod
from matplotlib.axes import Axes
import numpy as np

from utils import utils


class Solido(ABC):

      def __init__(self, ponto_inicial):
            self.ponto_inicial = ponto_inicial
            self.pontosX, self.pontosY, self.pontosZ, self.arestas = [], [], [], []
            self.faces = []  # Para armazenar as faces do sólido

      def get_centro_massa(self):
            lista_vertices = self.get_vertices_lista().T
            return np.mean(lista_vertices, axis=0)

      def get_vertices_lista(self):
            return np.array([self.pontosX, self.pontosY, self.pontosZ])

      def set_vertices_lista(self, new_vertices):
            self.pontosX, self.pontosY, self.pontosZ = new_vertices

      def plota_solido_com_faces(self, axes: Axes, cor_arestas="b", cor_faces="r", alpha=1) -> Axes:
            axes, pontos = utils.plotaSolido(self, axes, cor_arestas)
            self.preencher_faces(axes, pontos, cor_faces, cor_arestas, alpha)
            return axes

      @abstractmethod
      def preencher_faces(self, axes, pontos, cor_faces, cor_arestas, alpha):
            pass

      def plota_solido(self, axes: Axes, cor="b") -> Axes:
            # Plota o cone no gráfico 3D.
            return utils.plotaSolido(self, axes, cor)

      def plota_solido2D(self, axes: Axes, cor="g") -> Axes:
            # Plota o cone no gráfico 3D.
            return utils.plotaSolido2D(self, axes, cor)

      def escalar_solido(self, sx, sy, sz):
            self.pontosX, self.pontosY, self.pontosZ = utils.escalar(sx, sy, sz, self)

      def rotacionar_solido(self, angle_x, angle_y, angle_z):
            self.pontosX, self.pontosY, self.pontosZ = utils.rotacionar(
                  angle_x, angle_y, angle_z, self
            )

      def transladar_solido(self, dx, dy, dz):
            self.pontosX, self.pontosY, self.pontosZ = utils.transladar(dx, dy, dz, self)

      def converter_para_camera(self, U, V, N, eye):
            RTMatrix = np.array(
                  [
                  [U[0], U[1], U[2], -np.dot(eye, U)],
                  [V[0], V[1], V[2], -np.dot(eye, V)],
                  [N[0], N[1], N[2], -np.dot(eye, N)],
                  [0, 0, 0, 1],
                  ]
            )
            lista_vertices = self.get_vertices_lista().T
            cameraVertexList = np.dot(
                  RTMatrix,
                  np.concatenate([lista_vertices.T, np.ones((1, lista_vertices.shape[0]))]),
            )
            cameraVertexList = cameraVertexList[:3]
            self.set_vertices_lista(
                  cameraVertexList
            )  # isso aqui é o solido transformado (já foi rotacionado e transladado)

      def transformacao_perspectiva(self):
            near = 0.1
            far = 100.0
            alpha = np.pi / 2  # Ângulo alpha em radianos
            lista_vertices = self.get_vertices_lista()

            matrizHomogenea = np.vstack(
                  (lista_vertices, np.ones((1, lista_vertices.shape[1])))
            )
            verticesEmPerspectiva = np.zeros_like(matrizHomogenea)

            for i in range(matrizHomogenea.shape[1]):
                  verticesEmPerspectiva[:, i] = (
                  np.array(
                        [
                              [1 / (matrizHomogenea[2, i] * np.tan(alpha / 2)), 0, 0, 0],
                              [0, 1 / (matrizHomogenea[2, i] * np.tan(alpha / 2)), 0, 0],
                              [
                              0,
                              0,
                              (near + far) / (near - far),
                              (2 * near * far) / (near - far),
                              ],
                              [0, 0, -1, 0],
                        ]
                  )
                  @ matrizHomogenea[:, i]
                  )

            verticesEmPerspectiva = verticesEmPerspectiva[:-1, :]
            verticesEmPerspectiva[-1, :] = 0
            self.set_vertices_lista(verticesEmPerspectiva)

      @abstractmethod
      def gerar_coordenadas(self):
            pass

      @abstractmethod
      def gerar_solido(self):
            pass
