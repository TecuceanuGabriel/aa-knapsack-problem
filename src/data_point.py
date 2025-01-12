class DataPoint:
    def __init__(self, n, time, accuracy):
        self.n = n
        self.time = time
        self.accuracy = accuracy

    def toJSON(self):
        return {
            "n": self.n,
            "time": self.time,
            "accuracy": self.accuracy
        }
