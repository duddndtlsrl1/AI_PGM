def fibo(n):
    if n <= 0:
        return 0
    a, b = 0, 1
    for _ in range(1, n):
        a, b = b, a + b
    return b

def fib(count=10):
    sequence = []
    a, b = 0, 1
    for _ in range(count):
        sequence.append(a)
        a, b = b, a + b
    return sequence

if __name__ == "__main__":
    for value in fib(10):
        print(value)

