import numpy as np
import q2
import utils.utils as util

  
def main():
    cone, tronco_cone, cano, caixa = q2.main()
    # Calculando os centros de massa das formas geométricas
    coneCenterMass = cone.get_centro_massa()
    tronco_coneCenterMass = tronco_cone.get_centro_massa()
    canoCenterMass = cano.get_centro_massa()
    caixaCenterMass = caixa.get_centro_massa()

    # calculando a média de todos os centros para apontar a câmera
    at = util.calcular_at_medio(coneCenterMass, tronco_coneCenterMass, canoCenterMass, caixaCenterMass)

    # Posição da câmera
    eye = np.array([-4,-7, 3])


    # Calculando os vetores N, U e V da câmera
    U, V, N = util.calcular_vetores_aux(at, eye)

    cone.converter_para_camera( U, V, N, eye)
    cano.converter_para_camera( U, V, N, eye)
    tronco_cone.converter_para_camera( U, V, N, eye)
    caixa.converter_para_camera( U, V, N, eye)
    
    return cone, cano, tronco_cone, caixa, at, eye
    
if __name__ == "__main__":
    
    # Criação da figura e do subplot 3D
    ax = util.create_figure()
    
    cone, cano, tronco_cone, caixa, at, eye = main()
    util.include_legend(ax, eye, at)
    
    ax = cano.plota_solido_com_faces(ax)
    ax = cone.plota_solido_com_faces(ax)
    ax = tronco_cone.plota_solido_com_faces(ax)
    ax = caixa.plota_solido_com_faces(ax)

    util.show_figure(ax)
    
