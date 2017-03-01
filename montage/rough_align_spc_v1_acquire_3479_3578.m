
% configure montage
clc;
%% configure

nfirst = 3479;
nlast = 3578;

% configure montage
rcmontage.stack          = ['v1_SURF_acquire_gm_' num2str(nfirst) '_' num2str(nlast)];
rcmontage.owner          ='flyTEM';
rcmontage.project        = 'spc';
rcmontage.service_host   = '10.40.3.162:8080';
rcmontage.baseURL        = ['http://' rcmontage.service_host '/render-ws/v1'];
rcmontage.verbose        = 1;


% configure rough
rcrough.stack          = ['v1_SURF_gm_rough_' num2str(nfirst) '_' num2str(nlast)];
rcrough.owner          ='flyTEM';
rcrough.project        = 'spc';
rcrough.service_host   = '10.40.3.162:8080';
rcrough.baseURL        = ['http://' rcrough.service_host '/render-ws/v1'];
rcrough.verbose        = 1;
rcrough.versionNotes = 'Experimenting with rough alignment of Allen dataset: scale 0.1 and center box = 0.3 and no filter';

dir_rough_intermediate_store = ['/gpfs1/scratch/spc/matlab_work/montage/montage_gm/scratch/montage_scape_pms'];% intermediate storage of files
dir_store_rough_slab = [ '/gpfs1/scratch/spc/matlab_work/montage/montage_gm/scratch/matlab_slab_rough_aligned'];


if ~exist(dir_store_rough_slab, 'dir')
    mkdir(dir_store_rough_slab);
end

scale = 0.1;

% configure montage-scape point-match generation
ms.service_host                 = rcmontage.service_host;
ms.owner                        = rcmontage.owner;
ms.project                      = rcmontage.project;
ms.stack                        = rcmontage.stack;
ms.fd_size                      = '10'; % '8'
ms.min_sift_scale               = '0.2';%'0.55';
ms.max_sift_scale               = '1.0';
ms.steps                        = '3';
ms.similarity_range             = '3';
ms.skip_similarity_matrix       = 'y';
ms.skip_aligned_image_generation= 'y';
ms.base_output_dir              = ['/gpfs1/scratch/spc/matlab_work/montage/montage_gm/scratch/temp_rough_base_output'];
ms.script                       = '/gpfs1/scratch/spc/matlab_work/EM_aligner/renderer_api/generate_montage_scape_point_matches_box_0.3.sh';%'../unit_tests/generate_montage_scape_point_matches_stub.sh'; %
ms.number_of_spark_nodes        = '2.0';
ms.first                        = num2str(nfirst);
ms.last                         = num2str(nlast);
ms.scale                        = num2str(scale);
ms.center_box                   = 1.0; % 1.0 means do not apply surf allen hack
ms.run_dir                      = ['Slab_' ms.first '_' ms.last '_scale_' ms.scale];




% %
% kk_mkdir(dir_rough_intermediate_store);   % purge and make new empty
% kk_mkdir(ms.base_output_dir);
% %
run_now = 1;


ms.center_box = 1.0;  % using SIFT
[L2, needs_correction, pmfn, zsetd, zrange, t,dir_spark_work, cmd_str, fn_ids, ...
    target_solver_path, target_ids, target_matches, target_layer_images]= ...
    ...
    solve_rough_slab(dir_store_rough_slab, rcmontage, ...
    rcmontage, rcrough, ms, nfirst,...
    nlast, dir_rough_intermediate_store, ...
    run_now);
































