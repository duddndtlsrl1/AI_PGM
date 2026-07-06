class Televison:
    serial_number=0 #클래스 변수
    def __init__(self, channel, volume,on):
        Televison.serial_number+=1
        self.serial_number=Televison.serial_number
        self.channel = channel
        self.volume = volume
        self.on = on
    def set_channel(self, channel):
        self.channel = channel

    def get_channel(self):
        return self.channel
    def __str__(self):
        return f"Televison(serial_number={self.serial_number},channel={self.channel}, volume={self.volume}, on={self.on})"
    
tv1 = Televison(1, 10, True)
tv2 = Televison(5, 20, False)
tv3 = Televison(3,30,True)

print(tv1.get_channel())  # Output: 1
print(tv3.__str__())