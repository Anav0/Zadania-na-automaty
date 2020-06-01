import re
import random

regex = re.compile("a*")
matches = regex.split("caacaaaaaacaa")
print(matches)