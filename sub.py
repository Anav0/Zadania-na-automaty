import re
import random

result = re.sub("Igor","Krzysio","Igor Jacek Tomek Paweł Zbysio Czesio")
print(result) # Krzysio Jacek Tomek Paweł Zbysio Czesio

result = re.sub(r'(\D)\1+', r'\1', 'aaaabbbccccddddeeeefffggghhh')
print(result)
