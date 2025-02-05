class TaskError(Exception):
    def __init__(self, task, message):
        super().__init__(message)
        self.task = task
        self.message = message

class DeadlineMissed(TaskError):
    pass

class ExecutingFinishedTask(TaskError):
    pass