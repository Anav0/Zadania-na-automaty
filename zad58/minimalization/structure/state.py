class State:
    isStartState = False
    isAcceptingState = False
    name: None

    def __init__(self, name, isStartState = False, isAcceptingState = False):
        self.name = name
        self.isStartState = isStartState
        self.isAcceptingState = isAcceptingState

    def __str__(self):
        return '\nname: {}\nisStartState: {}\nisAcceptingState: {}\n'.format(self.name, self.isStartState,self.isAcceptingState)

    def __repr__(self):
        return self.__str__()