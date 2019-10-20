class Position:
    def __init__(self, x=0.0, y=0.0, z=0.0, time=0.0):
        self.x = x
        self.y = y
        self.z = z
        self.time = time
    
    def __str__(self):
        string = str(self.x) + " " + str(self.y) + " " + \
        str(self.z) + " " + str(self.time)
        return string
