from schedule_lib import JitterTask as Task
from schedule_lib import Processor
from schedule_lib.feasibility.tests import RTA
from schedule_lib import TaskShufflerScheduler
from schedule_lib import Analysis
from schedule_lib.partition.algorithms import ff

def main():

    task1 = Task(5, 1)
    task2 = Task(8, 2)
    task3 = Task(20, 3)

    tasks = [task1, task2, task3] 

    for i, task in enumerate(tasks):
        task.id = i

    def custom_scheduler(tasks):
        scheduler = TaskShufflerScheduler(tasks)
        scheduler.priority_policy = "RM" # Set the priority policy to RRM
        return scheduler

    processor = Processor(1, scheduler=custom_scheduler) # 2 core

    def custom_partition_algorithm(tasks, m):
        return ff(tasks, m, task_order="RM", test=RTA, priority_policy="RM")

    processor.load_tasks(tasks, partition_algorithm=custom_partition_algorithm) # Load tasks into the processor

    success = processor.run(40_000) # Run the processor for 80 time units

    if not success:
        print("ABORTING: Deadline missed")
        exit()

    analysis = Analysis(processor)

    analysis.create_cumulative_data()

    for core in range(analysis.data.m):
        coreEntropy = analysis.computeCoreScheduleEntropy(core)
        print(f"Total entropy in core {core}: {coreEntropy:.2f}")

    totalMultiCoreEntropy = analysis.computeMultiCoreScheduleEntropy()
    print(f"Total multi-core entropy: {totalMultiCoreEntropy:.2f}")

    anteriorEntropies = [analysis.computeAnteriorEntropy(task_id) for task_id in range(analysis.num_of_tasks)]
    totalAnteriorEntropy = analysis.geometric_mean(anteriorEntropies)
    print(f"Total anterior entropy: {totalAnteriorEntropy:.2f}")

    pincherEntropies = [analysis.computePincherEntropy(task_id) for task_id in range(analysis.num_of_tasks)]
    totalPincherEntropy = analysis.geometric_mean(pincherEntropies)
    print(f"Total pincher entropy: {totalPincherEntropy:.2f}")

    print("Slot\tPr0\tPr1\tPr2\tPr3\tTotalEntropy")

    for slot in range(5):
        print(f"{slot}: ", end="\t")
        slotData = analysis.cumdata[0][slot]
        probabilities = analysis.getSlotProbabilities(slotData)

        for p in probabilities:
            print(f"{p:.2f} ", end="\t")

        slotEntropy = analysis.computeSlotEntropy(slotData)

        print(f"{slotEntropy:.2f}")

    print("..."*20)
    print(f"Total\t\t\t\t\t\t{analysis.computeCoreScheduleEntropy(0)/analysis.hyperperiod:.2f} entropy/slot")

if __name__ == '__main__':
    main()