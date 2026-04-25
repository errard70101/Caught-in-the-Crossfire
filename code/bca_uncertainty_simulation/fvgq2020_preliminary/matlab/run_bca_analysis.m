% Apply CKM wedge extraction, local projections, and GIRFs to FVGQ outputs.

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

pp.alpha = 0.36;
pp.beta = 0.994;
pp.delta = 0.01625;
pp.gamma = 2;
pp.nu = 1;
l_ss = 0.3546099291;
y_ss = 1.422989127;
c_ss = 1.070799318;
pp.chi = (1 - pp.alpha) * y_ss / (l_ss^(pp.nu + 1) * c_ss^pp.gamma);
fprintf('Prototype chi = %.6f\n', pp.chi);

T = readtable(exp1_csv);

Y = T.y;
C = T.cspt;
I = 0.06 * T.ivst;
L = T.labor;
K = T.k;

wedges = estimate_ckm_wedges(Y, C, I, L, K, pp);
fprintf('CKM on Exp1: max |G_share| = %.3e\n', max(abs(wedges.G_share)));
writetable(wedges, fullfile(output_dir, 'wedges_exp1.csv'));
report_fixed = build_ckm_report_table(wedges.t, Y, wedges);
writetable(report_fixed, fullfile(output_dir, 'wedges_exp1_report.csv'));
lp_targets_fixed = build_ckm_lp_targets(wedges);

ckm_like = estimate_ckm_wedges_likelihood(T, pp);
writetable(ckm_like.proxy_wedges, fullfile(output_dir, 'wedges_exp1_proxy.csv'));
writetable(ckm_like.smoothed_wedges, fullfile(output_dir, 'wedges_exp1_likelihood.csv'));
report_likelihood = build_ckm_report_table(ckm_like.smoothed_wedges.t, Y, ckm_like.smoothed_wedges);
writetable(report_likelihood, fullfile(output_dir, 'wedges_exp1_likelihood_report.csv'));
[lp_targets_likelihood, like_target_info] = build_ckm_lp_targets( ...
    ckm_like.smoothed_wedges, struct('invalid_policy', 'nan'));
if like_target_info.bad_labor_count > 0 || like_target_info.bad_investment_count > 0
    fprintf(['Likelihood transformed LP targets: dropped %d labor-target and %d ', ...
             'investment-target observations due to domain violations.\n'], ...
            like_target_info.bad_labor_count, like_target_info.bad_investment_count);
end
save(fullfile(output_dir, 'ckm_likelihood_exp1.mat'), 'ckm_like', '-v7.3');
fprintf('CKM likelihood on Exp1: saved %s\n', fullfile(output_dir, 'wedges_exp1_likelihood.csv'));

raw_wedge_names = {'log_A', 'G_share', 'tau_l', 'tau_x'};
transformed_wedge_names = {'log_efficiency_wedge', 'log_labor_wedge', 'log_investment_wedge'};
lp_target_names = lp_targets_fixed.Properties.VariableNames(2:end);
lp_target_matrix = table2array(lp_targets_fixed(:, lp_target_names));
lagged_targets = [nan(1, size(lp_target_matrix, 2)); lp_target_matrix(1:end-1, :)];
shocks = [T.uA, T.ue];
controls = [T.eA, T.ed, T.ethet, T.ud, T.sigAt, T.sigdt, T.siget, lagged_targets];
H_lp = 60;

lp_results = struct();
for j = 1:numel(lp_target_names)
    lp_results.(lp_target_names{j}) = local_projection( ...
        lp_targets_fixed.(lp_target_names{j}), shocks, controls, H_lp);
end
panel_controls_macro = [T.eA, T.ed, T.ethet, T.ud, T.sigdt, T.siget, lagged_targets];
panel_controls_fin = [T.eA, T.ed, T.ethet, T.ud, T.sigAt, T.sigdt, lagged_targets];
lp_shock_panels = build_lp_shock_panels(T.sigAt, T.siget, shocks, ...
                                        panel_controls_macro, panel_controls_fin, H_lp);
save(fullfile(output_dir, 'lp_results.mat'), 'lp_results', 'lp_target_names', ...
      'lp_shock_panels', 'H_lp', '-v7.3');
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
save(fullfile(output_dir, 'lp_results_likelihood.mat'), ...
     'lp_results_likelihood', 'lp_target_names', 'lp_shock_panels_likelihood', ...
     'H_lp', '-v7.3');
fprintf('LP on Exp1 likelihood wedges: saved %s\n', ...
        fullfile(output_dir, 'lp_results_likelihood.mat'));

lp_width_table = compare_lp_widths(lp_results, lp_results_likelihood, lp_target_names);
writetable(lp_width_table, fullfile(output_dir, 'lp_interval_comparison.csv'));
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
        lp_targets_fixed.(lp_target_names{j}), shocks, controls_no_sv, H_lp);
end
panel_controls_macro_no_sv = [T.eA, T.ed, T.ethet, T.ud, lagged_targets];
panel_controls_fin_no_sv = [T.eA, T.ed, T.ethet, T.ud, lagged_targets];
lp_shock_panels_no_svctrl = build_lp_shock_panels(T.sigAt, T.siget, shocks, ...
                                                  panel_controls_macro_no_sv, ...
                                                  panel_controls_fin_no_sv, H_lp);
save(fullfile(output_dir, 'lp_results_no_svctrl.mat'), ...
     'lp_results_no_svctrl', 'lp_target_names', ...
     'lp_shock_panels_no_svctrl', 'H_lp', '-v7.3');
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
save(fullfile(output_dir, 'lp_results_likelihood_no_svctrl.mat'), ...
     'lp_results_likelihood_no_svctrl', 'lp_target_names', ...
     'lp_shock_panels_likelihood_no_svctrl', 'H_lp', '-v7.3');
fprintf('Sensitivity LP likelihood (no SV-state controls): saved %s\n', ...
        fullfile(output_dir, 'lp_results_likelihood_no_svctrl.mat'));

lp_sens_table = compare_lp_peak_table(lp_results, lp_results_no_svctrl, lp_target_names);
writetable(lp_sens_table, fullfile(output_dir, 'lp_no_svctrl_peak_comparison.csv'));
fprintf('LP no-SV-control peak comparison: saved %s\n', ...
        fullfile(output_dir, 'lp_no_svctrl_peak_comparison.csv'));

mc_config = struct('B', 10000, 'T', 400, 'H', H_lp, ...
                   'seed_base', 2026042400, 'verbose', true, ...
                   'progress_every', 250);
sim_workspace = load(workspace_mat, 'M_', 'oo_', 'options_', 'sss_state', 'var_names', 'exo_var_names');
lp_results_mc_fixed = monte_carlo_lp_bands(sim_workspace, pp, mc_config);
save(fullfile(output_dir, 'lp_results_mc_fixed.mat'), ...
     'lp_results_mc_fixed', 'lp_target_names', '-v7.3');
writetable(monte_carlo_summary_table(lp_results_mc_fixed), ...
           fullfile(output_dir, 'lp_results_mc_fixed_summary.csv'));
fprintf(['Monte Carlo LP on fixed-point wedges: saved %s ', ...
        'with B=%d, T=%d, center=median\n'], ...
        fullfile(output_dir, 'lp_results_mc_fixed.mat'), mc_config.B, mc_config.T);

S = load(exp2_mat);
if isfield(S, 'exp2_shock_size')
    exp2_shock_size = S.exp2_shock_size;
else
    exp2_shock_size = 1;
end
var_names = S.var_names;
y_idx = find(strcmp(var_names, 'y'));
cspt_idx = find(strcmp(var_names, 'cspt'));
ivst_idx = find(strcmp(var_names, 'ivst'));
labor_idx = find(strcmp(var_names, 'labor'));
k_idx = find(strcmp(var_names, 'k'));

girf = struct();
girf_likelihood = struct();
girf_transformed = struct();
girf_transformed_likelihood = struct();
girf_transform_info = struct();
girf_transform_info_likelihood = struct();
for tag = {'fin', 'macro'}
    tag_str = tag{1};
    pb = S.(['paths_base_' tag_str]);
    ps = S.(['paths_shock_' tag_str]);
    [Npairs, Hpairs, ~] = size(pb);

    wedge_base = zeros(Npairs, Hpairs, numel(raw_wedge_names));
    wedge_shock = zeros(Npairs, Hpairs, numel(raw_wedge_names));
    wedge_base_like = zeros(Npairs, Hpairs, numel(raw_wedge_names));
    wedge_shock_like = zeros(Npairs, Hpairs, numel(raw_wedge_names));
    for i = 1:Npairs
        wb = wedges_from_path(squeeze(pb(i, :, :)), y_idx, cspt_idx, ivst_idx, ...
                              labor_idx, k_idx, pp);
        ws = wedges_from_path(squeeze(ps(i, :, :)), y_idx, cspt_idx, ivst_idx, ...
                              labor_idx, k_idx, pp);
        wb_like = likelihood_wedges_from_path(squeeze(pb(i, :, :)), var_names, pp);
        ws_like = likelihood_wedges_from_path(squeeze(ps(i, :, :)), var_names, pp);
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
end

save(fullfile(output_dir, 'wedges_girf.mat'), 'girf', 'girf_transformed', ...
     'raw_wedge_names', 'transformed_wedge_names', 'girf_transform_info', ...
     'exp2_shock_size', '-v7.3');
fprintf('GIRF: saved %s\n', fullfile(output_dir, 'wedges_girf.mat'));
save(fullfile(output_dir, 'wedges_girf_likelihood.mat'), ...
     'girf_likelihood', 'girf_transformed_likelihood', 'raw_wedge_names', ...
     'transformed_wedge_names', 'girf_transform_info_likelihood', ...
     'exp2_shock_size', '-v7.3');
fprintf('GIRF likelihood: saved %s\n', fullfile(output_dir, 'wedges_girf_likelihood.mat'));

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

function tbl = compare_lp_widths(lp_fixed, lp_like, wedge_names)
    rows = {};
    for j = 1:numel(wedge_names)
        w = wedge_names{j};
        for s = 1:2
            fixed = lp_fixed.(w);
            like = lp_like.(w);
            rows(end + 1, :) = {w, s, ...
                mean(fixed.ci_hi(:, s) - fixed.ci_lo(:, s), 'omitnan'), ...
                mean(like.ci_hi(:, s) - like.ci_lo(:, s), 'omitnan'), ...
                mean(like.ci_hi(:, s) - like.ci_lo(:, s), 'omitnan') / ...
                    mean(fixed.ci_hi(:, s) - fixed.ci_lo(:, s), 'omitnan')}; %#ok<AGROW>
        end
    end
    tbl = cell2table(rows, 'VariableNames', ...
        {'wedge', 'shock_index', 'mean_ci_width_fixed', 'mean_ci_width_likelihood', 'width_ratio'});
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

function wedges = wedges_from_path(path_rows, y_idx, cspt_idx, ivst_idx, ...
                                   labor_idx, k_idx, pp)
    Y = path_rows(:, y_idx);
    C = path_rows(:, cspt_idx);
    I = 0.06 * path_rows(:, ivst_idx);
    L = path_rows(:, labor_idx);
    K = path_rows(:, k_idx);
    wedges = estimate_ckm_wedges(Y, C, I, L, K, pp);
end

function wedges = likelihood_wedges_from_path(path_rows, var_names, pp)
    tbl = array2table(path_rows, 'VariableNames', var_names);
    tbl.t = (1:height(tbl))';
    tbl = movevars(tbl, 't', 'Before', 1);
    like_opts = struct('force_recompile', false, 'verbose', false);
    evalc('tmp_result = estimate_ckm_wedges_likelihood(tbl, pp, like_opts);');
    wedges = tmp_result.smoothed_wedges;
end

function report = build_ckm_report_table(t, Y, wedges)
    efficiency_wedge = exp(wedges.log_A);
    labor_wedge = 1 - wedges.tau_l;
    investment_wedge = 1 ./ (1 + wedges.tau_x);

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
end

function idx = base_100(series)
    idx = 100 * series / series(1);
end
