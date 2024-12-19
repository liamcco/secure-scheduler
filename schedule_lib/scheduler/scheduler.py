class Scheduler:
    def __init__(self):
        self.processor = None
        self.compare = self.rate_monotonic_compare
    
    def rate_monotonic_compare(self, task1, task2):
        return task1.period < task2.period
    
