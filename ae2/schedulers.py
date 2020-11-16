from des import SchedulerDES
from event import Event, EventTypes
from process import Process, ProcessStates

class FCFS(SchedulerDES):
    """FCFS(First Come First Serve) is a non-preemptive scheduling algorithm,
    meaning that the processes are executed without interruption.
    Processes are scheduled in order of their arrival.
    """
    def scheduler_func(self, cur_event):
        return sorted(filter(lambda p : p.process_state==ProcessStates.READY, self.processes), key=lambda p : p.arrival_time)[0]

    def dispatcher_func(self, cur_process):
        time_run_for = cur_process.run_for(10000, self.time)
        cur_process.process_state = ProcessStates.TERMINATED
        return Event(process_id=cur_process.process_id,
                    event_time=self.time + time_run_for,
                    event_type=EventTypes.PROC_CPU_DONE)


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
