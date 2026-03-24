import random
import tracemalloc
import psutil
import os
import statistics
import matplotlib.pyplot as plt
import time

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
        self.results = []

        # Defines all benchmarked structures and their behaviors
        self.tests = [
            {
                "name": "LinearArray",
                "factory": lambda size: LinearArray(size),
                "insert": lambda ds, d: ds.insert(d),
                "search": lambda ds, d: ds.get(d.salary),
            },
            {
                "name": "BinaryTree (Balanced)",
                "factory": lambda size: SearchTree(balance=True),
                "insert": lambda ds, d: ds.insert(d),
                "search": lambda ds, d: ds.get(d.salary),
            },
            {
                "name": "BinaryTree (Unbalanced)",
                "factory": lambda size: SearchTree(balance=False),
                "insert": lambda ds, d: ds.insert(d),
                "search": lambda ds, d: ds.get(d.salary),
            },
            {
                "name": "HashTable (Modular)",
                "factory": lambda size: HashTable(size // 2, "modular"),
                "insert": lambda ds, d: ds.insert(d),
                "search": lambda ds, d: ds.get(d.salary),
            },
            {
                "name": "HashTable (Multiplicative)",
                "factory": lambda size: HashTable(size // 2, "multiplicative"),
                "insert": lambda ds, d: ds.insert(d),
                "search": lambda ds, d: ds.get(d.salary),
            },
            {
                "name": "HashTable (Universal)",
                "factory": lambda size: HashTable(size // 2, "universal"),
                "insert": lambda ds, d: ds.insert(d),
                "search": lambda ds, d: ds.get(d.salary),
            },
        ]

        os.makedirs("results", exist_ok=True)
        os.makedirs("results/insertion", exist_ok=True)
        os.makedirs("results/search", exist_ok=True)

    @staticmethod
    def get_cpu_cores():
        '''Displays CPU core information.'''
        rows = [
            ["Logical cores", psutil.cpu_count()],
            ["Physical cores", psutil.cpu_count(logical=False)]
        ]
        print(tabulate(rows, headers=["Metric", "Value"], tablefmt="grid"))

    def run(self):
        '''Executes all benchmarks for configured sizes and structures.'''

        process = psutil.Process(os.getpid())

        for size in self.sizes:

            data = DataGenerator.generate(size)
            rows = []
            inserts = []
            searchs = []

            for test in self.tests:

                # Perform insertion benchmark
                insert_result = self.run_insert(test, data)

                # Rebuild structure for search benchmark
                ds = test["factory"](len(data))
                for d in data:
                    test["insert"](ds, d)

                # Perform search benchmark
                search_result = self.run_search(test, ds, data)

                inserts.append([test["name"], "INSERT", *insert_result])
                searchs.append([test["name"], "SEARCH", *search_result])

            rows = inserts + searchs
            
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
                    "iterations": row[5]
                })

        self.generate_graphs()

    def run_insert(self, test, data):
        '''Executes insertion benchmark for a given structure.'''

        cpu_times, mem_peaks, cpu_peaks, iterations = [], [], [], []

        for _ in range(self.rounds):

            ds = test["factory"](len(data))

            tracemalloc.start()
            cpu_start = time.perf_counter()

            monitor = CPUMonitor()
            monitor.start()

            total_iter = 0
            for d in data:
                total_iter += test["insert"](ds, d)

            cpu_end = time.perf_counter()
            _, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()

            peak_cpu = monitor.stop()

            cpu_times.append(cpu_end - cpu_start)
            mem_peaks.append(peak / 1024)
            cpu_peaks.append(peak_cpu)
            iterations.append(total_iter / len(data))

        return (
            round(statistics.mean(cpu_times), 6),
            round(statistics.mean(mem_peaks), 2),
            round(statistics.mean(cpu_peaks), 2),
            round(statistics.mean(iterations), 2)
        )

    def run_search(self, test, ds, data):
        '''Executes search benchmark for a given structure.'''

        cpu_times, mem_peaks, cpu_peaks, iterations = [], [], [], []

        searches = int(len(data) * 0.01)

        for _ in range(self.rounds):

            tracemalloc.start()
            cpu_start = time.perf_counter()

            monitor = CPUMonitor()
            monitor.start()

            total_iter = 0

            for _ in range(searches):
                value = random.choice(data)
                _, it = test["search"](ds, value)
                total_iter += it

            cpu_end = time.perf_counter()
            _, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()

            peak_cpu = monitor.stop()

            cpu_times.append(cpu_end - cpu_start)
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
        '''Generates performance graphs for all collected metrics.'''

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