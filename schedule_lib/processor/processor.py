class Processor:
    """Creates a processor object to execute tasks"""
    def __init__(self, scheduler):
        self.tasks = []
        self.ready_queue = []

        self.scheduler = scheduler

    def __str__(self):
        return f"Processor: {len(self.queue)} tasks in queue"

    def __repr__(self):
        return self.__str__()

    def add_to_ready_queue(self, task):
        self.ready_queue.append(task)
        self.ready_queue.sort(key=lambda x: x.period)

    def remove_from_ready_queue(self, task):
        if task in self.ready_queue:
            self.ready_queue.remove(task)

    def add_task(self, task):
        self.tasks.append(task)
        task.processor = self
        task.id = len(self.tasks)

    def run(self, time):
        for task in self.tasks:
            self.add_to_ready_queue(task)

        for _ in range(time):

            if len(self.ready_queue) > 0:
                self.ready_queue[0].execute()
    
            for task in self.tasks:
                task.time_step()