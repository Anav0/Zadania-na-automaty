
class MinimalizationAlghorithm:
    def __init__(self):
        pass

    def minimize(self, automata):
        pass

class MooreAlghorithm(MinimalizationAlghorithm):
    def __init__(self):
        pass

    def minimize(self, automata):
        print(automata)

class Minimizer:
    def __init__(self, minimalizationAlghorithm):
        self.minimalizationAlghorithm = minimalizationAlghorithm

    def minimize(self, automata):
        self.minimalizationAlghorithm.minimize(automata)

class State:
    isStartState = False
    isFinishState = False
    name: None

    def __init__(self, name, isStartState = False, isFinishState = False):
        self.name = name
        self.isStartState = isStartState
        self.isFinishState = isFinishState

    def __str__(self):
        return '\nname: {}\nisStartState: {}\nisFinishState: {}\n'.format(self.name, self.isStartState,self.isFinishState)

    def __repr__(self):
        return self.__str__()

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

class Automata:
    states: []
    links: []
    symbols: []

    def __init__(self,states,links,symbols):
        self.states = states
        self.links = links
        self.symbols = symbols

    def getStateDestination(self, state, inputSymbol):
        for link in self.links:
            if link.stateA is state and link.symbol is inputSymbol:
                return link.stateB

    def __str__(self):
        printOut = "\t"
        for symbol in self.symbols:
            printOut += symbol+"\t"
        printOut+="\n"
        for state in self.states:
            printOut+=state.name+"\t"
            for symbol in self.symbols:
                printOut += self.getStateDestination(state,symbol).name+"\t"
            printOut+="\n"
        return printOut


    def __repr__(self):
        return self.__str__()

def getStateByName(states, name):
    for state in states:
        if state.name is name:
            return state
    return None

def getCleanStateName(name):
    return name.rstrip("'").rstrip('_')

def fileToAutomata(filePath):
    index = 0
    symbols = []
    states = []
    links = []
    with open(filePath,'r') as file:
        for line in file:
            if index is 0:
                symbols = line.strip().split("\t")
                index+=1
                continue
            splitedLine = line.strip().split("\t")
            stateAName = getCleanStateName(splitedLine[0])
            isStartState = True if  '_' in splitedLine[0] else False
            isAcceptingState = True if  "'" in splitedLine[0] else False
            state = getStateByName(states,stateAName)
            if not state:
                state = State(stateAName,isStartState,isAcceptingState)
                states.append(state)
            else:
                state.isFinishState = isAcceptingState
                state.isStartState = isStartState
            for i, symbol in enumerate(symbols):
                stateBName = splitedLine[i+1]
                stateB = getStateByName(states,stateBName)
                if not stateB:
                    stateB = State(stateBName)
                    states.append(stateB)
                links.append(Link(state,stateB,symbol))

            index+=1
    return Automata(states,links,symbols)


