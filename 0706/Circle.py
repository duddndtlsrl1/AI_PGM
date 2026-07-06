import math
class Circle:
    def __init__(self,radius):
        self.radius=radius
    def area(self):
        return math.pi*(self.radius**2)
    def circumference(self):
        return 2*math.pi*self.radius
    def __eq__(self, value):
        return self.radius==value.radius

c1=Circle(5)
c2=Circle(7)
#print("Circle radius: ",c1.radius)
#print("Circle area: ",c1.area())
#print("Circle circumference: ",c1.circumference())

if c1.__eq__(c2):
    print("반지름이 서로 다른 원입니다")


