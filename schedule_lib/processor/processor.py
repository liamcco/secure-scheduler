import numpy as np

from schedule_lib.processor.core import Core
from schedule_lib.partition.algorithms import ff
from schedule_lib.task.utils import calculate_hyperperiod
from schedule_lib.scheduler.basicscheduler import Scheduler
from schedule_lib.task.taskerror import DeadlineMissed, ExecutingFinishedTask
from schedule_lib.analysis.simulation import SimulationData

class Processor:
    def __init__(self, m: int, scheduler=Scheduler) -> None:
        self.tasks = {core_id:[] for core_id in range(m)}
        self.cores = [Core(core_id=core_id, tasks=tasks, scheduler=scheduler) for (core_id, tasks) in self.tasks.items()]
        
    def schedule_tasks(self) -> dict:
        return {core.core_id:core.schedule_task() for core in self.cores}

    def increment_time_step(self) -> None:
        for core in self.cores:
            core.increment_time_step()

    def load_tasks(self, tasks, partition_algorithm=ff) -> None:
        """tasks: list of Task objects
        partition_algorithm: function that partitions the tasks among the cores
                            ([tasks], m) -> {id:[tasks]}
        """
        
        partitioned_tasks = partition_algorithm(tasks, len(self.cores))

        for (core_id, taskset) in partitioned_tasks.items():
            self.tasks[core_id] += taskset
            self.cores[core_id].prioritize()

    def log_task_execution(self, tasks, time) -> None:
        for core, task in tasks.items():
            self.simulation[core][time][task.id] += 1

    def get_all_tasks(self):
        return [task for core in self.cores for task in core.tasks]
    
    def get_core_id_containing_task(self, task_id):
        for core in self.cores:
            for task in core.tasks:
                if task.id == task_id:
                    return core.core_id
        return None
    
    def run(self, time: int) -> bool:

        all_tasks = self.get_all_tasks()
        hyperperiod = calculate_hyperperiod(all_tasks)
        num_of_cores = len(self.cores)

        self.simulation = SimulationData(num_of_cores, hyperperiod, time)

        #print("| t\t| " + f" | ".join([f"Core{core.core_id}" for core in self.cores]) + " |")

        for t in range(time):
            
            # Pick a task to execute
            tasks_to_execute = self.schedule_tasks()
            
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
            self.simulation.log_task_execution(tasks_to_execute, t)
            #print(f"| {t}\t| " + f" | ".join([f"  {task.id}  " for task in tasks_to_execute.values()]) + " |")

        return True