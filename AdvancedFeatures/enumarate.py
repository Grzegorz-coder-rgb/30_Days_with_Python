lista = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

i = 0
for item in lista:
    # print(i, item)
    # i += 1
    pass

for i, item in enumerate(lista):
    # print(i, item)
    pass

# Task

names = ["Ala", "Ola", "Ela"]

for i, name in enumerate(names, start=1):
    print(i, name)


