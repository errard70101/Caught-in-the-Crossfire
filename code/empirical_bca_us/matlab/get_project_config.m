function conf = get_project_config()
    % GET_PROJECT_CONFIG Centralized path configuration for the US Empirical BCA module.
    
    this_file = mfilename('fullpath');
    matlab_dir = fileparts(this_file);
    module_root = fileparts(matlab_dir);
    
    conf.LOCAL_REPO_ROOT = '/Users/linshih-yang/Documents/GitHub/Caught-in-the-Crossfire';
    conf.EXTERNAL_DRIVE_PATH = '/Volumes/X9 Pro/2 Research Projects/Uncertainty and Financial Friction';
    conf.CROWN_SVAR_DIR = fullfile(conf.EXTERNAL_DRIVE_PATH, 'Crown replication code', 'insample');
    
    conf.DATA_DIR = fullfile(module_root, 'data');
    conf.OUTPUT_DIR = fullfile(module_root, 'output');
    conf.TEMP_DIR = fullfile(conf.OUTPUT_DIR, '.tmp');
    
    % Ensure directories exist
    if ~exist(conf.OUTPUT_DIR, 'dir'), mkdir(conf.OUTPUT_DIR); end
    if ~exist(conf.TEMP_DIR, 'dir'), mkdir(conf.TEMP_DIR); end
end
