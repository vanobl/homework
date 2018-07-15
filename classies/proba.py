from threading import Thread
import time


# def myclock():
#     while True:
#         print('Привет мир!')
#         time.sleep(5)


# def poki():
#     while True:
#         print('Опять мир?!')
#         time.sleep(1)


# t = Thread(target=myclock)
# t.start()

# t2 = Thread(target=poki)
# t2.start()

# print('Конец скрипта')

class PrivetMir(Thread):
    # def __init__(self):
    #     super.__init__()
    
    def run(self):
        while True:
            print('Привет мир!')
            time.sleep(3)


class PokaMir(Thread):
    def run(self):
        while True:
            print('Пока мир!')
            time.sleep(1.5)



t = PrivetMir()
t.start()

t2 = PokaMir()
t2.start()

print('Конец скрипта')