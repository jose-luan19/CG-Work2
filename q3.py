import numpy as np
import utils.utils as util

from cilindro import Cilindro
from cone import Cone
from cubo import Cubo
from esfera import Esfera
from tronco_piramide import Tronco_piramide

  
def main():
    # ENTRADA
    cubo = Cubo(4, [-6, -8, -7])
    cubo.gerar_solido()

    cone = Cone(1, 2, 5, [8, 6, 4])
    cone.gerar_solido()

    cilindro = Cilindro(1, 2, [2, 4, 3])
    cilindro.gerar_solido()

    tronco = Tronco_piramide(2, 1, 2, [-9, -3, -8])
    tronco.gerar_solido()

    esfera = Esfera(1, [7, -2, -6])
    esfera.gerar_solido()

    # Calculando os centros de massa das formas geométricas
    cubeCenterMass = cubo.get_centro_massa()
    coneCenterMass = cone.get_centro_massa()
    cilindroCenterMass = cilindro.get_centro_massa()
    troncoCenterMass = tronco.get_centro_massa()
    esferaCenterMass = esfera.get_centro_massa()

    # calculando a média de todos os centros para apontar a câmera
    media_solidos = util.calcular_media_solidos(cubeCenterMass, coneCenterMass, cilindroCenterMass, troncoCenterMass, esferaCenterMass)

    # Posição da câmera
    eye = np.array([-7, -1, 6])
    # -7,-1,6
    # 1,-4,2
    # -2, 3, -5

    # Calculando os vetores N, U e V da câmera
    U, V, N = util.calcular_vetores_aux(media_solidos, eye)

    cubo.convertWorldToCamera( U, V, N, eye)
    cone.convertWorldToCamera( U, V, N, eye)
    cilindro.convertWorldToCamera( U, V, N, eye)
    tronco.convertWorldToCamera( U, V, N, eye)
    esfera.convertWorldToCamera( U, V, N, eye)
    

    return cubo, cone, cilindro, tronco, esfera, (media_solidos, eye)

    

if __name__ == "__main__":
    
    # Criação da figura e do subplot 3D
    ax = util.create_figure()
    
    cubo, cone, cilindro, tronco, esfera, args = main()
    eye, media_solidos = args
    util.include_legend(ax, eye, media_solidos)
    
    ax = cubo.plota_solido(ax)
    ax = cone.plota_solido(ax)
    ax = cilindro.plota_solido(ax)
    ax = tronco.plota_solido(ax)
    ax = esfera.plota_solido(ax)

    util.show_figure(ax)
    
