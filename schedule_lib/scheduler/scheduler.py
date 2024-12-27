import random
from schedule_lib.scheduler.utils import worst_case_maximum_inversion_budget, minimum_inversion_priority


class Scheduler:
    def __init__(self):
        self.tasks = set()
        self.ready_queue = None
        self.time = 0
    
    def scheduleTasks(self):
        ready_tasks = sorted([task for task in self.tasks if task.remaining_execution_time > 0], key=lambda x: x.priority)
        
        if len(ready_tasks) == 0:
            return
        
        self.ready_queue = ready_tasks[0]
        
        if len(ready_tasks) == 1:
            return
        
        if worst_case_maximum_inversion_budget(self.ready_queue, self.tasks) <= 0:
            return
        
        # Step 1: Find the set of tasks that can be selected
        temp_queue = []
        temp_queue.append(ready_tasks[0])
        m1 = minimum_inversion_priority(temp_queue[0], self.tasks)
            
        for task in ready_tasks[1:]:
            if m1 > task.priority:
                temp_queue.append(task)
            if worst_case_maximum_inversion_budget(task, self.tasks) <= 0:
                break
            
        # Step 2: Random selection
        self.ready_queue = random.choice(temp_queue)

    def add_task(self, task):
        self.tasks.add(task)
        
    def prioritize_tasks(self):
        sorted_tasks = sorted(self.tasks, key=lambda x: x.period)
        for i, task in enumerate(sorted_tasks):
            task.priority = i
    
    def reset_tasks(self):
        for task in self.tasks:
            task.reset()

    def run(self, time):

        self.prioritize_tasks()
        self.reset_tasks()

        for _ in range(time):

            self.ready_queue = None

            self.scheduleTasks()

            if self.ready_queue:
                self.ready_queue.execute()
    
            for task in self.tasks:
                try:
                    task.time_step()
                except ValueError as e:
                    print(e)
            
            self.time += 1
    
