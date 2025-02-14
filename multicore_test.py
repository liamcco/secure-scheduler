from schedule_lib import Processor
from schedule_lib.feasibility.tests import RTA
from schedule_lib import TaskShufflerScheduler
from schedule_lib import Analysis
from schedule_lib.partition.algorithms import ff, nf
from schedule_lib.taskset.taskset import TaskSet

def main():

    # Generate taskset
    n = 25
    m = 4
    U = 2.3
    hyper_period = 3000
    tasks = TaskSet.generate_task_set(n, U, hyper_period=hyper_period)

    for i, task in enumerate(tasks):
        task.id = i
        print(f"Task {task.id}: T = {task.period}, C = {task.duration}")
    print()

    processor = Processor(m, scheduler=TaskShufflerScheduler)

    def custom_partition_algorithm(tasks, m):
        result = nf(tasks, m, task_order="RM", test=RTA, priority_policy="RM")
        print(result)

        return result

    # Next line will crash if the partitioning is not feasible
    processor.load_tasks(tasks, partition_algorithm=custom_partition_algorithm) # Load tasks into the processor

    for core in processor.cores:
        print(f"Core {core.core_id}:")
        if not core.tasks:
            print("No tasks")
        for task in core.tasks:
            print(f"Task {task.id}: T = {task.period}, C = {task.duration}")

    success = processor.run(3_000 * 1_0) # Run for 1000 hyperperiods

    if not success:
        print("ABORTING: Deadline missed")
        exit()

    analysis = Analysis(processor)

    analysis.create_cumulative_data()

    print("Cumulative data:")

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

if __name__ == '__main__':
    main()