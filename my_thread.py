import threading

# Class to manage a single thread that runs a given task
class MyThread():
    def __init__(self, work):
        self.event = threading.Event()  # Event to control thread execution (start/stop)
        self.thread = threading.Thread()  # Placeholder for the thread instance
        self.work = work  # The function that will be executed in the thread

    # Starts the thread and resets the stop event
    def start(self):
        self.event.clear()  # Ensures the event is cleared before starting
        self.thread = threading.Thread(target=self.run)  # Creates a new thread
        self.thread.start()  # Starts the thread execution

    # Stops the thread by setting the event flag and waiting for it to finish
    def stop(self):
        self.event.set()  # Signals the thread to stop
        self.thread.join()  # Waits for the thread to complete execution

    # The function executed within the thread
    def run(self):
        while not self.event.is_set():  # Keeps running until the stop event is set
            self.work()  # Executes the assigned work function

# Class to manage multiple threads as a group
class ThreadGroup:
    def __init__(self, list_thread):
        self.my_threads = list_thread  # Stores the list of threads to be managed
    
    # Starts all threads in the group
    def start(self):
        for thread in self.my_threads:
            thread.start()

    # Stops all threads in the group
    def stop(self):
        for thread in self.my_threads:
            thread.stop()
