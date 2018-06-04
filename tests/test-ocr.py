import logging
import argparse

argparser = argparse.ArgumentParser()
argparser.add_argument("FILE_TO_CHECK")
args = argparser.parse_args()

print(args.FILE_TO_CHECK)
