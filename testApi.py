import logging

logger = logging.getLogger("logger")
logger.setLevel(logging.DEBUG)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter("%(asctime)s;%(levelname)s;%(message)s")
# formatter = logging.Formatter("%(message)s")
# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)


def pretty(d, indent=0):
    for key, value in d.items():
        print('\t' * indent + str(key))
        if isinstance(value, dict):
            pretty(value, indent + 1)
        else:
            print('\t' * (indent + 1) + str(value))


def main():
    import os
    print(os.path.dirname(os.getcwd()))


if __name__ == '__main__':
    main()
