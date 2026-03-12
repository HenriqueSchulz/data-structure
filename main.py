from benchmark import Benchmark

if __name__ == "__main__":

    #sizes = [10000, 20000, 40000, 80000, 160000, 320000, 640000, 1280000]
    sizes = [10000]

    benchmark = Benchmark(rounds=5)
    benchmark.get_cpu_cores()
    benchmark.run_hash_table_test(sizes, hash_type='modular')