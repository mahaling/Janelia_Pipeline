
%% Script to run montage generation for several sections - 
%% Author: Gayathri Mahalingam

function generate_json(zfirst, zlast, dir_scratch)
    clc;

    fnsource = '/data/nc-em2/gayathrim/Janelia_Pipeline/montage/sample_solve_montage_json.json';

    sl = loadjson(fileread(fnsource));

    %zfirst = 3479;
    %zlast = 3578;

    %montage_collection.stack = ['v1_SURF_acquire_gm_' num2str(zfirst) '_' num2str(zlast)];
    %sl.target_collection.stack = montage_collection.stack;

    if ~isdir(dir_scratch)
        dir_scratch = [sl.scratch '/temp_json'];
        kk_mkdir(dir_scratch);
    end

    local_scratch = '/gpfs1/scratch/spc/matlab_work/montage/montage_gm/scratch';

    for z = zfirst:zlast
            sl.target_collection.versionNotes = ['z = ' num2str(z) ' of stack ' num2str(zfirst) '-' num2str(zlast) ' SURF features'];
        disp('------------------------------ montage section:');
        disp(z);
        disp('-----------------------------------------------');

        sl.section_number = z;
        sl.complete = 0;
        sl.ncpus = 16;

        fn = [dir_scratch '/' num2str(z) '.json'];
        disp(fn);
        % generate json file for this montage run
        jstr = savejson('', sl);
        fid = fopen(fn, 'w');
        fprintf(fid, jstr);
        fclose(fid);
        system(['chmod 775 ' fn]);
    end