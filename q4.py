import q3
import utils.utils as util

 
if __name__ == "__main__":
    
    cone, cano, tronco_cone, at, eye = q3.main()
    
    cone.transformacao_perspectiva(at, eye)
    tronco_cone.transformacao_perspectiva(at, eye)
    cano.transformacao_perspectiva(at, eye)
    
    # Criação da figura e do subplot 3D
    ax = util.create_figure2D()
    
    ax = cone.plota_solido2D_com_faces(ax)
    ax = tronco_cone.plota_solido2D_com_faces(ax)
    ax = cano.plota_solido2D_com_faces(ax)
    
    util.show_figure2D(ax)