import copy
from ..loger import log
from ..structure.automata import Automata
from ..structure.state import State
from ..structure.link import Link
from ..adhoc import AdHocObject


def getCleanStateName(name, startingStateChar, acceptingStateChar):
    return name.rstrip(acceptingStateChar).rstrip(startingStateChar)

def getStateByName(states,name):
    for state in states:
        if state.name is name:
            return state
    return None

def fileToAutomata(filePath, startChar="_", acceptingChar="'"):
    index = 0
    symbols = []
    states = []
    links = []

    with open(filePath,'r') as file:
        for line in file:
            if not line.strip(): continue;
            if index is 0:
                symbols = line.strip().split("\t")
                index+=1
                continue
            splitedLine = line.strip().split("\t")
            stateAName = getCleanStateName(splitedLine[0],startChar,acceptingChar)
            isStartState = True if  '_' in splitedLine[0] else False
            isAcceptingState = True if  "'" in splitedLine[0] else False
            state = getStateByName(states,stateAName)
            if not state:
                state = State(stateAName,isStartState,isAcceptingState)
                states.append(state)
            else:
                state.isAcceptingState = isAcceptingState
                state.isStartState = isStartState
            for i, symbol in enumerate(symbols):
                stateBName = splitedLine[i+1]
                stateB = getStateByName(states,stateBName)
                if not stateB:
                    stateB = State(stateBName)
                    states.append(stateB)
                links.append(Link(state,stateB,symbol))

            index+=1
    return Automata(states,links,symbols,startChar,acceptingChar)
