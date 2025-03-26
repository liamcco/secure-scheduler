import numpy as np

from schedule_lib.processor.core import Core
from schedule_lib.partition.algorithms import nf
from schedule_lib.task.utils import calculate_hyperperiod
from schedule_lib.scheduler.basicscheduler import Scheduler
from schedule_lib.task.taskerror import DeadlineMissed, ExecutingFinishedTask
from schedule_lib.analysis.simulation import SimulationData

class Processor:
    def __init__(self, m: int, scheduler=Scheduler) -> None:
        self.tasks = {core_id:[] for core_id in range(m)}
        self.cores = [Core(core_id=core_id, tasks=tasks, scheduler=scheduler) for (core_id, tasks) in self.tasks.items()]
        self.all_tasks = [task for core in self.cores for task in core.tasks]
        
    def schedule_tasks(self) -> dict:
        return {core.core_id:core.schedule_task() for core in self.cores}

    def increment_time_step(self) -> None:
        for core in self.cores:
            core.increment_time_step()

    def load_tasks(self, tasks, partition_algorithm=nf) -> None:
        """tasks: list of Task objects
        partition_algorithm: function that partitions the tasks among the cores
                            ([tasks], m) -> {id:[tasks]}
        """
        
        partitioned_tasks = partition_algorithm(tasks, len(self.cores))

        for (core_id, taskset) in partitioned_tasks.items():
            self.tasks[core_id] += taskset
            self.cores[core_id].prioritize()
        
        self.all_tasks = [task for core in self.cores for task in core.tasks]
    
    def get_core_id_containing_task(self, task_id):
        for core in self.cores:
            for task in core.tasks:
                if task.id == task_id:
                    return core.core_id
        return None
    
    def run(self, time: int) -> bool:

        hyperperiod = calculate_hyperperiod(self.all_tasks)
        num_of_cores = len(self.cores)

        self.simulation = SimulationData(num_of_cores, hyperperiod, time)

        self.attack_data = {task_a.id: {"anterior": {task.id:0 for task in self.all_tasks if task.id != task_a.id}, 
                                      "posterior": {task.id:0 for task in self.all_tasks if task.id != task_a.id},
                                      "pincher": {task.id:0 for task in self.all_tasks if task.id != task_a.id},
                                      "current_anteriors": {}, 
                                      "current_posteriors": {}} for task_a in self.all_tasks}

        for t in range(time // hyperperiod * hyperperiod):
            
            # Pick a task to execute
            tasks_to_execute = self.schedule_tasks()

            # Store Schedule
            self.simulation.log_task_execution(tasks_to_execute, t)

            tasks_to_execute = [task for task in tasks_to_execute.values() if task.id != -1]

            # Easiest to check posterior before execution
            for executed_task in tasks_to_execute:
                # Update the current posteriors
                for new_task in [task for task in self.all_tasks if task.is_complete()]:
                    self.attack_data[new_task.id]["current_posteriors"][executed_task.id] = 1
            
            # Executes task and increments time step
            try:
                self.increment_time_step()
            except DeadlineMissed as e:
                print(e.message)
                return False
            except ExecutingFinishedTask as e:
                print(e.message)
                return False
        
            # Statistics
            for task in self.all_tasks:
                # Will not happen in the first time step
                if task.is_new():
                    # Summarize the current anteriors
                    for anterior_task in self.attack_data[task.id]["current_anteriors"]:
                        self.attack_data[task.id]["anterior"][anterior_task] += 1

                    for posterior_task in self.attack_data[task.id]["current_posteriors"]:
                        self.attack_data[task.id]["posterior"][posterior_task] += 1
                        if posterior_task in self.attack_data[task.id]["current_anteriors"]:
                            self.attack_data[task.id]["pincher"][posterior_task] += 1

                    # reset lists
                    self.attack_data[task.id]["current_anteriors"] = {}
                    self.attack_data[task.id]["current_posteriors"] = {}

            for executed_task in tasks_to_execute:
                # Update the current anteriors
                for fresh_task in [task for task in self.all_tasks if task.is_fresh() and task.id != executed_task.id]:
                    self.attack_data[fresh_task.id]["current_anteriors"][executed_task.id] = 1
            
        return True