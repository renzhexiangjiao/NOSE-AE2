from des import SchedulerDES
from event import Event, EventTypes
from process import Process, ProcessStates

class FCFS(SchedulerDES):
    """FCFS(First Come First Serve) is a non-preemptive scheduling algorithm,
    meaning that the processes are executed wholly without interruption.
    Processes are scheduled in order of their arrival.
    """
    def scheduler_func(self, cur_event):
        # events of type PROC_ARRIVES happen in order of processes' arrivals, therefore:
        return self.processes[cur_event.process_id]
        # no need to account for PROC_CPU_DONE events returned by the dispatcher as they are not pushed onto the events queue

    def dispatcher_func(self, cur_process):
        # this scheduling algorithm is non-preemptive, so the processes will run for its entire length
        # process state is always set to TERMINATED and the returned event is always of type PROC_CPU_DONE
        time_run_for = cur_process.run_for(cur_process.service_time, self.time)
        cur_process.process_state = ProcessStates.TERMINATED
        return Event(process_id=cur_process.process_id,
                    event_time=self.time + time_run_for,
                    event_type=EventTypes.PROC_CPU_DONE)


class SJF(FCFS): # also a non-preemptive scheduling algorithm, so inherits from FCFS
    """SJF(Shortest Job First) is a non-preemptive scheduling algorithm,
    meaning that the processes are executed wholly without interruption.
    Processes are scheduled according to their service time,
    with the shortest one first.
    """
    def scheduler_func(self, cur_event):
        # return a READY process with the shortest service time
        return sorted(filter(lambda p: p.process_state==ProcessStates.READY, self.processes), key=lambda p : p.service_time)[0]

    # SJF's dispatcher is identical to FCFS's, no need to rewrite it 


class RR(SchedulerDES):
    """RR(Round Robin) is a preemptive scheduling algorithm,
    meaning that the process currently running on the CPU 
    can be interrupted in favor of another process.
    It interleaves the execution of processes which were not fully serviced.
    """
    def scheduler_func(self, cur_event):
        # returns the process which caused the first event in the event queue
        # could be either a PROC_ARRIVES or PROC_CPU_REQ event because PROC_CPU_DONE events are not pushed onto the queue
        return self.processes[cur_event.process_id]

    def dispatcher_func(self, cur_process):
        # runs a process for a quantum of time
        # if afterwards the process is finished:
        #    sets its state to TERMINATED
        #    returns an event of type PROC_CPU_DONE
        # if it still requires some more time on the CPU:
        #    sets its state to READY
        #    returns an event of type PROC_CPU_REQ
        time_run_for = cur_process.run_for(self.quantum, self.time)
        cur_process.process_state = ProcessStates.READY if cur_process.remaining_time > 0 else ProcessStates.TERMINATED
        return Event(process_id=cur_process.process_id,
                    event_time=self.time + time_run_for,
                    event_type=EventTypes.PROC_CPU_REQ if cur_process.remaining_time > 0 else EventTypes.PROC_CPU_DONE)


class SRTF(RR): # also a preemptive scheduling algorithm, so inherits from RR
    """SRTF(Shortest Remaining Time First) is a preemptive scheduling algorithm,
    meaning that the process currently running on the CPU 
    can be interrupted in favor of another process. 
    It prioritises processes which expect to be serviced sooner.
    """
    def scheduler_func(self, cur_event):
        # this scheduler should return a process whose remaining time is the shortest
        ready_procs_sorted = sorted(filter(lambda p: p.process_state==ProcessStates.READY, self.processes), key=lambda p : p.remaining_time)
        # we implemented an optimisation in which the context switch time is also taken into account
        # when a new (very short) process arrives during the execution of another process,
        # this scheduer may still decide to finish running the current process if 
        # (context switch time + service time of the arriving process) is greater than the current process's remaining time
        if self.process_on_cpu == None or \
            self.process_on_cpu.process_state == ProcessStates.TERMINATED or \
            self.process_on_cpu.remaining_time > self.context_switch_time + ready_procs_sorted[0].remaining_time:
            return ready_procs_sorted[0]
        return self.process_on_cpu

        # this is the version without optimisation:
        return ready_procs_sorted[0]

    def dispatcher_func(self, cur_process):
        # RR's dispatcher will run the current process for the time of self.quantum, 
        # so we replace it with the appropriate time duration for SRTF and call RR's dispatcher
        self.quantum = self.next_event_time()-self.time 
        return super().dispatcher_func(cur_process)
