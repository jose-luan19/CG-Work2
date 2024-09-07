import q3
import utils.utils as util

 
if __name__ == "__main__":
    
    cone, cano, tronco_cone, caixa, eye, at = q3.main()
    
    tronco_cone.transformacao_perspectiva(at=at, eye=eye)
    cano.transformacao_perspectiva(at=at, eye=eye)
    cone.transformacao_perspectiva(at=at, eye=eye)
    caixa.transformacao_perspectiva(at=at, eye=eye)
    
    # Criação da figura e do subplot 3D
    ax = util.create_figure2D()
    
    ax = cone.plota_solido2D_com_faces(ax)
    ax = tronco_cone.plota_solido2D_com_faces(ax, cor_arestas="g")
    ax = cano.plota_solido2D_com_faces(ax, cor_arestas="y")
    ax = caixa.plota_solido2D_com_faces(ax, cor_arestas="b")
    
    util.show_figure2D(ax)