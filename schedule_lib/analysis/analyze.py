import math
from schedule_lib.analysis.filehandler import FileHandler

class Analysis:
    def __init__(self, filehandler=None):
        self.filehandler = filehandler
    
    def computeScheduleEntropy(self, simulation):
        entropy = 0
        for slot in simulation.values():
            slotEntropy = self.computeSlotEntropy(slot)
            entropy += slotEntropy
        return entropy
    
    def computeSlotEntropy(self, slot):
        return sum([-p*math.log(p,2) for p in [pdata[1] for pdata in self.getSlotProbabilities(slot)] if p != 0])
    
    def getSlotProbabilities(self, slot):
        probabilities = []
        total = sum(slot.values())
        for task in slot:
            p = slot[task] / total
            probabilities.append((task, p))
        return probabilities

    
