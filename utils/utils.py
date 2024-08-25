from matplotlib import pyplot as plt
from abc import ABC, abstractmethod


def plotaSolido(pontos, arestas):
  # Plota o sólido definido pelos pontos e arestas no gráfico 3D.
  fig = plt.figure()
  ax = fig.add_subplot(111, projection="3d")

  for aresta in arestas:
    x = [pontos[0][aresta[0]], pontos[0][aresta[1]]]
    y = [pontos[1][aresta[0]], pontos[1][aresta[1]]]
    z = [pontos[2][aresta[0]], pontos[2][aresta[1]]]
    ax.plot(x, y, z, "b")
  
  ax.set_xlabel("X")
  ax.set_ylabel("Y")
  ax.set_zlabel("Z")
  
class Solido(ABC):
  
  def __init__(self, ponto_inicial):
    self.ponto_inicial = ponto_inicial
    self.pontosX, self.pontosY, self.pontosZ, self.arestas = [], [], [], []
    
  
  def plota_solido(self):
    # Plota o cone no gráfico 3D.
    plotaSolido([self.pontosX, self.pontosY, self.pontosZ], self.arestas)
    
  @abstractmethod
  def gerar_coordenadas(self):
    pass 
    
  @abstractmethod
  def gerar_solido(self):
    pass
  
  