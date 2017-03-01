
function generatePBSfileMontage(z,logDir, qsubDir)

logfile = [logDir '/' num2str(z) '_log.txt'];
errorfile = [logDir '/' num2str(z) '_err.txt'];
jobname = ['m_' num2str(z)];
jsonfile = [num2str(z) '.json'];

outfile = [qsubDir '/' num2str(z) '.pbs'];
fp = fopen(outfile, 'w');
fprintf(fp, '#PBS -l mem=60g\n');
fprintf(fp, '#PBS -l walltime=08:00:00\n');
fprintf(fp, '#PBS -l ncpus=1\n');
fprintf(fp, '#PBS -N %s\n', jobname);
fprintf(fp, '#PBS -r n\n');
fprintf(fp, '#PBS -m n\n');
fprintf(fp, '#PBS -o %s\n', logfile);
fprintf(fp, '#PBS -e %s\n', errorfile);
fprintf(fp, '/data/nc-em2/gayathrim/Janelia_Pipeline/montage/solve_montage_SL /data/nc-em2/gayathrim/Janelia_Pipeline/scratch/%s\n', jsonfile);
fclose(fp);
