# NOSE-AE2
Implementation of schedulers and dispatchers for FCFS, SJF, SRTF, RR scheduling algorithms.

# Ben Johnston 2432411J Lab 01
# Franciszek Sowul 2482997S Lab 10

>>> Your report should include a heading stating your full names, matriculation
numbers and lab groups, and a discussion of your findings for the “interesting” seed
values outlined earlier (i.e., what was the relative performance of the four algorithms,
whether it deviated from your expectations, and what you believe is the cause of the
deviation based on the internal state of the simulator). Feel free to also include any
feedback you may have on the assessed exercise.

![](avg_waiting_time.png)

On average FCFS waiting time and RR waiting time are identical so it is weird when they differ alot.
We can also see that the waiting time for for SRTF is less than the SJF waiting time.
Another observation is that we can see that FCFS and RR wait times on average are very similar however we found if all processes are long RR performs worse than FCFS for the seed 4243287395.
![](avg_turnaround_time.png)

We also know that turnaround time = waiting time + service time so the trends described above and the statements on the performance of algorithms compared to the others will stay the same.

For the two seeds given in the sample outputs in the specification we see that the seed 1523376833 has lower wait and turnaround times on average for all schedulers in comparison to the seed 3672961927.

Seed 3162636434:

FCFS
![](316fcfs.png)
RR
![](316rr.png)
As we can see all processes have a a very short service time and when the service time is less than the RR quantum, FCFS and RR proceed identically.

SJF
![](316sjf.png)
SRTF
![](316srtf.png)
Finnaly, we see that the SRTF scheduler will keep processing the process identically to SJF unless the next process's burst time is less than the current process time remaining and both schedulers still follow the shortest time first as we can see the longer processes 2 and 3 are performed last in both schedulers.


Seed 317537355:

FCFS
![](317fcfs.png)
RR
![](317rr.png)
As we see for this seed most processes have a very long service time, and both schedulers act extremely different, the RR is choosing to take smaller chunks with less service time in comparison to the FCFS.

SJF
![](317sjf.png)
SRTF
![](317srtf.png)

As we see SJF will execute process 8 right after it has finished executing process 0 as 8 has the next shortest job but where it varies from SRTF is when SRTF aknowledges another process with a shorter run time it will break up processes into chunks and will prioritise the shortest job.

We can see with both these seeds, one illustrating the effect of shorter service times and one of longer service times the difference of these schedulers with different processes.



When testing our schedulers with the test seeds we were pleased to see that the values we got for our average turnaround time and our average wait times were as expected.
Some brief feeeedback that I personally have is that this excercise actually helped me visualize the differences and also similarities between schedulers and also the differences between pre-emptive and non pre-emptive scheduling.
