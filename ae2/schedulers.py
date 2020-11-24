from des import SchedulerDES
from event import Event, EventTypes
from process import Process, ProcessStates
class RR(SchedulerDES):
    def scheduler_func(self, cur_event):
        return self.processes[cur_event.process_id]
    def dispatcher_func(self, cur_process):
        time_run_for = cur_process.run_for(self.quantum, self.time)
        cur_process.process_state = ProcessStates.READY if cur_process.remaining_time > 0 else ProcessStates.TERMINATED
        return Event(process_id=cur_process.process_id, event_time=self.time + time_run_for, event_type=EventTypes.PROC_CPU_REQ if cur_process.remaining_time > 0 else EventTypes.PROC_CPU_DONE)
class FCFS(RR):
    def dispatcher_func(self, cur_process):
        self.quantum = cur_process.service_time
        return super().dispatcher_func(cur_process)
class SJF(FCFS):
    def scheduler_func(self, cur_event):
        return sorted(filter(lambda p : p.process_state==ProcessStates.READY, self.processes), key=lambda p : p.service_time)[0]
class SRTF(RR):
    def scheduler_func(self, cur_event):
        return sorted(filter(lambda p : p.process_state==ProcessStates.READY, self.processes), key=lambda p : p.remaining_time)[0]
    def dispatcher_func(self, cur_process):
        self.quantum = self.next_event_time()-self.time
        return super().dispatcher_func(cur_process)