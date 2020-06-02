
from minimalization.moore import MooreAlghorithm
from minimalization.loger import clearLog
from minimalization.helpers import methods

'''
_   stan akceptujący
'   stan końcowy
'''
def main():
    clearLog()
    automata = methods.fileToAutomata('zad58/kol2.txt')
    minimizedAutomata = MooreAlghorithm().minimize(automata)
    print(str(minimizedAutomata))

if __name__ == "__main__":
    main()