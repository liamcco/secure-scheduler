import schedule_lib

scheduler = schedule_lib.Scheduler(schedule_lib.Processor(1))

task1 = schedule_lib.Task(3, 3, 1)
task2 = schedule_lib.Task(5, 5, 1)
task3 = schedule_lib.Task(7, 7, 1)
task4 = schedule_lib.Task(11, 11, 1)

tasks = [task1, task2, task3, task4]

for task in tasks:
    scheduler.add_task(task)

scheduler.run(100)
