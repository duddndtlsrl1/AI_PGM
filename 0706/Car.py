class Car:
    def __init__(self, maker, color, model, price):
        self.maker = maker
        self.color = color
        self.model = model
        self.price=price

    def set_maker(self, maker):
        self.maker = maker
    def get_maker(self):
        return self.maker
    def __str__(self):
        return f"Car(maker={self.maker}, color={self.color}, model={self.model}, price={self.price})"

class ElectricCar(Car):
    def __init__(self, maker, color, model, price, battery_capacity):
        super().__init__(maker, color, model, price)
        self.battery_capacity=battery_capacity
    def set_battery_capacity(self, battery_capacity):
        self.battery_capacity=battery_capacity
    def get_battery_capacity(self):
        return self.battery_capacity
    def __str__(self):
        return f"ElectricCar(maker={self.maker}, color={self.color}, model={self.model}, price={self.price}, battery_capacity={self.battery_capacity})"\


myCar=ElectricCar("Tesla", "Model S", "Red", 799999, 100)
print(myCar)