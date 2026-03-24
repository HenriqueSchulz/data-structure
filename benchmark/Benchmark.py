import random
import psutil
import os
import statistics
import matplotlib.pyplot as plt
import time
import tracemalloc

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

        self.cpu_cores = psutil.cpu_count()

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
                "factory": lambda size: HashTable(int(20000 + size * 0.1), "modular"),
                "insert": lambda ds, d: ds.insert(d),
                "search": lambda ds, d: ds.get(d.salary),
            },
            {
                "name": "HashTable (Multiplicative)",
                "factory": lambda size: HashTable(int(20000 + size * 0.1), "multiplicative"),
                "insert": lambda ds, d: ds.insert(d),
                "search": lambda ds, d: ds.get(d.salary),
            },
            {
                "name": "HashTable (Universal)",
                "factory": lambda size: HashTable(int(20000 + size * 0.1), "universal"),
                "insert": lambda ds, d: ds.insert(d),
                "search": lambda ds, d: ds.get(d.salary),
            },
        ]

        for base in ["general", "individuals/binary_tree", "individuals/hash_table"]:
            for op in ["insertion", "search"]:
                os.makedirs(f"results/{base}/{op}", exist_ok=True)

    def run(self):

        process = psutil.Process(os.getpid())

        for size in self.sizes:

            # Dataset gerado uma única vez (fair benchmark)
            data = DataGenerator.generate(size)

            rows = []

            for test in self.tests:

                insert_result, ds, extra = self.run_insert(test, data)
                search_result = self.run_search(test, ds, data)

                rows.append([test["name"], "INSERT", *insert_result])
                rows.append([test["name"], "SEARCH", *search_result])

                # INSERT
                self.results.append({
                    "size": size,
                    "structure": test["name"],
                    "operation": "INSERT",
                    "cpu_time": insert_result[0],
                    "memory": insert_result[1],
                    "cpu_peak": insert_result[2],
                    "iterations": insert_result[3],
                    "collisions": extra.get("collisions"),
                    "load_factor": extra.get("load_factor")
                })

                # SEARCH
                self.results.append({
                    "size": size,
                    "structure": test["name"],
                    "operation": "SEARCH",
                    "cpu_time": search_result[0],
                    "memory": search_result[1],
                    "cpu_peak": search_result[2],
                    "iterations": search_result[3],
                    "collisions": None,
                    "load_factor": None
                })

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

        self.generate_graphs()

    def run_insert(self, test, data):

        cpu_times, mem_peaks, cpu_peaks, iterations = [], [], [], []

        collisions_list = []
        load_factors = []

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

            peak_cpu = monitor.stop() / self.cpu_cores

            cpu_times.append(cpu_end - cpu_start)
            mem_peaks.append(peak / 1024)
            cpu_peaks.append(peak_cpu)
            iterations.append(total_iter / len(data))

            if isinstance(ds, HashTable):
                collisions_list.append(ds.get_collisions())
                load_factors.append(ds.load_factor())

        extra = {}
        if collisions_list:
            extra["collisions"] = statistics.mean(collisions_list)
            extra["load_factor"] = statistics.mean(load_factors)

        return (
            (
                round(statistics.mean(cpu_times), 6),
                round(statistics.mean(mem_peaks), 2),
                round(statistics.mean(cpu_peaks), 2),
                round(statistics.mean(iterations), 2)
            ),
            ds,
            extra
        )

    def run_search(self, test, ds, data):

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

            peak_cpu = monitor.stop() / self.cpu_cores

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

        self._generate_group(lambda r: True, "results/general")
        self._generate_group(lambda r: "BinaryTree" in r["structure"], "results/individuals/binary_tree")
        self._generate_group(lambda r: "HashTable" in r["structure"], "results/individuals/hash_table")

    def _generate_group(self, filter_fn, base_path):

        metrics = {
            "cpu_time": "CPU Time (s)",
            "memory": "Memory Peak (KB)",
            "cpu_peak": "CPU Peak (%)",
            "iterations": "Avg Iterations"
        }

        if "hash_table" in base_path:
            metrics["collisions"] = "Collisions"
            metrics["load_factor"] = "Load Factor"

        operations = {
            "INSERT": "insertion",
            "SEARCH": "search"
        }

        for op_key, folder in operations.items():

            op_data = [
                r for r in self.results
                if r["operation"] == op_key and filter_fn(r)
            ]

            for metric, label in metrics.items():

                if metric in ["collisions", "load_factor"] and op_key != "INSERT":
                    continue

                grouped = defaultdict(lambda: defaultdict(list))

                for r in op_data:
                    if r.get(metric) is None:
                        continue
                    grouped[r["structure"]][r["size"]].append(r[metric])

                if not grouped:
                    continue

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

                path = f"{base_path}/{folder}/{metric}.png"
                os.makedirs(os.path.dirname(path), exist_ok=True)

                plt.savefig(path)
                plt.close()