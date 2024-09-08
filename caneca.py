from cilindro import Cilindro
from toroide import Toroide
import utils.utils as util

class Caneca(util.Solido):
    def __init__(self, raio_cilindro, altura_cilindro, raio_toroide, raio_central_toroide, ponto_inicial):
        super().__init__()  # Inicializa a classe base sem parâmetros
        self.ponto_inicial = ponto_inicial
        self.cilindro = Cilindro(raio_cilindro, altura_cilindro, ponto_inicial)
        
        # Altura e posicionamento da alça (toroide)
        altura_toroide = raio_toroide * 2  # Ajustando a altura do toroide conforme necessário
        ponto_toroide = [
            ponto_inicial[0] + raio_cilindro + raio_toroide * 0.9,  # Ajusta para ficar próximo ao cilindro
            ponto_inicial[1] + altura_cilindro / 2,  # Centraliza o toroide em altura
            ponto_inicial[2]  # Mantém a profundidade
        ]
        self.toroide = Toroide(raio_toroide, raio_central_toroide, ponto_toroide, altura_toroide)  # Passando a altura

    def gerar_coordenadas(self):
        # Gerar coordenadas para o corpo (cilindro)
        x_cilindro, y_cilindro, z_cilindro = self.cilindro.gerar_coordenadas()
        
        # Gerar coordenadas para a alça (toroide)
        x_toroide, y_toroide, z_toroide = self.toroide.gerar_coordenadas()

        return (x_cilindro, y_cilindro, z_cilindro), (x_toroide, y_toroide, z_toroide)

    def gerar_solido(self):
        # Gerar sólidos para o corpo (cilindro) e a alça (toroide)
        self.cilindro.gerar_solido()
        self.toroide.gerar_solido()

        # Adicionar pontos e arestas do toroide ao cilindro
        self.pontosX.extend(self.cilindro.pontosX + self.toroide.pontosX)
        self.pontosY.extend(self.cilindro.pontosY + self.toroide.pontosY)
        self.pontosZ.extend(self.cilindro.pontosZ + self.toroide.pontosZ)
        self.arestas.extend(self.cilindro.arestas + self.toroide.arestas)

    def preencher_faces(self, axes, cor_faces_cilindro='brown', cor_faces_toroide='brown', cor_arestas='black', alpha=0.7):
        # Preencher a superfície do corpo (cilindro)
        self.cilindro.preencher_faces(axes, cor_faces_cilindro, cor_arestas, alpha)
        
        # Preencher a superfície da alça (toroide)
        self.toroide.preencher_faces(axes, cor_faces_toroide, cor_arestas, alpha)

    def preencher_faces_2D(self, axes, pontos_2d, cor_faces, cor_arestas, alpha):
        pass

if __name__ == "__main__":
    # Parâmetros da caneca
    raio_cilindro = 0.5
    altura_cilindro = 1.0
    raio_toroide = 0.1
    raio_central_toroide = 0.4
    ponto_inicial_caneca = [0, 0, 0]
    
    caneca = Caneca(raio_cilindro, altura_cilindro, raio_toroide, raio_central_toroide, ponto_inicial_caneca)
    caneca.gerar_solido()
    
    # Cria e plota a caneca
    axes = util.create_figure()
    caneca.plota_solido(axes)
    caneca.preencher_faces(axes)
    util.show_figure(axes)

















# ==========FUNCIONANDO DE MANEIRA ERRADA========

'''class Caneca (util.Solido):
    def __init__(self, raio_cilindro, altura_cilindro, raio_toroide, raio_central_toroide, ponto_inicial):
        self.cilindro = Cilindro(raio_cilindro, altura_cilindro, ponto_inicial)
        self.toroide = Toroide(raio_toroide, raio_central_toroide, [ponto_inicial[0], ponto_inicial[1] + altura_cilindro / 2, ponto_inicial[2]])
        super().__init__(ponto_inicial)

    def gerar_coordenadas(self):
        # Gerar coordenadas para o corpo (cilindro)
        x_cilindro, y_cilindro, z_cilindro = self.cilindro.gerar_coordenadas()
        
        # Gerar coordenadas para a alça (toroide)
        x_toroide, y_toroide, z_toroide = self.toroide.gerar_coordenadas()

        return (x_cilindro, y_cilindro, z_cilindro), (x_toroide, y_toroide, z_toroide)

    def gerar_solido(self):
        # Gerar sólidos para o corpo (cilindro) e a alça (toroide)
        self.cilindro.gerar_solido()
        self.toroide.gerar_solido()

        # Adicionar pontos e arestas do toroide ao cilindro
        self.pontosX.extend(self.cilindro.pontosX + self.toroide.pontosX)
        self.pontosY.extend(self.cilindro.pontosY + self.toroide.pontosY)
        self.pontosZ.extend(self.cilindro.pontosZ + self.toroide.pontosZ)
        self.arestas.extend(self.cilindro.arestas + self.toroide.arestas)

    def preencher_faces(self, axes, cor_faces_cilindro='blue', cor_faces_toroide='red', alpha=0.7):
        # Preencher a superfície do corpo (cilindro)
        self.cilindro.preencher_faces(axes, cor_faces_cilindro, alpha)
        
        # Preencher a superfície da alça (toroide)
        self.toroide.preencher_faces(axes, cor_faces_toroide, alpha)

    def preencher_faces_2D(self, axes, pontos_2d, cor_faces, cor_arestas, alpha):
        pass


if __name__ == "__main__":
    # Parâmetros da caneca
    raio_cilindro = 0.5
    altura_cilindro = 1.0
    raio_toroide = 0.1
    raio_central_toroide = 0.6
    ponto_inicial_caneca = [0, 0, 0]
    
    caneca = Caneca(raio_cilindro, altura_cilindro, raio_toroide, raio_central_toroide, ponto_inicial_caneca)
    caneca.gerar_solido()
    
    # Cria e plota a caneca
    axes = util.create_figure()
    caneca.plota_solido(axes)
    caneca.preencher_faces(axes)
    util.show_figure(axes) '''