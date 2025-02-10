import random
import math

from schedule_lib.scheduler.utils import worst_case_maximum_inversion_budget, minimum_inversion_priority, next_schedule_decision_to_be_made, hp_i_of_tasks
from schedule_lib.task.idletask import IdleTask

from schedule_lib.scheduler.basicscheduler import Scheduler

from schedule_lib.priority.priority import task_sorting_operators

class TaskShufflerScheduler(Scheduler):

    priority_policy = "RM"

    def __init__(self, tasks) -> None:
        self.idle_task = IdleTask()
        self.tasks = tasks

        if self.tasks:
            self.prioritize_tasks()

        self.toSchedule = 0

    # Sort tasks by PERIOD and assign priority
    def prioritize_tasks(self) -> None:
        task_sorting_operators[self.priority_policy](self.tasks)
        for i, task in enumerate(self.tasks):
            task.priority = i
            if not hasattr(task, 'id'):
                task.id = i
        
        # Only when tasks have been prioritized, we can calculate the maximum inversion budget
        for task in self.tasks:
            task.maximum_inversion_budget = worst_case_maximum_inversion_budget(task, self.tasks)
            task.remaining_inversion_budget = task.maximum_inversion_budget
        
        # Add idle task
        self.idle_task.priority = math.inf
        self.idle_task.id = len(self.tasks)
        self.idle_task.maximum_inversion_budget = math.inf
        self.idle_task.remaining_inversion_budget = math.inf
    
    def schedule_task(self):
        # Check if it's time to schedule new task
        if self.toSchedule == 0:
            self.previous_task = self.pickTask()
        
        return self.previous_task
    
    # Implemets TaskShuffler
    def pickTask(self):
        # Tasks ready for execution
        ready_tasks = [task for task in self.tasks if task.is_ready()]

        # If there are no tasks ready, keep idling, indefinetly 
        if len(ready_tasks) == 0:
            self.toSchedule = math.inf
            return self.idle_task
        
        # Select the first task
        selection = ready_tasks[0]
        
        # Can we afford to select any other task?
        if selection.remaining_inversion_budget <= 0:
            self.toSchedule = selection.remaining_execution_time
            return selection
        
        # Step 1: Find the set of tasks that can be selected
        ready_tasks.append(self.idle_task) # Treat idle task as a task
        temp_queue = [ready_tasks[0]] # First task is always considered
        m1 = minimum_inversion_priority(temp_queue[0], self.tasks) # Minimum inversion priority
            
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
            self.toSchedule = random.randint(1, selection.remaining_execution_time)
        else:
            self.toSchedule = next_schedule_decision_to_be_made(selection, ready_tasks)
        
        return selection
    
    def decrement_task_budgets(self) -> None:
        for task in hp_i_of_tasks(self.previous_task, self.tasks):
            if task.is_ready():
                task.remaining_inversion_budget -= 1
    
    def task_arrived(self, task) -> None:
        self.toSchedule = 0
        task.remaining_inversion_budget = task.maximum_inversion_budget
        task.remaining_inversion_budget -= task.remaining_jitter
    
    def task_completed(self, task) -> None:
        self.toSchedule = 0

    def time_step(self) -> None:
        # Decrement task budget after we now wich task is going to be executed
        self.decrement_task_budgets()
        self.toSchedule -= 1

