import time

def normal():
    return [i for i in range(10_000_000)]

def generator():
    for i in range(10_000_000):
        yield i

# LISTA
start = time.perf_counter()
data = normal()
print("Lista pierwsza wartość:", data[0])
print("Czas:", time.perf_counter() - start)

# GENERATOR
start = time.perf_counter()
g = generator()
print("Generator pierwsza wartość:", next(g))
print("Czas:", time.perf_counter() - start)
