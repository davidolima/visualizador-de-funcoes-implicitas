import math

import pyglet as pg
from cArvore import ArvoreQuad
from random import randrange
from math import *

from funcAux import *

global resolucao, equacoes, it, a, zoom, modo_visualizacao

####### Configurações #######
jan_altura = 700
jan_largura = 700


modo_visualizacao = 1
resolucao = 7
zoom = 10
dom_arvore = ((-10, -10), (10, 10))
#############################


def recarregarVisualizacao(jan, res=resolucao, mv=modo_visualizacao, del_arvore=True):
    global a, resolucao, batch
    if del_arvore:
        del a

    batch = pg.graphics.Batch()
    a = ArvoreQuad(lim_inf_esq=dom_arvore[0], lim_sup_dir=dom_arvore[1])

    a.inserirCurva(equacoes[it][1], res, jan, zoom=zoom)
    desenharDominio(a, batch, jan, arvore, equacoes[it][1], modo=mv)


if __name__ == "__main__":

    equacoes = [("Cardióide",  lambda x, y: (x**2 + y**2 - 4)**3 - x**2 * y**3),
                ("Círculo",    lambda x, y: x**2 + y**2 - 49),
                ("Laço",       lambda x, y: x**7 - y**5 + x**2 * y**3 - (x*y)**2),
                ("Hipérbole",  lambda x, y: y**2-x**2 - 16),
                ("Curva",      lambda x, y: (x**4)*(1-x)**5+x+(y**2)*(1-y)+0.1),
                ("Curva 2",    lambda x, y: x*(1-x)*(1+x)+y*(1-y)*(1+y)+0.1),
                ("Exemplo 3",  lambda x, y: x**2 + y**2 + x*y - (x*y)**2 * 0.5 - 0.25),
                ("Exemplo 5",  lambda x, y: x**3 + y**2 - 6*x*y)]
    it = 0

    arvore = []
    a = ArvoreQuad(lim_inf_esq=dom_arvore[0], lim_sup_dir=dom_arvore[1], debug=False)

    jan = pg.window.Window(jan_largura, jan_altura)
    batch = pg.graphics.Batch()

    a.inserirCurva(equacoes[it][1], resolucao, jan)

    desenharDominio(a, batch, jan, arvore, equacoes[it][1], modo=modo_visualizacao)


    @jan.event
    def on_draw():
        jan.clear()
        batch.draw()
        jan.set_caption(f"Visualizador (f: {equacoes[it][0]} res: {str(resolucao)})")

    @jan.event
    def on_key_press(symbol, modifier):
        global resolucao, it, zoom, modo_visualizacao
        if symbol == pg.window.key.DOWN:  # Diminuir resolução/refinamento
            if resolucao > 0:
                resolucao -=1
                recarregarVisualizacao(jan, res=resolucao, mv=modo_visualizacao)
        elif symbol == pg.window.key.UP:  # Aumentar resolução/refinamento
            if resolucao < 10:
                resolucao += 1
                recarregarVisualizacao(jan, res=resolucao, mv=modo_visualizacao)
        elif symbol == pg.window.key.LEFT:  # Voltar equação
            it -= 1
            if it < 0:  # Rotacionar seleção
                it = len(equacoes) - 1
            recarregarVisualizacao(jan, res=resolucao, mv=modo_visualizacao)
        elif symbol == pg.window.key.RIGHT:  # Próxima equação
            it += 1
            if it > len(equacoes) - 1:  # Rotacionar seleção
                it = 0
            recarregarVisualizacao(jan, res=resolucao, mv=modo_visualizacao)

        elif symbol == pg.window.key._1:  # Modo de visualizaçao 1
            modo_visualizacao = 1
            recarregarVisualizacao(jan, res=resolucao, mv=modo_visualizacao, del_arvore=False)

        elif symbol == pg.window.key._2:  # Modo de visualização 2
            modo_visualizacao = 2
            recarregarVisualizacao(jan, res=resolucao, mv=modo_visualizacao, del_arvore=False)

        elif symbol == pg.window.key._3:  # Modo de visuzalização 3
            modo_visualizacao = 3
            recarregarVisualizacao(jan, res=resolucao, mv=modo_visualizacao , del_arvore=False)

    # Suporte para mouse reconhecer pontos
    @jan.event
    def on_mouse_release(x, y, button, modifiers):
        if button == pg.window.mouse.LEFT:
            print(normalizarCoordernadas((x, y), a.__lim_sup_dir__, jan, inverso=True))

    pg.app.run()

