import os
import sys
import argparse
import json
import subprocess
import time

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Materialize a stack')
    parser.add_argument('--jsonfile', dest='jsonfile', help='input json file with input parameters', type=str, default=None)
    args = parser.parse_args()

    if args.jsonfile is None:
        print "Need an input json file with input parameters"
        sys.exit()

    starttime = time.time()

    with open(args.jsonfile) as inputJson:
        ip = json.load(inputJson)

    if ip["imgformat"] == "jpg":
        formt = "jpeg-image"
    elif ip["imgformat"] == "png":
        formt = "png-image"
    elif ip["imgformat"] == "tiff":
        formt = "tiff-image"

    # Set parallel process
    processes = set()
    max_processes = 5

    for z in xrange(ip["startz"], ip["endz"]+1):
        outfile = os.path.join(ip["outdir"], str(z))
        outfile = outfile + '.' + ip["imgformat"]
        cmd = "curl -o " + outfile + " '" + ip["baseDataUrl"] + "/owner/" + ip["owner"] + "/project/" + ip["project"] + "/stack/" + ip["stack"] + "/z/" + str(z) + "/" + formt + "?scale=" + str(ip["scale"]) + "&filter=" + ip["filter"] + "'"
        print "Generating scape for z: " + str(z)
        print cmd
        processes.add(subprocess.Popen([cmd], shell=True))
        if len(processes) >= max_processes:
            os.wait()
            processes.difference_update([p for p in processes if p.poll() is not None])

    # check if all the child processes were closed
    for p in processes:
        if p.poll() is None:
            p.wait()

    endtime = time.time()
    print (endtime-starttime)
