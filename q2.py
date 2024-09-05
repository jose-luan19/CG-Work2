from cano import Cano
from tronco_cone import TroncoCone
from cone import Cone
import utils.utils as util

def main():
      # Cone
      radius = 2.0
      height = 2 * radius
      num_slices = 10
      ponto_inicial_cone = [0, 0, 0]

      cone = Cone(radius, height, num_slices, ponto_inicial_cone)
      cone.gerar_solido()
      # axes = cone.plota_solido_com_faces(axes)
      cone.transladar_solido(8, 5, 1)
      cone.escalar_solido(.4, .3, 1.3)
      cone.rotacionar_solido(180, 0, 0)
      # axes = cone.plota_solido_com_faces(axes, cor_arestas="g")

      # Tronco de Cone
      radius_major = 2
      radius_minor = 1
      height = 2 * radius_major
      num_slices = 10
      ponto_inicial_tronco_cone = [0, 0, 0]

      tronco_cone = TroncoCone(radius_major, radius_minor, height, num_slices, ponto_inicial_tronco_cone)
      tronco_cone.gerar_solido()
      # axes = tronco_cone.plota_solido_com_faces(axes)
      tronco_cone.rotacionar_solido(90, 0, 0)
      tronco_cone.escalar_solido(.8, .5, .5)
      tronco_cone.transladar_solido(-5,5, -1)
      # tronco_cone.plota_solido_com_faces(axes, cor_arestas="g")

      # Cano
      P1 = [0, 0, 0]  
      P2 = [0, 1, 8]  
      T1 = [1, 2, 4]  
      T2 = [-3, -4, 9]
      raio_cano = 1 
      resolucao_curva = 9 
      num_camadas = 9 

      cano = Cano(raio_cano, P1, P2, T1, T2, resolucao_curva, num_camadas)
      cano.gerar_solido()
      # axes = cano.plota_solido_com_faces(axes)
      cano.rotacionar_solido(90, 0, 90)
      cano.transladar_solido(4, -1, 1)
      cano.escalar_solido(.7, .5, .6)
      # axes = cano.plota_solido_com_faces(axes, cor_arestas="g")
      
      return cone, tronco_cone, cano


if __name__ == "__main__":
      cone, tronco_cone, cano = main()
      axes = util.create_figure()
      axes = cone.plota_solido_com_faces(axes)
      tronco_cone.plota_solido_com_faces(axes)
      axes = cano.plota_solido_com_faces(axes)
      util.show_figure(axes)
 