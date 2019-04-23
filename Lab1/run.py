from shell import shell_proc
import logging
import argparse

def parse_cmd():
    parser = argparse.ArgumentParser(description='os lab1: test shell.')

    return parser.parse_args()

def init_logging(args):
    logger = logging.getLogger("os_lab1")
    logger.setLevel(logging.DEBUG)
    # file_handler = logging.FileHandler(args.log_file)
    # file_handler.setLevel(logging.DEBUG)
    console_handler = logging.StreamHandler() 
    #console_handler.setLevel(eval('logging.' + args.log_level))
    formatter = logging.Formatter( "%(asctime)s - %(name)s - %(levelname)s - %(thread)d - %(message)s") 
    # file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    return logger

if __name__ == '__main__':
    args = parse_cmd()
    logger = init_logging(args)
    shell_proc.run(logger = logger)