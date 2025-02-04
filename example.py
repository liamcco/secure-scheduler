import schedule_lib
import schedule_lib.scheduler
import schedule_lib.scheduler.utils

task1 = schedule_lib.Task(24, 6)
task2 = schedule_lib.Task(750, 47)
task3 = schedule_lib.Task(50, 16)
task4 = schedule_lib.Task(375, 27)
task5 = schedule_lib.Task(30, 8)

tasks = [task1, task2, task3, task4, task5]

scheduler = schedule_lib.Scheduler(tasks)

simulation = schedule_lib.Simulation(scheduler)

simulation.run(3000)

analysis = schedule_lib.Analysis()
data = simulation.simulation
hyperPeriod = len(data)
totalEntropy = analysis.computeScheduleEntropy(data)

print("Slot\tPr0\tPr1\tPr2\tPr3\tTotalEntropy")

for slot in range(16):
    print(f"{slot}: ", end="\t")
    slotData = data[slot]

    pdatas = sorted(analysis.getSlotProbabilities(slotData), key=lambda x: x[0])

    for pdata in pdatas:
        print(f"{pdata[1]:.2f} ", end="\t")

    slotEntropy = analysis.computeSlotEntropy(slotData)

    print(f"{slotEntropy:.2f}")

print("..."*15)
print(f"Total\t\t\t\t\t{totalEntropy/hyperPeriod:.2f} entropy/slot")