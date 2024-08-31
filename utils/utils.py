import os
from matplotlib import pyplot as plt
from abc import ABC, abstractmethod
import inspect


from matplotlib.axes import Axes
import numpy as np
  
class Solido(ABC):
  
  def __init__(self, ponto_inicial):
    self.ponto_inicial = ponto_inicial
    self.pontosX, self.pontosY, self.pontosZ, self.arestas = [], [], [], []
  
  def get_centro_massa(self):
    lista_vertices = self.get_vertices_lista().T
    return np.mean(lista_vertices, axis=0)
  
  def get_vertices_lista(self):
    return np.array([self.pontosX, self.pontosY, self.pontosZ])
  
  def set_vertices_lista(self, new_vertices):
    self.pontosX, self.pontosY, self.pontosZ = new_vertices
    
  def plota_solido(self, axes: Axes, cor="b") -> Axes:
    # Plota o cone no gráfico 3D.
    return plotaSolido(self, axes, cor)    
  
  def plota_solido2D(self, axes: Axes, cor="g") -> Axes:
    # Plota o cone no gráfico 3D.
    return plotaSolido2D(self, axes, cor)
    
  def escalar_solido(self, sx, sy, sz):
    self.pontosX, self.pontosY, self.pontosZ = escalar(sx, sy, sz, self)
  
  def rotacionar_solido(self, angle_x, angle_y, angle_z):
    self.pontosX, self.pontosY, self.pontosZ = rotacionar(angle_x, angle_y, angle_z, self)
  
  def transladar_solido(self, dx, dy, dz):
    self.pontosX, self.pontosY, self.pontosZ = transladar(dx, dy, dz, self)
  
  def converter_para_camera(self ,U, V, N, eye):
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
        RTMatrix, np.concatenate([lista_vertices.T, np.ones((1, lista_vertices.shape[0]))])
    )
    cameraVertexList = cameraVertexList[:3]
    self.set_vertices_lista(cameraVertexList)  # isso aqui é o solido transformado (já foi rotacionado e transladado)
    
  def transformacao_perspectiva(self):
    near = 0.1  
    far = 100.0
    alpha = np.pi / 2 # Ângulo alpha em radianos
    lista_vertices = self.get_vertices_lista()
    
    matrizHomogenea = np.vstack((lista_vertices, np.ones((1, lista_vertices.shape[1]))))
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
  
  
def calcular_vetores_aux(media_solidos, eye):
  # Calculando os vetores N, U e V da câmera
  at = np.array(media_solidos)
  n = at - eye
  aux = np.array([0, 1, 0])
  v = np.cross(aux, n)
  u = np.cross(v, n)
  N = n / np.linalg.norm(n)
  V = v / np.linalg.norm(v)
  U = u / np.linalg.norm(u)
  return U, V, N
  
def create_figure() -> Axes:
  fig = plt.figure()
  axes = fig.add_subplot(111, projection="3d")
  return axes  

def create_figure2D() -> Axes:
  fig = plt.figure()
  axes = fig.add_subplot(111)
  return axes

def calcular_media_solidos(cubeCenterMass, coneCenterMass, cilindroCenterMass, troncoCenterMass, esferaCenterMass):
  media = (cubeCenterMass
    + coneCenterMass
    + cilindroCenterMass
    + troncoCenterMass
    + esferaCenterMass
  ) / 5
  return media

def plotaSolido(solido: Solido, axes: Axes, cor) -> Axes:
  # Plota o sólido definido pelos pontos e arestas no gráfico 3D.
  pontos = [solido.pontosX, solido.pontosY, solido.pontosZ]
  for aresta in solido.arestas:
    x = [pontos[0][aresta[0]], pontos[0][aresta[1]]]
    y = [pontos[1][aresta[0]], pontos[1][aresta[1]]]
    z = [pontos[2][aresta[0]], pontos[2][aresta[1]]]
    axes.plot(x, y, z, cor)
  return axes

def plotaSolido2D(solido: Solido, axes: Axes, cor):
  pontos = [solido.pontosX, solido.pontosY]

  for aresta in solido.arestas:
    x = [pontos[0][aresta[0]], pontos[0][aresta[1]]]
    y = [pontos[1][aresta[0]], pontos[1][aresta[1]]]
    axes.plot(x, y, cor)
  return axes

def include_legend(ax: Axes, eye, media_solidos):
  # Plot do ponto de vista da câmera
  ax.scatter(eye[0], eye[1], eye[2], color="r", label="eye")

  # Média dos pontos
  ax.scatter(media_solidos[0], media_solidos[1], media_solidos[2], color="y", label="at")

  # Ponto Origem do Mundo
  ax.scatter(0, 0, 0, color="m", label="origem")
  
  ax.legend()
 

def show_figure(axes: Axes):
  axes.set_xlabel("X")
  axes.set_ylabel("Y")
  axes.set_zlabel("Z")
  # Obter o nome do arquivo que chamou esta função
  caller_frame = inspect.stack()[1]
  caller_filename = caller_frame.filename
  file_name = 'images/'+ os.path.splitext(os.path.basename(caller_filename))[0] + '.png'
  
  plt.savefig(file_name)
  plt.show()

def show_figure2D(axes: Axes):
  axes.set_xlabel("X")
  axes.set_ylabel("Y")
  caller_frame = inspect.stack()[1]
  caller_filename = caller_frame.filename
  file_name = 'images/'+ os.path.splitext(os.path.basename(caller_filename))[0] + '.png'
  
  plt.savefig(file_name)
  plt.show()

def rotacionar(angle_x, angle_y, angle_z, solido: Solido):
  angle_x = np.radians(angle_x)
  angle_y = np.radians(angle_y)
  angle_z = np.radians(angle_z)

  rotation_x = np.array(
    [
      [1, 0, 0],
      [0, np.cos(angle_x), -np.sin(angle_x)],
      [0, np.sin(angle_x), np.cos(angle_x)],
    ]
  )

  rotation_y = np.array(
    [
      [np.cos(angle_y), 0, np.sin(angle_y)],
      [0, 1, 0],
      [-np.sin(angle_y), 0, np.cos(angle_y)],
    ]
  )

  rotation_z = np.array(
    [
      [np.cos(angle_z), -np.sin(angle_z), 0],
      [np.sin(angle_z), np.cos(angle_z), 0],
      [0, 0, 1],
    ]
  )
  rotated_points = []
  for i in range(len(solido.pontosX)):
    point = np.array([solido.pontosX[i], solido.pontosY[i], solido.pontosZ[i]])
    rotated_point = np.dot(rotation_x, np.dot(rotation_y, np.dot(rotation_z, point)))
    rotated_points.append(rotated_point)

  return zip(*rotated_points)

def escalar(sx, sy, sz, solido: Solido):
  # Cria matriz de escala
  matriz_escala = np.array([[sx, 0, 0], [0, sy, 0], [0, 0, sz]])
  pontos_scaled = matriz_escala.dot([solido.pontosX, solido.pontosY, solido.pontosZ])

  # Ajustar a posição dos pontos escalados
  pontos_scaled[0] += solido.ponto_inicial[0] * (1 - sx)
  pontos_scaled[1] += solido.ponto_inicial[1] * (1 - sy)
  pontos_scaled[2] += solido.ponto_inicial[2] * (1 - sz)
  return pontos_scaled[0], pontos_scaled[1], pontos_scaled[2]

def transladar(dx, dy, dz, solido: Solido):
  T = np.array([[1, 0, 0, dx], 
                [0, 1, 0, dy], 
                [0, 0, 1, dz], 
                [0, 0, 0, 1]
                ])
  
  complete_row = np.full((1, len(solido.pontosX)), 1)[0]
  new_matrix = T.dot([solido.pontosX, solido.pontosY, solido.pontosZ, complete_row])
  x = new_matrix[0]
  y = new_matrix[1]
  z = new_matrix[2]
  return x, y, z


def calculateCenterMass(vertexList):
  return np.mean(vertexList, axis=0)


def convertWorldToCamera(vertexList, U, V, N, eye):
  RTMatrix = np.array(
    [
      [U[0], U[1], U[2], -np.dot(eye, U)],
      [V[0], V[1], V[2], -np.dot(eye, V)],
      [N[0], N[1], N[2], -np.dot(eye, N)],
      [0, 0, 0, 1],
    ]
  )
  cameraVertexList = np.dot(
    RTMatrix, np.concatenate([vertexList.T, np.ones((1, vertexList.shape[0]))])
  )
  cameraVertexList = cameraVertexList[:3].T
  return cameraVertexList  # isso aqui é o solido transformado (já foi rotacionado e transladado)