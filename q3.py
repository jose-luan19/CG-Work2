import numpy as np
from cano import Cano
from tronco_cone import TroncoCone
import utils.utils as util
from cone import Cone


  
def main():
   # Cone
    radius = 2.0
    height = 2 * radius
    num_slices = 10
    ponto_inicial_cone = [9, 6, 0]

    cone = Cone(radius, height, num_slices, ponto_inicial_cone)
    cone.gerar_solido()
    # axes = cone.plota_solido_com_faces(axes)
    # cone.escalar_solido(1, 2, 3)
    # cone.rotacionar_solido(90, 0, 0)
    # axes = cone.plota_solido_com_faces(axes, cor_arestas="g")

    # Tronco de Cone
    radius_major = 3
    radius_minor = 1
    height = 2 * radius_major
    num_slices = 10
    ponto_inicial_tronco_cone = [-9, -3, 0]

    tronco_cone = TroncoCone(radius_major, radius_minor, height, num_slices, ponto_inicial_tronco_cone)
    tronco_cone.gerar_solido()
    # axes = tronco_cone.plota_solido_com_faces(axes)
    # tronco_cone.rotacionar_solido(-45, 0, 0)
    # tronco_cone.escalar_solido(2, 2, 1)
    # tronco_cone.transladar_solido(1, 1, -6)
    # tronco_cone.plota_solido_com_faces(axes, cor_arestas="g")

    # Cano
    P1 = [1, 1, 0]  
    P2 = [1, 1, 8]  
    T1 = [1, 2, 4]  
    T2 = [-3, -4, 9]
    raio_cano = 1 
    resolucao_curva = 9 
    num_camadas = 9 

    cano = Cano(raio_cano, P1, P2, T1, T2, resolucao_curva, num_camadas)
    cano.gerar_solido()
    # axes = cano.plota_solido_com_faces(axes)

    # Calculando os centros de massa das formas geométricas
    coneCenterMass = cone.get_centro_massa()
    tronco_coneCenterMass = tronco_cone.get_centro_massa()
    canoCenterMass = cano.get_centro_massa()

    # calculando a média de todos os centros para apontar a câmera
    at = util.calcular_at_medio(coneCenterMass, tronco_coneCenterMass, canoCenterMass)

    # Posição da câmera
    eye = np.array([-10, 10, 8])
    # -7,-1,6
    # 1,-4,2
    # -2, 3, -5

    # Calculando os vetores N, U e V da câmera
    U, V, N = util.calcular_vetores_aux(at, eye)

    cone.converter_para_camera( U, V, N, eye)
    cano.converter_para_camera( U, V, N, eye)
    tronco_cone.converter_para_camera( U, V, N, eye)
    

    return cone, cano, tronco_cone, at, eye

    

if __name__ == "__main__":
    
    # Criação da figura e do subplot 3D
    ax = util.create_figure()
    
    cone, cano, tronco_cone, at, eye = main()
    util.include_legend(ax, eye, at)
    
    ax = cano.plota_solido_com_faces(ax)
    ax = cone.plota_solido_com_faces(ax)
    ax = tronco_cone.plota_solido_com_faces(ax)

    util.show_figure(ax)
    
