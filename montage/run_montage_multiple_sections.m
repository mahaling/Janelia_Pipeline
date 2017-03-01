%% script to run montage generation for several sections
%% Author: Gayathri Mahalingam


function run_montage_multiple_sections(zfirst, zlast, json_fldr_path)
    clc;
    %bin_fn = '/gpfs1/scratch/spc/matlab_work/montage/montage_section_SL_prll';   % where is the executable
    %parfor_progress(100);
    for z = zfirst:zlast
        disp('------------------------------ montage section:');
        disp(z);
        disp('-----------------------------------------------');
    
        fn = [json_fldr_path '/' num2str(z) '.json'];
        %jbname = sprintf('m_%d', z);
        %log_fn = sprintf('/gpfs1/scratch/spc/matlab_work/montage/montage_gm/logs/log_%d.txt', z);
        
        montage_section_SL_prll(fn);
    end
    