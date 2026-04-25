function setup_paths()
%SETUP_PATHS Add Dynare 6.2 and the local MATLAB folder to the path.

    dynare_dir = '/Applications/Dynare/6.2-arm64/matlab';
    if ~isfolder(dynare_dir)
        error('setup_paths:dynare_missing', ...
              'Dynare 6.2 not found at %s.', dynare_dir);
    end

    if exist('dynare', 'file') ~= 2
        addpath(dynare_dir);
    end
    if exist('simult_', 'file') ~= 2
        addpath(fullfile(dynare_dir, 'stochastic_solver'));
    end
    if ~contains(which('A_times_B_kronecker_C'), '.mex')
        mex_root = fullfile(fileparts(dynare_dir), 'mex', 'matlab');
        mex_dirs = dir(fullfile(mex_root, 'maca64-*'));
        if ~isempty(mex_dirs)
            addpath(fullfile(mex_root, mex_dirs(end).name));
        else
            addpath(fullfile(dynare_dir, 'missing', 'mex', 'kronecker'));
        end
    end
    fprintf('Configured Dynare paths from: %s\n', dynare_dir);

    this_file = mfilename('fullpath');
    this_dir = fileparts(this_file);
    if exist(fullfile(this_dir, 'run_fvgq2020_simulation.m'), 'file') == 2
        addpath(this_dir);
    end
end
