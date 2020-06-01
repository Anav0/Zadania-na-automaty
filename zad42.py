#! /usr/bin/env python
#encoding:UTF-8
#python 3.7.4
import re

# Zmienne typu float w cpp są to liczby 32bitowe z zakresu od 1.175494351E-38 do 3.402823466E+38
# Przykłady akceptowalnych formatów zmiennej float:
# 1 1.1 .1 1. 1.1e10 1.1e-10 1.1e+10
def isContainingOnlyCppFloats(filePath):
    cppFloatRegex = re.compile(r"[+-]?\d*\.?\d*([Ee][+-]?\d+)?")
    with open(filePath) as f:
        for line in f:
            elements = line.strip("\n").split(" ")
            for element in elements:
                matchingResult = cppFloatRegex.fullmatch(element)
                if not matchingResult:
                    return element + " is not a cpp float"
    f.close()
    return "file: " + filePath + " contains only cpp floats"


print(isContainingOnlyCppFloats("floats.txt"))