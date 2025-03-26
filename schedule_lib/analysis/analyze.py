import math
from functools import reduce
from operator import mul

class Analysis:
    def __init__(self, processor) -> None:
        self.data = processor.simulation
        self.num_of_tasks = len(processor.all_tasks)
        self.hyperperiod = self.data.hyperperiod
        self.num_of_cores = self.data.m
        self.cumdata = {}

    def create_cumulative_data(self):
        self.cumdata = {}
        for core in range(self.data.m):
            core_cum_data = []
            for t in range(self.data.hyperperiod):
                task_data = self.data[:, core, t]
                task_cum_data = {}
                for task in task_data:
                    if task in task_cum_data:
                        task_cum_data[int(task)] += 1
                    else:
                        task_cum_data[int(task)] = 1
                core_cum_data.append(task_cum_data)
            self.cumdata[core] = core_cum_data

    def flatten_simulation_data(self):
        return self.data.schedule.transpose(1, 0, 2).reshape(self.data.m, -1).T
    
    def get_schedule_of_core(self, core_id):
        return self.flatten_simulation_data()[:, core_id]
    
    def computeMultiCoreScheduleEntropy(self) -> float:
        if not self.cumdata:
            self.create_cumulative_data()

        data = [self.computeCoreScheduleEntropy(m) for m in range(self.data.m)]
        active_processors = [coreEntropy for coreEntropy in data if coreEntropy != 0]
        return self.geometric_mean(active_processors) if active_processors else 0
    
    def geometric_mean(self, data) -> float:
        return reduce(mul, data, 1) ** (1/len(data))
    
    def computeCoreScheduleEntropy(self, m) -> float:
        if not self.cumdata:
            self.create_cumulative_data()

        return sum(self.computeSlotEntropy(slot) for slot in self.cumdata[m]) # /(self.hyperperiod * math.log(self.num_of_tasks + 1, 2))
    
    def computeSlotEntropy(self, slot) -> float:
        return sum([-p*math.log(p,2) for p in self.getSlotProbabilities(slot) if p != 0]) # / math.log(self.num_of_tasks + 1, 2)
    
    def getSlotProbabilities(self, slot, include_idle=True):
        total = sum(slot.values())
        if total == 0:
            return []
        probabilities = [slot[task_id]/total if (task_id in slot) else 0 for task_id in range(self.num_of_tasks)] + ( [slot[-1]/total if (-1 in slot) else 0] if include_idle else [] )

        return probabilities
