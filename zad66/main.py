import copy
import sys
from loger import Loger
import argparse

acceptingStateChar = "'"
startStateChar = "_"
noTransitionChar = "-"

class MinimalistDFA:
    startingState = 0
    finalStates = []
    transitionTable = []
    entriesTable = []

    def __init__(self, startingState, finalStates, transitionTable):
        self.startingState = startingState
        self.finalStates = finalStates
        self.transitionTable = transitionTable

    def prepereEntriesTable(self):
        N = len(self.transitionTable[0])
        M = len(self.transitionTable)
        self.entriesTable = res = [ [ None for o in range(N) ] for j in range(M) ]
        for i, transition in enumerate(self.transitionTable):
            for k, enteredState in enumerate(transition):
                if enteredState is not noTransitionChar:
                    entries = self.entriesTable[int(enteredState)][k]
                    if entries:
                        shouldAdd = True
                        for existing in entries:
                            if existing is i:
                                shouldAdd = False
                        if shouldAdd:
                                self.entriesTable[int(enteredState)][k].append(i)
                    else:
                        self.entriesTable[int(enteredState)][k] = [i]
        return self.entriesTable

class HopcroftAlghorithm:

    def __init__(self,logPath):
        self.loger = Loger(logPath)
        self.loger.clear()

    def minimize(self, automata):
        L = []
        P = [automata.finalStates]
        entries = automata.prepereEntriesTable()

        # initialize P and L
        regularStates = []
        for i, state in enumerate(automata.transitionTable):
            if i not in automata.finalStates:
                regularStates.append(i)
        P.append(regularStates)

        # put smaller list on L
        toPutOnListL = []
        if len(P) < len(automata.finalStates):
            toPutOnListL = ''.join(str(x) for x in P)
        else:
            toPutOnListL = ''.join(str(x) for x in automata.finalStates)

        for i,d in enumerate(automata.transitionTable[0]):
            L.append('{}{}'.format(toPutOnListL,i))

        # as long as there are elements in L
        loopCounter = 1;
        while L:
            self.loger.log('\n======== {}. loop ========\n'.format(loopCounter))
            self.loger.log('P: {}'.format(P))
            self.loger.log('L: {}'.format(L))
            itemFromL = L.pop(0)
            states = list(itemFromL)
            symbol = states.pop()
            whatEnteres = []
            for state in states:
                potentialEntry = automata.entriesTable[int(state)][int(symbol)]
                if not potentialEntry:
                    continue
                else:
                    whatEnteres += potentialEntry

            # łamanie
            self.loger.log('State: {}\nSymbol: {}'.format(state,symbol))
            self.loger.log('What to break i.e what enters {} by {}? {}'.format(state,symbol,whatEnteres))
            tmpP = copy.deepcopy(P)
            self.loger.log('\nLooking for subset \'B\' of P to break apart')
            for i, B in enumerate(P):
                self.loger.log('B: {}'.format(B))
                splited = splitOff(B, whatEnteres)
                self.loger.log('Broken B: {}'.format(splited))
                if len(splited) > 1:
                    tmpP.pop(i)
                    for split in splited:
                        tmpP.append(split)
                    self.loger.log('P after breaking up: {}'.format(tmpP))
                    # Uzupełnienie list L
                    self.loger.log("\nFilling L")
                    flattenB = ''.join(str(x) for x in B)
                    elementToReplace = None

                    wasFoundInL = False
                    self.loger.log('L before filling: {}'.format(L))
                    for g, element in enumerate(L):
                        states = list(element)
                        symbol = states.pop()
                        joinedStates = "".join(states)

                        if flattenB in joinedStates:
                            replaced = L.pop(g)
                            for split in splited:
                                joinedSplit = ''.join(str(x) for x in split)
                                self.loger.log('Replaced {} with {} in L'.format(replaced,joinedSplit+symbol))
                                L.insert(g,joinedSplit+symbol)
                            wasFoundInL = True

                    if not wasFoundInL:
                        splited.sort(reverse=True)
                        smallerBreak = splited[0]
                        smallerBreak = ''.join(str(x) for x in smallerBreak)
                        for i, transition in enumerate(automata.transitionTable[0]):
                            L.append(smallerBreak+str(i))
                            self.loger.log('Added {} to L'.format(smallerBreak+str(i)))
                    self.loger.log('L after filling: {}'.format(L))

            P = tmpP
            loopCounter+=1
        self.loger.log("\n")
        self.loger.log('Final P: {}'.format(P))
        automataPrint = self.getAutomataPrintOut(P,automata)
        return automataPrint;

    def getAutomataPrintOut(self,P,automata):
        printOut = "\t"
        for i, symbol in enumerate(automata.transitionTable[0]):
            printOut+=str(i)+"\t"
        printOut+="\n"
        for subset in P:
            addStartStateMarker = False
            addFinishStateMarker = False
            for state in subset:
                printOut+=str(state)
                if state in automata.finalStates:
                    addFinishStateMarker = True
                if state is automata.startingState:
                    addStartStateMarker = True

            printOut+=acceptingStateChar if addFinishStateMarker else ""
            printOut+=startStateChar if addStartStateMarker else ""

            printOut+="\t"
            printOut+='\t'.join(str(x) for x in automata.transitionTable[subset[0]]);
            printOut+="\n"
        self.loger.log("\nMinimized automata transition table:\n")
        self.loger.log(printOut)
        return printOut

def minimalistDFAfromFile(filePath):
    startingState = 0
    finalStates = []
    transitionTable = []
    with open(filePath,'r') as file:
        index = 0
        for line in file:
            if index is 0:
                index+=1
                continue
            splitedLine = line.strip().split("\t")
            if startStateChar in splitedLine[0]:
                startingState = index-1
            if acceptingStateChar in splitedLine[0]:
                finalStates.append(index-1)
            transition = []
            for i, char in enumerate(splitedLine):
                if i is 0: continue
                transition.append(splitedLine[i])
            transitionTable.append(transition)
            index+=1

        return MinimalistDFA(startingState,finalStates,transitionTable)

def splitOff(array,toSplit):
    a = []
    b = []
    for value in array:
        if value in toSplit:
            b.append(value)
        else:
            a.append(value)
    if b and a:
        return [a,b]
    else:
        return [a]

def main():
    parser = argparse.ArgumentParser(description='Minimizes automata from file using Hopcroft alghorithm')
    parser.add_argument('filePath', metavar='f', help='path to transition table of DFA')
    parser.add_argument('--logPath', metavar='l', help='path to store log file')
    args = parser.parse_args()

    # W pliku log.txt jest szczegółowy opis kroków jakie podejmuje algorytm
    logPath = sys.argv[0]
    fileName = sys.argv[1]
    if logPath:
        logPath = 'zad66/log.txt'
    automata = minimalistDFAfromFile(fileName)
    alghorithm = HopcroftAlghorithm(logPath)
    print(alghorithm.minimize(automata))

if __name__ == "__main__":
    main()

