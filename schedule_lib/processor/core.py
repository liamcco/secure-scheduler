from schedule_lib.scheduler.basicscheduler import Scheduler
from schedule_lib.task.idletask import IdleTask

class Core:
    def __init__(self, core_id: int, tasks=[], scheduler=Scheduler) -> None:
        self.core_id = core_id
        self.tasks = tasks
        self.scheduler = scheduler(self.tasks)
        self.idle_task = IdleTask()

    def reload_tasks(self, tasks) -> None:
        self.tasks = tasks
        self.scheduler.reload_tasks(tasks)
    
    def prioritize(self) -> None:
        self.scheduler.prioritize_tasks()

    def schedule_task(self):
        selected_task = self.scheduler.schedule_task()
        self.task_to_execute = selected_task if selected_task else self.idle_task
        
        return self.task_to_execute
    
    def execute_task(self) -> None:
        did_complete = self.task_to_execute.execute()
        if did_complete:
            self.scheduler.task_completed(self.task_to_execute)
    
    def increment_time_step(self) -> None:
        self.scheduler.time_step()

        self.execute_task()

        for task in self.tasks:
            if task.time_step():
                self.scheduler.task_arrived(task)
        