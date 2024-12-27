# Class for a task, including duration, deadline

class Task:
    def __init__(self, period, deadline, duration):
        self.period = period
        self.deadline = deadline
        self.duration = duration

        self.remaining_execution_time = duration
        self.remaining_deadline = deadline
        self.time_until_next_period = period

    def execute(self):
        if self.remaining_execution_time == 0:
            raise ValueError("Task already complete")
        
        self.remaining_execution_time -= 1

    def reset(self):
        self.remaining_execution_time = self.duration
        self.remaining_deadline = self.deadline
        self.time_until_next_period = self.period
    
    def time_step(self):
        # Only decrement time until deadline if task is not complete
        if self.remaining_execution_time > 0 and self.remaining_deadline > 0:
            self.remaining_deadline -= 1

        # If task is not complete and deadline is missed, raise error
        if self.remaining_deadline == 0:
            raise ValueError(f"Task {self.id} missed deadline")

        # Always decrement time until next period
        self.time_until_next_period -= 1

        # If time until next period is 0, reset task
        if self.time_until_next_period == 0:
            self.reset()