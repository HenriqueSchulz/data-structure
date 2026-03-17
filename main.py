from benchmark import Benchmark

if __name__ == "__main__":

    sizes = [10000, 20000, 40000, 60000, 80000, 100000, 120000, 140000, 160000]

    benchmark = Benchmark(rounds=5, sizes=sizes)
    benchmark.run()
