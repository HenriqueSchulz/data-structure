import random
import tracemalloc
import psutil
import os
import statistics

from algorithms import HashTable, SearchTree, LinearArray
from benchmark.CPUMonitor import CPUMonitor


class Benchmark:
    '''Performs benchmarks on different data structures and algorithms.'''
    
    def __init__(self, rounds: int = 5):
        self.rounds = rounds

    @staticmethod
    def get_cpu_cores():
        print("\nLogical cores:", psutil.cpu_count())
        print("Physical cores:", psutil.cpu_count(logical=False))

    def run_search_tree_test(self, balance=True, sizes=[1000, 10000, 100000]):
        '''Tests insertion performance of SearchTree with or without balancing.'''

        process = psutil.Process(os.getpid())

        print(f"\nTesting insertion on Search Tree {'with' if balance else 'without'} balancing")

        for size in sizes:

            cpu_times = []
            mem_peaks = []
            rss_values = []
            cpu_peaks = []

            print("\n-----------------------------")
            print(f"Size={size}")

            for r in range(self.rounds):

                tree = SearchTree(balance=balance)

                tracemalloc.start()
                cpu_start = process.cpu_times()

                monitor = CPUMonitor()
                monitor.start()

                for _ in range(size):
                    value = random.randint(1000, 9999)
                    tree.insert(value)

                cpu_end = process.cpu_times()
                _, peak = tracemalloc.get_traced_memory()
                tracemalloc.stop()
                peak_cpu = monitor.stop()

                cpu_time = (cpu_end.user - cpu_start.user) + (cpu_end.system - cpu_start.system)
                memory_rss = process.memory_info().rss / (1024 * 1024)

                cpu_times.append(cpu_time)
                mem_peaks.append(peak / 1024)
                rss_values.append(memory_rss)
                cpu_peaks.append(peak_cpu)

                print(f"Round {r+1}: CPU {cpu_time:.4f}s | Mem {peak/1024:.2f}KB | CPU Peak {peak_cpu:.2f}%")

            print("\nResults (mean ± stddev)")
            print(f"CPU time: {statistics.mean(cpu_times):.4f} ± {statistics.stdev(cpu_times):.4f} s")
            print(f"Memory Peak (tracemalloc): {statistics.mean(mem_peaks):.2f} ± {statistics.stdev(mem_peaks):.2f} KB")
            print(f"Memory Process (RSS): {statistics.mean(rss_values):.2f} ± {statistics.stdev(rss_values):.2f} MB")
            print(f"CPU Peak: {statistics.mean(cpu_peaks):.2f} ± {statistics.stdev(cpu_peaks):.2f}%")

    def run_hash_table_test(self, sizes: list, hash_type: str = 'modular'):
        '''Tests insertion performance of HashTable.'''

        process = psutil.Process(os.getpid())

        print("\nTesting HashTable")

        for size in sizes:

            cpu_times = []
            mem_peaks = []
            rss_values = []
            cpu_peaks = []

            print("\n-----------------------------")
            print(f"Size={size}")

            for r in range(self.rounds):

                table = HashTable(size=size, hash_type=hash_type)

                tracemalloc.start()
                cpu_start = process.cpu_times()

                monitor = CPUMonitor()
                monitor.start()

                for _ in range(size):
                    value = random.randint(1000, 9999)
                    table.insert(value, value)

                cpu_end = process.cpu_times()
                _, peak = tracemalloc.get_traced_memory()
                tracemalloc.stop()

                peak_cpu = monitor.stop()

                cpu_time = (cpu_end.user - cpu_start.user) + (cpu_end.system - cpu_start.system)
                memory_rss = process.memory_info().rss / (1024 * 1024)

                cpu_times.append(cpu_time)
                mem_peaks.append(peak / 1024)
                rss_values.append(memory_rss)
                cpu_peaks.append(peak_cpu)

                print(f"Round {r+1}: CPU {cpu_time:.4f}s | Mem {peak/1024:.2f}KB | CPU Peak {peak_cpu:.2f}%")

            print("\nResults (mean ± stddev)")
            print(f"CPU time: {statistics.mean(cpu_times):.4f} ± {statistics.stdev(cpu_times):.4f} s")
            print(f"Memory Peak (tracemalloc): {statistics.mean(mem_peaks):.2f} ± {statistics.stdev(mem_peaks):.2f} KB")
            print(f"Memory Process (RSS): {statistics.mean(rss_values):.2f} ± {statistics.stdev(rss_values):.2f} MB")
            print(f"CPU Peak: {statistics.mean(cpu_peaks):.2f} ± {statistics.stdev(cpu_peaks):.2f}%")
    
    def run_linear_array_test(self, sizes=[1000, 10000, 100000]):
        '''Tests insertion performance of LinearArray.'''

        process = psutil.Process(os.getpid())

        print("\nTesting LinearArray")

        for size in sizes:

            cpu_times = []
            mem_peaks = []
            rss_values = []
            cpu_peaks = []

            print("\n-----------------------------")
            print(f"Size={size}")

            for r in range(self.rounds):

                array = LinearArray(size)

                tracemalloc.start()
                cpu_start = process.cpu_times()

                monitor = CPUMonitor()
                monitor.start()

                for _ in range(size):
                    value = random.randint(1000, 9999)
                    array.insert(value)

                cpu_end = process.cpu_times()
                _, peak = tracemalloc.get_traced_memory()
                tracemalloc.stop()

                peak_cpu = monitor.stop()

                cpu_time = (cpu_end.user - cpu_start.user) + (cpu_end.system - cpu_start.system)
                memory_rss = process.memory_info().rss / (1024 * 1024)

                cpu_times.append(cpu_time)
                mem_peaks.append(peak / 1024)
                rss_values.append(memory_rss)
                cpu_peaks.append(peak_cpu)

                print(f"Round {r+1}: CPU {cpu_time:.4f}s | Mem {peak/1024:.2f}KB | CPU Peak {peak_cpu:.2f}%")

            print("\nResults (mean ± stddev)")
            print(f"CPU time: {statistics.mean(cpu_times):.4f} ± {statistics.stdev(cpu_times):.4f} s")
            print(f"Memory Peak (tracemalloc): {statistics.mean(mem_peaks):.2f} ± {statistics.stdev(mem_peaks):.2f} KB")
            print(f"Memory Process (RSS): {statistics.mean(rss_values):.2f} ± {statistics.stdev(rss_values):.2f} MB")
            print(f"CPU Peak: {statistics.mean(cpu_peaks):.2f} ± {statistics.stdev(cpu_peaks):.2f}%")