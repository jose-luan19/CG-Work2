import numpy as np
import utils.utils as util


class Cano(util.Solido):
    def __init__(self, raio, P1, P2, T1, T2, resolucao_curva=20, num_camadas=20):
        self.raio = raio
        self.P1 = np.array(P1)
        self.P2 = np.array(P2)
        self.T1 = np.array(T1)
        self.T2 = np.array(T2)
        self.resolucao_curva = resolucao_curva
        self.num_camadas = num_camadas
        super().__init__(self.P1)

    def gerar_coordenadas(self):
        t = np.linspace(0, 1, self.resolucao_curva)  
        # As funções de base Hermite (h00, h10, h01, h11) são derivadas da multiplicação 
        # da matriz inversa de coeficientes pelas potências de t.
        # 
        # Matriz inversa (M^-1):
        # [ 1   0  0   0  ]
        # [ 0   1  0   0  ]
        # [-3  -2  3  -1  ]
        # [ 2   1 -2   1  ]
        #
        # Multiplicamos essa matriz pelas potências de t:
        # [1, t, t^2, t^3]^T
        # 
        # Para h00(t), realizamos:
        # h00(t) = 1 * 1 + 0 * t + 0 * t^2 + 0 * t^3 = 1
        #
        # E fazendo a combinação linear completa:
        # h00(t) = 1 + 0 - 3 * t^2 + 2 * t^3 = 2 * t^3 - 3 * t^2 + 1
        #
        # Dessa forma, obtemos:
        # h00(t) =  2 * t^3 - 3 * t^2 + 1
        # h10(t) =  t^3 - 2 * t^2 + t
        # h01(t) = -2 * t^3 + 3 * t^2
        # h11(t) =  t^3 - t^2

        h00 = 2 * t**3 - 3 * t**2 + 1
        h10 = t**3 - 2 * t**2 + t
        h01 = -2 * t**3 + 3 * t**2
        h11 = t**3 - t**2 

        # Calcular as funções de Hermite para os valores de t
        # h00, h10, h01 e h11 são vetores (um para cada valor de t)
        h00_t = h00[:, None] # Adiciona uma dimensão para transformar o vetor 1D em uma matriz coluna 2D.
        h10_t = h10[:, None]
        h01_t = h01[:, None]
        h11_t = h11[:, None]

        # Combinar as funções de Hermite com os pontos de controle e os vetores tangentes
        contribuicao_p1 = h00_t * self.P1  # Contribuição de P1 ao longo da curva
        contribuicao_t1 = h10_t * self.T1  # Contribuição de T1 ao longo da curva
        contribuicao_p2 = h01_t * self.P2  # Contribuição de P2 ao longo da curva
        contribuicao_t2 = h11_t * self.T2  # Contribuição de T2 ao longo da curva

        # Somar todas as contribuições para obter os pontos da curva
        curva = (
            contribuicao_p1
            + contribuicao_t1
            + contribuicao_p2
            + contribuicao_t2
        )


        # Gerar as circunferências ao longo dos pontos da curva
        theta = np.linspace(0, 2 * np.pi, self.num_camadas)  # Array de ângulos para criar circunferências
        x_circ = self.raio * np.cos(theta)  # Coordenadas X da circunferência no plano XY
        y_circ = self.raio * np.sin(theta)  # Coordenadas Y da circunferência no plano XY

        # Listas para armazenar as coordenadas X, Y e Z de todos os pontos do cano
        x_var = []
        y_var = []
        z_var = []

        # Para cada ponto ao longo da curva de Hermite
        for ponto in curva:
            x_var.append(ponto[0] + x_circ)  # Desloca a circunferência ao longo da coordenada X
            y_var.append(ponto[1] + y_circ)  # Desloca a circunferência ao longo da coordenada Y
            z_var.append(np.full_like(x_circ, ponto[2]))  # Mantém a coordenada Z constante ao longo da circunferência

        # Converte as listas em arrays numpy e retorna as coordenadas X, Y, Z dos pontos do cano
        return np.array(x_var), np.array(y_var), np.array(z_var)


    def gerar_solido(self):
        # Obtém as coordenadas x, y e z dos pontos ao longo da curva
        x_var, y_var, z_var = self.gerar_coordenadas()

        # Número de linhas e colunas na matriz de coordenadas
        num_rows, num_cols = x_var.shape
        
        # Contador para rastrear as colunas durante a adição das arestas horizontais
        cont = 0

        # Itera sobre as linhas da matriz de coordenadas, exceto a última linha
        for i in range(num_rows - 1):
            # Itera sobre as colunas da matriz de coordenadas, exceto a última coluna
            for j in range(num_cols - 1):
                # Para evitar acessar índices fora dos limites e garantir a formação completa das células da malha.
                # pois não haveria uma linha ou coluna extra para formar uma célula completa.

                # Calcula as coordenadas dos quatro vértices do quadrado da célula atual
                # Cada célula é formada por 4 vértices que definem um quadrado ou retângulo na superfície do cilindro

                # Vértice inferior esquerdo da célula (i, j)
                x1, y1, z1 = x_var[i, j], y_var[i, j], z_var[i, j]
                # Vértice inferior direito da célula (i, j+1)
                x2, y2, z2 = x_var[i, j + 1], y_var[i, j + 1], z_var[i, j + 1]
                # Vértice superior direito da célula (i+1, j+1)
                x3, y3, z3 = x_var[i + 1, j + 1], y_var[i + 1, j + 1], z_var[i + 1, j + 1]
                # Vértice superior esquerdo da célula (i+1, j)
                x4, y4, z4 = x_var[i + 1, j], y_var[i + 1, j], z_var[i + 1, j]

                # Adiciona as coordenadas dos vértices às listas de pontos
                self.pontosX.extend([x1, x2, x3, x4])
                self.pontosY.extend([y1, y2, y3, y4])
                self.pontosZ.extend([z1, z2, z3, z4])

                # Calcula as posições atuais dos vértices na lista de pontos formar as arestas dos retangulos/quadrados
                posicaov1 = len(self.pontosX) - 4
                posicaov2 = len(self.pontosX) - 3
                posicaov3 = len(self.pontosX) - 2
                posicaov4 = len(self.pontosX) - 1

                # Adiciona arestas horizontais entre os vértices da mesma linha
                if cont < num_cols - 1:
                    self.arestas.append([posicaov1, posicaov2])  # Aresta horizontal entre v1 e v2
                    cont += 1

                # Adiciona arestas verticais entre as linhas de vértices
                self.arestas.append([posicaov2, posicaov3])  # Aresta vertical entre v2 e v3
                self.arestas.append([posicaov3, posicaov4])  # Aresta horizontal entre v3 e v4


if __name__ == "__main__":
    # Definindo os parâmetros da curva de Hermite
    P1 = [1, 1, 1]  # Ponto inicial da curva
    P2 = [1, 1, 25]  # Ponto final da curva
    T1 = [1, 2, 12]  # Vetor tangente inicial
    T2 = [-3, -4, 30]  # Vetor tangente final
    raio_cano = 0.3 # Define o raio do cano
    resolucao_curva = 15 # mais curvo
    num_camadas = 20 # mais redondo
    

    # Criando o "cano"
    # Cano é dividido em celulas quadradas que compõem a face do mesmo
    cano = Cano(raio_cano, P1, P2, T1, T2, resolucao_curva, num_camadas)

    # quantidade de pontos = (resolucao_curva - 1) * (num_camadas - 1) * 4 (O 4 é por representar a face do cano com retangulos e quadrados)
    cano.gerar_solido()

    # Plotando o "cano"
    axes = cano.plota_solido(util.create_figure())
    util.show_figure(axes)
