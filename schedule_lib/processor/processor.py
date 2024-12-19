from schedule_lib.processor.core import Core

class Processor:
    """Creates a processor object to execute tasks"""
    def __init__(self):
        self.cores = [Core()]

    def __str__(self):
        return f"Processor: {len(self.queue)} tasks in queue"

    def __repr__(self):
        return self.__str__()
    
    def execute(self, task):
        self.cores[task.core_id].execute(task)