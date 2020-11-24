from des import SchedulerDES
from event import Event, EventTypes
from process import Process, ProcessStates

class FCFS(SchedulerDES):
    """FCFS(First Come First Serve) is a non-preemptive scheduling algorithm,
    meaning that the processes are executed without interruption.
    Processes are scheduled in order of their arrival.
    """
    def scheduler_func(self, cur_event):
        return self.processes[cur_event.process_id]

    def dispatcher_func(self, cur_process):
        time_run_for = cur_process.run_for(cur_process.service_time, self.time)
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
        x=sorted(self.processes,key=lambda p:p.service_time)
        for process in x:
            if process.process_state==process.process_state.READY:
                return process
            else:
                continue

    def dispatcher_func(self, cur_process):
        time_run_for = cur_process.run_for(cur_process.service_time, self.time)
        cur_process.process_state = ProcessStates.TERMINATED
        return Event(process_id=cur_process.process_id,
                    event_time=self.time + time_run_for,
                    event_type=EventTypes.PROC_CPU_DONE)
        



class RR(SchedulerDES):
    """RR(Round Robin) is a preemptive scheduling algorithm,
    meaning that the process currently running on the CPU 
    can be interrupted in favor of another process.
    It interleaves the execution of processes which are not serviced yet.
    """
    def scheduler_func(self, cur_event):
        return self.processes[cur_event.process_id]

    def dispatcher_func(self, cur_process):
        time_run_for = cur_process.run_for(self.quantum, self.time)
        cur_process.process_state = ProcessStates.READY if cur_process.remaining_time > 0 else ProcessStates.TERMINATED
        return Event(process_id=cur_process.process_id,
                    event_time=self.time + time_run_for,
                    event_type=EventTypes.PROC_CPU_REQ if cur_process.remaining_time > 0 else EventTypes.PROC_CPU_DONE)


class SRTF(SchedulerDES):
    """SRTF(Shortest Remaining Time First) is a preemptive scheduling algorithm,
    meaning that the process currently running on the CPU 
    can be interrupted in favor of another process. 
    It prioritises processes which expect to be serviced sooner.
    """
    def scheduler_func(self, cur_event):
        x=sorted(self.processes,key=lambda p:p.remaining_time)
        for process in x:
            if process.process_state==process.process_state.READY:
                return process
            else:
                continue

    def dispatcher_func(self, cur_process):
        time_run_for=cur_process.run_for(self.next_event_time()-self.time,self.time)
        cur_process.process_state = ProcessStates.READY if cur_process.remaining_time > 0 else ProcessStates.TERMINATED
        return Event(process_id=cur_process.process_id,
                    event_time=self.time + time_run_for,
                    event_type=EventTypes.PROC_CPU_REQ if cur_process.remaining_time > 0 else EventTypes.PROC_CPU_DONE)
