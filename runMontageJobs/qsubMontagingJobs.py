import json
import sys
import os
import argparse

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description="Create json files and submit qsub montaging jobs")
	parser.add_argument('--jsonfile', dest='jsonfile', help='input json file with input parameters', type=str, default=None)
	parser.add_argument('--minz', dest='minz', help='minz value', type=int)
	parser.add_argument('--maxz', dest='maxz', help='maxz value', type=int)
	args = parser.parse_args()

	if args.jsonfile is None:
		print "Need an input json file with input parameters"
		sys.exit()
	with open(args.jsonfile) as ipJson:
		params = json.load(ipJson)

	# read the solver json template file
	solverJson = '/data/nc-em2/gayathrim/Janelia_Pipeline/runMontageJobs/sample_solve_montage_json.json'
	with open(solverJson) as tpJson:
		template = json.load(tpJson)
	
	# TODO: check for availability of inputs from the ipJson

	# replace placeholders with actual value

	params["sourceStack"] = params["sourceStack"].replace("ZMIN", str(args.minz))
	params["sourceStack"] = params["sourceStack"].replace("ZMAX", str(args.maxz))
	params["targetStack"] = params["targetStack"].replace("ZMIN", str(args.minz))
	params["targetStack"] = params["targetStack"].replace("ZMAX", str(args.maxz))
	params["targetPMCollection"] = params["targetPMCollection"].replace("ZMIN", str(args.minz))
	params["targetPMCollection"] = params["targetPMCollection"].replace("ZMAX", str(args.maxz))
	params["minz"] = int(params["minz"].replace('ZMIN', str(args.minz)))
	params["maxz"] = int(params["maxz"].replace('ZMAX', str(args.maxz)))

	print params

	
	template["solver_options"]["degree"] = params["solverDegree"]
	template["source_collection"]["stack"] = params["sourceStack"]
	template["source_collection"]["owner"] = params["owner"]
	template["source_collection"]["project"] = params["project"]
	template["source_point_match_collection"]["owner"] = params["owner"]
	template["source_point_match_collection"]["match_collection"] = params["targetPMCollection"]
	template["target_collection"]["stack"] = params["targetStack"]
	template["target_collection"]["owner"] = params["owner"]
	template["target_collection"]["project"] = params["project"]
	template["scratch"] = params["scratchdir"]
	template["temp_dir"] = params["scratchdir"]
	
	# for each z from minz to maxz generate json files
	for z in xrange(params["minz"], params["maxz"]+1):
		outjson = str(z) + ".json"
		outjson = os.path.join(params["outputdir"], outjson)
		template["z_value"] = z
		with open(outjson, 'w') as f:
			json.dump(template,f)

		cmd = "chmod 777 " + outjson
		os.system(cmd)

		# generate the qsub file that can be run from qmaster
		logfile = str(z) + "_log.txt"
		logfile = os.path.join(params["logdir"], logfile)
		errfile = str(z) + "_err.txt"
		errfile = os.path.join(params["logdir"], errfile)
		jobname = "m_" + str(z)
		outfile = str(z) + ".pbs"
		outfile = os.path.join(params["qsubdir"], outfile)
		
		print outfile
		pbs = open(outfile, 'w')
		pbs.write('#PBS -l mem=60g\n')
		pbs.write('#PBS -l walltime=08:00:00\n')
		pbs.write('#PBS -l ncpus=1\n')
		pbs.write('#PBS -N ' + jobname + '\n')
		pbs.write('#PBS -r n\n')
		pbs.write('#PBS -m n \n')
		pbs.write('#PBS -o ' + logfile + '\n')
		pbs.write('#PBS -e ' + errfile + '\n')
		pbs.write('#PBS -q connectome\n')
		pbs.write('/data/nc-em2/gayathrim/Janelia_Pipeline/montage/solve_montage_SL ' + outjson + '\n')
		pbs.close()

		# submit the qsub jobs 
		# NOTE: This script has to be run from qmaster to make this work
		cmd = "qsub " + outfile
		#os.system(cmd)
