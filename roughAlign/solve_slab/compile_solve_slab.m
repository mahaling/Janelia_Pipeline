%% compile (you must customize this script to your system/environment


%cd /groups/flyTEM/home/khairyk/EM_aligner/matlab_compiled

astr = [];
fn = dir('/data/nc-em2/gayathrim/Janelia_Pipeline/EM_aligner/classes/@Msection*.m');
for ix = 1:numel(fn)
astr = [astr sprintf(' -a /data/nc-em2/gayathrim/Janelia_Pipeline/EM_aligner/classes/@Msection/%s',fn(ix).name)];
end

astr = [];
fn = dir('/data/nc-em2/gayathrim/Janelia_Pipeline/EM_aligner/classes/@tile*.m');
for ix = 1:numel(fn)
astr = [astr sprintf(' -a /data/nc-em2/gayathrim/Janelia_Pipeline/EM_aligner/classes/@tile/%s',fn(ix).name)];
end

fn = dir('/data/nc-em2/gayathrim/Janelia_Pipeline/EM_aligner/solver/*.m');
for ix = 1:numel(fn)
astr = [astr sprintf(' -a /data/nc-em2/gayathrim/Janelia_Pipeline/EM_aligner/solver/%s',fn(ix).name)];
end

fn = dir('/data/nc-em2/gayathrim/Janelia_Pipeline/EM_aligner/external/jsonlab/*.m');
for ix = 1:numel(fn)
astr = [astr sprintf(' -a /data/nc-em2/gayathrim/Janelia_Pipeline/EM_aligner/external/jsonlab/%s',fn(ix).name)];
end


str = sprintf('mcc -m -R -nodesktop -v /data/nc-em2/gayathrim/Janelia_Pipeline/EM_aligner/matlab_compiled/solve_slab_SL.m %s;', astr);
eval(str);
