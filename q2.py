from caixa import Caixa
from cano import Cano
from tronco_cone import TroncoCone
from cone import Cone
import utils.utils as util

def main():
      # Cone
      radius = 2.0
      height = 2 * radius
      num_slices = 10

      cone = Cone(radius, height, num_slices)
      cone.gerar_solido()
      # axes = cone.plota_solido_com_faces(axes)
      cone.escalar_solido(.4, .3, 1.3)
      cone.rotacionar_solido(180, 0, 0)
      cone.transladar_solido(9, 1, 6)
      # axes = cone.plota_solido_com_faces(axes, cor_arestas="g")

      # Cano
      P1 = [0, 0, 0]  
      P2 = [0, 1, 6]  
      T1 = [1, 2, 4]  
      T2 = [-3, -4, 9]
      raio_cano = 1 
      resolucao_curva = 9 
      num_camadas = 20 

      cano = Cano(raio_cano, P1, P2, T1, T2, resolucao_curva, num_camadas)
      cano.gerar_solido()
      # axes = cano.plota_solido_com_faces(axes)
      cano.rotacionar_solido(0, 0, 0)
      cano.escalar_solido(.7, .5, .6)
      cano.transladar_solido(8, 2.5, 1)
      # axes = cano.plota_solido_com_faces(axes, cor_arestas="g")
      
      # Tronco de Cone
      radius_major = 2
      radius_minor = 1
      height = 2 * radius_major
      num_slices = 10

      tronco_cone = TroncoCone(radius_major, radius_minor, height, num_slices)
      tronco_cone.gerar_solido()
      # axes = tronco_cone.plota_solido_com_faces(axes)
      tronco_cone.rotacionar_solido(90, 0, 0)
      tronco_cone.escalar_solido(.8, .5, .5)
      tronco_cone.transladar_solido(1.7,9, 1)
      # tronco_cone.plota_solido_com_faces(axes, cor_arestas="g")

      
      
      lado_base_externa = 2.0  # Define o lado da base externa
      altura_externa = 3.0  # Define a altura da caixa externa

      caixa = Caixa(lado_base_externa, altura_externa)
      caixa.gerar_solido()
      caixa.rotacionar_solido(60, 0, 45)
      caixa.escalar_solido(1.3, .5, .6)
      caixa.transladar_solido(8, 9, 1)
      
      return cone, tronco_cone, cano, caixa


if __name__ == "__main__":
      cone, tronco_cone, cano, caixa = main()
      axes = util.create_figure()
      axes = cone.plota_solido_com_faces(axes)
      axes = tronco_cone.plota_solido_com_faces(axes)
      axes = cano.plota_solido_com_faces(axes)
      axes = caixa.plota_solido_com_faces(axes)
      util.show_figure(axes)
 