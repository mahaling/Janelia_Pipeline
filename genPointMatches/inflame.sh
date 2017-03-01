#!/usr/bin/env bash
# Usage inflame.sh #nodes, alignjar, className, argv
sparkhome="/data/nc-em/russelt/spark/"

no_nodes="$1"
alignjar="$2"
className="$3"
echo $no_nodes
echo $alignjar
echo $className
shift 3

inputargs="$@"
echo $inputargs

qsub -l nodes=${no_nodes}:ppn=20 -q connectome -v logdir=$sparkhome,SPARK_HOME=$sparkhome,sparkjar=$alignjar,sparkclass=$className,sparkargs="$inputargs" ${sparkhome}/"spinup_spark.pbs"
