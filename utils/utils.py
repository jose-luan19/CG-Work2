from matplotlib import pyplot as plt
from abc import ABC, abstractmethod

from matplotlib.axes import Axes
import numpy as np
  
class Solido(ABC):
  
  def __init__(self, ponto_inicial):
    self.ponto_inicial = ponto_inicial
    self.pontosX, self.pontosY, self.pontosZ, self.arestas = [], [], [], []
    
  
  def plota_solido(self, axes: Axes, cor="b") -> Axes:
    # Plota o cone no gráfico 3D.
    return plotaSolido(self, axes, cor)
    
  def escalar_solido(self, sx, sy, sz):
    self.pontosX, self.pontosY, self.pontosZ = escalar(sx, sy, sz, self)
  
  def rotacionar_solido(self, angle_x, angle_y, angle_z):
    self.pontosX, self.pontosY, self.pontosZ = rotacionar(angle_x, angle_y, angle_z, self)
  
  def transladar_solido(self, dx, dy, dz):
    self.pontosX, self.pontosY, self.pontosZ = transladar(dx, dy, dz, self)
  
  @abstractmethod
  def gerar_coordenadas(self):
    pass 
    
  @abstractmethod
  def gerar_solido(self):
    pass
  
def create_figure() -> Axes:
  fig = plt.figure()
  axes = fig.add_subplot(111, projection="3d")
  return axes



def plotaSolido(solido: Solido, axes: Axes, cor) -> Axes:
  # Plota o sólido definido pelos pontos e arestas no gráfico 3D.
  pontos = [solido.pontosX, solido.pontosY, solido.pontosZ]
  for aresta in solido.arestas:
    x = [pontos[0][aresta[0]], pontos[0][aresta[1]]]
    y = [pontos[1][aresta[0]], pontos[1][aresta[1]]]
    z = [pontos[2][aresta[0]], pontos[2][aresta[1]]]
    axes.plot(x, y, z, cor)
  return axes


def show_figure(axes: Axes):
  axes.set_xlabel("X")
  axes.set_ylabel("Y")
  axes.set_zlabel("Z")
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
