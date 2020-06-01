
from minimizer import Minimizer, MinimalizationAlghorithm, MooreAlghorithm, fileToAutomata
'''
_   stan akceptujący
'   stan końcowy
'''
def main():
    automata = fileToAutomata('C:/Projects/Zadania na automaty/zad58/automata.txt')
    minimizer = Minimizer(MooreAlghorithm())
    minimizer.minimize(automata)

if __name__ == "__main__":
    main()