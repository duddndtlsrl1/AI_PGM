def plus(a, b):
    return a + b

def minus(a, b):
    return a - b

def mul(a, b):
    return a * b

def div(a, b):
    if b == 0:
        raise ValueError("division by zero")
    return a / b

print("Hello, World!")

print(plus(1, 2))
print(minus(5, 3))
print(mul(4, 6))
print(div(8, 2))
