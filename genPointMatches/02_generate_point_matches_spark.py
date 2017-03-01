import json
import sys
import os
import argparse
import jsonschema


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate tile pairs for given sections')
    parser.add_argument('--jsonfile', dest='jsonfile', help='input json file with input parameters', type=str, default=None)
    args = parser.parse_args()

    if args.jsonfile is None:
        print "Need an input json file with input parameters"
        sys.exit()

    with open(args.jsonfile) as inputJson:
        inputParams = json.load(inputJson)

    if inputParams["SIFTfdSize"] is None:
        inputParams["SIFTfdSize"] = 4

    if inputParams["SIFTsteps"] is None:
        inputParams["SIFTsteps"] = 3

    if inputParams["matchMaxEpsilon"] is None:
        inputParams["matchMaxEpsilon"] = 20

    if inputParams["maxFeatureCacheGb"] is None:
        inputParams["maxFeatureCacheGb"] = 12 

    if inputParams["SIFTminScale"] is None:
        inputParams["SIFTminSCale"] = 0.58

    if inputParams["renderScale"] is None:
        inputParams["renderScale"] = 0.6

    if inputParams["SIFTmaxScale"] is None:
        inputParams["SIFTmaxScale"] = 0.62

    if inputParams["matchRod"] is None:
        inputParams["matchRod"] = 0.8

    if inputParams["matchMaxNumInliers"] is None:
        inputParams["matchMaxNumInliers"] = 20

    cmd = inputParams["sparkPath"] + " --master " + inputParams["masterUrl"] + " --executor-memory " + inputParams["memory"] + " --class org.janelia.render.client.spark.SIFTPointMatchClient " + inputParams["jarfile"] + " --baseDataUrl " + inputParams["baseDataUrl"] + " --owner " + inputParams["owner"] + " --collection " + inputParams["targetCollection"] + " --pairJson " + inputParams["pairJson"]
    params = " --SIFTfdSize " + str(inputParams["SIFTfdSize"]) + " --SIFTsteps " + str(inputParams["SIFTsteps"]) + " --matchMaxEpsilon " + str(inputParams["matchMaxEpsilon"]) + " --maxFeatureCacheGb " + str(inputParams["maxFeatureCacheGb"]) + " --SIFTminScale " + str(inputParams["SIFTminScale"]) + " --renderScale " + str(inputParams["renderScale"]) + " --SIFTmaxScale " + str(inputParams["SIFTmaxScale"]) + " --matchRod " + str(inputParams["matchRod"]) + " --matchMaxNumInliers " + str(inputParams["matchMaxNumInliers"]) + " --matchMinNumInliers " + str(inputParams["matchMinNumInliers"])

    cmd = cmd + params
    os.system(cmd)
    print cmd

