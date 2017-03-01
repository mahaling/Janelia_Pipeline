
% Run Montage generation for several sections

clc;

fnsource = '/gpfs1/scratch/spc/matlab_work/montage/montage_gm/gm_sample_montage_input.json';
bin_fn = '/gpfs1/scratch/spc/matlab_work/montage/montage_gm/montage_section_SL_prll';   % where is the executable
%bin_fn = '/gpfs1/scratch/spc/matlab_work/montage/montage_section_SL_prll';   % where is the executable

sl = loadjson(fileread(fnsource));

zfirst = 3479;
zlast = 3578;

montage_collection.stack = ['v1_SURF_acquire_gm_' num2str(zfirst) '_' num2str(zlast)];
sl.target_collection.stack = montage_collection.stack;
dir_scratch = [sl.scratch '/temp_' num2str(randi(10000))];
kk_mkdir(dir_scratch);

%cd(dir_scratch);
local_scratch = '/gpfs1/scratch/spc/matlab_work/montage/montage_gm/scratch';

for z = zfirst:zfirst%zlast
    sl.target_collection.versionNotes = ['z = ' num2str(z) ' of stack ' num2str(zfirst) '-' num2str(zlast) ' SURF features'];
    disp('------------------------------ montage section:');
    disp(z);
    disp('-----------------------------------------------');
    
    sl.section_number = z;
    sl.complete = 0;
    sl.ncpus = 16;
    
    fn = [dir_scratch '/temp_' num2str(randi(10000)) '_' num2str(z) '.json'];
    disp(fn);
    % generate json file for this montage run
    jstr = savejson('', sl);
    fid = fopen(fn, 'w');
    fprintf(fid, jstr);
    fclose(fid);
    
    % prepare qsub jobs
    jbname = sprintf('m_%d', z);
    log_fn = sprintf('./log_%d.txt', z);
       % prepare Matlab cache for this job
    cache_str = ['export MCR_CACHE_ROOT=' local_scratch '/mcr_cache_root.' num2str(z) ';mkdir -p $MCR_CACHE_ROOT'];
    mcr_root = [dir_scratch '/mcr_cache_root.' jbname];
    del_dir_mcr_root = sprintf(';rm -rf %s', mcr_root);
    
    % prepare job qsub string
    str = sprintf('qsub -N %s -A spc -j y -o %s -l d_rt=1200 -cwd -V -b y -pe batch %d "%s;%s %s;%s"',...
        jbname, log_fn, sl.ncpus, cache_str, bin_fn, fn, del_dir_mcr_root);
    
    disp(str);
    [a resp] = system(str);
    disp(a);disp(resp);
    %montage_section_SL_prll(fn);
    %delete(fn);
end