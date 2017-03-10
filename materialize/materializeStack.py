import os
import sys
import argparse
import json

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Materialize a stack')
    parser.add_argument('--jsonfile', dest='jsonfile', help='input json file with input parameters', type=str, default=None)
    args = parser.parse_args()

    if args.jsonfile is None:
        print "Need an input json file with input parameters"
        sys.exit()

    with open(args.jsonfile) as inputJson:
        inputParams = json.load(inputJson)



