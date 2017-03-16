
dir_curr = pwd;
dir_EM_aligner = '/data/nc-em2/gayathrim/Janelia_Pipeline/EM_aligner';
%cd /data/nc-em2/gayathrim/Janelia_Pipeline/EM_aligner/matlab_compiled

setenv('MCC_USE_DEPFUN', '1')

astr = [];
fn_use = dir([dir_EM_aligner '/classes/@Msection*.m']);
for ix = 1:numel(fn_use)
astr = [astr sprintf(' -a %s/classes/@Msection/%s',dir_EM_aligner, fn_use(ix).name)];
end

%astr = [];
fn_use = dir([dir_EM_aligner '/classes/@tile*.m']);
for ix = 1:numel(fn_use)
astr = [astr sprintf(' -a %s/classes/@tile/%s',dir_EM_aligner, fn_use(ix).name)];
end

fn_use = dir([dir_EM_aligner '/solver/*.m']);
for ix = 1:numel(fn_use)
astr = [astr sprintf(' -a %s/solver/%s',dir_EM_aligner, fn_use(ix).name)];
end

%astr = [];
fn_use = dir([dir_EM_aligner '/external/jsonlab/*.m']);
for ix = 1:numel(fn_use)
astr = [astr sprintf(' -a %s/external/jsonlab/%s',dir_EM_aligner, fn_use(ix).name)];
end

fn_use = dir([dir_EM_aligner '/level_1/*.m']);
for ix = 1:numel(fn_use)
    astr = [astr sprintf(' -a %s/level_1/%s', dir_EM_aligner, fn_use(ix).name)];
end

str = sprintf('mcc -m -R -nodesktop -v rough_align.m %s;', astr);
eval(str);