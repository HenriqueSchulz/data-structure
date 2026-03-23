import random
import tracemalloc
import psutil
import os
import statistics
import matplotlib.pyplot as plt
import time  # <-- added

from collections import defaultdict
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
        self.search_tree_unbalanced = None
        self.hash_table = None
        self.results = []

        os.makedirs("results", exist_ok=True)
        os.makedirs("results/insertion", exist_ok=True)
        os.makedirs("results/search", exist_ok=True)

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
                ["BinaryTree (Balanced)", "INSERT",
                 *self.binary_tree_insert(data, process)]
            )

            rows.append(
                ["BinaryTree (Unbalanced)", "INSERT",
                 *self.binary_tree_insert_unbalanced(data, process)]
            )

            rows.append(
                ["HashTable", "INSERT", *self.hash_table_insert(data, process)]
            )

            # SEARCH
            rows.append(
                ["LinearArray", "SEARCH", *self.linear_array_search(data, process)]
            )

            rows.append(
                ["BinaryTree (Balanced)", "SEARCH",
                 *self.binary_tree_search(data, process)]
            )

            rows.append(
                ["BinaryTree (Unbalanced)", "SEARCH",
                 *self.binary_tree_search_unbalanced(data, process)]
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

            for row in rows:
                self.results.append({
                    "size": size,
                    "structure": row[0],
                    "operation": row[1],
                    "cpu_time": row[2],
                    "memory": row[3],
                    "cpu_peak": row[4],
                    "iterations": row[5] if len(row) > 5 else None
                })

        self.generate_graphs()

    def linear_array_insert(self, data: list[Data], process):

        cpu_times, mem_peaks, cpu_peaks, iterations = [], [], [], []

        for _ in range(self.rounds):

            self.linear_array = LinearArray(len(data))

            tracemalloc.start()
            cpu_start = time.perf_counter()

            monitor = CPUMonitor()
            monitor.start()
            
            total_iter = 0
            for d in data:
                total_iter += self.linear_array.insert(d)

            cpu_end = time.perf_counter()
            _, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()

            peak_cpu = monitor.stop()

            cpu_time = cpu_end - cpu_start

            cpu_times.append(cpu_time)
            mem_peaks.append(peak / 1024)
            cpu_peaks.append(peak_cpu)
            iterations.append(total_iter / len(data))

        return (
            round(statistics.mean(cpu_times), 6),
            round(statistics.mean(mem_peaks), 2),
            round(statistics.mean(cpu_peaks), 2),
            round(statistics.mean(iterations), 2)
        )

    def binary_tree_insert(self, data: list[Data], process):

        cpu_times, mem_peaks, cpu_peaks, iterations = [], [], [], []

        for _ in range(self.rounds):

            self.search_tree = SearchTree(balance=True)

            tracemalloc.start()
            cpu_start = time.perf_counter()

            monitor = CPUMonitor()
            monitor.start()

            total_iter = 0
            for d in data:
                total_iter += self.search_tree.insert(d)

            cpu_end = time.perf_counter()
            _, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()

            peak_cpu = monitor.stop()

            cpu_time = cpu_end - cpu_start

            cpu_times.append(cpu_time)
            mem_peaks.append(peak / 1024)
            cpu_peaks.append(peak_cpu)
            iterations.append(total_iter / len(data))

        return (
            round(statistics.mean(cpu_times), 6),
            round(statistics.mean(mem_peaks), 2),
            round(statistics.mean(cpu_peaks), 2),
            round(statistics.mean(iterations), 2)
        )

    def binary_tree_insert_unbalanced(self, data: list[Data], process):

        cpu_times, mem_peaks, cpu_peaks, iterations = [], [], [], []

        for _ in range(self.rounds):

            self.search_tree_unbalanced = SearchTree(balance=False)

            tracemalloc.start()
            cpu_start = time.perf_counter()

            monitor = CPUMonitor()
            monitor.start()

            total_iter = 0
            for d in data:
                total_iter += self.search_tree_unbalanced.insert(d)

            cpu_end = time.perf_counter()
            _, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()

            peak_cpu = monitor.stop()

            cpu_time = cpu_end - cpu_start

            cpu_times.append(cpu_time)
            mem_peaks.append(peak / 1024)
            cpu_peaks.append(peak_cpu)
            iterations.append(total_iter / len(data))

        return (
            round(statistics.mean(cpu_times), 6),
            round(statistics.mean(mem_peaks), 2),
            round(statistics.mean(cpu_peaks), 2),
            round(statistics.mean(iterations), 2)
        )

    def hash_table_insert(self, data: list[Data], process):

        cpu_times, mem_peaks, cpu_peaks, iterations = [], [], [], []

        for _ in range(self.rounds):

            self.hash_table = HashTable(len(data)//2)

            tracemalloc.start()
            cpu_start = time.perf_counter()

            monitor = CPUMonitor()
            monitor.start()

            total_iter = 0
            for d in data:
                total_iter += self.hash_table.insert(d)
            
            cpu_end = time.perf_counter()
            _, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()

            peak_cpu = monitor.stop()

            cpu_time = cpu_end - cpu_start

            cpu_times.append(cpu_time)
            mem_peaks.append(peak / 1024)
            cpu_peaks.append(peak_cpu)
            iterations.append(total_iter / len(data))

        return (
            round(statistics.mean(cpu_times), 6),
            round(statistics.mean(mem_peaks), 2),
            round(statistics.mean(cpu_peaks), 2),
            round(statistics.mean(iterations), 2)
        )

    def linear_array_search(self, data: list[Data], process):

        cpu_times, mem_peaks, cpu_peaks, iterations = [], [], [], []

        searches = len(data) * 0.01

        for _ in range(self.rounds):

            tracemalloc.start()
            cpu_start = time.perf_counter()

            monitor = CPUMonitor()
            monitor.start()

            total_iter = 0

            for _ in range(int(searches)):
                value = random.choice(data)
                _, it = self.linear_array.get(value.salary)
                total_iter += it

            cpu_end = time.perf_counter()
            _, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()

            peak_cpu = monitor.stop()

            cpu_time = cpu_end - cpu_start

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
            cpu_start = time.perf_counter()

            monitor = CPUMonitor()
            monitor.start()

            total_iter = 0

            for _ in range(int(searches)):
                value = random.choice(data)
                _, it = self.search_tree.get(value.salary)
                total_iter += it

            cpu_end = time.perf_counter()
            _, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()

            peak_cpu = monitor.stop()

            cpu_time = cpu_end - cpu_start

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

    def binary_tree_search_unbalanced(self, data: list[Data], process):

        cpu_times, mem_peaks, cpu_peaks, iterations = [], [], [], []

        searches = len(data) * 0.01

        for _ in range(self.rounds):

            tracemalloc.start()
            cpu_start = time.perf_counter()

            monitor = CPUMonitor()
            monitor.start()

            total_iter = 0

            for _ in range(int(searches)):
                value = random.choice(data)
                _, it = self.search_tree_unbalanced.get(value.salary)
                total_iter += it

            cpu_end = time.perf_counter()
            _, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()

            peak_cpu = monitor.stop()

            cpu_time = cpu_end - cpu_start

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
            cpu_start = time.perf_counter()

            monitor = CPUMonitor()
            monitor.start()

            total_iter = 0

            for _ in range(int(searches)):
                value = random.choice(data)
                _, it = self.hash_table.get(value.salary)
                total_iter += it

            cpu_end = time.perf_counter()
            _, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()

            peak_cpu = monitor.stop()

            cpu_time = cpu_end - cpu_start

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

    def generate_graphs(self):

        metrics = {
            "cpu_time": "CPU Time (s)",
            "memory": "Memory Peak (KB)",
            "cpu_peak": "CPU Peak (%)",
            "iterations": "Avg Iterations"
        }

        operations = {
            "INSERT": "insertion",
            "SEARCH": "search"
        }

        for op_key, folder in operations.items():

            op_data = [r for r in self.results if r["operation"] == op_key]

            for metric, label in metrics.items():

                grouped = defaultdict(lambda: defaultdict(list))

                for r in op_data:
                    if r[metric] is None:
                        continue
                    grouped[r["structure"]][r["size"]].append(r[metric])

                plt.figure()

                for structure, sizes_dict in grouped.items():

                    sizes = sorted(sizes_dict.keys())
                    values = [
                        sum(sizes_dict[s]) / len(sizes_dict[s])
                        for s in sizes
                    ]

                    plt.plot(sizes, values, marker='o', label=structure)

                plt.xlabel("Input Size")
                plt.ylabel(label)
                plt.title(f"{label} ({op_key})")
                plt.legend()
                plt.grid()

                path = f"results/{folder}/{metric}.png"
                plt.savefig(path)
                plt.close()