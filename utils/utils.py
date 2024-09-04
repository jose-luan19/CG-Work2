import os
from matplotlib import pyplot as plt
import inspect
from matplotlib.axes import Axes
import numpy as np

from utils.solido import Solido

def calcular_vetores_aux(at, eye):
  # Calculando os vetores N, U e V da câmera
  at = np.array(at)
  n = at - eye
  aux = np.array([0, 1, 0])
  u = aux - projecao(aux, n)
  v = np.cross(u, n)
  N = n / np.linalg.norm(n)
  V = v / np.linalg.norm(v)
  U = u / np.linalg.norm(u)
  return U, V, N

def projecao(a, b):
  return (np.dot(a, b) / np.dot(b, b)) * b
  
def create_figure() -> Axes:
  fig = plt.figure()
  axes = fig.add_subplot(111, projection="3d")
  return axes  

def create_figure2D() -> Axes:
  fig = plt.figure()
  axes = fig.add_subplot()
  return axes

def calcular_at_medio(*centros_massas):
  # Calcula a soma de todos os elementos do array
  soma = sum(centros_massas)
  # Divide pela quantidade de elementos para obter a média
  media = soma / len(centros_massas)
  return media

def plotaSolido(solido: Solido, axes: Axes, cor) -> Axes:
  # Plota o sólido definido pelos pontos e arestas no gráfico 3D.
  pontos = [solido.pontosX, solido.pontosY, solido.pontosZ]
  for aresta in solido.arestas:
    x = [pontos[0][aresta[0]], pontos[0][aresta[1]]]
    y = [pontos[1][aresta[0]], pontos[1][aresta[1]]]
    z = [pontos[2][aresta[0]], pontos[2][aresta[1]]]
    axes.plot(x, y, z, cor)
  return axes, pontos

def plotaSolido2D(solido: Solido, axes: Axes, cor):
  pontos = [solido.pontosX, solido.pontosY]

  for aresta in solido.arestas:
    x = [pontos[0][aresta[0]], pontos[0][aresta[1]]]
    y = [pontos[1][aresta[0]], pontos[1][aresta[1]]]
    axes.plot(x, y, cor)
  return axes,pontos


def include_legend(ax: Axes, eye, at):
  # Plot do ponto de vista da câmera
  ax.scatter(eye[0], eye[1], eye[2], color="g", label="eye")

  # Média dos pontos
  ax.scatter(at[0], at[1], at[2], color="y", label="at")

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



