import multiprocessing


class queues():
    def __init__(self):
        self.kill_queue = multiprocessing.Queue()
        self.log_queue = multiprocessing.Queue()
        self.command_queue = multiprocessing.Queue()
        self.out_queue = multiprocessing.Queue()
        self.var_queue = multiprocessing.Queue()
        self.control_queue = multiprocessing.Queue()
        self.database_queue = multiprocessing.Queue()