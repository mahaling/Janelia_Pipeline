%%%% select subset of tiles of a section
clear all;clc
%% configure

% source stack for sections
rc.stack          = 'Phase1RawData_AIBS';
rc.owner          ='gayathri';
rc.project        = 'EM_Phase1';
rc.service_host   = 'em-131fs:8080';
rc.baseURL        = ['http://' rc.service_host '/render-ws/v1'];

% output stack with only selected tiles
% rcout.stack          = ['v2_rough_reduced'];
% rcout.stack          = 'v2_rough_try_7_slab_g_reduced';
rcout.stack          = 'Phase1RawData_ReImaged_Reduced';
rcout.owner          ='gayathri';
rcout.project        = 'EM_Phase1';
rcout.service_host   = 'em-131fs:8080';
rcout.baseURL        = ['http://' rcout.service_host '/render-ws/v1'];
rcout.renderbinPath ='/data/nc-em2/gayathrim/Janelia_Pipeline/renderBin/bin';

% where are the source image montage-scapes?
dir_source_images = '/data/em-131fs/gayathri/downsampledSections';
dir_temp_ingest = '/data/em-131fs/gayathri/downsampledSections/tiles';

%% load sections and associate (load) mosaic images
fn = dir([dir_source_images '/2267.jpg'] );
scale = 0.05;
zid  = {};
for fix = 1:numel(fn)
    zid{fix} = fn(fix).name(1:end-4);
end

L(numel(fn)) = Msection;
%% % Specify set of sections to work on. 
%%%% sections to be redone:

redo_lst = [2267];

z_num = str2double(zid);
indx_redo = [];
for ix = 1:numel(redo_lst)
    ix
    indx_redo(ix) = find(z_num==redo_lst(ix));
end
vec = indx_redo;

%note that loading and saving the images for all sections can cause memory problems
vec = 1:4;
vec = 5:50;
vec = 51:200;
vec = 194:200;
vec = [indx_redo 395:400];

vec = 574:600;
vec = 713:1000;
vec = 1:numel(fn);

%% this can take some time --- don't go overboards with the range of vec
for fix = vec
    L(fix) = Msection(rc, str2double(zid{fix}));
    L(fix).mosaic = imread([dir_source_images '/' fn(fix).name]);
end

%%
% % select tiles manually: Figure opens and tile boxes appear. Make selection
% of tiles to keep, as soon as mouse is released the selected tiles will be ingested
% in case of mistake, ctrl-c, then record the value of fix, and set vec to start from 
% current section to be repeated. then run only this current Matlab code section
% with the for loop below.
for fix = vec
    % show the user tiles and montage-scape
    clf;
    show_map_with_mosaic(L(fix), scale);title([ num2str(fix) ' -- ' num2str(L(fix).z)]);
    [pl,xs,ys] = selectdata('sel','lasso');  % the user can select tiles
    % do we need to have a wait state here?
    
    
    handles.x = vertcat(xs{:});
    handles.y = vertcat(ys{:});
    hold on;
    plot(handles.x, handles.y,'y*'); % plot to confirm selection to user
    drawnow;pause(2);
    %% determine the selected tiles
    tix = zeros(numel(handles.x),1);
    for pix = 1:numel(handles.x)
        tix(pix) =get_tile_index(L(fix), handles.x(pix), handles.y(pix));
    end
    tix = unique(tix);
    Ls1(fix) = Msection(L(fix).tiles(tix));
    
    
    ntiles = numel(Ls1(fix).tiles);
    %Tout = zeros(ntiles,6);
    tiles = Ls1(fix).tiles;
    %for tix = 1:ntiles
    %   Tout(tix,:) = tiles(tix).tform.T(1:6)';
    %end
    tIds = cell(ntiles,1);
    for tix = 1:ntiles
     tIds{tix} = Ls1(fix).tiles(tix).renderer_id;
    end
    z_val = zeros(ntiles,1);
    for tix = 1:ntiles
     z_val(tix)= Ls1(fix).tiles(tix).z;
    end
    fp = fopen([dir_temp_ingest '/' num2str(zid{fix}) '.txt'], 'w');
    for tix = 1:ntiles
        fprintf(fp, '%s\n', Ls1(fix).tiles(tix).path);
    end
    fclose(fp);
end
    