import random
import tracemalloc
import psutil
import os
import statistics

from tabulate import tabulate
from algorithms import HashTable, SearchTree, LinearArray
from benchmark.CPUMonitor import CPUMonitor
from data import DataGenerator, Data


class Benchmark:
    '''Performs benchmarks on different data structures and algorithms.'''

    def __init__(self, rounds: int = 5, sizes: list = [100, 200, 400, 800, 1600]):

        self.rounds = rounds
        self.sizes = sizes
        self.linear_array = None
        self.search_tree = None
        self.hash_table = None

    @staticmethod
    def get_cpu_cores():
        rows = [
            ["Logical cores", psutil.cpu_count()],
            ["Physical cores", psutil.cpu_count(logical=False)]
        ]
        print(tabulate(rows, headers=["Metric", "Value"], tablefmt="grid"))

    def run(self):

        process = psutil.Process(os.getpid())

        for size in self.sizes:

            data = DataGenerator.generate(size)

            rows = []

            # INSERT
            rows.append(
                ["LinearArray", "INSERT", *self.linear_array_insert(data, process)]
            )

            rows.append(
                ["BinaryTree", "INSERT", *self.binary_tree_insert(data, process)]
            )

            rows.append(
                ["HashTable", "INSERT", *self.hash_table_insert(data, process)]
            )

            # SEARCH
            rows.append(
                ["LinearArray", "SEARCH", *self.linear_array_search(data, process)]
            )

            rows.append(
                ["BinaryTree", "SEARCH", *self.binary_tree_search(data, process)]
            )

            rows.append(
                ["HashTable", "SEARCH", *self.hash_table_search(data, process)]
            )

            headers = [
                f"Structure (Size={size})",
                "Operation",
                "CPU Time (s)",
                "Memory Peak (KB)",
                "CPU Peak (%)",
                "Avg Iterations"
            ]

            print("\n")
            print(tabulate(rows, headers=headers, tablefmt="grid"))

    def linear_array_insert(self, data: list[Data], process):

        cpu_times, mem_peaks, cpu_peaks = [], [], []

        for _ in range(self.rounds):

            self.linear_array = LinearArray(len(data))

            tracemalloc.start()
            cpu_start = process.cpu_times()

            monitor = CPUMonitor()
            monitor.start()

            for d in data:
                self.linear_array.insert(d)

            cpu_end = process.cpu_times()
            _, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()

            peak_cpu = monitor.stop()

            cpu_time = (cpu_end.user - cpu_start.user) + (cpu_end.system - cpu_start.system)

            cpu_times.append(cpu_time)
            mem_peaks.append(peak / 1024)
            cpu_peaks.append(peak_cpu)

        return (
            round(statistics.mean(cpu_times), 6),
            round(statistics.mean(mem_peaks), 2),
            round(statistics.mean(cpu_peaks), 2)
        )

    def binary_tree_insert(self, data: list[Data], process):

        cpu_times, mem_peaks, cpu_peaks = [], [], []

        for _ in range(self.rounds):

            self.search_tree = SearchTree()

            tracemalloc.start()
            cpu_start = process.cpu_times()

            monitor = CPUMonitor()
            monitor.start()

            for d in data:
                self.search_tree.insert(d)

            cpu_end = process.cpu_times()
            _, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()

            peak_cpu = monitor.stop()

            cpu_time = (cpu_end.user - cpu_start.user) + (cpu_end.system - cpu_start.system)

            cpu_times.append(cpu_time)
            mem_peaks.append(peak / 1024)
            cpu_peaks.append(peak_cpu)

        return (
            round(statistics.mean(cpu_times), 6),
            round(statistics.mean(mem_peaks), 2),
            round(statistics.mean(cpu_peaks), 2)
        )

    def hash_table_insert(self, data: list[Data], process):

        cpu_times, mem_peaks, cpu_peaks = [], [], []

        for _ in range(self.rounds):

            self.hash_table = HashTable(len(data))

            tracemalloc.start()
            cpu_start = process.cpu_times()

            monitor = CPUMonitor()
            monitor.start()

            for d in data:
                self.hash_table.insert(d)

            cpu_end = process.cpu_times()
            _, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()

            peak_cpu = monitor.stop()

            cpu_time = (cpu_end.user - cpu_start.user) + (cpu_end.system - cpu_start.system)

            cpu_times.append(cpu_time)
            mem_peaks.append(peak / 1024)
            cpu_peaks.append(peak_cpu)

        return (
            round(statistics.mean(cpu_times), 6),
            round(statistics.mean(mem_peaks), 2),
            round(statistics.mean(cpu_peaks), 2)
        )

    def linear_array_search(self, data: list[Data], process):

        cpu_times, mem_peaks, cpu_peaks, iterations = [], [], [], []

        searches = len(data) * 0.01

        for _ in range(self.rounds):

            tracemalloc.start()
            cpu_start = process.cpu_times()

            monitor = CPUMonitor()
            monitor.start()

            total_iter = 0

            for _ in range(int(searches)):
                value = random.choice(data)
                _, it = self.linear_array.get(value.salary)
                total_iter += it

            cpu_end = process.cpu_times()
            _, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()

            peak_cpu = monitor.stop()

            cpu_time = (cpu_end.user - cpu_start.user) + (cpu_end.system - cpu_start.system)

            cpu_times.append(cpu_time)
            mem_peaks.append(peak / 1024)
            cpu_peaks.append(peak_cpu)
            iterations.append(total_iter / searches)

        return (
            round(statistics.mean(cpu_times), 6),
            round(statistics.mean(mem_peaks), 2),
            round(statistics.mean(cpu_peaks), 2),
            round(statistics.mean(iterations), 2)
        )

    def binary_tree_search(self, data: list[Data], process):

        cpu_times, mem_peaks, cpu_peaks, iterations = [], [], [], []

        searches = len(data) * 0.01

        for _ in range(self.rounds):

            tracemalloc.start()
            cpu_start = process.cpu_times()

            monitor = CPUMonitor()
            monitor.start()

            total_iter = 0

            for _ in range(int(searches)):
                value = random.choice(data)
                _, it = self.search_tree.get(value.salary)
                total_iter += it

            cpu_end = process.cpu_times()
            _, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()

            peak_cpu = monitor.stop()

            cpu_time = (cpu_end.user - cpu_start.user) + (cpu_end.system - cpu_start.system)

            cpu_times.append(cpu_time)
            mem_peaks.append(peak / 1024)
            cpu_peaks.append(peak_cpu)
            iterations.append(total_iter / searches)

        return (
            round(statistics.mean(cpu_times), 6),
            round(statistics.mean(mem_peaks), 2),
            round(statistics.mean(cpu_peaks), 2),
            round(statistics.mean(iterations), 2)
        )

    def hash_table_search(self, data: list[Data], process):

        cpu_times, mem_peaks, cpu_peaks, iterations = [], [], [], []

        searches = len(data) * 0.01

        for _ in range(self.rounds):

            tracemalloc.start()
            cpu_start = process.cpu_times()

            monitor = CPUMonitor()
            monitor.start()

            total_iter = 0

            for _ in range(int(searches)):
                value = random.choice(data)
                _, it = self.hash_table.get(value.salary)
                total_iter += it

            cpu_end = process.cpu_times()
            _, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()

            peak_cpu = monitor.stop()

            cpu_time = (cpu_end.user - cpu_start.user) + (cpu_end.system - cpu_start.system)

            cpu_times.append(cpu_time)
            mem_peaks.append(peak / 1024)
            cpu_peaks.append(peak_cpu)
            iterations.append(total_iter / searches)

        return (
            round(statistics.mean(cpu_times), 6),
            round(statistics.mean(mem_peaks), 2),
            round(statistics.mean(cpu_peaks), 2),
            round(statistics.mean(iterations), 2)
        )