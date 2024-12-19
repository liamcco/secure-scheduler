from schedule_lib.task.idle_task import IdleTask

class Core:
    def __init__(self):
        self.processor = None
        self.ready_queue = []
        self.idle_task = IdleTask()
    
    def execute(self):
        if len(self.ready_queue) > 0:
            task = self.ready_queue[0]
        else:
            task = self.idle_task
        task.execute()