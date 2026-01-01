def user_info(**kwargs):
    print(kwargs)

user_info(name="Jan", age=20, city="Warszawa")

def suma(*args):
    return sum(args)

print(suma(1, 2, 3))
print(suma(5, 10, 20, 30))
