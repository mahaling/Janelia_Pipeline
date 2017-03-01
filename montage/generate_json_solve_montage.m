%% Script to run montage generation for several sections - 
%% Author: Gayathri Mahalingam

function generate_json_solve_montage(zfirst, zlast, dir_scratch)
    clc;

    fnsource = '/data/nc-em2/gayathrim/Janelia_Pipeline/montage/sample_solve_montage_json.json';

    sl = loadjson(fileread(fnsource));

    for z = zfirst:zlast
        disp('------------------------------ montage section:');
        disp(z);
        disp('-----------------------------------------------');

        sl.z_value = z;
        %sl.complete = 0;
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