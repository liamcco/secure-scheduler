import math
import random
from schedule_lib.scheduler.utils import worst_case_maximum_inversion_budget, minimum_inversion_priority, next_schedule_decision_to_be_made, hp_i_of_tasks
from schedule_lib.task.task import IdleTask


class Scheduler:
    def __init__(self):
        self.tasks = set()
        self.idle_task = IdleTask()

    def add_task(self, task):
        self.tasks.add(task)
        
    def prioritize_tasks(self):
        sorted_tasks = sorted(self.tasks, key=lambda x: x.period)
        
        for i, task in enumerate(sorted_tasks):
            task.priority = i
        
        self.idle_task.priority = len(self.tasks)

    def calcualte_budgets(self):
        for task in self.tasks:
            task.maximum_inversion_budget = worst_case_maximum_inversion_budget(task, self.tasks)
    
    def reset_tasks(self):
        for task in self.tasks:
            task.reset()

    def run(self, time):

        self.prioritize_tasks()
        self.calcualte_budgets()
        self.reset_tasks()

        self.toSchedule = 0
        self.ready_queue = self.idle_task

        for t in range(time):

            self.scheduleTasks()

            self.decrement_task_budgets()
            if(self.ready_queue.execute()):
                self.toSchedule = 0

            for task in self.tasks:
                if(task.time_step()):
                    self.toSchedule = 0
    
    def scheduleTasks(self):
        # Check if it's time to schedule new task
        if self.toSchedule > 1:
            self.toSchedule -= 1
            return
        
        self.ready_queue = self.idle_task
        ready_tasks = sorted([task for task in self.tasks if task.remaining_execution_time > 0], key=lambda x: x.priority)    

        # If there are no tasks ready, keep idling
        if len(ready_tasks) == 0:
            return
        
        # If there is only one task, select it
        selection = ready_tasks[0]
        self.ready_queue = selection
        self.toSchedule = random.randint(1, selection.remaining_execution_time)
        
        # Can we afford to select any other task?
        if self.ready_queue.remaining_inversion_budget <= 0:
            return
        
        # Step 1: Find the set of tasks that can be selected
        temp_queue = []
        temp_queue.append(ready_tasks[0])
        m1 = minimum_inversion_priority(temp_queue[0], self.tasks)
            
        for task in ready_tasks[1:]:
            if m1 > task.priority:
                temp_queue.append(task)
            if task.remaining_inversion_budget <= 0:
                break

        # Check if idle task can be selected
        if len(temp_queue) == len(ready_tasks) and ready_tasks[-1].remaining_inversion_budget > 0:
            if m1 > self.idle_task.priority:
                temp_queue.append(self.idle_task)
            
        # Step 2: Random selection
        idx = random.randint(0, len(temp_queue)-1)
        selection = temp_queue[idx]
        self.ready_queue = selection

        #Check if idle task is selected
        if selection == self.idle_task:
            max = min([task.remaining_inversion_budget for task in ready_tasks])
            self.toSchedule = random.randint(1, max)
            return

        if idx > 0:
            self.toSchedule = next_schedule_decision_to_be_made(selection, ready_tasks)
    
    def decrement_task_budgets(self):
        tasks_to_decrement = [task for task in hp_i_of_tasks(self.ready_queue, self.tasks) if task.remaining_execution_time > 0]
        for task in tasks_to_decrement:
            task.remaining_inversion_budget -= 1

    
