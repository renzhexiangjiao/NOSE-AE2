import argparse
import logging
import sys
import matplotlib.pyplot as plt

from numpy import random, linspace

from des import SchedulerDES
from schedulers import FCFS, SJF, RR, SRTF

# default values
seed = int.from_bytes(random.bytes(4), byteorder="little")
num_processes = 10
arrivals_per_time_unit = 3.0
avg_cpu_burst_time = 2
quantum = 0.5
context_switch_time = 0.0
logging.basicConfig(level=logging.WARNING, stream=sys.stderr)

# parse arguments
parser = argparse.ArgumentParser(description='NOSE2 AE2: Discrete Event Simulation')
parser.add_argument('--seed', '-S', help='PRNG random seed value', type=int)
parser.add_argument('--processes', '-P', help='Number of processes to simulate', default=num_processes, type=int)
parser.add_argument('--arrivals', '-L', help='Avg number of process arrivals per time unit',
                    default=arrivals_per_time_unit, type=float)
parser.add_argument('--cpu_time', '-c', help='Avg duration of CPU burst', default=avg_cpu_burst_time, type=float)
parser.add_argument('--cs_time', '-x', help='Duration of each context switch', default=context_switch_time, type=float)
parser.add_argument('--quantum', '-q', help='Duration of each quantum (Round Robin scheduling)', default=quantum,
                    type=float)
parser.add_argument('--verbose', '-v', help='Turn logging on; specify multiple times for more verbosity',
                    action='count')
args = parser.parse_args()
if args.seed:
    seed = args.seed
if args.verbose == 1:
    logging.getLogger().setLevel(logging.INFO)
elif args.verbose is not None:
    logging.getLogger().setLevel(logging.DEBUG)
num_processes = args.processes
arrivals_per_time_unit = args.arrivals
avg_cpu_burst_time = args.cpu_time
context_switch_time = args.cs_time
quantum = args.quantum

data = {'FCFS':list(),
        'SJF' :list(),
        'RR'  :list(),
        'SRTF':list()}

stats_turnaround = {'FCFS':{'expected':9.562, 'deviation':3.943},
                    'SJF' :{'expected':6.413, 'deviation':2.721},
                    'RR'  :{'expected':9.557, 'deviation':3.934},
                    'SRTF':{'expected':5.549, 'deviation':2.211}}

stats_waiting = {'FCFS':{'expected':7.551, 'deviation':3.388},
                 'SJF' :{'expected':4.402, 'deviation':2.199},
                 'RR'  :{'expected':7.555, 'deviation':3.388},
                 'SRTF':{'expected':3.549, 'deviation':1.653}}

interesing_seed_list = list()

for i in range(10000):
    #print("NOSE2 :: AE2 :: Scheduler Discrete Event Simulation")
    #print("---------------------------------------------------")

    seed = int.from_bytes(random.bytes(4), byteorder='little')

    # print input specification
    #print("Using seed: " + str(seed))
    #base_sim = SchedulerDES(num_processes=num_processes, arrivals_per_time_unit=arrivals_per_time_unit,
    #                        avg_cpu_burst_time=avg_cpu_burst_time)
    #base_sim.generate_and_init(seed)
    #print("Processes to be executed:")
    #base_sim.print_processes()

    # instantiate simulators
    simulators = [FCFS(num_processes=num_processes, arrivals_per_time_unit=arrivals_per_time_unit,
                       avg_cpu_burst_time=avg_cpu_burst_time, context_switch_time=context_switch_time),
                  SJF(num_processes=num_processes, arrivals_per_time_unit=arrivals_per_time_unit,
                       avg_cpu_burst_time=avg_cpu_burst_time, context_switch_time=context_switch_time),
                  RR(num_processes=num_processes, arrivals_per_time_unit=arrivals_per_time_unit,
                       avg_cpu_burst_time=avg_cpu_burst_time, context_switch_time=context_switch_time, quantum=quantum),
                  SRTF(num_processes=num_processes, arrivals_per_time_unit=arrivals_per_time_unit,
                       avg_cpu_burst_time=avg_cpu_burst_time, context_switch_time=context_switch_time)]

    weirdness = 0

    # run simulators
    for sim in simulators:
        #print("-----")
        #print(sim.full_name() + ":")
        #logging.info("--- " + sim.full_name() + " ---")
        sim.run(seed)
        turnaround, waiting = sim.print_statistics()
        data[sim.simple_name()].append(waiting)

        weirdness += abs(waiting-stats_waiting[sim.simple_name()]['expected'])/stats_waiting[sim.simple_name()]['deviation']

    interesing_seed_list.append((seed, weirdness))

    if i % 1000 == 0:
        print(i / 1000, '%')
    
colors = iter(['red', 'blue', 'green', 'yellow'])

for sim, values in data.items():
    plt.hist(values, 300, density=True, alpha=0.5, color=next(colors), label=sim)
    EX = sum(values)/len(values)
    EXX = sum(map(lambda x:x*x, values))/len(values)
    VARX = EXX - EX*EX
    STDX = VARX**0.5
    print(sim, "E(X):", EX, "E(X^2):", EXX, "Var(X):", VARX, "sigma(X):", STDX)
plt.legend(loc='upper right')
plt.title('Avg waiting time')
plt.yticks([])
plt.show()

interesing_seed_list.sort(key=lambda x:-x[1])
for seed in range(10):
    print(interesing_seed_list[seed])

