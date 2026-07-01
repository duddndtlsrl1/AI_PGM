number=int(input("Enter a number to calculate its factorial : "))
factorial=1

print(f"{number}!=", end="")
for i in range(number,0,-1):
    print(i, end="")
    if i!=1:
        print("x", end="")

for i in range(number,0,-1):
    factorial=factorial*i

print(f" = {factorial}")

import random

flag=True

while flag:
    x=random.randint(1,100)
    y=random.randint(1,100)
    answer=int(input(f"{x} + {y} = "))
    if answer==x+y:
        print("Correct answer")
    else:
        print("Wrong answer")
        flag=False
                

