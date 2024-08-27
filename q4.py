import q3
import utils.utils as util

 
if __name__ == "__main__":
    
    cubo, cone, cilindro, tronco, esfera, _ = q3.main()
    
    cubo.transformacao_perspectiva()
    cone.transformacao_perspectiva()
    cilindro.transformacao_perspectiva()
    tronco.transformacao_perspectiva()
    esfera.transformacao_perspectiva()
    
    # Criação da figura e do subplot 3D
    ax = util.create_figure2D()
    
    ax = cubo.plota_solido2D(ax, cor="g")
    ax = cone.plota_solido2D(ax, cor="k")
    ax = cilindro.plota_solido2D(ax, cor="b")
    ax = tronco.plota_solido2D(ax, cor="c")
    ax = esfera.plota_solido2D(ax, cor="m")
    
    util.show_figure2D(ax)