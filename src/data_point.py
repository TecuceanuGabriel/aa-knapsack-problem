class DataPoint:
    def __init__(self, n, capacity, time, accuracy):
        self.n = n
        self.capacity = capacity
        self.time = time
        self.accuracy = accuracy

    def toJSON(self):
        return {
            "n": self.n,
            "capacity": self.capacity,
            "time": self.time,
            "accuracy": self.accuracy
        }
