#!/bin/bash
qsub -b y -N m_2428 -A spc -j y -o /nrs/spc/matlab_work/montage/montage_gm/scratch/logs/log_2428.txt -l d_rt=1200 -cwd -V -pe batch 16 "/nrs/spc/matlab_work/montage/montage_gm/montage_section_SL_prll /nrs/spc/matlab_work/montage/montage_gm/scratch/temp_json/2428.json"
