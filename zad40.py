#! /usr/bin/env python
#encoding:UTF-8
#python 3.7.4

import re

def check(w,E):
    index = 0
    for word in w:
        regexp=re.compile(E[index].replace("+","|"))
        if regexp.fullmatch(word):
            print('Tak')
        else:
            print('Nie')
        index+=1

check(["abaabcca"],["ab((a(b)∗a)+(bc)+(ca))*ca"])

