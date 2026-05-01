% Apply Inside-Dynare CKM wedge observables, local projections, and GIRFs.

clear;
clc;

this_file = mfilename('fullpath');
matlab_dir = fileparts(this_file);
root_dir = fileparts(matlab_dir);
output_dir = fullfile(root_dir, 'output');

exp1_csv = fullfile(output_dir, 'experiment1_sample.csv');
exp2_mat = fullfile(output_dir, 'experiment2_paths.mat');
workspace_mat = fullfile(output_dir, 'simulated_workspace.mat');
if ~isfile(exp1_csv) || ~isfile(exp2_mat)
    error('run_bca_analysis:missing_input', ...
          'Missing Experiment 1 or Experiment 2 output. Run run_fvgq2020_simulation first.');
end
if ~isfile(workspace_mat)
    error('run_bca_analysis:missing_workspace', ...
          'Missing simulated_workspace.mat. Run run_fvgq2020_simulation first.');
end

addpath(matlab_dir);

pp = ckm_prototype_calibration(workspace_mat);
run_id = make_run_id();
legacy_manifest_entries = detect_legacy_manifest_entries(output_dir);
fprintf(['Prototype chi = %.6f (steady state source: y=%.6f, c=%.6f, l=%.6f)\n'], ...
        pp.chi, pp.y_ss, pp.c_ss, pp.l_ss);

aux_provenance = make_provenance('inside_dynare_auxiliary', run_id);
posthoc_provenance = make_provenance('posthoc_ckm_accounting', run_id);
likelihood_provenance = make_provenance('likelihood_kalman_filter', run_id);
manifest_entries = empty_manifest_entries();

T = readtable(exp1_csv);
Y = T.y;
I = pp.ifrac * T.ivst;

wedges_aux = inside_dynare_wedges_from_table(T);
wedges_posthoc = compute_ckm_posthoc_wedges(T.y, T.cspt, I, T.labor, T.k, pp);
fprintf('Inside-Dynare auxiliary wedges on Exp1: max |G_share| = %.3e\n', ...
        max(abs(wedges_aux.G_share)));
write_provenance_csv(fullfile(output_dir, 'wedges_exp1.csv'), wedges_aux, ...
                     aux_provenance, 'exp1_inside_dynare_auxiliary_wedges');
manifest_entries = append_manifest_entry(manifest_entries, 'wedges_exp1.csv', ...
    'csv', 'exp1_inside_dynare_auxiliary_wedges', aux_provenance, 'current_generated');
report_aux = build_ckm_report_table(wedges_aux.t, Y, wedges_aux);
write_provenance_csv(fullfile(output_dir, 'wedges_exp1_report.csv'), report_aux, ...
                     aux_provenance, 'exp1_inside_dynare_auxiliary_report');
manifest_entries = append_manifest_entry(manifest_entries, 'wedges_exp1_report.csv', ...
    'csv', 'exp1_inside_dynare_auxiliary_report', aux_provenance, 'current_generated');
[report_posthoc, posthoc_level_info] = build_ckm_report_table(wedges_posthoc.t, Y, wedges_posthoc);
write_provenance_csv(fullfile(output_dir, 'wedges_exp1_posthoc.csv'), wedges_posthoc, ...
                     posthoc_provenance, 'exp1_posthoc_ckm_wedges');
manifest_entries = append_manifest_entry(manifest_entries, 'wedges_exp1_posthoc.csv', ...
    'csv', 'exp1_posthoc_ckm_wedges', posthoc_provenance, 'current_generated');
write_provenance_csv(fullfile(output_dir, 'wedges_exp1_posthoc_report.csv'), report_posthoc, ...
                     posthoc_provenance, 'exp1_posthoc_ckm_report');
manifest_entries = append_manifest_entry(manifest_entries, 'wedges_exp1_posthoc_report.csv', ...
    'csv', 'exp1_posthoc_ckm_report', posthoc_provenance, 'current_generated');
[lp_targets_dgp, dgp_target_info] = build_ckm_lp_targets( ...
    wedges_aux, struct('invalid_policy', 'nan'));
if dgp_target_info.bad_labor_count > 0 || dgp_target_info.bad_investment_count > 0
    fprintf(['Inside-Dynare auxiliary transformed LP targets: dropped %d labor-target and %d ', ...
             'investment-target observations due to domain violations.\n'], ...
            dgp_target_info.bad_labor_count, dgp_target_info.bad_investment_count);
end
if posthoc_level_info.bad_labor_count > 0 || posthoc_level_info.bad_investment_count > 0
    fprintf(['Post-hoc CKM report levels: dropped %d labor-level and %d ', ...
             'investment-level observations due to domain violations.\n'], ...
            posthoc_level_info.bad_labor_count, posthoc_level_info.bad_investment_count);
end

ckm_like = estimate_ckm_wedges_likelihood(T, pp);
write_provenance_csv(fullfile(output_dir, 'wedges_exp1_proxy.csv'), ckm_like.proxy_wedges, ...
                     aux_provenance, 'exp1_inside_dynare_auxiliary_proxy_wedges');
manifest_entries = append_manifest_entry(manifest_entries, 'wedges_exp1_proxy.csv', ...
    'csv', 'exp1_inside_dynare_auxiliary_proxy_wedges', aux_provenance, 'current_generated');
write_provenance_csv(fullfile(output_dir, 'wedges_exp1_likelihood.csv'), ...
                     ckm_like.smoothed_wedges, likelihood_provenance, ...
                     'exp1_likelihood_smoothed_wedges');
manifest_entries = append_manifest_entry(manifest_entries, 'wedges_exp1_likelihood.csv', ...
    'csv', 'exp1_likelihood_smoothed_wedges', likelihood_provenance, 'current_generated');
report_likelihood = build_ckm_report_table(ckm_like.smoothed_wedges.t, Y, ckm_like.smoothed_wedges);
write_provenance_csv(fullfile(output_dir, 'wedges_exp1_likelihood_report.csv'), ...
                     report_likelihood, likelihood_provenance, ...
                     'exp1_likelihood_report');
manifest_entries = append_manifest_entry(manifest_entries, ...
    'wedges_exp1_likelihood_report.csv', 'csv', 'exp1_likelihood_report', ...
    likelihood_provenance, 'current_generated');
[lp_targets_likelihood, like_target_info] = build_ckm_lp_targets( ...
    ckm_like.smoothed_wedges, struct('invalid_policy', 'nan'));
if like_target_info.bad_labor_count > 0 || like_target_info.bad_investment_count > 0
    fprintf(['Likelihood transformed LP targets: dropped %d labor-target and %d ', ...
             'investment-target observations due to domain violations.\n'], ...
            like_target_info.bad_labor_count, like_target_info.bad_investment_count);
end
provenance = likelihood_provenance;
save(fullfile(output_dir, 'ckm_likelihood_exp1.mat'), ...
     'ckm_like', 'provenance', '-v7.3');
manifest_entries = append_manifest_entry(manifest_entries, 'ckm_likelihood_exp1.mat', ...
    'mat', 'exp1_likelihood_workspace', likelihood_provenance, 'current_generated');
fprintf('CKM likelihood on Exp1: saved %s\n', fullfile(output_dir, 'wedges_exp1_likelihood.csv'));

raw_wedge_names = {'log_A', 'G_share', 'tau_l', 'tau_x'};
transformed_wedge_names = {'log_efficiency_wedge', 'log_labor_wedge', 'log_investment_wedge'};
lp_target_names = lp_targets_dgp.Properties.VariableNames(2:end);
lp_target_matrix = table2array(lp_targets_dgp(:, lp_target_names));
lagged_targets = [nan(1, size(lp_target_matrix, 2)); lp_target_matrix(1:end-1, :)];
shocks = [T.uA, T.ue];
controls = [T.eA, T.ed, T.ethet, T.ud, T.sigAt, T.sigdt, T.siget, lagged_targets];
H_lp = 60;

lp_results = struct();
for j = 1:numel(lp_target_names)
    lp_results.(lp_target_names{j}) = local_projection( ...
        lp_targets_dgp.(lp_target_names{j}), shocks, controls, H_lp);
end
panel_controls_macro = [T.eA, T.ed, T.ethet, T.ud, T.sigdt, T.siget, lagged_targets];
panel_controls_fin = [T.eA, T.ed, T.ethet, T.ud, T.sigAt, T.sigdt, lagged_targets];
lp_shock_panels = build_lp_shock_panels(T.sigAt, T.siget, shocks, ...
                                        panel_controls_macro, panel_controls_fin, H_lp);
provenance = aux_provenance;
save(fullfile(output_dir, 'lp_results.mat'), 'lp_results', 'lp_target_names', ...
      'lp_shock_panels', 'H_lp', 'provenance', '-v7.3');
manifest_entries = append_manifest_entry(manifest_entries, 'lp_results.mat', ...
    'mat', 'lp_results_inside_dynare_auxiliary', aux_provenance, 'current_generated');
fprintf('LP on Exp1: saved %s\n', fullfile(output_dir, 'lp_results.mat'));

lp_target_matrix_like = table2array(lp_targets_likelihood(:, lp_target_names));
lagged_targets_like = [nan(1, size(lp_target_matrix_like, 2)); ...
                       lp_target_matrix_like(1:end-1, :)];
controls_like = [T.eA, T.ed, T.ethet, T.ud, T.sigAt, T.sigdt, T.siget, lagged_targets_like];
lp_results_likelihood = struct();
for j = 1:numel(lp_target_names)
    lp_results_likelihood.(lp_target_names{j}) = local_projection( ...
        lp_targets_likelihood.(lp_target_names{j}), shocks, controls_like, H_lp);
end
panel_controls_macro_like = [T.eA, T.ed, T.ethet, T.ud, T.sigdt, T.siget, lagged_targets_like];
panel_controls_fin_like = [T.eA, T.ed, T.ethet, T.ud, T.sigAt, T.sigdt, lagged_targets_like];
lp_shock_panels_likelihood = build_lp_shock_panels(T.sigAt, T.siget, shocks, ...
                                                   panel_controls_macro_like, ...
                                                   panel_controls_fin_like, H_lp);
provenance = likelihood_provenance;
save(fullfile(output_dir, 'lp_results_likelihood.mat'), ...
     'lp_results_likelihood', 'lp_target_names', 'lp_shock_panels_likelihood', ...
     'H_lp', 'provenance', '-v7.3');
manifest_entries = append_manifest_entry(manifest_entries, 'lp_results_likelihood.mat', ...
    'mat', 'lp_results_likelihood', likelihood_provenance, 'current_generated');
fprintf('LP on Exp1 likelihood wedges: saved %s\n', ...
        fullfile(output_dir, 'lp_results_likelihood.mat'));

lp_width_table = compare_lp_widths(lp_results, lp_results_likelihood, lp_target_names);
writetable(lp_width_table, fullfile(output_dir, 'lp_interval_comparison.csv'));
manifest_entries = append_manifest_entry(manifest_entries, 'lp_interval_comparison.csv', ...
    'csv', 'lp_interval_comparison', likelihood_provenance, 'current_generated');
fprintf('LP interval comparison: saved %s\n', ...
        fullfile(output_dir, 'lp_interval_comparison.csv'));

% --- Sensitivity LP: drop contemporaneous SV-state controls (sigAt, sigdt, siget) ---
% Rationale: the SV states are mediators of (uA, ue) by construction
% (sigAt = rho*sigAt(-1) + scale*uA), so including them as controls shuts
% down the very channel we want to identify. This sensitivity LP keeps
% level-shock and preference-SV controls plus lagged wedges, but removes
% the three SV states so that the LP coefficients on (uA, ue) capture the
% full SV transmission.
controls_no_sv = [T.eA, T.ed, T.ethet, T.ud, lagged_targets];
lp_results_no_svctrl = struct();
for j = 1:numel(lp_target_names)
    lp_results_no_svctrl.(lp_target_names{j}) = local_projection( ...
        lp_targets_dgp.(lp_target_names{j}), shocks, controls_no_sv, H_lp);
end
panel_controls_macro_no_sv = [T.eA, T.ed, T.ethet, T.ud, lagged_targets];
panel_controls_fin_no_sv = [T.eA, T.ed, T.ethet, T.ud, lagged_targets];
lp_shock_panels_no_svctrl = build_lp_shock_panels(T.sigAt, T.siget, shocks, ...
                                                  panel_controls_macro_no_sv, ...
                                                  panel_controls_fin_no_sv, H_lp);
provenance = aux_provenance;
save(fullfile(output_dir, 'lp_results_no_svctrl.mat'), ...
     'lp_results_no_svctrl', 'lp_target_names', ...
     'lp_shock_panels_no_svctrl', 'H_lp', 'provenance', '-v7.3');
manifest_entries = append_manifest_entry(manifest_entries, 'lp_results_no_svctrl.mat', ...
    'mat', 'lp_results_inside_dynare_auxiliary_no_svctrl', aux_provenance, 'current_generated');
fprintf('Sensitivity LP (no SV-state controls): saved %s\n', ...
        fullfile(output_dir, 'lp_results_no_svctrl.mat'));

controls_no_sv_like = [T.eA, T.ed, T.ethet, T.ud, lagged_targets_like];
lp_results_likelihood_no_svctrl = struct();
for j = 1:numel(lp_target_names)
    lp_results_likelihood_no_svctrl.(lp_target_names{j}) = local_projection( ...
        lp_targets_likelihood.(lp_target_names{j}), shocks, controls_no_sv_like, H_lp);
end
panel_controls_macro_no_sv_like = [T.eA, T.ed, T.ethet, T.ud, lagged_targets_like];
panel_controls_fin_no_sv_like = [T.eA, T.ed, T.ethet, T.ud, lagged_targets_like];
lp_shock_panels_likelihood_no_svctrl = build_lp_shock_panels(T.sigAt, T.siget, shocks, ...
                                                             panel_controls_macro_no_sv_like, ...
                                                             panel_controls_fin_no_sv_like, H_lp);
provenance = likelihood_provenance;
save(fullfile(output_dir, 'lp_results_likelihood_no_svctrl.mat'), ...
     'lp_results_likelihood_no_svctrl', 'lp_target_names', ...
     'lp_shock_panels_likelihood_no_svctrl', 'H_lp', 'provenance', '-v7.3');
manifest_entries = append_manifest_entry(manifest_entries, ...
    'lp_results_likelihood_no_svctrl.mat', 'mat', ...
    'lp_results_likelihood_no_svctrl', likelihood_provenance, 'current_generated');
fprintf('Sensitivity LP likelihood (no SV-state controls): saved %s\n', ...
        fullfile(output_dir, 'lp_results_likelihood_no_svctrl.mat'));

lp_sens_table = compare_lp_peak_table(lp_results, lp_results_no_svctrl, lp_target_names);
writetable(lp_sens_table, fullfile(output_dir, 'lp_no_svctrl_peak_comparison.csv'));
manifest_entries = append_manifest_entry(manifest_entries, ...
    'lp_no_svctrl_peak_comparison.csv', 'csv', 'lp_no_svctrl_peak_comparison', ...
    aux_provenance, 'current_generated');
fprintf('LP no-SV-control peak comparison: saved %s\n', ...
        fullfile(output_dir, 'lp_no_svctrl_peak_comparison.csv'));

mc_config = struct('B', 10000, 'T', 400, 'H', H_lp, ...
                   'seed_base', 2026042400, 'verbose', true, ...
                   'progress_every', 250);
sim_workspace = load(workspace_mat, 'M_', 'oo_', 'options_', 'sss_state', 'var_names', 'exo_var_names');
lp_results_mc_dgp = monte_carlo_lp_bands(sim_workspace, pp, mc_config);
provenance = aux_provenance;
save(fullfile(output_dir, 'lp_results_mc_dgp.mat'), ...
     'lp_results_mc_dgp', 'lp_target_names', 'provenance', '-v7.3');
manifest_entries = append_manifest_entry(manifest_entries, 'lp_results_mc_dgp.mat', ...
    'mat', 'lp_results_mc_inside_dynare_auxiliary', aux_provenance, 'current_generated');
writetable(monte_carlo_summary_table(lp_results_mc_dgp), ...
           fullfile(output_dir, 'lp_results_mc_dgp_summary.csv'));
manifest_entries = append_manifest_entry(manifest_entries, ...
    'lp_results_mc_dgp_summary.csv', 'csv', 'lp_results_mc_inside_dynare_auxiliary_summary', ...
    aux_provenance, 'current_generated');
fprintf(['Monte Carlo LP on Inside-Dynare auxiliary wedges: saved %s ', ...
        'with B=%d, T=%d, center=median\n'], ...
        fullfile(output_dir, 'lp_results_mc_dgp.mat'), mc_config.B, mc_config.T);

S = load(exp2_mat);
if isfield(S, 'exp2_shock_size')
    exp2_shock_size = S.exp2_shock_size;
else
    exp2_shock_size = 1;
end
var_names = S.var_names;
wedge_idx = locate_inside_dynare_wedge_indices(var_names);

girf = struct();
girf_likelihood = struct();
girf_transformed = struct();
girf_transformed_likelihood = struct();
girf_transform_info = struct();
girf_transform_info_likelihood = struct();
girf_likelihood_path_info = struct();
for tag = {'fin', 'macro'}
    tag_str = tag{1};
    pb = S.(['paths_base_' tag_str]);
    ps = S.(['paths_shock_' tag_str]);
    [Npairs, Hpairs, ~] = size(pb);
    girf_likelihood_path_info.(tag_str) = struct( ...
        'base_fail_count', 0, ...
        'shock_fail_count', 0, ...
        'base_fail_indices', zeros(0, 1), ...
        'shock_fail_indices', zeros(0, 1));

    wedge_base = zeros(Npairs, Hpairs, numel(raw_wedge_names));
    wedge_shock = zeros(Npairs, Hpairs, numel(raw_wedge_names));
    wedge_base_like = zeros(Npairs, Hpairs, numel(raw_wedge_names));
    wedge_shock_like = zeros(Npairs, Hpairs, numel(raw_wedge_names));
    for i = 1:Npairs
        wb = inside_dynare_wedges_from_path(squeeze(pb(i, :, :)), wedge_idx);
        ws = inside_dynare_wedges_from_path(squeeze(ps(i, :, :)), wedge_idx);
        [wb_like, wb_like_status] = likelihood_wedges_from_path( ...
            squeeze(pb(i, :, :)), var_names, pp);
        [ws_like, ws_like_status] = likelihood_wedges_from_path( ...
            squeeze(ps(i, :, :)), var_names, pp);
        if ~wb_like_status.success
            girf_likelihood_path_info.(tag_str).base_fail_count = ...
                girf_likelihood_path_info.(tag_str).base_fail_count + 1;
            girf_likelihood_path_info.(tag_str).base_fail_indices(end + 1, 1) = i; %#ok<AGROW>
        end
        if ~ws_like_status.success
            girf_likelihood_path_info.(tag_str).shock_fail_count = ...
                girf_likelihood_path_info.(tag_str).shock_fail_count + 1;
            girf_likelihood_path_info.(tag_str).shock_fail_indices(end + 1, 1) = i; %#ok<AGROW>
        end
        for j = 1:numel(raw_wedge_names)
            wedge_base(i, :, j) = wb.(raw_wedge_names{j});
            wedge_shock(i, :, j) = ws.(raw_wedge_names{j});
            wedge_base_like(i, :, j) = wb_like.(raw_wedge_names{j});
            wedge_shock_like(i, :, j) = ws_like.(raw_wedge_names{j});
        end
    end

    diff_wedges = wedge_shock - wedge_base;
    diff_wedges_like = wedge_shock_like - wedge_base_like;
    girf.(tag_str).mean = squeeze(mean(diff_wedges, 1));
    girf.(tag_str).q05 = squeeze(quantile(diff_wedges, 0.05, 1));
    girf.(tag_str).q95 = squeeze(quantile(diff_wedges, 0.95, 1));
    girf.(tag_str).se_mean = squeeze(std(diff_wedges, 0, 1) ./ sqrt(Npairs));
    girf.(tag_str).ci_lo_mean = girf.(tag_str).mean - 1.96 * girf.(tag_str).se_mean;
    girf.(tag_str).ci_hi_mean = girf.(tag_str).mean + 1.96 * girf.(tag_str).se_mean;
    girf.(tag_str).N = Npairs;
    girf.(tag_str).wedges_base = wedge_base;
    girf.(tag_str).wedges_shock = wedge_shock;
    girf_likelihood.(tag_str).mean = squeeze(mean(diff_wedges_like, 1));
    girf_likelihood.(tag_str).q05 = squeeze(quantile(diff_wedges_like, 0.05, 1));
    girf_likelihood.(tag_str).q95 = squeeze(quantile(diff_wedges_like, 0.95, 1));
    girf_likelihood.(tag_str).se_mean = squeeze(std(diff_wedges_like, 0, 1) ./ sqrt(Npairs));
    girf_likelihood.(tag_str).ci_lo_mean = girf_likelihood.(tag_str).mean - ...
        1.96 * girf_likelihood.(tag_str).se_mean;
    girf_likelihood.(tag_str).ci_hi_mean = girf_likelihood.(tag_str).mean + ...
        1.96 * girf_likelihood.(tag_str).se_mean;
    girf_likelihood.(tag_str).N = Npairs;
    girf_likelihood.(tag_str).wedges_base = wedge_base_like;
    girf_likelihood.(tag_str).wedges_shock = wedge_shock_like;
    [girf_transformed.(tag_str), girf_transform_info.(tag_str)] = ...
        build_transformed_girf_summary(wedge_base, wedge_shock);
    [girf_transformed_likelihood.(tag_str), girf_transform_info_likelihood.(tag_str)] = ...
        build_transformed_girf_summary(wedge_base_like, wedge_shock_like);
    fprintf('GIRF (%s): %d pairs x H=%d x %d wedges computed\n', ...
            tag_str, Npairs, Hpairs, numel(raw_wedge_names));
    fprintf('GIRF likelihood (%s): %d pairs x H=%d x %d wedges computed\n', ...
            tag_str, Npairs, Hpairs, numel(raw_wedge_names));
    fprintf(['GIRF transformed (%s): dropped %d labor and %d investment pair-horizon ', ...
             'points due to domain violations\n'], ...
            tag_str, girf_transform_info.(tag_str).bad_labor_count, ...
            girf_transform_info.(tag_str).bad_investment_count);
    fprintf(['GIRF transformed likelihood (%s): dropped %d labor and %d investment ', ...
             'pair-horizon points due to domain violations\n'], ...
            tag_str, girf_transform_info_likelihood.(tag_str).bad_labor_count, ...
            girf_transform_info_likelihood.(tag_str).bad_investment_count);
    if girf_likelihood_path_info.(tag_str).base_fail_count > 0 || ...
            girf_likelihood_path_info.(tag_str).shock_fail_count > 0
        fprintf(['GIRF likelihood (%s): %d base paths and %d shock paths failed ', ...
                 'CKM steady-state refresh and were set to NaN.\n'], ...
                tag_str, ...
                girf_likelihood_path_info.(tag_str).base_fail_count, ...
                girf_likelihood_path_info.(tag_str).shock_fail_count);
    end
end

provenance = aux_provenance;
save(fullfile(output_dir, 'wedges_girf.mat'), 'girf', 'girf_transformed', ...
     'raw_wedge_names', 'transformed_wedge_names', 'girf_transform_info', ...
     'exp2_shock_size', 'provenance', '-v7.3');
manifest_entries = append_manifest_entry(manifest_entries, 'wedges_girf.mat', ...
    'mat', 'girf_inside_dynare_auxiliary', aux_provenance, 'current_generated');
fprintf('GIRF: saved %s\n', fullfile(output_dir, 'wedges_girf.mat'));
provenance = likelihood_provenance;
save(fullfile(output_dir, 'wedges_girf_likelihood.mat'), ...
     'girf_likelihood', 'girf_transformed_likelihood', 'raw_wedge_names', ...
     'transformed_wedge_names', 'girf_transform_info_likelihood', ...
     'girf_likelihood_path_info', ...
     'exp2_shock_size', 'provenance', '-v7.3');
manifest_entries = append_manifest_entry(manifest_entries, 'wedges_girf_likelihood.mat', ...
    'mat', 'girf_likelihood', likelihood_provenance, 'current_generated');
fprintf('GIRF likelihood: saved %s\n', fullfile(output_dir, 'wedges_girf_likelihood.mat'));

write_output_manifest(output_dir, manifest_entries, legacy_manifest_entries);
if ~isempty(legacy_manifest_entries)
    fprintf(['Detected %d legacy *fixed* artifacts in %s; ', ...
             'see analysis_output_manifest.csv before comparing outputs.\n'], ...
            numel(legacy_manifest_entries), output_dir);
end

function provenance = make_provenance(wedge_source, run_id)
    provenance = struct();
    provenance.schema_version = 'ckm_dual_track_v1';
    provenance.wedge_source = wedge_source;
    provenance.generated_by = 'run_bca_analysis';
    provenance.run_id = run_id;
end

function write_provenance_csv(path, tbl, provenance, artifact_role)
    tbl = attach_provenance_columns(tbl, provenance, artifact_role);
    writetable(tbl, path);
end

function tbl = attach_provenance_columns(tbl, provenance, artifact_role)
    n = height(tbl);
    tbl.schema_version = repmat(string(provenance.schema_version), n, 1);
    tbl.wedge_source = repmat(string(provenance.wedge_source), n, 1);
    tbl.generated_by = repmat(string(provenance.generated_by), n, 1);
    tbl.run_id = repmat(string(provenance.run_id), n, 1);
    tbl.artifact_role = repmat(string(artifact_role), n, 1);
end

function entries = empty_manifest_entries()
    entries = struct('artifact', {}, 'format', {}, 'artifact_role', {}, ...
                     'status', {}, 'schema_version', {}, 'wedge_source', {}, ...
                     'run_id', {}, 'generated_by', {});
end

function entries = append_manifest_entry(entries, artifact, format, artifact_role, provenance, status)
    entry = struct();
    entry.artifact = string(artifact);
    entry.format = string(format);
    entry.artifact_role = string(artifact_role);
    entry.status = string(status);
    entry.schema_version = string(provenance.schema_version);
    entry.wedge_source = string(provenance.wedge_source);
    entry.run_id = string(provenance.run_id);
    entry.generated_by = string(provenance.generated_by);
    entries(end + 1) = entry; %#ok<AGROW>
end

function entries = detect_legacy_manifest_entries(output_dir)
    entries = empty_manifest_entries();
    legacy_files = dir(fullfile(output_dir, '*fixed*'));
    legacy_files = legacy_files(~[legacy_files.isdir]);
    for ii = 1:numel(legacy_files)
        [~, ~, ext] = fileparts(legacy_files(ii).name);
        entry = struct();
        entry.artifact = string(legacy_files(ii).name);
        entry.format = string(strip(ext, 'left', '.'));
        entry.artifact_role = "legacy_fixed_artifact";
        entry.status = "legacy_existing";
        entry.schema_version = "legacy_pre_v2";
        entry.wedge_source = "legacy_fixed_point";
        entry.run_id = "";
        entry.generated_by = "pre_v2_pipeline";
        entries(end + 1) = entry; %#ok<AGROW>
    end
end

function write_output_manifest(output_dir, generated_entries, legacy_entries)
    entries = [generated_entries, legacy_entries];
    if isempty(entries)
        return;
    end
    manifest_table = struct2table(entries);
    manifest_table = sortrows(manifest_table, {'status', 'artifact'});
    writetable(manifest_table, fullfile(output_dir, 'analysis_output_manifest.csv'));
end

function run_id = make_run_id()
    run_id = char(datetime('now', 'TimeZone', 'UTC', ...
                           'Format', "yyyyMMdd'T'HHmmss'Z'"));
end

function tbl = compare_lp_peak_table(lp_baseline, lp_no_sv, wedge_names)
    rows = {};
    shock_labels = {'macro_uA', 'fin_ue'};
    for j = 1:numel(wedge_names)
        w = wedge_names{j};
        for s = 1:2
            base = lp_baseline.(w);
            sens = lp_no_sv.(w);
            [~, hb] = max(abs(base.beta(:, s)));
            [~, hs] = max(abs(sens.beta(:, s)));
            rows(end + 1, :) = {w, shock_labels{s}, ...
                base.beta(hb, s), hb - 1, ...
                sens.beta(hs, s), hs - 1, ...
                sens.beta(hs, s) / base.beta(hb, s)}; %#ok<AGROW>
        end
    end
    tbl = cell2table(rows, 'VariableNames', ...
        {'wedge', 'shock', 'baseline_peak', 'baseline_h', ...
         'no_svctrl_peak', 'no_svctrl_h', 'ratio_no_sv_over_base'});
end

function tbl = compare_lp_widths(lp_dgp, lp_like, wedge_names)
    rows = {};
    for j = 1:numel(wedge_names)
        w = wedge_names{j};
        for s = 1:2
            dgp = lp_dgp.(w);
            like = lp_like.(w);
            rows(end + 1, :) = {w, s, ...
                mean(dgp.ci_hi(:, s) - dgp.ci_lo(:, s), 'omitnan'), ...
                mean(like.ci_hi(:, s) - like.ci_lo(:, s), 'omitnan'), ...
                mean(like.ci_hi(:, s) - like.ci_lo(:, s), 'omitnan') / ...
                    mean(dgp.ci_hi(:, s) - dgp.ci_lo(:, s), 'omitnan')}; %#ok<AGROW>
        end
    end
    tbl = cell2table(rows, 'VariableNames', ...
        {'wedge', 'shock_index', 'mean_ci_width_dgp', 'mean_ci_width_likelihood', 'width_ratio'});
end

function panels = build_lp_shock_panels(sigAt_series, siget_series, shocks, controls_macro, controls_fin, H)
    panels = struct();
    panels.macro = local_projection(sigAt_series, shocks, controls_macro, H);
    panels.fin = local_projection(siget_series, shocks, controls_fin, H);
end

function [summary, info] = build_transformed_girf_summary(wedge_base, wedge_shock)
    diff_efficiency = wedge_shock(:, :, 1) - wedge_base(:, :, 1);

    labor_base = 1 - wedge_base(:, :, 3);
    labor_shock = 1 - wedge_shock(:, :, 3);
    valid_labor = labor_base > 0 & labor_shock > 0;
    diff_labor = nan(size(labor_base));
    diff_labor(valid_labor) = log(labor_shock(valid_labor)) - log(labor_base(valid_labor));

    invest_base = 1 + wedge_base(:, :, 4);
    invest_shock = 1 + wedge_shock(:, :, 4);
    valid_invest = invest_base > 0 & invest_shock > 0;
    diff_invest = nan(size(invest_base));
    diff_invest(valid_invest) = log(invest_base(valid_invest)) - log(invest_shock(valid_invest));

    diff_wedges = cat(3, diff_efficiency, diff_labor, diff_invest);
    summary.mean = squeeze(mean(diff_wedges, 1, 'omitnan'));
    summary.q05 = summarize_quantile(diff_wedges, 0.05);
    summary.q95 = summarize_quantile(diff_wedges, 0.95);
    [summary.se_mean, summary.N_eff] = summarize_se_of_mean(diff_wedges);
    summary.ci_lo_mean = summary.mean - 1.96 * summary.se_mean;
    summary.ci_hi_mean = summary.mean + 1.96 * summary.se_mean;
    summary.diff_wedges = diff_wedges;

    info = struct();
    info.bad_labor_count = nnz(~valid_labor);
    info.bad_investment_count = nnz(~valid_invest);
end

function q = summarize_quantile(values, prob)
    [~, H, W] = size(values);
    q = nan(H, W);
    for h = 1:H
        for w = 1:W
            x = values(:, h, w);
            x = x(isfinite(x));
            if ~isempty(x)
                q(h, w) = quantile(x, prob);
            end
        end
    end
end

function [se_mean, N_eff] = summarize_se_of_mean(values)
    [~, H, W] = size(values);
    se_mean = nan(H, W);
    N_eff = nan(H, W);
    for h = 1:H
        for w = 1:W
            x = values(:, h, w);
            x = x(isfinite(x));
            n = numel(x);
            N_eff(h, w) = n;
            if n > 1
                se_mean(h, w) = std(x, 0) / sqrt(n);
            end
        end
    end
end

function tbl = monte_carlo_summary_table(mc)
    rows = {};
    for j = 1:numel(mc.wedge_names)
        wedge = mc.wedge_names{j};
        stats = mc.summary.(wedge);
        for s = 1:numel(mc.shock_names)
            shock = mc.shock_names{s};
            for h = 1:numel(stats.horizons)
                rows(end + 1, :) = { ...
                    wedge, shock, stats.horizons(h), ...
                    stats.median(h, s), stats.mean(h, s), ...
                    stats.q025(h, s), stats.q975(h, s)}; %#ok<AGROW>
            end
        end
    end

    tbl = cell2table(rows, 'VariableNames', ...
        {'wedge', 'shock', 'horizon', 'median', 'mean', 'q025', 'q975'});
end

function wedges = inside_dynare_wedges_from_table(tbl)
    required_vars = {'wedge_A', 'wedge_G', 'wedge_l', 'wedge_x'};
    missing_vars = setdiff(required_vars, tbl.Properties.VariableNames);
    if ~isempty(missing_vars)
        error('run_bca_analysis:missing_inside_dynare_wedges', ...
              ['Missing Inside-Dynare wedge columns: %s. ', ...
               'Rerun run_fvgq2020_simulation after updating fvgq2020_solveonly.mod.'], ...
              strjoin(missing_vars, ', '));
    end
    wedges = table( ...
        tbl.t(:), ...
        tbl.wedge_A(:), ...
        tbl.wedge_G(:), ...
        tbl.wedge_l(:), ...
        tbl.wedge_x(:), ...
        'VariableNames', {'t', 'log_A', 'G_share', 'tau_l', 'tau_x'});
end

function idx = locate_inside_dynare_wedge_indices(var_names)
    idx = struct();
    idx.wedge_A = find(strcmp(var_names, 'wedge_A'));
    idx.wedge_G = find(strcmp(var_names, 'wedge_G'));
    idx.wedge_l = find(strcmp(var_names, 'wedge_l'));
    idx.wedge_x = find(strcmp(var_names, 'wedge_x'));

    names = fieldnames(idx);
    for ii = 1:numel(names)
        if isempty(idx.(names{ii}))
            error('run_bca_analysis:missing_inside_dynare_wedge_index', ...
                  ['Missing Inside-Dynare wedge variable %s in Experiment 2 paths. ', ...
                   'Rerun run_fvgq2020_simulation after updating fvgq2020_solveonly.mod.'], ...
                  names{ii});
        end
    end
end

function wedges = inside_dynare_wedges_from_path(path_rows, wedge_idx)
    T = size(path_rows, 1);
    wedges = table( ...
        (1:T)', ...
        path_rows(:, wedge_idx.wedge_A), ...
        path_rows(:, wedge_idx.wedge_G), ...
        path_rows(:, wedge_idx.wedge_l), ...
        path_rows(:, wedge_idx.wedge_x), ...
        'VariableNames', {'t', 'log_A', 'G_share', 'tau_l', 'tau_x'});
end

function [wedges, status] = likelihood_wedges_from_path(path_rows, var_names, pp) %#ok<INUSD>
    tbl = array2table(path_rows, 'VariableNames', var_names);
    tbl.t = (1:height(tbl))';
    tbl = movevars(tbl, 't', 'Before', 1); %#ok<NASGU>
    like_opts = struct('force_recompile', false, 'verbose', false); %#ok<NASGU>
    status = struct('success', true, 'failure_reason', "", 'error_id', "");
    try
        evalc('tmp_result = estimate_ckm_wedges_likelihood(tbl, pp, like_opts);');
        wedges = tmp_result.smoothed_wedges;
    catch ME
        if any(strcmp(ME.identifier, { ...
                'estimate_ckm_wedges_likelihood:steady_state_failed', ...
                'estimate_ckm_wedges_likelihood:stoch_simul_failed'}))
            T = size(path_rows, 1);
            wedges = table( ...
                (1:T)', nan(T, 1), nan(T, 1), nan(T, 1), nan(T, 1), ...
                'VariableNames', {'t', 'log_A', 'G_share', 'tau_l', 'tau_x'});
            status.success = false;
            status.failure_reason = string(ME.identifier);
            status.error_id = string(ME.identifier);
        else
            rethrow(ME);
        end
    end
end

function [report, info] = build_ckm_report_table(t, Y, wedges)
    efficiency_wedge = exp(wedges.log_A);
    labor_wedge = 1 - wedges.tau_l;
    investment_wedge = 1 ./ (1 + wedges.tau_x);
    invalid_labor = labor_wedge <= 0;
    invalid_investment = investment_wedge <= 0;
    labor_wedge(invalid_labor) = NaN;
    investment_wedge(invalid_investment) = NaN;

    report = table( ...
        t(:), ...
        Y(:), ...
        base_100(Y(:)), ...
        efficiency_wedge(:), ...
        base_100(efficiency_wedge(:)), ...
        labor_wedge(:), ...
        base_100(labor_wedge(:)), ...
        investment_wedge(:), ...
        base_100(investment_wedge(:)), ...
        'VariableNames', { ...
            't', ...
            'output', 'output_index', ...
            'efficiency_wedge', 'efficiency_index', ...
            'labor_wedge', 'labor_index', ...
            'investment_wedge', 'investment_index'});
    info = struct('bad_labor_count', nnz(invalid_labor), ...
                  'bad_investment_count', nnz(invalid_investment));
end

function idx = base_100(series)
    idx = 100 * series / series(1);
end
