## Performance Profiling

Our initial results included over 20 benchmarks that timed out (>= 1.0 sec) and our passing benchmarks were ~200ms slower than the original BlinkFill paper.

As such, we perform some profiling using [cProfile](https://docs.python.org/3/library/profile.html#module-cProfile) and produe a dot-formatted PNG using [gprof2dot](https://github.com/jrfonseca/gprof2dot)
