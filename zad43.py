#! /usr/bin/env python
#encoding:UTF-8
#python 3.7.4

import re
import random
# podział słowa w na uvuv to de facto to samo co podział na w=ll gdzie l=uv

def getInterchangingParts(word,splitOn, debug=False):
    # u i v oddzielone np. spacją
    regex = r"(.+){}(.+){}\1{}\2".format(splitOn,splitOn,splitOn)
    if debug : print("\nRegex: {}".format(regex))
    chunkRegex = re.compile(regex)
    wordLen = len(word)
    sub = []
    for i in range(wordLen):
        if i is 0:
            continue
        putin1 = '{'+str(i)+'}'
        regex = r"(.+)((.+){})\1\2".format(putin1)
        result = re.compile(regex).findall(word)
        if result:
            sub.append(result[0])

    return sub

def isFullyMatched(word,regexStr,debug=False):
        regex=re.compile(regexStr.replace("+","|"))
        if regex.fullmatch(word):
            return True
        else:
             return False

def check(words,regexes,debug=False):
    index = 0
    anwsers = []
    for word in words:
        parts = getInterchangingParts(word, debug)
        if debug : print("Słowo: '{}' dzieli się na:\n".format(word))
        isCorrect = False
        if not parts:
            if debug : print('nic\n')
        for pair in parts:
            u = pair[0]
            v = pair[1]
            isUMatched = isFullyMatched(u,regexes[index],debug)
            isVMatched = isFullyMatched(v,regexes[index],debug)
            if isCorrect is False:
                isCorrect = True if isUMatched is True and isVMatched is False else False
                if isCorrect: anwsers.append(isCorrect)

            if isUMatched:
                if debug : print("u: '{}' pasuje do wzorca: {}".format(u,regexes[index]))
            else:
                if debug : print("u: '{}' nie pasuje do wzorca: {}".format(u,regexes[index]))

            if isVMatched:
                if debug : print("v: '{}' pasuje do wzorca: {}".format(v,regexes[index]))
            else:
                if debug : print("v: '{}' nie pasuje do wzorca: {}".format(v,regexes[index]))

            if debug : print('---------------------------------')

        if debug : print("TAK") if isCorrect else print("NIE")
        if debug : print('\n+++++++++++++++++++++++++++++++++\n')
        index+=1
    return anwsers

anwsers = check(["abccabcc","abbcabbc","abab"],["(a|b)*","(a|b)*","b*"], debug=True)

