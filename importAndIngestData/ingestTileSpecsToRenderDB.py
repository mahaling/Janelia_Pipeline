#!/usr/bin/env python

import json
import sys
import os
import argparse
import jsonschema
import time


def parse_args():
    parser = argparse.ArgumentParser(
        description='Tile specs ingest client for Render')
    parser.add_argument('--baseDataURL', dest='baseDataUrl',
                        help='base URL for render', type=str, default=None)
    parser.add_argument('--owner', dest='owner',
                        help='owner of the source stack', type=str,
                        default=None)
    parser.add_argument('--project', dest='project', help='project name',
                        type=str, default=None)
    parser.add_argument('--stackResX', dest='stackResX',
                        help='stack resolution X', type=float, default=3.58)
    parser.add_argument('--stackResY', dest='stackResY',
                        help='stack resolution Y', type=float, default=3.58)
    parser.add_argument('--stackResZ', dest='stackResZ',
                        help='stack resolution Z', type=float, default=40.0)
    parser.add_argument('--stackName', dest='stackName',
                        help='name of the stack to be ingested', type=str,
                        default=None)
    parser.add_argument('--importDir', dest='importDir',
                        help='dir path to input tile specs json files',
                        type=str, default=None)
    parser.add_argument('--delExisting', dest='delExisting',
                        help='set to delete existing stack with the same name',
                        type=int, default=0)

    args = parser.parse_args()
    return args

if __name__ == '__main__':

    #args = parse_args()
    parser = argparse.ArgumentParser(description='Tile specs ingest client for Render')
    parser.add_argument('--jsonfile', dest='jsonfile', help='input json file with input parameters', type=str, default=None)
    args = parser.parse_args()

    starttime = time.time()

    if args.jsonfile is None:
        print "Need an input json file with input parameters"
        sys.exit()

    with open(args.jsonfile) as inputJson:
        inputParams = json.load(inputJson)

    projectParams = "--baseDataUrl " + inputParams["baseDataUrl"] + " --owner " + inputParams["owner"] + " --project " + inputParams["project"]
    stackParams = "--stackResolutionX " + str(inputParams["stackResX"]) + " --stackResolutionY " + str(inputParams["stackResY"]) + " --stackResolutionZ " + str(inputParams["stackResZ"])
    stack = inputParams["stack"]

    manageCmd = os.path.join(inputParams["renderBinPath"], "manage_stacks.sh")
    manageCmd = manageCmd + " " + projectParams

    if inputParams["delExisting"] == 1:
        cycleParams = "--cycleNumber 1 --cycleStepNumber 1"
        delCmd = manageCmd + " --action DELETE --stack " + stack
        createCmd = manageCmd + " --action CREATE --stack " + stack + " " + cycleParams + " " + stackParams
        os.system(delCmd)
        os.system(createCmd)

    setLoading = manageCmd + " --action SET_STATE --stackState LOADING --stack " + stack
    os.system(setLoading)

    importCmd = os.path.join(inputParams["renderBinPath"], "run_ws_client.sh") + " 6G org.janelia.render.client.ImportJsonClient " + projectParams
    if inputParams["validateTiles"] == 1:
        validatorClass = "--validatorClass org.janelia.alignment.spec.validator.TemTileSpecValidator"
        validatorData = "--validatorData minCoordinate:-500,maxCoordinate:50000,minSize:500,maxSize:10000"
        importCmd = importCmd + " --stack " + stack + " " + validatorClass + " " + validatorData + " --transformFile " + os.path.join(inputParams["importDataDir"], "lens_specs.json") + " " + os.path.join(inputParams["importDataDir"], "[0-9]*.json")
    else:
        importCmd = importCmd + " --stack " + stack + " --transformFile " + os.path.join(inputParams["importDataDir"], "lens_specs.json") + " " + os.path.join(inputParams["importDataDir"], "[0-9]*.json")
    
    print importCmd
    os.system(importCmd)

    setComplete = manageCmd + " --action SET_STATE --stackState COMPLETE --stack " + stack
    os.system(setComplete)

    endtime = time.time()
    print (endtime-starttime)
