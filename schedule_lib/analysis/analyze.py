import math

class Analysis:
    def __init__(self, simulation):
        self.simulation = simulation
        self.hyperPeriod = len(simulation)
    
    def computeScheduleEntropy(self):
        return sum(self.computeSlotEntropy(slot) for slot in self.simulation)
    
    def computeSlotEntropy(self, slot):
        return sum([-p*math.log(p,2) for p in self.getSlotProbabilities(slot) if p != 0])
    
    def getSlotProbabilities(self, slot):
        total = sum(slot)
        probabilities = [p/total for p in slot]

        return probabilities


    
