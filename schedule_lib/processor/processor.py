from schedule_lib.processor.core import Core

class Processor:
    """Creates a processor object to execute tasks"""
    def __init__(self, num_cores):
        if num_cores < 1:
            raise ValueError("Processor must have at least one core")
        self.cores = [Core() for _ in range(num_cores)]

    def __str__(self):
        return f"Processor: {len(self.queue)} tasks in queue"

    def __repr__(self):
        return self.__str__()
    
    def execute(self):
        for core in self.cores:
            core.execute()