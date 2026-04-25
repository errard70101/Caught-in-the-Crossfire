% Three-phase pipeline for the BCA uncertainty simulation.
%
% Phase 0: solve the RA-RBC-TFP-uncertainty model with Dynare (order=3, pruning).
% Phase 1: shared warm-up from DSS to SSS (T_wu = 50000, zero innovations).
% Phase 2: Experiment 1 -- one long ergodic path of length T_exp1 = 20000.
% Phase 3: Experiment 2 -- N antithetic pairs of length H, for GIRFs.
%
% Requirement:
%   MATLAB with Dynare on the path. Apple Silicon Dynare 6.2 tested.

clear;
clc;

this_file = mfilename('fullpath');
root_dir = fileparts(fileparts(this_file));
dynare_dir = fullfile(root_dir, 'dynare');
output_dir = fullfile(root_dir, 'output');

if ~exist(output_dir, 'dir')
    mkdir(output_dir);
end

if exist('dynare', 'file') ~= 2
    error(['Dynare is not on the MATLAB path. Add Dynare first, then rerun ', ...
           'code/bca_uncertainty_simulation/matlab/run_simulation.m.']);
end

old_dir = pwd;
cleanup = onCleanup(@() cd(old_dir));

% --- Phase 0: solve ------------------------------------------------------
cd(dynare_dir);
dynare ra_rbc_tfp_uncertainty.mod noclearall;
cd(old_dir);

endo_names = dynare_names_to_cell(M_.endo_names);
endo_names = cellfun(@strtrim, endo_names, 'UniformOutput', false);
var_names = matlab.lang.makeValidName(endo_names);

exo_names = dynare_names_to_cell(M_.exo_names);
exo_names = cellfun(@strtrim, exo_names, 'UniformOutput', false);
exo_var_names = matlab.lang.makeValidName(exo_names);

v_idx = find(strcmp(exo_names, 'eps_v'));
a_idx = find(strcmp(exo_names, 'eps_a'));
if isempty(v_idx) || isempty(a_idx)
    error('Could not locate eps_v / eps_a in M_.exo_names.');
end

params = dynare_params_to_struct(M_);

% --- Phase 1: warm-up to SSS ---------------------------------------------
T_wu = 50000;
[sss_state, warmup_diag] = run_warmup(M_, options_, oo_, T_wu, endo_names);

% --- Phase 2: Experiment 1 -----------------------------------------------
T_exp1 = 20000;
exp1_table = run_experiment1(M_, options_, oo_, sss_state, T_exp1, ...
                             var_names, exo_var_names);

% --- Phase 3: Experiment 2 -----------------------------------------------
N = 1000;
H = 60;
[paths_base, paths_shock] = run_experiment2(M_, options_, oo_, sss_state, ...
                                            N, H, v_idx);

% --- Outputs -------------------------------------------------------------
param_names = fieldnames(params);
param_values = cellfun(@(name) params.(name), param_names);
param_table = table(param_names, param_values, ...
    'VariableNames', {'name', 'value'});

writetable(exp1_table, fullfile(output_dir, 'experiment1_sample.csv'));
writetable(param_table, fullfile(output_dir, 'parameters.csv'));
writetable(warmup_diag, fullfile(output_dir, 'warmup_diagnostics.csv'));

exp2_path = fullfile(output_dir, 'experiment2_paths.mat');
save(exp2_path, 'paths_base', 'paths_shock', 'var_names', 'v_idx', ...
     'N', 'H', '-v7.3');

workspace_path = fullfile(output_dir, 'simulated_workspace.mat');
save(workspace_path, 'M_', 'oo_', 'options_', 'sss_state', ...
     'exp1_table', 'paths_base', 'paths_shock', 'params', ...
     'var_names', 'exo_var_names', 'v_idx', 'a_idx', 'warmup_diag', '-v7.3');

fprintf('Phase 1 SSS gap norm = %.4e; tail-diff = %.4e\n', ...
        warmup_diag.value(strcmp(warmup_diag.name, 'sss_dss_gap_norm')), ...
        warmup_diag.value(strcmp(warmup_diag.name, 'sss_tail_diff_norm')));
fprintf('Wrote simulation outputs to %s\n', output_dir);

% =========================================================================
% Helpers
% =========================================================================
function [sss_state, diag_tbl] = run_warmup(M_, options_, oo_, T_wu, endo_names)
    ex_warmup = zeros(T_wu, M_.exo_nbr);
    path_wu = simult_(M_, options_, oo_.dr.ys, oo_.dr, ex_warmup, 3);
    % simult_ returns (n_endo x T_wu+1); column 1 is the initial state.
    sss_state = path_wu(:, end);

    tail_diff_norm = norm(path_wu(:, end) - path_wu(:, end - 1000));
    sss_dss_gap = sss_state - oo_.dr.ys;
    gap_norm = norm(sss_dss_gap);

    names = {'sss_dss_gap_norm'; 'sss_tail_diff_norm'};
    values = [gap_norm; tail_diff_norm];
    for ii = 1:numel(endo_names)
        names{end + 1, 1} = sprintf('sss_minus_dss_%s', endo_names{ii}); %#ok<AGROW>
        values(end + 1, 1) = sss_dss_gap(ii); %#ok<AGROW>
    end
    diag_tbl = table(names, values, 'VariableNames', {'name', 'value'});
end

function tbl = run_experiment1(M_, options_, oo_, sss_state, T_exp1, ...
                                var_names, exo_var_names)
    rng(20260424, 'twister');
    ex_exp1 = randn(T_exp1, M_.exo_nbr);
    path_exp1 = simult_(M_, options_, sss_state, oo_.dr, ex_exp1, 3);
    % Drop column 1 (initial state). Keep T_exp1 observations.
    sim_matrix = path_exp1(:, 2:end)';
    tbl = array2table(sim_matrix, 'VariableNames', var_names);
    tbl.t = (1:height(tbl))';
    % Store innovations aligned with the kept observations.
    eps_tbl = array2table(ex_exp1, 'VariableNames', exo_var_names);
    tbl = [tbl, eps_tbl];
    tbl = movevars(tbl, 't', 'Before', 1);
end

function [paths_base, paths_shock] = run_experiment2(M_, options_, oo_, ...
                                                     sss_state, N, H, v_idx)
    n_obs = M_.endo_nbr;
    paths_base = zeros(N, H, n_obs);
    paths_shock = zeros(N, H, n_obs);

    for i = 1:N
        rng(20260424 + i, 'twister');
        ex_i = randn(H, M_.exo_nbr);

        ex_base = ex_i; ex_base(1, v_idx) = 0;
        ex_shock = ex_i; ex_shock(1, v_idx) = 1;

        path_base = simult_(M_, options_, sss_state, oo_.dr, ex_base, 3);
        path_shock = simult_(M_, options_, sss_state, oo_.dr, ex_shock, 3);

        % Drop column 1 (initial state); keep H horizons.
        paths_base(i, :, :) = path_base(:, 2:end)';
        paths_shock(i, :, :) = path_shock(:, 2:end)';
    end
end

function names = dynare_names_to_cell(raw_names)
    if iscell(raw_names)
        names = raw_names(:);
    elseif isstring(raw_names)
        names = cellstr(raw_names(:));
    else
        names = cellstr(raw_names);
    end
end

function params = dynare_params_to_struct(M_)
    raw_names = dynare_names_to_cell(M_.param_names);
    params = struct();
    for ii = 1:numel(raw_names)
        field = matlab.lang.makeValidName(strtrim(raw_names{ii}));
        params.(field) = M_.params(ii);
    end
end
