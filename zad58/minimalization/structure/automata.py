from ..adhoc import AdHocObject
import copy
from .state import State
from .link import Link

class Automata:
    states: []
    links: []
    symbols: []

    def __init__(self,states,links,symbols,startingStateChar="_",acceptingStateChar="'"):
        self.states = states
        self.links = links
        self.symbols = symbols
        self.acceptingStateChar = acceptingStateChar
        self.startingStateChar = startingStateChar

    def combineLinks(self, statesToCombine):
        newLinks = []
        newName = ""
        isAccepting = False
        isStart = False
        correctedLinks = []
        for state in statesToCombine:
            # self.states.remove(state)
            newName+=state.name
            if isStart is False:
                isStart = state.isStartState
            if isAccepting is False:
                isAccepting = state.isAcceptingState
            for symbol in self.symbols:
                removed = self.removeStateLinksForSymbol(state,symbol)
                newLinks.append(removed)

        combinedState = State(newName,isStart,isAccepting)

        currected = {}
        for linkPair in newLinks:
            ins = linkPair.inLinks
            outs = linkPair.outLinks
            for link in ins:
                if '{}{}'.format(link.stateA.name,combinedState.name) not in currected:
                    linkToAdd = Link(link.stateA,combinedState,link.symbol)
                    correctedLinks.append(linkToAdd)
                    currected['{}{}'.format(link.stateA.name,combinedState.name)] = True
            for link in outs:
                if '{}{}'.format(combinedState.name,link.stateB.name) not in currected:
                    linkToAdd = Link(combinedState,link.stateB,link.symbol)
                    correctedLinks.append(linkToAdd)
                    currected['{}{}'.format(combinedState.name,link.stateB.name)] = True

        self.links += correctedLinks
        self.states.append(combinedState)
        return statesToCombine

    def getStatesThatEnter(self, stateIndex):
        output = []
        for link in self.links:
            entered = AdHocObject()
            stateBIndex = self.states.index(link.stateB)
            if stateBIndex is stateIndex:
                entered.symbolIndex = self.symbols.index(link.symbol)
                entered.stateIndex = self.states.index(link.stateA)
                output.append(entered)
        return output

    def getStateOutLinksForSymbol(self, state, inputSymbol):
        for link in self.links:
            if link.stateA.name is state.name and link.symbol is inputSymbol:
                return link

    def removeStateLinksForSymbol(self, state, inputSymbol):
        output = AdHocObject()
        output.inLinks = []
        output.outLinks = []
        toRemove = []
        for link in self.links:
            if link.stateA.name is state.name and link.symbol is inputSymbol:
                output.outLinks.append(copy.deepcopy(link))
                toRemove.append(link)
            if link.stateB.name is state.name and link.symbol is inputSymbol:
                output.inLinks.append(copy.deepcopy(link))
                toRemove.append(link)

        for link in toRemove:
            try:
                self.links.remove(link)
            except:
                pass
        return output;


    def getStateInLinksForSymbol(self, state, inputSymbol):
        for link in self.links:
            if link.stateB is state and link.symbol is inputSymbol:
                return link

    def getAcceptingAndRegularStates(self):
        accepting = []
        regular = []

        for state in self.states:
            if state.isAcceptingState:
                accepting.append(state)
            else:
                regular.append(state)
        obj = AdHocObject()
        obj.accepting = accepting
        obj.regular = regular
        return obj

    def getAcceptingStates(self):
        output = []
        for state in self.states:
            if state.isAcceptingState:
                output.append(state)
        return output

    def getStartingState(self):
        for state in self.states:
            if state.isStartState:
                return state
        return None

    def __str__(self):
        printOut = "\t"
        for symbol in self.symbols:
            printOut += symbol+"\t"
        printOut+="\n"
        for state in self.states:
            printOut+=state.name
            if state.isStartState:
                printOut+=self.startingStateChar
            if state.isAcceptingState:
                printOut+=self.acceptingStateChar
            printOut+="\t"
            for symbol in self.symbols:
                printOut += self.getStateOutLinksForSymbol(state,symbol).stateB.name+"\t"
            printOut+="\n"
        return printOut

    def __repr__(self):
        return self.__str__()