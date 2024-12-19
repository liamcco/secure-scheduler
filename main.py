import schedule_lib

scheduler = schedule_lib.Scheduler(schedule_lib.Processor())

task1 = schedule_lib.Task(5, 5, 1)
task2 = schedule_lib.Task(10, 10, 1)
task3 = schedule_lib.Task(15, 15, 1)

tasks = [task1, task2, task3]

for task in tasks:
    scheduler.add_task(task)

scheduler.run(100)
