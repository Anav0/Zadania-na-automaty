#! /usr/bin/env python
#encoding:UTF-8
#python 3.7.4

import re
import random

# podział słowa w na uvuv to de facto to samo co podział na w=ll gdzie l=uv

def getInterchangingParts(word,splitOn, debug=False):
    # u i v oddzielone np. spacją
    regex = r"(.+){}(.+){}\1{}\2".format(splitOn,splitOn,splitOn)
    if debug : print("Regex: {}".format(regex))
    chunkRegex = re.compile(regex)
    sub = chunkRegex.findall(word)
    if len(sub) is not 1:
        if debug : print("Nie znaleziono wzorca '{}' w słowie '{}'".format(regex,word))
        return None;
    try:
        splited = sub[0]
        u = splited[0]
        v = splited[1]
        return {'u':u,'v':v}
    except:
        if debug : print("Nie można podzielić słowa '{}' znakiem '{}'".format(word,splitOn))
    return None

def isFullyMatched(word,regexStr,debug=False):
        regex=re.compile(regexStr.replace("+","|"))
        if regex.fullmatch(word):
            if debug : print("Część: '{}' PASUJE dp wyrażenia regularnego: '{}'".format(word,regexStr))
            return True
        else:
             if debug : print("Część: '{}' NIE PASUJE dp wyrażenia regularnego: '{}'".format(word,regexStr))
             return False

def check(words,regexes,splitOn="",debug=False):
    index = 0
    anwsers = []
    for word in words:
        parts = getInterchangingParts(word,splitOn, debug)
        if not parts:
            continue
        u = parts.get('u')
        v = parts.get('v')
        if debug : print("Słowo: '{}' dzieli się na u: '{}' i v: '{}'".format(word,u,v))
        isUMatched = isFullyMatched(u,regexes[index],debug)
        isVMatched = isFullyMatched(v,regexes[index],debug)
        if isUMatched and not isVMatched:
            if debug : print("\n{}. jest dobre".format(index+1))
            anwsers.append(True)
        else:
            if debug : print("\n{}. jest niedobre".format(index+1))
            anwsers.append(False)
        index+=1
        print('\n')
        print('---------------------------------')
        print('\n')
    return anwsers

anwsers = check(["igor jacek igor jacek ","igorjacekigorjacek"],["igor jacek","igorjace"], debug=True)

