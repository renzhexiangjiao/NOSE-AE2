from des import SchedulerDES
from event import Event, EventTypes
from process import Process, ProcessStates
class RR(SchedulerDES):
    def scheduler_func(self, cur_event):
        return sorted(filter(lambda p:p.process_state==ProcessStates.READY,self.processes),key=lambda p:p.service_time if type(self)==SJF else p.remaining_time)[0] if type(self) in [SJF,SRTF] else self.processes[cur_event.process_id]
    def dispatcher_func(self, cur_process):
        time_run_for = cur_process.run_for(self.quantum if type(self)==RR else self.next_event_time()-self.time if type(self)==SRTF else cur_process.service_time,self.time)
        cur_process.process_state=ProcessStates.READY if cur_process.remaining_time>0 else ProcessStates.TERMINATED
        return Event(process_id=cur_process.process_id,event_time=self.time+time_run_for,event_type=EventTypes.PROC_CPU_REQ if cur_process.remaining_time>0 else EventTypes.PROC_CPU_DONE)
class FCFS(RR):
    pass
class SJF(RR):
    pass
class SRTF(RR):
    pass