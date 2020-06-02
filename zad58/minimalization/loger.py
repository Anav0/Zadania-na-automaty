def log(text):
    with open('zad58/log.txt', 'a') as file:
        file.write(text)

def clearLog():
    with open('zad58/log.txt', 'w') as file:
        file.write("")