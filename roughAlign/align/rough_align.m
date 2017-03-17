
function rough_align(argin)

% Intended for deployment: solve matrix system based on json input provided
% by fn

if isstruct(argin)
    sl = argin;
else
    fn = argin;
    sl = loadjson(fileread(fn));
end

if sl.verbose,
    kk_clock();
    
    disp(['Rough aligning on scale:' num2str(sl.scale)]);
    disp('Using montage scape point-match generation:');disp(sl.montage_scape_pm_generation);
    disp('Using source collection:');disp(sl.source_collection);
    disp('Using target collection:');disp(sl.target_collection);
end

%% override and checks and execution part

if sl.filter_option == 1
    sl.montage_scape_pm_generation.script = [sl.EM_aligner_path '/renderer_api/generate_montage+scape_point_matches_box_0.3.sh'];
elseif sl.filter_option == 2
    sl.montage_scape_pm_generation.script = [sl.EM_aligner_path '/renderer_api/generate_montage_scape_point_matches_box_filter_no.sh'];
else
    sl.montage_scape_pm_generation.script = [sl.EM_aligner_path '/renderer_api/generate_montage_scape_point_matches.sh'];
end

if ~exist(sl.dir_store_rough_slab, 'dir')
    mkdir(sl.dir_store_rough_slab);
end
%kk_mkdir(sl.montage_scape_pm_generation.base_output_dir); % this has to be created first as it is the upper level directory
%kk_mkdir(sl.dir_rough_intermediate_store); % purge and make new empty

[L2, needs_correction, pmfn, zsetd, zrange, t, dir_spark_work, cmd_str, fn_ids, ...
    target_solver_path, target_ids, target_matches, target_layer_images]= ...
    ...
    solve_rough_slab(sl.dir_store_rough_slab, sl.source_collection, ...
    sl.source_collection, sl.target_collection, sl.montage_scape_pm_generation, sl.zfirst, ...
    sl.zlast, sl.dir_rough_intermediate_store, ...
    sl.run_now);

