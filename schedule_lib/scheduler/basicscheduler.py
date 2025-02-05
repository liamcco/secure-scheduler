from schedule_lib.priority.priority import task_sorting_operators

class Scheduler:

    priority_policy = "RM"

    def __init__(self, tasks=[]) -> None:
        self.tasks = tasks

    def schedule_task(self):
        for task in self.tasks:
            if task.is_ready():
                return task
        
        return None
    
    def reload_tasks(self, tasks) -> None:
        self.tasks = tasks
        self.prioritize_tasks()
    
    def prioritize_tasks(self) -> None:
        task_sorting_operators[self.priority_policy](self.tasks)
        for i, task in enumerate(self.tasks):
            task.priority = i

    def task_completed(self, task) -> None:
        pass

    def task_arrived(self, task) -> None:
        pass

    def time_step(self) -> None:
        pass