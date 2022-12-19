class ArvoreQuad:
    """
    Implementação da Árvore Quaternária
    """

    def __init__(self, lim_sup_dir,  lim_inf_esq=(0, 0), geracao=0, f=None, debug=False):
        self.debug = debug

        # Vertices
        self.__lim_inf_esq__ = lim_inf_esq
        self.__lim_sup_dir__ = lim_sup_dir
        self.v_sup_esq = (self.__lim_inf_esq__[0], self.__lim_sup_dir__[1])
        self.v_inf_dir = (self.__lim_sup_dir__[0], self.__lim_inf_esq__[1])

        self.__folha__ = True
        self.__geracao__ = geracao
        self.ponto = -2  # -1 -> Interior, 0 -> Exterior, 1 -> Frontal

        self.supEsq = None
        self.supDir = None
        self.infEsq = None
        self.infDir = None

        if f:
            self.contemFunc(f)

    def __repr__(self):
        return f"({self.__lim_inf_esq__}, {self.__lim_sup_dir__})"

    def __del__(self):
        if not self.__folha__:
            del self.supEsq
            del self.supDir
            del self.infEsq
            del self.infDir
        del self

    def getGeracao(self):
        return self.__geracao__

    def contemFunc(self, f):
        # Checar o sinal de seus vértices
        self.v_sup_dir_sin = f(self.__lim_sup_dir__[0], self.__lim_sup_dir__[1]) > 0
        self.v_sup_esq_sin = f(self.v_sup_esq[0], self.v_sup_esq[1]) > 0
        self.v_inf_dir_sin = f(self.v_inf_dir[0], self.v_inf_dir[1]) > 0
        self.v_inf_esq_sin = f(self.__lim_inf_esq__[0], self.__lim_inf_esq__[1]) > 0

        if self.v_sup_esq_sin == self.v_inf_esq_sin == self.v_sup_dir_sin == self.v_inf_dir_sin:
            if self.v_sup_esq_sin: # Todos positivos
                self.ponto = 0
                return 0
            self.ponto = -1
            return -1 # Todos negativos
        else:
            self.ponto = 1
            return 1

    def inserirCurva(self, f, resolucao, jan, zoom=1, res_atual=0):
        self.contemFunc(f)
        if self.__geracao__ <= 1: # Para funções que não são encontradas nas primeiras divisões
            if self.ponto == 0 or self.ponto == -1 and self.__folha__ and self.__geracao__ < resolucao:
                self.__subDividir__(f, resolucao, jan)
                for i in self.getFilhos():
                    if i.contemFunc(f):
                        self.__inserirCurva__(f, resolucao, jan)
                        break
                return


            if self.ponto == 0 and self.__folha__ and self.__geracao__ < resolucao:
                self.__subDividir__(f, resolucao, jan)
                for i in self.getFilhos():
                    if i.contemFunc(f):
                        self.__inserirCurva__(f, resolucao, jan)
                        break
                return
        if self.ponto >= 1:
            if self.__folha__ and self.__geracao__ < resolucao:
                self.__subDividir__(f, resolucao, jan)
                self.__inserirCurva__(f, resolucao, jan)

                return

            if not self.__folha__ and self.ponto == 1:
                self.__inserirCurva__(f, resolucao, jan, zoom=zoom, res_atual=res_atual)

    def __inserirCurva__(self, f, resolucao, jan, zoom=1, res_atual=0):
        assert not self.isFolha(), "Erro: Tentativa de olhar filhos de uma folha."
        for filho in self.getFilhos():
            filho.inserirCurva(f, resolucao, jan, zoom=1, res_atual=res_atual)

    def getFilhos(self) -> tuple:
        return (self.infEsq, self.infDir, self.supEsq, self.supDir)

    def isFolha(self):
        return self.__folha__

    def __subDividir__(self, f, resolucao, jan):
        assert self.isFolha(), "Erro: Tentativa de subdividir uma árvore já dividida."
        # Sub divisão superior esquerda
        self.infDir = ArvoreQuad(lim_inf_esq=(self.__lim_inf_esq__[0]/2+self.__lim_sup_dir__[0] / 2, self.__lim_inf_esq__[1]),
                                 lim_sup_dir=(self.__lim_sup_dir__[0], self.__lim_inf_esq__[1]/2 + self.__lim_sup_dir__[1]/2),
                                 geracao=self.__geracao__+1,
                                 debug=self.debug)
        # Sub divisão superior direita
        self.infEsq = ArvoreQuad(lim_inf_esq=(self.__lim_inf_esq__[0], self.__lim_inf_esq__[1]),
                                 lim_sup_dir=(self.__lim_inf_esq__[0]/2+self.__lim_sup_dir__[0] / 2, self.__lim_inf_esq__[1]/2 + self.__lim_sup_dir__[1]/2),
                                 geracao=self.__geracao__+1,
                                 debug=self.debug)
        # Sub divisão inferior esquerda
        self.supEsq = ArvoreQuad(lim_inf_esq=(self.__lim_inf_esq__[0], self.__lim_inf_esq__[1]/2 + self.__lim_sup_dir__[1] / 2),
                                 lim_sup_dir=(self.__lim_inf_esq__[0]/2+self.__lim_sup_dir__[0] / 2, self.__lim_sup_dir__[1]),
                                 geracao=self.__geracao__+1,
                                 debug=self.debug)
        # Sub divisão inferior direita
        self.supDir = ArvoreQuad(lim_inf_esq=(self.__lim_inf_esq__[0]/2+self.__lim_sup_dir__[0] / 2, self.__lim_inf_esq__[1]/2 + self.__lim_sup_dir__[1] / 2),
                                 lim_sup_dir=(self.__lim_sup_dir__[0],self.__lim_sup_dir__[1]),
                                 geracao=self.__geracao__+1,
                                 debug=self.debug)

        # Não é mais folha
        self.__folha__ = False

        # if self.ponto:
            # self.__inserirCurva__(f, resolucao, jan)

        print(f"Subdiv: {self} -> (ie:{self.infEsq},id:{self.infDir},se:{self.supEsq},sd:{self.supDir})") if self.debug else False
