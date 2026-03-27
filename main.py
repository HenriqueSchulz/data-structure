from benchmark import Benchmark

if __name__ == "__main__":

    sizes = [20000, 40000, 60000, 80000, 100000, 120000, 140000, 1600]

    benchmark = Benchmark(rounds=5, sizes=sizes)
    benchmark.run()
