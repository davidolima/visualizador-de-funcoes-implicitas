import pyglet as pg
from cArvore import ArvoreQuad

cores = {'vermelho': (255, 0, 0, 255),
         'verde': (0, 255, 0, 255),
         'azul': (0, 0, 255, 255),
         'ciano': (0, 255, 255, 255),
         'magenta': (255,255, 0, 255),
         'preto': (0, 0, 0, 255),
         'branco': (255, 255, 255, 255),
         }

cores_it = [(255,   0,   0, 255),
            (  0, 255,   0, 255),
            (  0,   0, 255, 255),
            (  0, 255, 255, 255),
            (255, 255,   0, 255),
            (255,   0, 255, 255),
            (  0, 255, 255, 255),]

def normalizarCoordernadas(coords, dom, jan, zoom=1,inverso=False, debug=False):
    if not dom[0] or not dom[1]:
        dom = (10, 10)

    if not inverso:
        if coords[0] != 0:
            x = jan.get_size()[0]/2+(coords[0]*(jan.get_size()[0]*zoom/dom[0])/2)
        else:
            x = jan.get_size()[0]/2

        if coords[1] != 0:
            y = jan.get_size()[1]/2+(coords[1]*(jan.get_size()[1]*zoom/dom[1])/2)
        else:
            y = jan.get_size()[1]/2

    else:
        if coords[0] != jan.get_size()[0]:
            x = (coords[0]/(jan.get_size()[0]/dom[0])*2)-dom[0]
        else:
            x = 0

        if coords[1] != jan.get_size()[0]:
            y = (coords[0]/(jan.get_size()[0]/dom[0])*2)-dom[0]
        else:
            y = 0

    print(coords, "->", (x, y), '|', dom, '|', jan.get_size()) if debug else False
    return (x, y)

def inserirCurva(quad: ArvoreQuad, f, m_erro, resolucao, jan, passo=1, zoom=1):
    y = -jan.get_size()[1]//2
    while y <= jan.get_size()[1]//2:
        x = -jan.get_size()[0]//2
        while x <= jan.get_size()[0]//2:
            p = normalizarCoordernadas((x, y), jan, zoom=zoom, inverso=False)
            if (0, 0) <= p < jan.get_size():
                quad.refinar(p, resolucao) if abs(f(x, y)) < m_erro else None
            x += passo
        y += passo

def desenharDominio(quad: ArvoreQuad, batch: pg.graphics.Batch, jan, arvore: list, f, zoom=1, color=None, modo=1, com_pontos=False):
    if quad is None:
        return

    t_borda = 1
    t_ponto = 3

    lsd = normalizarCoordernadas(quad.__lim_sup_dir__,                   (10,10), jan, zoom=zoom)
    lie = normalizarCoordernadas(quad.__lim_inf_esq__,                   (10,10), jan, zoom=zoom)
    lse = normalizarCoordernadas((quad.v_sup_esq[0], quad.v_sup_esq[1]), (10,10), jan, zoom=zoom)
    lid = normalizarCoordernadas((quad.v_inf_dir[0], quad.v_inf_dir[1]), (10,10), jan, zoom=zoom)

    if modo == 1:
        cor = cores['branco']
        if quad.ponto == 1:
            cor = cores['preto']

        cor_borda = quad.getGeracao() % len(cores_it)

        outline = pg.shapes.Rectangle(x=lie[0],
                                      y=lie[1],
                                      width=lsd[0],
                                      height=lsd[1],
                                      color=cores_it[cor_borda],
                                      batch=batch)

        quadrado = pg.shapes.Rectangle(x=lie[0]+t_borda,
                                       y=lie[1]+t_borda,
                                       width=lsd[0]-t_borda,
                                       height=lsd[1]-t_borda,
                                       # Em branco aqueles que não apresentam ponto
                                       color=cor,
                                       batch=batch)
        arvore += [outline, quadrado]
        if not quad.isFolha():
            for i in quad.getFilhos():
                desenharDominio(i, batch, jan, arvore, f, modo=modo)


    elif modo == 2:
        assert f, "É necessário o fornecimento de uma função para desenhar a curva neste modo."

        quadrado = pg.shapes.Rectangle(x=lie[0],
                                       y=lie[1],
                                       width=lsd[0],
                                       height=lsd[1],
                                       # Em branco aqueles que não apresentam ponto
                                       color=cores['branco'] if quad.ponto == 1 else cores['preto'],
                                       batch=batch)
        arvore.append(quadrado)
        if not quad.isFolha():
            for i in quad.getFilhos():
                desenharDominio(i, batch, jan, arvore, f, modo=modo)

    elif modo == 3:
        if quad.ponto == 0:
            cor = cores['azul']
        elif abs(quad.ponto) == 1:
            cor = cores['vermelho']

        quadrado = pg.shapes.Rectangle(x=lie[0],
                                       y=lie[1],
                                       width=lsd[0],
                                       height=lsd[1],
                                       # Em branco aqueles que não apresentam ponto
                                       color=cor,
                                       batch=batch)
        arvore += [quadrado]
        if not quad.isFolha():
            for i in quad.getFilhos():
                desenharDominio(i, batch, jan, arvore, f, modo=modo)



    # if quad.ponto:
    #     ponto = pg.shapes.Circle(quad.ponto[0], quad.ponto[1], t_ponto, color=(0, 0, 0), batch=batch)
    #     arvore.append(ponto)
    if com_pontos:
        sup_esq = pg.shapes.Circle(lse[0], lse[1], t_ponto, color=cores['ciano'], batch=batch)
        sup_dir = pg.shapes.Circle(lsd[0], lsd[1], t_ponto, color=cores['ciano'], batch=batch)
        inf_esq = pg.shapes.Circle(lie[0], lie[1], t_ponto, color=cores['ciano'], batch=batch)
        inf_dir = pg.shapes.Circle(lid[0], lid[1], t_ponto, color=cores['ciano'], batch=batch)
        arvore += [sup_esq, sup_dir, inf_dir, inf_esq]

