import random

from schedule_lib.task.basictask import Task

class JitterTask(Task):
    def __init__(self, period: int, duration: int, deadline:int=None, jitter_amount:int=0) -> None:   
        self.max_jitter = int(period * jitter_amount)
        self.remaining_jitter = 0
        super().__init__(period, duration, deadline)

    def reset(self) -> None:
        super().reset()

        if self.max_jitter == 0:
            return
        
        self.remaining_jitter = random.randint(0, self.max_jitter)
    
    def time_step(self) -> bool:
        if self.remaining_jitter > 0:
            self.remaining_jitter -= 1
            
        return super().time_step()
    
    def is_ready(self) -> bool:
        return super().is_ready() and self.remaining_jitter == 0