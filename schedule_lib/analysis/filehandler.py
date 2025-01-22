class FileHandler:
    def __init__(self, filename):
        self.filename = filename
        with open(self.filename, 'w') as file:
            file.write('')

    def write(self, tasks):
        with open(self.filename, 'a') as file:
            data = ''
            for task in tasks:
                file.write(f"{task.id}")
            file.write("\n")

    def getHeader(self):
        # Read the first line of the file
        with open(self.filename, 'r') as file:
            header = file.readline()
            return header

    def getData(self):
        # Return an iterator for the rest of the file
        file = open(self.filename, 'r')
        file.readline()
        return file

    def updateProperties(self, properties):
        with open(self.filename, 'w') as file:
            file.write(f"{properties}\n")
    
