function out = afqConverter()

if ~isdeployed
	addpath(genpath('/N/u/brlife/git/vistasoft'));
	addpath(genpath('/N/u/brlife/git/jsonlab'));
	addpath(genpath('/N/u/brlife/git/o3d-code'));
end

config = loadjson('config.json');
ref_src = fullfile(config.t1);

disp('Converting wmc to .trk');
load(fullfile(config.segmentation));

for tract=1:length(fg_classified)
    tract_name=strrep(fg_classified(tract).name,' ','_');
    write_fg_to_trk_shift(fg_classified(tract),ref_src,sprintf('%s_tract.trk',tract_name));
end 

exit;
end
