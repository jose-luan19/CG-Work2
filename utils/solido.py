from abc import ABC, abstractmethod
from matplotlib.axes import Axes
import numpy as np

from utils import utils


class Solido(ABC):

      def __init__(self):
            self.ponto_inicial = [0,0,0]
            self.pontosX, self.pontosY, self.pontosZ, self.arestas = [], [], [], []
            self.faces = []  # Para armazenar as faces do sólido

      def calcular_d(self, at, eye):
            # Calcule o vetor de visão N
            N = at - eye
            N = N / np.linalg.norm(N)  # Normaliza o vetor N

            # Calcule o centro de massa do sólido
            centro_massa = self.get_centro_massa()

            # Calcule d como a projeção do vetor (C - eye) no vetor N
            d = np.dot((centro_massa - eye), N)
            return d

      def get_centro_massa(self):
            lista_vertices = self.get_vertices_lista().T
            return np.mean(lista_vertices, axis=0)
      
      def get_vertices_lista(self):
            return np.array([self.pontosX, self.pontosY, self.pontosZ])

      def set_vertices_lista(self, new_vertices):
            self.pontosX, self.pontosY, self.pontosZ = new_vertices
            
      @abstractmethod
      def preencher_faces(self, axes, pontos, cor_faces, cor_arestas, alpha):
            pass
      
      @abstractmethod
      def preencher_faces_2D(self, axes, pontos_2d, cor_faces, cor_arestas, alpha):
            pass

      def plota_solido_com_faces(self, axes: Axes, cor_faces = "brown", cor_arestas = "black", alpha = 0.7) -> Axes:
            axes, pontos_2d = utils.plotaSolido(self, axes, cor_arestas)
            axes = self.preencher_faces(axes, pontos_2d, cor_faces, cor_arestas, alpha)
            return axes

      def plota_solido2D_com_faces(self, axes: Axes, cor_faces = "brown", cor_arestas = "black", alpha = 0.7) -> Axes:
            # Plota o cone no gráfico 3D.
            axes, pontos = utils.plotaSolido2D(self, axes, cor_arestas)
            axes = self.preencher_faces_2D(axes, pontos, cor_faces, cor_arestas, alpha)
            return axes
      
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
            R = np.array(
                  [
                        [U[0], U[1], U[2], 0],
                        [V[0], V[1], V[2], 0],
                        [N[0], N[1], N[2], 0],
                        [0, 0, 0, 1],
                  ]
            )
            T = np.array(
                  [
                        [1, 0, 0, -eye[0]],
                        [0, 1, 0, -eye[1]],
                        [0, 0, 1, -eye[2]],
                        [0, 0, 0, 1],
                  ]
            )
            RT = R @ T
            lista_vertices = self.get_vertices_lista()
            vertices_homogeneos = np.hstack((lista_vertices.T, np.ones((lista_vertices.shape[1], 1))))
            vertices_camera = RT @ vertices_homogeneos.T
            vertices_camera = vertices_camera.T[:, :3].T  # Ignorar a coordenada homogênea
            self.set_vertices_lista(vertices_camera)  # Atualizar o sólido com os vértices no sistema de coordenadas da câmera

      def transformacao_perspectiva(self, at, eye):
            # Projeta os vértices do sólido em um plano 2D usando a transformação em perspectiva simples

            # Calcule o valor de d dinamicamente
            d = self.calcular_d(at, eye)
            
            # Obtém os vértices do sólido em coordenadas homogêneas (com 1 no final)
            lista_vertices = self.get_vertices_lista()
            matrizHomogenea = np.vstack((lista_vertices, np.ones((1, lista_vertices.shape[1]))))
            
            # Inicializa a matriz de vértices transformados em perspectiva
            verticesEmPerspectiva = np.zeros_like(matrizHomogenea)

            # Para cada vértice, aplica a projeção em perspectiva
            for i in range(matrizHomogenea.shape[1]):
                  x, y, z = matrizHomogenea[0, i], matrizHomogenea[1, i], matrizHomogenea[2, i]
                  
                  # Aplica a fórmula da projeção em perspectiva
                  verticesEmPerspectiva[0, i] = d * x / z  # x'
                  verticesEmPerspectiva[1, i] = d * y / z  # y'
                  verticesEmPerspectiva[2, i] = 0  # z' será 0, pois estamos projetando no plano 2D
            
            # Atualiza os vértices do sólido com as novas coordenadas 2D projetadas
            self.set_vertices_lista(verticesEmPerspectiva[:3, :])  # Mantém apenas as coordenadas 2D (x, y)
      
      # def transformacao_perspectiva(self, at, eye):
      #       # Projeta os vértices do sólido em um plano 2D usando a transformação em perspectiva
      #       near = 0.1  # Plano de recorte próximo
      #       far = 100.0  # Plano de recorte distante
      #       alpha = np.pi / 2  # Ângulo de visão em radianos

      #       # Calcule o valor de d dinamicamente
      #       d = self.calcular_d(at, eye)
            
      #       lista_vertices = self.get_vertices_lista()
      #       matrizHomogenea = np.vstack((lista_vertices, np.ones((1, lista_vertices.shape[1]))))
      #       verticesEmPerspectiva = np.zeros_like(matrizHomogenea)

      #       for i in range(matrizHomogenea.shape[1]):
      #             z = matrizHomogenea[2, i]
      #             perspectiva = np.array([
      #                   [d / (z * np.tan(alpha / 2)), 0, 0, 0],
      #                   [0, d / (z * np.tan(alpha / 2)), 0, 0],
      #                   [0, 0, (near + far) / (near - far), (2 * near * far) / (near - far)],
      #                   [0, 0, -1, 0]
      #             ])
      #             verticesEmPerspectiva[:, i] = perspectiva @ matrizHomogenea[:, i]

      #       # Normaliza os vértices em perspectiva
      #       verticesEmPerspectiva = verticesEmPerspectiva[:-1, :] / verticesEmPerspectiva[-1, :]
            
      #       # Preenche o terceiro array (coordenadas z) com zeros
      #       verticesEmPerspectiva[2, :] = 0
            
      #       # Atualiza os vértices do sólido
      #       self.set_vertices_lista(verticesEmPerspectiva[:3, :])  # Mantém apenas as coordenadas 2D (x, y)

      
      @abstractmethod
      def gerar_coordenadas(self):
            pass

      @abstractmethod
      def gerar_solido(self):
            pass
