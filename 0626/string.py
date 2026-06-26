# print("Hello Python!")
# print('Hello \nP\nython!')
# print(""""Hello Python!""")
# a="Life is too short, you need Python"
# print(a[3])
# print(a[0:4])
# print(a[0:-1])
# print(a[-6:])
# print(a[-6:-1])
# a=3
# b='rotten'
# print("I eat %d apples and %s bananas." % (a, b))
# print("I eat {0} apples and {0} bananas".format(2))
# print("I eat {0}{0}{0} apples and {1} oranges.".format(a, b))
# print(f"{a} {b}")
# s="0x16D"
# print(s.isdigit())
# s="Life is too short"
# print(f"{s.startswith('Life')}")
# print(f"{s.startswith('is')}")
# print(f"{s.endswith('short')}")
# print(f"{s.endswith('Life')}")

# a=int(input("Enter a number: "))
# b=int(input("Enter second number: "))
# print(f"{a} + {b} = {a+b}")
# print(f"{a} - {b} = {a-b}")
# print(f"{a} * {b} = {a*b}")
# print(f"{a} / {b} = {a/b}")

# s=input("Enter five numbers separated by spaces: ")
# numbers = s.split()
# # Convert the string numbers to integers
# numbers = [int(x) for x in numbers]
# print(f"{sum(numbers)}, {min(numbers)}, {max(numbers)}, {sum(numbers)/len(numbers)}")
# fruits = input("Enter a list of fruits separated by spaces: ").split()
# print(f"{fruits[0]},  {fruits[-1]}")
      
# t1=tuple()
# t1=(1,)
# t1=(1)
# t3=([1,2,3],1)

import keyword


a={1:'HI', "ba": "banana"}
print(a[1], a["ba"])
stud1 = {'name': 'Honggildong', 'age': 20, 'major': 'Software Engineering'}
print(keyword.kwlist)

a=True, b=False
a=a and b

#선택문: if, match~case
#반복문: for, while (do~while 없음)
#무시문: break, continue, pass
#복귀문: return, yield
