import schedule_lib

scheduler = schedule_lib.Scheduler()

task1 = schedule_lib.Task(20, 20, 2)
task2 = schedule_lib.Task(25, 25, 2)
task3 = schedule_lib.Task(30, 30, 2)

tasks = [task1, task2, task3]

for task in tasks:
    scheduler.add_task(task)

scheduler.run(100_000)