class Television:
    def __int__(self, channel, volume, on):
        self.channel=channel
        self.volume=volume
        self.on=on
    def show(self):
        print(f"Channel: {self.channel}, Volume:{self.volume}, On:{self.on}")
    
    def __str__(self):
        return f"Channel: {self.channel}, Volume:{self.volume}, On:{self.on}"
    
    def set_channel(self, channel):
        self.channel=channel
    
    def get_channel(self):
        return self.channel
    