from schedule_lib import JitterTask as Task
from schedule_lib import Processor
from schedule_lib.feasibility.tests import RTA
from schedule_lib import TaskShufflerScheduler
from schedule_lib import Analysis
from schedule_lib.partition.algorithms import ff

task1 = Task(5, 1)
task2 = Task(8, 2)
task3 = Task(20, 3)

tasks = [task1, task2, task3]

for i, task in enumerate(tasks):
    task.id = i

if RTA(tasks, priority_policy="RM"): # Check if the taskset is feasible
    print("Taskset is feasible")
else:
    print("WARNING: Taskset is not feasible")

TaskShufflerScheduler.priority_policy = "RM" # Set the priority policy to RRM

processor = Processor(1, scheduler=TaskShufflerScheduler) # 1 core

def custom_partition_algorithm(tasks, m):
    return ff(tasks, m, task_order="RM", test=RTA, priority_policy="RM")

processor.load_tasks(tasks, partition_algorithm=custom_partition_algorithm) # Load tasks into the processor

success = processor.run(400_000) # Run the processor for 100 time units

if not success:
    print("ABORTING: Deadline missed")
    exit()

analysis = Analysis(processor.simulation[0])
totalEntropy = analysis.computeScheduleEntropy()

print("Slot\tPr0\tPr1\tPr2\tPr3\tTotalEntropy")

for slot in range(5):
    print(f"{slot}: ", end="\t")
    slotData = analysis.simulation[slot]
    probabilities = analysis.getSlotProbabilities(slotData)

    for p in probabilities:
        print(f"{p:.2f} ", end="\t")

    slotEntropy = analysis.computeSlotEntropy(slotData)

    print(f"{slotEntropy:.2f}")

print("..."*20)
print(f"Total\t\t\t\t\t\t{totalEntropy/analysis.hyperPeriod:.2f} entropy/slot")