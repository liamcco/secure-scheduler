class Simulation:
    def __init__(self, scheduler, save_to=None):
        self.scheduler = scheduler
        self.filehandler = save_to
    
    def run(self, time):

        # SETUP
        self.simulation = {}
        hyperPeriod = self.scheduler.calculateHyperPeriod()
        numOfTasks = len(self.scheduler.tasks)+1
        for slot in range(hyperPeriod):
            taskCounter = {}
            for task_id in range(numOfTasks):
                taskCounter[task_id] = 0
            self.simulation[slot] = taskCounter
        
        for t in range(time):

            # Pick a task to execute
            taskToExecute = self.scheduler.scheduleTasks()
            
            # Execute the task
            taskToExecute.execute(self.scheduler.whenTaskComplete)

            # Statistics
            self.simulation[t % hyperPeriod][taskToExecute.id] += 1

            # Increment time step
            self.scheduler.increment_time_step()
            
            # if event = min( completion(execex of current task) and min(floor(t/T_i)*T_i+T_i)-t)
            # RelSet= sort (all release time of all tasks)

