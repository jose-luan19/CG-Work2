import utils.utils as util

from cilindro import Cilindro
from cone import Cone
from cubo import Cubo
from esfera import Esfera
from tronco_piramide import Tronco_piramide

axes = util.create_figure()

# Cone #ROTACIONADO
radius = 1.0
height = 2 * radius
num_slices = 15
ponto_inicial_cone = [9, 6, 4]

cone = Cone(radius, height, num_slices, ponto_inicial_cone)
cone.gerar_solido()
axes = cone.plota_solido(axes)
cone.rotacionar_solido(90, 0, 0)
cone.plota_solido(axes, cor = "g")

# Cubo #ESCALADO e DESLOCADO
raio_cubo = 1
ponto_inicial_cubo = [-6, -8, -7]

cubo = Cubo(raio_cubo, ponto_inicial_cubo)
cubo.gerar_solido()
cubo.plota_solido(axes)
cubo.transladar_solido(1,0,1)
cubo.plota_solido(axes, cor = 'y')


# cubo.escalar_cubo(2, 2, 2)
# cubo.plota_cubo()

# Tronco Piramide
tronco = Tronco_piramide(2, 1, 3, (-9, -3, -8))
tronco.gerar_solido()
tronco.plota_solido(axes)
# posicao_final = (2, 3, 1)
tronco.rotacionar_solido(45, 0, 0)
tronco.plota_solido(axes, cor = "g")
# tronco.plota_tronco()

# Esfera

# Cria um objeto Esfera com raio 1 e ponto inicial (0, 0, 0)
esfera = Esfera(1, (7, -2, -6))

# Plota a esfera original
esfera.gerar_solido()
esfera.plota_solido(axes)

# Aplica a escala de fator 2 em todos os eixos
esfera.escalar_solido(2, 2, 2)
esfera.plota_solido(axes, cor = "r")

# Cilindro  #ESCALADO 
raio_cilindro = 1
altura_cilindro = 2
ponto_inicial_cilindro = [2, 4, 3]
cilindro = Cilindro(raio_cilindro, altura_cilindro, ponto_inicial_cilindro)
cilindro.gerar_solido()
cilindro.plota_solido(axes)


cilindro.escalar_solido(2, 2, 2,)  # esse valor 2 é o valor do "fator"
cilindro.plota_solido(axes, cor = "r")

util.show_figure(axes)
 