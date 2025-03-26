from schedule_lib.task.basictask import Task

class IdleTask(Task):
    """
    IdleTask inherits from Task and has infinite deadline, period, and duration
    """
    def __init__(self) -> None:
        super().__init__(float("inf"), float("inf"), float("inf"))
        self.id = -1
    
    def execute(self) -> bool:
        return False
    
    def time_step(self) -> bool:
        return False
    
    def is_complete(self) -> bool:
        return False
    
    def is_new(self):
        return False
    
    def is_fresh(self):
        return False