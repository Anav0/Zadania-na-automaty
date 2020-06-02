class Link:
    stateA = None
    stateB = None
    symbol: None

    def __init__(self, stateA,stateB,symbol):
        self.stateA = stateA
        self.stateB = stateB
        self.symbol = symbol

    def __str__(self):
        return '\nsymbol: {}\nstateA: {}\nstateB: {}\n'.format(self.symbol,str(self.stateA),str(self.stateB))

    def __repr__(self):
        return self.__str__()