import numpy as np

class SimulationData:
    def __init__(self, m, hyperperiod, t):
        if t // hyperperiod == 0:
            t = hyperperiod
        self.schedule = -np.ones((t // hyperperiod, m, hyperperiod), dtype=int)
        self.hyperperiod = hyperperiod
        self.m = m

    def log_task_execution(self, tasks, time) -> None:
        for scheduled_task in tasks.items():
            core, task = scheduled_task
            t = time % self.hyperperiod
            hp = time // self.hyperperiod
            self.schedule[hp][core][t] = task.id

    def __getitem__(self, index):
        return self.schedule[index]

