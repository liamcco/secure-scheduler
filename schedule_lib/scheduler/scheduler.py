import random
import math
from schedule_lib.scheduler.utils import worst_case_maximum_inversion_budget, minimum_inversion_priority, next_schedule_decision_to_be_made, hp_i_of_tasks, calculate_hyperperiod
from schedule_lib.task.task import IdleTask


class Scheduler:
    idle_task = IdleTask()

    def __init__(self, tasks=[]):
        self.prioritize_tasks(tasks)
        self.toSchedule = 0
        
    def prioritize_tasks(self, tasks):
        self.tasks = sorted(tasks, key=lambda x: x.period)
        
        for i, task in enumerate(self.tasks):
            task.priority = i
            task.id = task.priority
        
        for task in self.tasks:
            task.maximum_inversion_budget = worst_case_maximum_inversion_budget(task, self.tasks)
            task.remaining_inversion_budget = task.maximum_inversion_budget
        
        Scheduler.idle_task.priority = math.inf
        Scheduler.idle_task.id = len(self.tasks)
        Scheduler.idle_task.maximum_inversion_budget = math.inf
        Scheduler.idle_task.remaining_inversion_budget = math.inf
    
    def scheduleTasks(self):

        # Check if it's time to schedule new task
        if self.toSchedule == 0:
            self.previous_task = self.pickTask()

        self.decrement_task_budgets()
        self.toSchedule -= 1
        
        return self.previous_task
    
    def pickTask(self):
        ready_tasks = [task for task in self.tasks if task.remaining_execution_time > 0]

        # If there are no tasks ready, keep idling
        if len(ready_tasks) == 0:
            self.toSchedule = math.inf
            return Scheduler.idle_task
        
        # If there is only one task, select it
        selection = ready_tasks[0]
        
        # Can we afford to select any other task?
        if selection.remaining_inversion_budget <= 0:
            self.toSchedule = selection.remaining_execution_time
            return selection
        
        # Step 1: Find the set of tasks that can be selected
        ready_tasks.append(Scheduler.idle_task)
        temp_queue = [ready_tasks[0]]
        m1 = minimum_inversion_priority(temp_queue[0], self.tasks)
            
        for task in ready_tasks[1:]:
            if task.priority <= m1:
                temp_queue.append(task)
            if task.remaining_inversion_budget <= 0:
                break
            
        # Step 2: Random selection
        idx = random.randint(0, len(temp_queue)-1)
        selection = temp_queue[idx]

        # Step 3: if lower priority task is selected, schedule decision
        if idx == 0:
            self.toSchedule = selection.remaining_execution_time
        else:
            self.toSchedule = next_schedule_decision_to_be_made(selection, ready_tasks)
        
        return selection
    
    def decrement_task_budgets(self):
        tasks_to_decrement = [task for task in hp_i_of_tasks(self.previous_task, self.tasks) if task.remaining_execution_time > 0]
        for task in tasks_to_decrement:
            task.remaining_inversion_budget -= 1
    
    def increment_time_step(self):
        for task in self.tasks:
            task.time_step(self.new_task_period)
    
    def new_task_period(self, task):
        self.toSchedule = 0
        task.remaining_inversion_budget = task.maximum_inversion_budget
    
    def whenTaskComplete(self, task):
        self.toSchedule = 0
    
    def getProperties(self):
        return f"{len(self.tasks)+1} {self.calculateHyperperiod()}"

    def calculateHyperPeriod(self):
        return calculate_hyperperiod(self.tasks)