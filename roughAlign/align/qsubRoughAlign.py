import os
import sys
import json
import argparse
import types


def findAndReplace(string, **kwargs):
    if type(string) is int or type(string) is float:
        return string

    #minz = kwargs.pop('minz')
    #maxz = kwargs.pop('maxz')

    for key, value in kwargs.items():
        string = string.replace(key, str(value))
        string = string.replace(key, str(value))

    if all(i.isdigit() for i in string):
        string = int(string)
    return string


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Create json files and submit qsub rough alignment jobs")
    parser.add_argument('--jsonfile', dest='jsonfile', help='input json file with input parameters', type=str, default=None)
    #parser.add_argument('--template', '-t', dest='template', help='template json file to fill in', type=str, default=None)
    #parser.add_argument('--script', '-s', dest='script', help='the script that need to be qsubd', type=str, default=None)
    parser.add_argument('--minz', dest='minz', help='minz value', type=int)
    parser.add_argument('--maxz', dest='maxz', help='maxz value', type=int)
    args = parser.parse_args()

    if args.jsonfile is None:
        print "Need and input template json"
        sys.exit()

    if os.path.isfile(args.jsonfile):
        with open(args.jsonfile) as f:
            params = json.load(f)
    else:
        print "Json file doesn't exist"
        sys.exit()

    with open(params['templateJson']) as tpJson:
        tjson = json.load(tpJson)

    # replace all occurence of ZMIN and ZMAX

    for key, value in tjson.items():
        if type(value) is dict:
            for k,v in value.items():
                tjson[key][k] = findAndReplace(v, ZMIN=args.minz, ZMAX=args.maxz)
        else:
            tjson[key] = findAndReplace(value, ZMIN=args.minz, ZMAX=args.maxz)

    outfile = "rough_" + str(args.minz) + "_" + str(args.maxz)
    outjson = os.path.join(params['jsonoutdir'], outfile) + '.json'

    with open(outjson, 'w') as f:
        json.dump(tjson, f, indent=4)

    cmd = "chmod 777 " + outjson
    os.system(cmd)

    logfile = os.path.join(params['logdir'], outfile) + '_log.txt'
    errfile = os.path.join(params['logdir'], outfile) + '_err.txt'
    jobname = outfile
    qsubfile = os.path.join(params['qsubdir'], outfile) + '.pbs'

    pbs = open(qsubfile, 'w')
    pbs.write('#PBS -l mem=60g\n')
    pbs.write('#PBS -l walltime=50:00:00\n')
    pbs.write('#PBS -l ncpus=1\n')
    pbs.write('#PBS -N ' + jobname + '\n')
    pbs.write('#PBS -r n\n')
    pbs.write('#PBS -m n \n')
    pbs.write('#PBS -o ' + logfile + '\n')
    pbs.write('#PBS -e ' + errfile + '\n')
    pbs.write('#PBS -q emconnectome\n')
    pbs.write(params["script"] + " " + outjson + '\n')
    pbs.close()

    # submit the jobs
    cmd = "qsub " + qsubfile
    #os.system(cmd)
