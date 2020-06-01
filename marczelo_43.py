import re

def spra(w,LE):
    wTabLength = len(w)
    index = 0
    nextIndex = 1
    i=0
    x=0
    flag = 0
    while i<wTabLength:                             #iterujemy po tyle razy ile argumentów
        wObjLength=(len(w[i]))
        mat = int(wObjLength / 2)
        if (mat + mat != wObjLength):               #jesli jest nieparzysta długość
            break
        oneBigWord=w[i]                             #cale slowo
        while x<wObjLength:                         #iterujemy tyle ile dlugosc slowa
            firstWord = oneBigWord[index:nextIndex] #pobieramy od poczatku czesci slowa
            print(firstWord)
            rp = re.compile(LE[i])
            if (rp.fullmatch(firstWord)):           #sprawdzamy czy pobrana czesc zawiera sie w LE
                print("mam: " + firstWord)
                firstWordLength = nextIndex
                print(firstWordLength)
                if(firstWordLength*2 == wObjLength):#dla tylko dwoch takich samych podslów znajdujacych sie w calym slowie
                    secondWord = oneBigWord[firstWordLength:wObjLength]
                    if(firstWord==secondWord):
                        print("Tak")
                        flag = 1
                        break
                secondWordLength = int((wObjLength-(2*firstWordLength))/2)
                secondWord = oneBigWord[firstWordLength:int(firstWordLength+secondWordLength)]
                thirdWordBegin = int((firstWordLength+secondWordLength))
                print(secondWord)
                thirdWord = oneBigWord[thirdWordBegin:int(thirdWordBegin+firstWordLength)]
                print(thirdWord)
                fourthWordBegin = thirdWordBegin+firstWordLength
                fourthWord = oneBigWord[fourthWordBegin:int(fourthWordBegin+secondWordLength)]
                print(fourthWord)
                if((firstWord==thirdWord) and (secondWord == fourthWord) and ((firstWord or thirdWord)!=(secondWord or fourthWord))):
                    if (rp.fullmatch(firstWord) and (not(rp.fullmatch(secondWord)))):
                        print("Tak")
                        flag = 1
                        x=0
                        nextIndex = 0
                        break
                    else:
                        break
                else:
                    break
            nextIndex+=1
            x+=1
        i+=1
        if (flag==0):
            print("Nie")
            x=0
            nextIndex=0

spra(['abaacaabcaabaacaabca','abbaaaabbaaa'],['ab(aa)*ca','ab(aa)*ba'])