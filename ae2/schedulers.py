from des import SchedulerDES


class FCFS(SchedulerDES):
    """FCFS(First Come First Serve) is a non-preemptive scheduling algorithm,
    meaning that the processes are executed without interruption.
    Processes are scheduled in order of their arrival.
    """
    def scheduler_func(self, cur_event):
        #TODO
        pass

    def dispatcher_func(self, cur_process):
        #TODO
        pass


class SJF(SchedulerDES):
    """SJF(Shortest Job First) is a non-preemptive scheduling algorithm,
    meaning that the processes are executed without interruption.
    Processes are scheduled according to their service time,
    with the shortest one first.
    """
    def scheduler_func(self, cur_event):
        #TODO
        pass

    def dispatcher_func(self, cur_process):
        #TODO
        pass


class RR(SchedulerDES):
    """RR(Round Robin) is a preemptive scheduling algorithm,
    meaning that the process currently running on the CPU 
    can be interrupted in favor of another process.
    It interleaves the execution of processes which are not serviced yet.
    """
    def scheduler_func(self, cur_event):
        #TODO
        pass

    def dispatcher_func(self, cur_process):
        #TODO
        pass


class SRTF(SchedulerDES):
    """SRTF(Shortest Remaining Time First) is a preemptive scheduling algorithm,
    meaning that the process currently running on the CPU 
    can be interrupted in favor of another process. 
    It prioritises processes which expect to be serviced sooner.
    """
    def scheduler_func(self, cur_event):
        #TODO
        pass

    def dispatcher_func(self, cur_process):
        #TODO
        pass
