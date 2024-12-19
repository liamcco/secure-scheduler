import schedule_lib

scheduler = schedule_lib.Scheduler()
processor = schedule_lib.Processor(scheduler)

task1 = schedule_lib.Task(5, 5, 1)
task2 = schedule_lib.Task(10, 10, 1)
task3 = schedule_lib.Task(15, 15, 1)
task1.processor = processor
task2.processor = processor
task3.processor = processor

tasks = [task1, task2, task3]

for task in tasks:
    processor.add_task(task)

processor.run(1000)
