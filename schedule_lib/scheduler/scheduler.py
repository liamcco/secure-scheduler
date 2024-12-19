class Scheduler:
    def __init__(self, processor):
        self.processor = processor
        self.compare = self.rate_monotonic_compare
        self.tasks = []
    
    def rate_monotonic_compare(self, task1, task2):
        return task1.period < task2.period
    
    def add_to_ready_queue(self, task):
        if task not in self.processor.cores[task.core_id].ready_queue:
            self.processor.cores[task.core_id].ready_queue.append(task)
        self.processor.cores[task.core_id].ready_queue.sort(key=lambda x: x.period)

    def remove_from_ready_queue(self, task):
        if task in self.processor.cores[task.core_id].ready_queue:
            self.processor.cores[task.core_id].ready_queue.remove(task)

    def add_task(self, task):
        self.tasks.append(task)
        task.scheduler = self
        task.id = len(self.tasks)

    def assign_tasks_to_cores(self):
        for task in self.tasks:
            task.core_id = 0
    
    def reset_tasks(self):
        for task in self.tasks:
            task.reset()

    def run(self, time):

        self.assign_tasks_to_cores()
        self.reset_tasks()

        for task in self.tasks:
            self.add_to_ready_queue(task)

        for _ in range(time):

            for core in self.processor.cores:
                core.execute()
    
            for task in self.tasks:
                task.time_step()
    
