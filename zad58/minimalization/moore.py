from .loger import log
from .helpers.methods import getStateByName

class MinimalizationAlghorithm:
    def __init__(self):
        pass

    def minimize(self, automata):
        pass

class MooreAlghorithm(MinimalizationAlghorithm):

    turnsMatrix = [] # matrix where index equals to index of state in automata
    turns = []

    def initTurns(self, automata):
        self.turnsMatrix = ['0'] * len(automata.states)
        states = automata.getAcceptingAndRegularStates()
        firstTurn = []
        for i, state in enumerate(automata.states):
            self.turnsMatrix[i] = ['0']*len(automata.states)
            self.turnsMatrix[i][i] = "-"

        for regularState in states.regular:
            y = automata.states.index(regularState)
            for acceptingState in states.accepting:
                x = automata.states.index(acceptingState)
                self.turnsMatrix[x][y] = "1"
                self.turnsMatrix[y][x] = "1"
                firstTurn.append([x,y])
        self.turns.append(firstTurn)

    def combineArrays(self,arrayA,arrayB):
        output = []
        for i, itemA in enumerate(arrayA):
            for k, itemB in enumerate(arrayB):
                output.append(arrayA[i]+arrayB[k])
        return output

    def fillMatrixFromEntries(self, entries, numberOfSymbols,turnIndex, automata):
        output = {}
        start = 0
        end = numberOfSymbols

        for i, key in enumerate(entries):
            slice = {k: entries[k] for k in list(entries)[start:end]}
            values = list(slice.values())
            permutations = self.combineArrays(values[0],values[1])
            output[list(slice.keys())[0].split('/',1)[1]] = permutations
            for pair in permutations:
                digits = [x for x in str(pair)]
                x=automata.states.index(getStateByName(automata.states,digits[0]))
                y=automata.states.index(getStateByName(automata.states,digits[1]))
                if self.turnsMatrix[x][y] is '0':
                    self.turnsMatrix[x][y] = str(turnIndex+1)
                    self.turnsMatrix[y][x] = str(turnIndex+1)
                    self.turns.append([])
                    self.turns[turnIndex].append([x,y])
            end+=numberOfSymbols
            start+=numberOfSymbols
            if len(entries) < end:
                break
        return output

    def fillTurns(self,automata):
        for i,turn in enumerate(self.turns):
            log("Tura {}".format(i+1))
            for pos in turn:
                posNameA = automata.states[pos[0]].name
                posNameB = automata.states[pos[1]].name
                log('\n\nPair of states: {}{}\n'.format(posNameA,posNameB))
                whatEntersA = automata.getStatesThatEnter(pos[0])
                whatEntersB = automata.getStatesThatEnter(pos[1])
                entries = {}
                for symbol in automata.symbols:
                    entries['{}/{}'.format(posNameA,symbol)] = []
                    entries['{}/{}'.format(posNameB,symbol)] = []
                for entered in whatEntersA:
                    entries['{}/{}'.format(posNameA,automata.symbols[entered.symbolIndex])].append(automata.states[entered.stateIndex].name)
                    log('{} was entered by: {} via symbol: {}\n'.format(posNameA,automata.states[entered.stateIndex].name,automata.symbols[entered.symbolIndex]))
                for entered in whatEntersB:
                    entries['{}/{}'.format(posNameB,automata.symbols[entered.symbolIndex])].append(automata.states[entered.stateIndex].name)
                    log('{} was entered by: {} via symbol: {}\n'.format(posNameB,automata.states[entered.stateIndex].name,automata.symbols[entered.symbolIndex]))
                log(str(entries)+"\n")
                common = self.fillMatrixFromEntries(entries,len(automata.symbols),i+1,automata)
                log(str(common))
            log("\n\n")
            log(self.getAutomataPrint(automata))
            log("\n")

    def getAutomataPrint(self,automata):
        printOut = "   "
        for state in automata.states:
            printOut += state.name+"  "
        printOut+="\n"
        for i, row in enumerate(self.turnsMatrix):
            splitedRow = "  ".join(row)
            printOut+=automata.states[i].name+"  "+splitedRow+"\n"
        return printOut

    def getStatesAfterMinimalization(self,automata):
        positionsOfZeros = []
        visitedPlace = {}
        toRemove = []
        for i, row in enumerate(self.turnsMatrix):
            stateC = None
            for k, element in enumerate(row):
                if element is '0':
                    if '{}{}'.format(i,k) in visitedPlace or '{}{}'.format(k,i) in visitedPlace :
                        continue
                    else:
                         visitedPlace['{}{}'.format(i,k)] = True
                    stateA = automata.states[i]
                    stateB = automata.states[k]
                    statesToRemove = automata.combineLinks([stateA,stateB])
                    toRemove+=statesToRemove
                    positionsOfZeros.append([stateA.name,stateB.name])

        for state in toRemove:
            try:
                automata.states.remove(state)
            except:
                pass
        return automata

    def minimize(self, automata):
        self.initTurns(automata)
        log(self.getAutomataPrint(automata)+"\n")
        self.fillTurns(automata)
        minimalizedAutomata = self.getStatesAfterMinimalization(automata)
        log('\nMinimalized automata:\n\n')
        log(str(minimalizedAutomata))
        print("\nW pliku log.txt znajduje się opis krok po kroku co robił algorytm\n")
        return minimalizedAutomata