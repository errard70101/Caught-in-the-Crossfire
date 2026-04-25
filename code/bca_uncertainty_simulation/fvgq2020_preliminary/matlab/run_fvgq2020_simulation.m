% Three-phase pipeline for the FVGQ (2020) preliminary simulated BCA.
%
% Phase 0: solve the Dynare model with order=3 native pruning.
% Phase 1: shared warm-up from DSS to SSS.
% Phase 2: one long ergodic sample.
% Phase 3: antithetic-pairs GIRF panels for ue and uA.

clear;
clc;

this_file = mfilename('fullpath');
matlab_dir = fileparts(this_file);
root_dir = fileparts(matlab_dir);
dynare_dir = fullfile(root_dir, 'dynare');
output_dir = fullfile(root_dir, 'output');

if ~exist(output_dir, 'dir')
    mkdir(output_dir);
end

if exist('dynare', 'file') ~= 2
    error(['Dynare is not on the MATLAB path. Run setup_paths first, then ', ...
           'rerun run_fvgq2020_simulation.']);
end

old_dir = pwd;
cleanup = onCleanup(@() cd(old_dir)); %#ok<NASGU>

% --- Phase 0: solve ------------------------------------------------------
cd(dynare_dir);
dynare fvgq2020_solveonly.mod noclearall;
cd(old_dir);

endo_names = dynare_names_to_cell(M_.endo_names);
endo_names = cellfun(@strtrim, endo_names, 'UniformOutput', false);
var_names = matlab.lang.makeValidName(endo_names);

exo_names = dynare_names_to_cell(M_.exo_names);
exo_names = cellfun(@strtrim, exo_names, 'UniformOutput', false);
exo_var_names = matlab.lang.makeValidName(exo_names);

uA_idx = find(strcmp(exo_names, 'uA'));
ue_idx = find(strcmp(exo_names, 'ue'));
if isempty(uA_idx) || isempty(ue_idx)
    error('run_fvgq2020_simulation:shock_missing', ...
          'Could not locate uA and ue in M_.exo_names.');
end

y_idx = find(strcmp(endo_names, 'y'));
cspt_idx = find(strcmp(endo_names, 'cspt'));
ivst_idx = find(strcmp(endo_names, 'ivst'));
labor_idx = find(strcmp(endo_names, 'labor'));
k_idx = find(strcmp(endo_names, 'k'));
if isempty(y_idx) || isempty(cspt_idx) || isempty(ivst_idx) || ...
        isempty(labor_idx) || isempty(k_idx)
    error('run_fvgq2020_simulation:endo_missing', ...
          'Missing one of y/cspt/ivst/labor/k in M_.endo_names.');
end

params = dynare_params_to_struct(M_);

% --- Phase 1: warm-up to SSS ---------------------------------------------
T_wu = 50000;
[sss_state, warmup_diag] = run_warmup(M_, options_, oo_, T_wu, endo_names);

fprintf('Phase 1 SSS gap norm = %.4e; tail-diff = %.4e\n', ...
        warmup_diag.value(strcmp(warmup_diag.name, 'sss_dss_gap_norm')), ...
        warmup_diag.value(strcmp(warmup_diag.name, 'sss_tail_diff_norm')));

% --- Phase 2: Experiment 1 -----------------------------------------------
T_exp1 = 20000;
exp1_table = run_experiment1(M_, options_, oo_, sss_state, T_exp1, ...
                             var_names, exo_var_names);
writetable(exp1_table, fullfile(output_dir, 'experiment1_sample.csv'));
fprintf('Phase 2: wrote %d rows to experiment1_sample.csv\n', height(exp1_table));

% --- Phase 3: Experiment 2 -----------------------------------------------
N = 1000;
H = 60;
exp2_shock_size = 2;
[paths_base_fin, paths_shock_fin] = run_experiment2(M_, options_, oo_, sss_state, ...
                                                    N, H, ue_idx, 'fin', exp2_shock_size);
[paths_base_macro, paths_shock_macro] = run_experiment2(M_, options_, oo_, sss_state, ...
                                                        N, H, uA_idx, 'macro', exp2_shock_size);

exp2_path = fullfile(output_dir, 'experiment2_paths.mat');
save(exp2_path, 'paths_base_fin', 'paths_shock_fin', ...
      'paths_base_macro', 'paths_shock_macro', ...
      'var_names', 'exo_var_names', 'uA_idx', 'ue_idx', ...
      'N', 'H', 'exp2_shock_size', '-v7.3');
fprintf('Phase 3: wrote %d financial pairs + %d macro pairs with %.1f s.d. shocks to %s\n', ...
        N, N, exp2_shock_size, exp2_path);

param_names = fieldnames(params);
param_values = cellfun(@(name) params.(name), param_names);
param_table = table(param_names, param_values, ...
    'VariableNames', {'name', 'value'});
writetable(param_table, fullfile(output_dir, 'parameters.csv'));
writetable(warmup_diag, fullfile(output_dir, 'warmup_diagnostics.csv'));

workspace_path = fullfile(output_dir, 'simulated_workspace.mat');
save(workspace_path, 'M_', 'oo_', 'options_', 'sss_state', ...
     'exp1_table', 'paths_base_fin', 'paths_shock_fin', ...
     'paths_base_macro', 'paths_shock_macro', 'params', ...
      'var_names', 'exo_var_names', 'uA_idx', 'ue_idx', ...
      'y_idx', 'cspt_idx', 'ivst_idx', 'labor_idx', 'k_idx', ...
      'warmup_diag', 'exp2_shock_size', '-v7.3');
fprintf('Wrote consolidated workspace to %s\n', workspace_path);
fprintf('Wrote parameters and warmup diagnostics to %s\n', output_dir);

function [sss_state, diag_tbl] = run_warmup(M_, options_, oo_, T_wu, endo_names)
    ex_warmup = zeros(T_wu, M_.exo_nbr);
    path_wu = simult_(M_, options_, oo_.dr.ys, oo_.dr, ex_warmup, 3);
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
    sim_matrix = path_exp1(:, 2:end)';
    tbl = array2table(sim_matrix, 'VariableNames', var_names);
    tbl.t = (1:height(tbl))';
    eps_tbl = array2table(ex_exp1, 'VariableNames', exo_var_names);
    tbl = [tbl, eps_tbl];
    tbl = movevars(tbl, 't', 'Before', 1);
end

function [paths_base, paths_shock] = run_experiment2(M_, options_, oo_, ...
                                                     sss_state, N, H, ...
                                                     shock_idx, tag, shock_size)
    n_obs = M_.endo_nbr;
    paths_base = zeros(N, H, n_obs);
    paths_shock = zeros(N, H, n_obs);

    tag_offset = tag_to_offset(tag);
    for i = 1:N
        rng(20260424 + tag_offset + i, 'twister');
        ex_i = randn(H, M_.exo_nbr);

        ex_base = ex_i;
        ex_base(1, shock_idx) = 0;
        ex_shock = ex_i;
        ex_shock(1, shock_idx) = shock_size;

        path_base = simult_(M_, options_, sss_state, oo_.dr, ex_base, 3);
        path_shock = simult_(M_, options_, sss_state, oo_.dr, ex_shock, 3);

        paths_base(i, :, :) = path_base(:, 2:end)';
        paths_shock(i, :, :) = path_shock(:, 2:end)';
    end
    fprintf('  Experiment 2 (%s): generated %d pairs x H=%d\n', tag, N, H);
end

function offset = tag_to_offset(tag)
    switch lower(tag)
        case 'fin'
            offset = 0;
        case 'macro'
            offset = 1000000;
        otherwise
            error('run_fvgq2020_simulation:bad_tag', 'Unknown tag: %s', tag);
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
