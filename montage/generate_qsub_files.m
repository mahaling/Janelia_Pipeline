
function qsubfile = generate_qsub_files(z)
str1 = '#!/bin/bash';
log_file = ['log_' num2str(z) '.txt'];
jsonfile = [num2str(z) '.json'];
jobname = ['m_' num2str(z)];
cmd = ['qsub -l nodes=12:ppn=20 -N ' jobname ' -q connectome -o /data/nc-em2/gayathrim/Janelia_Pipeline/montage/scratch/logs/' log_file ' -V batch 16 "/data/nc-em2/gayathrim/Janelia_Pipeline/montage/solve_montage_SL /data/nc-em2/gayathrim/Janelia_Pipeline/scratch/' jsonfile '"'];
qsubfile = ['/data/nc-em2/gayathrim/Janelia_Pipeline/scratch/qsub_files/qsub_job_' num2str(z) '.sh'];
fp = fopen(qsubfile, 'w');
fprintf(fp, '%s\n', str1);
fprintf(fp, '%s\n', cmd);
fclose(fp);
disp(cmd)
cmd1 = ['chmod 775 ' qsubfile];
system(cmd1);

cmd2 = ['sh ' qsubfile];
system(cmd2)
