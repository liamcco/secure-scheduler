import random

from schedule_lib.task.basictask import Task

class JitterTask(Task):
    def __init__(self, period: int, duration: int, deadline:int=None, jitter_amount:float=0) -> None:   
        self.max_jitter = int(period * jitter_amount)
        self.remaining_jitter = 0
        super().__init__(period, duration, deadline)

    def reset(self) -> None:
        super().reset()

        if self.max_jitter == 0:
            return
        
        self.remaining_jitter = random.randint(0, self.max_jitter)
    
    def time_step(self) -> bool:
        did_reset = super().time_step()
        task_did_arrive = did_reset and self.remaining_jitter == 0

        if self.remaining_jitter > 0:
            self.remaining_jitter -= 1
            task_did_arrive = self.remaining_jitter == 0
            
        return task_did_arrive
    
    def is_ready(self) -> bool:
        return super().is_ready() and self.remaining_jitter == 0