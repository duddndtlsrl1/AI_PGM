import math


class Shape:
    def __init__(self, name):
        self.name=name
    def area(self):
        raise NotImplementedError("추상클래스는 정의되어야만 합니다.")
    
class Circle(Shape):
    def __init__(self, radius):
        print("초기화 시작!")
        super().__init__("Circle")
        self.radius=radius
    
    def area(self):
        return math.pi*(self.radius**2)
        
    
class Rectangle(Shape):
    def __init__(self, width, height):
        print("초기화")
        super().__init__("Rectangle")
        self.width=width
        self.height=height
    def area(self):
        return self.width*self.height
    
shapeList=[Circle(5), Rectangle(4,6)]
for shape in shapeList:
    print(f"{shape.name} area: {shape.area()}")