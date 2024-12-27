import random
from schedule_lib.scheduler.utils import worst_case_maximum_inversion_budget, minimum_inversion_priority


class Scheduler:
    def __init__(self, processor):
        self.processor = processor
        self.tasks = []
        self.time = 0
    
    def shuffleTasks(self):
        for core in self.processor.cores:
            core.ready_queue.sort(key=lambda x: x.priority)
            # Step 1: Finding candidates
            temp_queue = []
            if len(core.ready_queue) <= 1:
                continue
            
            if worst_case_maximum_inversion_budget(core.ready_queue[0], self.tasks) <= 0:
                continue
            
            temp_queue.append(core.ready_queue[0])
            m1 = minimum_inversion_priority(core.ready_queue[0], self.tasks)
            
            for task in core.ready_queue[1:]:
                if m1 > task.priority:
                    temp_queue.append(task)
                if worst_case_maximum_inversion_budget(task, self.tasks) <= 0:
                    break
            
            # Step 2: Random selection
            selected_task = random.choice(temp_queue)
            selected_task_index = core.ready_queue.index(selected_task)
            core.ready_queue.insert(0, core.ready_queue.pop(selected_task_index))

    def add_to_ready_queue(self, task):
        if task not in self.processor.cores[task.core_id].ready_queue:
            self.processor.cores[task.core_id].ready_queue.append(task)

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
        
    def prioritize_tasks(self):
        self.tasks.sort(key=lambda x: x.period)
        for i, task in enumerate(self.tasks):
            task.priority = i
    
    def reset_tasks(self):
        for task in self.tasks:
            task.reset()

    def run(self, time):

        self.prioritize_tasks()
        self.assign_tasks_to_cores()
        self.reset_tasks()

        for task in self.tasks:
            self.add_to_ready_queue(task)

        for _ in range(time):

            self.shuffleTasks()

            self.processor.execute()
    
            for task in self.tasks:
                try:
                    task.time_step()
                except ValueError as e:
                    print(e)
            
            self.time += 1
    
