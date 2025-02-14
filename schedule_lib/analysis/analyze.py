import math
import numpy as np
from functools import reduce
from operator import mul

class Analysis:
    def __init__(self, processor) -> None:
        self.data = processor.simulation
        self.num_of_tasks = len(processor.get_all_tasks())
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
    
    def computePosteriorEntropy(self, task_id, m=None):
        return self.computeAnteriorEntropy(task_id, m, posterior=True)
    
    def computeAnteriorEntropy(self, task_id, m=None, posterior=False, get_data=False):
        data_to_search = self.flatten_simulation_data()
        if m is not None:
            data_to_search = data_to_search[:][m:m+1]
        if posterior:
            data_to_search = data_to_search[::-1]
        anterior_data = {}

        for t, slot in enumerate(data_to_search):
            if task_id in slot:
                for preceding_task in data_to_search[t-1]:
                    if preceding_task != task_id:
                        if preceding_task in anterior_data:
                            anterior_data[preceding_task] += 1
                        else:
                            anterior_data[int(preceding_task)] = 1

        return self.computeSlotEntropy(anterior_data) if not get_data else anterior_data
    
    def computePincherEntropy(self, task_id, m=None, get_data=False):
        data_to_search = self.flatten_simulation_data()
        if m is not None:
            data_to_search = data_to_search[:][m:m+1]
        pincher_data = {}

        start_search_index = 0
        if task_id in data_to_search[0]:
            for t, slot in enumerate(data_to_search[1:]):
                if task_id not in slot:
                    start_search_index = t+1
                    break

        current_potential_pinchers = None

        for t, slot in enumerate(data_to_search[start_search_index+1:]):

            if task_id in slot and current_potential_pinchers is None:
                current_slot = data_to_search[t-1]
                current_potential_pinchers = current_slot[current_slot != -1]
                continue

            if task_id not in slot and current_potential_pinchers is not None:
                for preceding_task in slot:
                    if preceding_task in current_potential_pinchers:
                        if preceding_task in pincher_data:
                            pincher_data[preceding_task] += 1
                        else:
                            pincher_data[int(preceding_task)] = 1
                current_potential_pinchers = None

        return self.computeSlotEntropy(pincher_data) if not get_data else pincher_data

    
    def computeMultiCoreScheduleEntropy(self) -> float:
        if not self.cumdata:
            self.create_cumulative_data()

        data = [self.computeCoreScheduleEntropy(m) for m in range(self.data.m)]
        return self.geometric_mean(data)
    
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
        probabilities = [slot[task_id]/total if (task_id in slot) else 0 for task_id in range(self.num_of_tasks)] + [slot[-1]/total if (-1 in slot) else 0] if include_idle else []

        return probabilities
