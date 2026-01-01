numbers = []
for i in range(5):
    numbers.append(i * 2)

# print(numbers)

numbers = [i * 2 for i in range(10) if i % 2 == 0]
# print(numbers)


# While
a = []
for x in range(5):
    a.append(x + 1)

# list comprehension
b = [x + 1 for x in range(5)] #

print(a) # While
print(b) # List Comprehension

