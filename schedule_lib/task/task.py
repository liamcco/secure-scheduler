import math
import random

class Task:
    def __init__(self, period, duration, deadline=None, add_jitter=False):
        self.period = period
        self.duration = duration
        self.deadline = deadline if deadline else period
        self.jitter = int(self.period * 0.1) if add_jitter else 0
        self.jitter_left = -1
        self.reset()        

    def execute(self, callback):
        if self.remaining_execution_time == 0:
            raise ValueError("Task already complete")
        
        self.remaining_execution_time -= 1

        if self.remaining_execution_time == 0:
            callback(self)

    def reset(self):
        self.remaining_deadline = self.deadline
        self.time_until_next_period = self.period
        self.remaining_execution_time = self.duration

        if self.jitter == 0:
            return
        
        self.jitter_left = random.randint(0, self.jitter)
        if self.jitter_left > 0:
            self.remaining_execution_time = 0
    
    def time_step(self, new_task_period):
        if self.remaining_execution_time > 0 or self.jitter_left > 0:
            self.remaining_deadline -= 1

        if self.remaining_deadline == 0:
            raise ValueError(f"{self} missed deadline")
        
        if self.jitter_left > 0:
            self.jitter_left -= 1

        if self.jitter_left == 0:
            self.remaining_execution_time = self.duration
            self.jitter_left = -1
        
            
        # Always decrement time until next period
        self.time_until_next_period -= 1

        # If time until next period is 0, reset task
        if self.time_until_next_period == 0:
            self.reset()
            new_task_period(self)
    
    def __str__(self):
        if self.priority is None:
            return "Task ?"
        else:
            return f"Task {self.priority}"
        
class IdleTask(Task):
    def __init__(self):
        self.period = math.inf
        self.deadline = math.inf
        self.duration = math.inf
        self.remaining_execution_time = math.inf
        self.remaining_deadline = math.inf
        self.time_until_next_period = math.inf

    def __str__(self):
        return "Idle task"