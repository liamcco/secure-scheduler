from schedule_lib.task.task import Task

class IdleTask(Task):
    """
    IdleTask inherits from Task and has infinite deadline, period, and duration
    """
    def __init__(self):
        super().__init__(float("inf"), float("inf"), float("inf"))
        self.periority = 0
        self.id = 0
    
    def execute(self):
        #print("Idle task executing") 
        pass
    
    def reset(self):
        pass
    
    def time_step(self):
        pass