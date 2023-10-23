import multiprocessing

from pytest import main

tests_with_coverage = True
parallel = False

if __name__ == '__main__':

    args = []
    if tests_with_coverage:
        args.append("--cov")
        args.append("--cov-config=.coveragerc")
    if parallel:
        process_count = multiprocessing.cpu_count() - 1
        args.append(f"-n {process_count}")

    main(args)
