from schedule_lib.task.taskerror import DeadlineMissed, ExecutingFinishedTask

class Task:
    def __init__(self, period, duration, deadline=None) -> None:
        self.period = period
        self.duration = duration
        self.deadline = deadline if deadline else period

        self.reset()
    
    def execute(self) -> bool:
        if self.remaining_execution_time == 0:
            raise ExecutingFinishedTask(self, "Task already complete")
        
        self.remaining_execution_time -= 1

        if self.remaining_execution_time == 0:
            return True

    def time_step(self) -> bool:
        if self.remaining_execution_time > 0:
            self.remaining_deadline -= 1

        if self.remaining_deadline == 0:
            raise DeadlineMissed(self, "Deadline missed")
        
        # Always decrement time until next period
        self.time_until_next_period -= 1

        # If time until next period is 0, reset task
        if self.time_until_next_period == 0:
            self.reset()
            return True

    def reset(self) -> None:
        self.remaining_deadline = self.deadline
        self.time_until_next_period = self.period
        self.remaining_execution_time = self.duration
    
    def is_ready(self) -> bool:
        return self.remaining_execution_time > 0
    
    def is_fresh(self) -> bool:
        return self.duration == self.remaining_execution_time
    
    def is_complete(self) -> bool:
        return self.remaining_execution_time == 0
    
    def is_new(self) -> bool:
        return self.time_until_next_period == self.period
    
    def __str__(self) -> str:
        info = "Task {\n" \
        + f"\tperiod={self.period},\n" \
        + f"\tduration={self.duration},\n" \
        + f"\tdeadline={self.deadline},\n" \
        + "}"

        return info