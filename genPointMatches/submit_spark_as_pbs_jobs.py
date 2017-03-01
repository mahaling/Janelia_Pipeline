import json
import sys
import os
import argparse


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate tile pairs for given sections')
    parser.add_argument('--jsonfile', dest='jsonfile', help='input json file with input parameters', type=str, default=None)
    args = parser.parse_args()

    if args.jsonfile is None:
        print "Need an input json file with input parameters"
        sys.exit()

    with open(args.jsonfile) as inputJson:
        inputParams = json.load(inputJson)

    if inputParams["no_nodes"] is None:
        inputParams["no_nodes"] = 20

    if inputParams["className"] is None:
        print "Need a class name"
        sys.exit(0)

    if inputParams["jarfile"] is None:
        print "Need a jar file with full path"
        sys.exit(0)

    if inputParams["sparkhome"] is None:
        inputParams["sparkhome"] = "/data/nc-em/russelt/spark/"

    cmd = "qsub -l nodes=" + str(inputParams["no_nodes"]) + ":ppn=20 -q connectome -v logdir=" + inputParams["logdir"]
    cmd = cmd + ",SPARK_HOME=" + inputParams["sparkhome"] + ",sparkjar=" + inputParams["jarfile"] + ",sparkclass=" + inputParams["className"] + ",sparkargs="
    arguments = "\""
    for key,value in inputParams["args"].items():
        if inputParams["args"][key] is None:
            continue
        arguments = arguments + " --" + key + " " + str(value)

    arguments = arguments + "\""
    cmd = cmd + arguments
    cmd = cmd + " " + os.path.join(inputParams["sparkhome"], "spinup_spark.pbs")
#    os.system(cmd)
    print cmd
