% Plot LP and GIRF wedge responses from the preliminary FVGQ pipeline.

clear;
clc;

this_file = mfilename('fullpath');
matlab_dir = fileparts(this_file);
root_dir = fileparts(matlab_dir);
output_dir = fullfile(root_dir, 'output');

LP = load(fullfile(output_dir, 'lp_results.mat'));
G = load(fullfile(output_dir, 'wedges_girf.mat'));
assert_provenance(LP, 'lp_results.mat', 'inside_dynare_auxiliary');
assert_provenance(G, 'wedges_girf.mat', 'inside_dynare_auxiliary');
lp_mc_path = fullfile(output_dir, 'lp_results_mc_dgp.mat');
lp_like_path = fullfile(output_dir, 'lp_results_likelihood.mat');
girf_like_path = fullfile(output_dir, 'wedges_girf_likelihood.mat');
report_aux_path = fullfile(output_dir, 'wedges_exp1_report.csv');
report_posthoc_path = fullfile(output_dir, 'wedges_exp1_posthoc_report.csv');
report_like_path = fullfile(output_dir, 'wedges_exp1_likelihood_report.csv');
lp_no_sv_path = fullfile(output_dir, 'lp_results_no_svctrl.mat');
lp_like_no_sv_path = fullfile(output_dir, 'lp_results_likelihood_no_svctrl.mat');

has_lp_mc = isfile(lp_mc_path);
if has_lp_mc
    LP_mc = load(lp_mc_path);
    assert_provenance(LP_mc, 'lp_results_mc_dgp.mat', 'inside_dynare_auxiliary');
end
has_likelihood = isfile(lp_like_path);
if has_likelihood
    LP_like = load(lp_like_path);
    assert_provenance(LP_like, 'lp_results_likelihood.mat', 'likelihood_kalman_filter');
end
has_girf_likelihood = isfile(girf_like_path);
if has_girf_likelihood
    G_like = load(girf_like_path);
    assert_provenance(G_like, 'wedges_girf_likelihood.mat', 'likelihood_kalman_filter');
end
has_lp_no_sv = isfile(lp_no_sv_path);
if has_lp_no_sv
    LP_no_sv = load(lp_no_sv_path);
    assert_provenance(LP_no_sv, 'lp_results_no_svctrl.mat', 'inside_dynare_auxiliary');
end
has_lp_like_no_sv = isfile(lp_like_no_sv_path);
if has_lp_like_no_sv
    LP_like_no_sv = load(lp_like_no_sv_path);
    assert_provenance(LP_like_no_sv, ...
                      'lp_results_likelihood_no_svctrl.mat', ...
                      'likelihood_kalman_filter');
end

R_aux = readtable(report_aux_path);
assert_csv_provenance(R_aux, 'wedges_exp1_report.csv', 'inside_dynare_auxiliary');
R_posthoc = readtable(report_posthoc_path);
assert_csv_provenance(R_posthoc, 'wedges_exp1_posthoc_report.csv', 'posthoc_ckm_accounting');
assert_matching_run_id(R_aux, R_posthoc, ...
                       'wedges_exp1_report.csv', ...
                       'wedges_exp1_posthoc_report.csv');
has_report_likelihood = isfile(report_like_path);
if has_report_likelihood
    R_like = readtable(report_like_path);
    assert_csv_provenance(R_like, 'wedges_exp1_likelihood_report.csv', ...
                          'likelihood_kalman_filter');
    assert_matching_run_id(R_posthoc, R_like, ...
                           'wedges_exp1_posthoc_report.csv', ...
                           'wedges_exp1_likelihood_report.csv');
end

girf_shock_label = girf_shock_size_label(G);
lp_meta = lp_panel_meta(get_lp_names(LP));
girf_meta = transformed_girf_panel_meta(get_transformed_girf_names(G));
dgp_fill = [0.82 0.87 0.95];
dgp_line = [0.00 0.25 0.75];
like_fill = [0.98 0.88 0.78];
like_line = [0.85 0.33 0.10];

for shock_tag = {'macro', 'fin'}
    ts = shock_tag{1};
    shock_col = shock_name_to_col(ts);
    shock_meta = shock_panel_meta(ts);

    fig = figure('Visible', 'off', 'Position', [100 100 980 760], 'Color', 'w');
    for j = 1:numel(lp_meta)
        subplot(2, 2, j);
        lp = LP.lp_results.(lp_meta(j).name);
        plot_lp_single(lp, shock_col, lp_meta(j).scale, dgp_fill, dgp_line);
        title(lp_meta(j).title);
        xlabel('Horizon');
        ylabel(lp_meta(j).ylabel);
    end
    subplot(2, 2, 4);
    if isfield(LP, 'lp_shock_panels') && isfield(LP.lp_shock_panels, ts)
        plot_lp_single(LP.lp_shock_panels.(ts), shock_col, 1, dgp_fill, dgp_line);
        title(shock_meta.title);
        xlabel('Horizon');
        ylabel(shock_meta.ylabel);
    else
        axis off;
    end
    sgtitle(sprintf(['LP (Inside-Dynare auxiliary wedges, T=20000 HAC): ', ...
                     'response to %s uncertainty shock'], ts));
    saveas(fig, fullfile(output_dir, sprintf('bca_lp_%s.png', ts)));
    saveas(fig, fullfile(output_dir, sprintf('bca_lp_%s_dgp.png', ts)));
    close(fig);

    if has_lp_mc
        fig = figure('Visible', 'off', 'Position', [100 100 980 760], 'Color', 'w');
        for j = 1:numel(lp_meta)
            subplot(2, 2, j);
            lp_mc = LP_mc.lp_results_mc_dgp.summary.(lp_meta(j).name);
            plot_lp_mc_single(lp_mc, shock_col, lp_meta(j).scale, dgp_fill, dgp_line);
            title(lp_meta(j).title);
            xlabel('Horizon');
            ylabel(lp_meta(j).ylabel);
        end
        subplot(2, 2, 4);
        if isfield(LP_mc.lp_results_mc_dgp, 'shock_panel_summary') && ...
                isfield(LP_mc.lp_results_mc_dgp.shock_panel_summary, ts)
            plot_lp_shock_mc_single(LP_mc.lp_results_mc_dgp.shock_panel_summary.(ts), ...
                                    dgp_fill, dgp_line);
            title(shock_meta.title);
            xlabel('Horizon');
            ylabel(shock_meta.ylabel);
        else
            axis off;
        end
        sgtitle(sprintf(['LP (Inside-Dynare auxiliary wedges): Monte Carlo median ', ...
                         'and 95%% band to %s uncertainty shock'], ts));
        saveas(fig, fullfile(output_dir, sprintf('bca_lp_%s_mc.png', ts)));
        close(fig);
    end

    if has_likelihood
        fig = figure('Visible', 'off', 'Position', [100 100 980 760], 'Color', 'w');
        for j = 1:numel(lp_meta)
            subplot(2, 2, j);
            lp = LP_like.lp_results_likelihood.(lp_meta(j).name);
            plot_lp_single(lp, shock_col, lp_meta(j).scale, like_fill, like_line);
            title(lp_meta(j).title);
            xlabel('Horizon');
            ylabel(lp_meta(j).ylabel);
        end
        subplot(2, 2, 4);
        if isfield(LP_like, 'lp_shock_panels_likelihood') && isfield(LP_like.lp_shock_panels_likelihood, ts)
            lp_diag = LP_like.lp_shock_panels_likelihood.(ts);
            plot_lp_single(lp_diag, shock_col, 1, like_fill, like_line);
            title(shock_meta.title);
            xlabel('Horizon');
            ylabel(shock_meta.ylabel);
        else
            axis off;
        end
        sgtitle(sprintf(['LP (Likelihood Kalman-filter wedges, T=20000 HAC): ', ...
                         'response to %s uncertainty shock'], ts));
        saveas(fig, fullfile(output_dir, sprintf('bca_lp_%s_likelihood.png', ts)));
        close(fig);

        fig = figure('Visible', 'off', 'Position', [100 100 980 760], 'Color', 'w');
        for j = 1:numel(lp_meta)
            subplot(2, 2, j);
            dgp_lp = LP.lp_results.(lp_meta(j).name);
            like_lp = LP_like.lp_results_likelihood.(lp_meta(j).name);
            plot_lp_compare(dgp_lp, like_lp, shock_col, lp_meta(j).scale, ...
                            dgp_fill, dgp_line, like_fill, like_line);
            title(lp_meta(j).title);
            xlabel('Horizon');
            ylabel(lp_meta(j).ylabel);
            if j == 1
                legend({'True DGP 95% CI', 'True DGP', ...
                        'Likelihood 95% CI', 'Likelihood'}, ...
                       'Location', 'best', 'Box', 'off');
            end
        end
        subplot(2, 2, 4);
        if isfield(LP, 'lp_shock_panels') && isfield(LP.lp_shock_panels, ts) && ...
                isfield(LP_like, 'lp_shock_panels_likelihood') && ...
                isfield(LP_like.lp_shock_panels_likelihood, ts)
            plot_lp_compare(LP.lp_shock_panels.(ts), LP_like.lp_shock_panels_likelihood.(ts), ...
                            shock_col, 1, dgp_fill, dgp_line, like_fill, like_line);
            title(shock_meta.title);
            xlabel('Horizon');
            ylabel(shock_meta.ylabel);
        else
            axis off;
        end
         sgtitle(sprintf(['LP comparison: Inside-Dynare auxiliary vs ', ...
                          'Likelihood-smoothed CKM wedges, %s shock'], ts));
        saveas(fig, fullfile(output_dir, sprintf('bca_lp_compare_%s.png', ts)));
        close(fig);
    end
end

for shock_tag = {'macro', 'fin'}
    ts = shock_tag{1};
    gd = G.girf_transformed.(ts);
    h = (0:size(gd.mean, 1) - 1)';

    fig = figure('Visible', 'off', 'Position', [100, 100, 1200, 500], 'Color', 'w');
    t = tiledlayout(1, 3, 'TileSpacing', 'compact', 'Padding', 'compact');
    for j = 1:numel(girf_meta)
        nexttile;
        plot_girf_single(gd, j, h, girf_meta(j).scale, ...
                         girf_meta(j).fill_color, girf_meta(j).line_color);
        title(girf_meta(j).title, 'FontWeight', 'bold');
        xlabel('Horizon');
        ylabel(girf_meta(j).ylabel);
        if j == 1
            legend({'95% CI for mean', 'Mean GIRF'}, ...
                   'Location', 'best', 'Box', 'off', 'FontSize', 8);
        end
    end
    title(t, sprintf(['FVGQ GIRF Wedge Responses to %s Uncertainty Shock\n', ...
                      'Inside-Dynare Auxiliary Wedges, %s, 95%% CI for Mean'], ...
                     title_case_shock(ts), girf_shock_label), ...
          'FontWeight', 'bold', 'FontSize', 14);
    saveas(fig, fullfile(output_dir, sprintf('bca_girf_%s.png', ts)));
    close(fig);

    if has_girf_likelihood
        gd_like = G_like.girf_transformed_likelihood.(ts);

        fig = figure('Visible', 'off', 'Position', [100, 100, 1200, 500], 'Color', 'w');
        t = tiledlayout(1, 3, 'TileSpacing', 'compact', 'Padding', 'compact');
        for j = 1:numel(girf_meta)
            nexttile;
            plot_girf_single(gd_like, j, h, girf_meta(j).scale, ...
                             girf_meta(j).fill_color, girf_meta(j).line_color);
            title(girf_meta(j).title, 'FontWeight', 'bold');
            xlabel('Horizon');
            ylabel(girf_meta(j).ylabel);
            if j == 1
                legend({'95% CI for mean', 'Mean GIRF'}, ...
                       'Location', 'best', 'Box', 'off', 'FontSize', 8);
            end
        end
        title(t, sprintf(['FVGQ GIRF Wedge Responses to %s Uncertainty Shock\n', ...
                          'Likelihood-Smoothed CKM Wedges, %s, 95%% CI for Mean'], ...
                         title_case_shock(ts), girf_shock_label), ...
              'FontWeight', 'bold', 'FontSize', 14);
        saveas(fig, fullfile(output_dir, sprintf('bca_girf_%s_likelihood.png', ts)));
        close(fig);

        fig = figure('Visible', 'off', 'Position', [100, 100, 1200, 500], 'Color', 'w');
        t = tiledlayout(1, 3, 'TileSpacing', 'compact', 'Padding', 'compact');
        for j = 1:numel(girf_meta)
            nexttile;
            plot_girf_compare(gd, gd_like, j, h, girf_meta(j).scale, ...
                              dgp_fill, dgp_line, like_fill, like_line);
            title(girf_meta(j).title, 'FontWeight', 'bold');
            xlabel('Horizon');
            ylabel(girf_meta(j).ylabel);
            if j == 1
                legend({'True DGP 95% CI for mean', 'True DGP', ...
                        'Likelihood 95% CI for mean', 'Likelihood'}, ...
                       'Location', 'best', 'Box', 'off');
            end
        end
        title(t, sprintf(['FVGQ GIRF Wedge Comparison to %s Uncertainty Shock\n', ...
                          'Inside-Dynare Auxiliary vs Likelihood-Smoothed CKM Wedges, %s'], ...
                         title_case_shock(ts), girf_shock_label), ...
              'FontWeight', 'bold', 'FontSize', 14);
        saveas(fig, fullfile(output_dir, sprintf('bca_girf_compare_%s.png', ts)));
        close(fig);
    end
end

% --- Sensitivity LP figures: drop contemporaneous SV-state controls ---
% Removing (sigAt, sigdt, siget) from the control set lets the LP coefficient
% on (uA, ue) capture the full SV transmission channel rather than only the
% residual after the mediator is partialled out. Compare with the baseline
% LP (which conditions on SV states and may understate the channel).
if has_lp_no_sv
    for shock_tag = {'macro', 'fin'}
        ts = shock_tag{1};
        shock_col = shock_name_to_col(ts);
        shock_meta = shock_panel_meta(ts);
        fig = figure('Visible', 'off', 'Position', [100 100 980 760], 'Color', 'w');
        for j = 1:numel(lp_meta)
            subplot(2, 2, j);
            lp_base = LP.lp_results.(lp_meta(j).name);
            lp_sens = LP_no_sv.lp_results_no_svctrl.(lp_meta(j).name);
            plot_lp_compare(lp_base, lp_sens, shock_col, lp_meta(j).scale, ...
                            dgp_fill, dgp_line, like_fill, like_line);
            title(lp_meta(j).title);
            xlabel('Horizon');
            ylabel(lp_meta(j).ylabel);
            if j == 1
                legend({'Baseline 95% CI', 'Baseline (with SV ctrl)', ...
                        'No-SV 95% CI', 'No-SV control'}, ...
                       'Location', 'best', 'Box', 'off', 'FontSize', 8);
            end
        end
        subplot(2, 2, 4);
        if isfield(LP, 'lp_shock_panels') && isfield(LP.lp_shock_panels, ts) && ...
                isfield(LP_no_sv, 'lp_shock_panels_no_svctrl') && ...
                isfield(LP_no_sv.lp_shock_panels_no_svctrl, ts)
            plot_lp_compare(LP.lp_shock_panels.(ts), ...
                            LP_no_sv.lp_shock_panels_no_svctrl.(ts), ...
                            shock_col, 1, dgp_fill, dgp_line, like_fill, like_line);
            title(shock_meta.title);
            xlabel('Horizon');
            ylabel(shock_meta.ylabel);
        else
            axis off;
        end
        sgtitle(sprintf(['LP sensitivity (Inside-Dynare auxiliary, T=20000 HAC): ' ...
                         'baseline vs. SV-state controls dropped, %s shock'], ts));
        saveas(fig, fullfile(output_dir, sprintf('bca_lp_%s_no_svctrl.png', ts)));
        close(fig);
    end
end

plot_measured_wedge_overlay(R_aux, dgp_line, ...
    fullfile(output_dir, 'bca_measured_wedges_auxiliary.png'), ...
    'Inside-Dynare auxiliary wedges (t=1=100)');

plot_measured_wedge_overlay(R_posthoc, dgp_line, ...
    fullfile(output_dir, 'bca_measured_wedges_posthoc.png'), ...
    'Post-hoc CKM accounting wedges (t=1=100)');

if has_report_likelihood
    plot_measured_wedge_overlay(R_like, like_line, ...
        fullfile(output_dir, 'bca_measured_wedges_likelihood.png'), ...
        'Likelihood-smoothed CKM wedges (t=1=100)');

    fig = figure('Visible', 'off', 'Position', [100 100 980 760], 'Color', 'w');
    compare_meta = { ...
        {'output_index', 'Output'}, ...
        {'efficiency_index', 'Efficiency wedge'}, ...
        {'labor_index', 'Labor wedge'}, ...
        {'investment_index', 'Investment wedge'}};
    for j = 1:numel(compare_meta)
        subplot(2, 2, j);
        name = compare_meta{j}{1};
        title_text = compare_meta{j}{2};
        if strcmp(name, 'output_index')
            plot(R_posthoc.t, R_posthoc.(name), '-', 'Color', dgp_line, 'LineWidth', 1.2);
        else
            plot(R_posthoc.t, R_posthoc.(name), '-', 'Color', dgp_line, 'LineWidth', 1.2);
            hold on;
            plot(R_like.t, R_like.(name), '--', 'Color', like_line, 'LineWidth', 1.2);
        end
        yline(100, 'k:');
        title(title_text);
        xlabel('t');
        ylabel('Index (t=1=100)');
        grid on;
        if j == 2
            legend({'Post-hoc CKM', 'Likelihood (Kalman filter)'}, ...
                   'Location', 'best', 'Box', 'off');
        end
    end
    sgtitle('Measured wedges and output: post-hoc CKM vs likelihood');
    saveas(fig, fullfile(output_dir, 'bca_wedges_exp1_compare.png'));
    close(fig);

    fig = figure('Visible', 'off', 'Position', [100 100 980 760], 'Color', 'w');
    for j = 1:numel(compare_meta)
        subplot(2, 2, j);
        name = compare_meta{j}{1};
        title_text = compare_meta{j}{2};
        plot(R_aux.t, R_aux.(name), '-', 'Color', dgp_line, 'LineWidth', 1.2);
        hold on;
        plot(R_posthoc.t, R_posthoc.(name), '--', 'Color', like_line, 'LineWidth', 1.2);
        yline(100, 'k:');
        title(title_text);
        xlabel('t');
        ylabel('Index (t=1=100)');
        grid on;
        if j == 2
            legend({'Inside-Dynare auxiliary', 'Post-hoc CKM'}, ...
                   'Location', 'best', 'Box', 'off');
        end
    end
    sgtitle('Measured wedges and output: auxiliary vs post-hoc CKM');
    saveas(fig, fullfile(output_dir, 'bca_wedges_exp1_aux_vs_posthoc.png'));
    close(fig);
end

fprintf('Wrote LP, CKM-style measured-wedge, comparison, and GIRF figures to %s\n', output_dir);

function shock_col = shock_name_to_col(ts)
    if strcmp(ts, 'macro')
        shock_col = 1;
    else
        shock_col = 2;
    end
end

function assert_provenance(S, filename, expected_source)
    expected_schema = 'ckm_dual_track_v1';
    if ~isfield(S, 'provenance') || ~isstruct(S.provenance)
        error('plot_bca_responses:missing_provenance', ...
              ['%s has no Inside-Dynare provenance metadata. ', ...
               'Delete stale outputs and rerun run_bca_analysis.'], filename);
    end
    if ~isfield(S.provenance, 'schema_version') || ...
            ~strcmp(S.provenance.schema_version, expected_schema)
        error('plot_bca_responses:bad_schema_version', ...
              '%s has schema %s, expected %s.', filename, ...
              field_or_missing(S.provenance, 'schema_version'), expected_schema);
    end
    if ~isfield(S.provenance, 'wedge_source') || ...
            ~strcmp(S.provenance.wedge_source, expected_source)
        error('plot_bca_responses:bad_wedge_source', ...
              '%s has wedge_source %s, expected %s.', filename, ...
              field_or_missing(S.provenance, 'wedge_source'), expected_source);
    end
end

function assert_csv_provenance(T, filename, expected_source)
    expected_schema = 'ckm_dual_track_v1';
    required_cols = {'schema_version', 'wedge_source', 'run_id', 'artifact_role'};
    missing_cols = setdiff(required_cols, T.Properties.VariableNames);
    if ~isempty(missing_cols)
        error('plot_bca_responses:missing_csv_provenance', ...
              '%s is missing provenance columns: %s.', ...
              filename, strjoin(missing_cols, ', '));
    end
    schema_values = unique(string(T.schema_version));
    schema_values = schema_values(strlength(schema_values) > 0);
    if numel(schema_values) ~= 1 || ~strcmp(char(schema_values), expected_schema)
        error('plot_bca_responses:bad_csv_schema', ...
              '%s has schema %s, expected %s.', filename, ...
              char(join(schema_values, ', ')), expected_schema);
    end
    wedge_sources = unique(string(T.wedge_source));
    wedge_sources = wedge_sources(strlength(wedge_sources) > 0);
    if numel(wedge_sources) ~= 1 || ~strcmp(char(wedge_sources), expected_source)
        error('plot_bca_responses:bad_csv_wedge_source', ...
              '%s has wedge_source %s, expected %s.', filename, ...
              char(join(wedge_sources, ', ')), expected_source);
    end
end

function assert_matching_run_id(T_left, T_right, left_name, right_name)
    left_run_ids = unique(string(T_left.run_id));
    left_run_ids = left_run_ids(strlength(left_run_ids) > 0);
    right_run_ids = unique(string(T_right.run_id));
    right_run_ids = right_run_ids(strlength(right_run_ids) > 0);
    if numel(left_run_ids) ~= 1 || numel(right_run_ids) ~= 1 || ...
            ~strcmp(char(left_run_ids), char(right_run_ids))
        error('plot_bca_responses:mismatched_csv_runs', ...
              '%s and %s do not share a single run_id.', left_name, right_name);
    end
end

function value = field_or_missing(S, field)
    if isfield(S, field)
        value = S.(field);
    else
        value = '<missing>';
    end
end

function meta = lp_panel_meta(wedge_names)
    expected = {'log_efficiency_wedge', 'log_labor_wedge', 'log_investment_wedge'};
    if ~isequal(wedge_names(:)', expected)
        error('plot_bca_responses:unexpected_lp_targets', ...
              'Unexpected LP target ordering in lp_results.mat.');
    end

    meta = struct( ...
        'name', wedge_names(:)', ...
        'title', {'Efficiency wedge: log A', 'Labor wedge: log(1-\tau_l)', ...
                  'Investment wedge: log(1/(1+\tau_x))'}, ...
        'ylabel', {'Approx. percent deviation', 'Approx. percent deviation', ...
                   'Approx. percent deviation'}, ...
        'scale', {100, 100, 100}, ...
        'fill_color', {[0.8 0.85 0.95], [0.95 0.8 0.8], [0.8 0.95 0.8]}, ...
        'line_color', {[0 0.447 0.741], [0.85 0.325 0.098], [0.466 0.674 0.188]});
end

function meta = transformed_girf_panel_meta(wedge_names)
    expected = {'log_efficiency_wedge', 'log_labor_wedge', 'log_investment_wedge'};
    if ~isequal(wedge_names(:)', expected)
        error('plot_bca_responses:unexpected_transformed_girf_targets', ...
              'Unexpected transformed GIRF wedge ordering in wedges_girf.mat.');
    end

    meta = struct( ...
        'name', wedge_names(:)', ...
        'title', {'Efficiency wedge: log A', 'Labor wedge: log(1-\tau_l)', ...
                  'Investment wedge: log(1/(1+\tau_x))'}, ...
        'ylabel', {'Approx. percent deviation', 'Approx. percent deviation', ...
                   'Approx. percent deviation'}, ...
        'scale', {100, 100, 100}, ...
        'fill_color', {[0.8 0.85 0.95], [0.95 0.8 0.8], [0.8 0.95 0.8]}, ...
        'line_color', {[0 0.447 0.741], [0.85 0.325 0.098], [0.466 0.674 0.188]});
end

function meta = raw_resource_panel_meta()
    meta = struct('title', 'Resource residual: G/Y (raw diagnostic)', ...
                   'ylabel', 'Percentage points', ...
                   'scale', 100, ...
                   'ylim', [-1e-12, 1e-12]);
end

function meta = shock_panel_meta(ts)
    if strcmp(ts, 'macro')
        meta.title = 'Volatility state: sigAt';
    else
        meta.title = 'Volatility state: siget';
    end
    meta.ylabel = 'Log-volatility state';
end

function label = title_case_shock(ts)
    if strcmp(ts, 'macro')
        label = 'Macro';
    elseif strcmp(ts, 'fin')
        label = 'Financial';
    else
        label = ts;
    end
end

function names = get_lp_names(LP)
    if isfield(LP, 'lp_target_names')
        names = LP.lp_target_names;
    elseif isfield(LP, 'wedge_names')
        names = LP.wedge_names;
    else
        error('plot_bca_responses:missing_lp_names', ...
              'Could not locate LP target names in lp_results.mat.');
    end
end

function names = get_raw_girf_names(G)
    if isfield(G, 'raw_wedge_names')
        names = G.raw_wedge_names;
    elseif isfield(G, 'wedge_names')
        names = G.wedge_names;
    else
        error('plot_bca_responses:missing_raw_girf_names', ...
               'Could not locate raw wedge names in wedges_girf.mat.');
    end
end

function names = get_transformed_girf_names(G)
    if isfield(G, 'transformed_wedge_names')
        names = G.transformed_wedge_names;
    else
        error('plot_bca_responses:missing_transformed_girf_names', ...
              'Could not locate transformed GIRF wedge names in wedges_girf.mat.');
    end
end

function plot_lp_single(lp, shock_col, scale, fill_color, line_color)
    h = lp.horizons;
    b = scale * lp.beta(:, shock_col);
    lo = scale * lp.ci_lo(:, shock_col);
    hi = scale * lp.ci_hi(:, shock_col);
    fill([h; flipud(h)], [lo; flipud(hi)], fill_color, ...
         'EdgeColor', 'none', 'FaceAlpha', 0.75);
    hold on;
    plot(h, b, '-', 'Color', line_color, 'LineWidth', 1.5);
    yline(0, 'k:');
    grid on;
end

function plot_lp_compare(lp_dgp, lp_like, shock_col, scale, dgp_fill, dgp_line, like_fill, like_line)
    h = lp_dgp.horizons;
    fill([h; flipud(h)], ...
         scale * [lp_dgp.ci_lo(:, shock_col); flipud(lp_dgp.ci_hi(:, shock_col))], ...
         dgp_fill, 'EdgeColor', 'none', 'FaceAlpha', 0.50);
    hold on;
    plot(h, scale * lp_dgp.beta(:, shock_col), '-', 'Color', dgp_line, 'LineWidth', 1.5);
    fill([h; flipud(h)], ...
         scale * [lp_like.ci_lo(:, shock_col); flipud(lp_like.ci_hi(:, shock_col))], ...
         like_fill, 'EdgeColor', 'none', 'FaceAlpha', 0.45);
    plot(h, scale * lp_like.beta(:, shock_col), '--', 'Color', like_line, 'LineWidth', 1.5);
    yline(0, 'k:');
    grid on;
end

function plot_lp_mc_single(lp_mc, shock_col, scale, fill_color, line_color)
    h = lp_mc.horizons;
    fill([h; flipud(h)], scale * [lp_mc.q025(:, shock_col); flipud(lp_mc.q975(:, shock_col))], ...
         fill_color, 'EdgeColor', 'none', 'FaceAlpha', 0.75);
    hold on;
    plot(h, scale * lp_mc.median(:, shock_col), '-', 'Color', line_color, 'LineWidth', 1.5);
    yline(0, 'k:');
    grid on;
end

function plot_lp_shock_mc_single(lp_mc, fill_color, line_color)
    h = lp_mc.horizons;
    fill([h; flipud(h)], [lp_mc.q025; flipud(lp_mc.q975)], ...
         fill_color, 'EdgeColor', 'none', 'FaceAlpha', 0.75);
    hold on;
    plot(h, lp_mc.median, '-', 'Color', line_color, 'LineWidth', 1.5);
    yline(0, 'k:');
    grid on;
end

function plot_girf_single(gd, wedge_idx, h, scale, fill_color, line_color)
    % 95% CI for the mean GIRF (precision of average response across pairs).
    % The 5-95% pair-dispersion band is intentionally dropped because, at the
    % typical 26x ratio vs the precision band, it visually drowns out the
    % mean signal and conflates state-dependence with estimation precision.
    if isfield(gd, 'ci_lo_mean') && isfield(gd, 'ci_hi_mean')
        fill([h; flipud(h)], scale * [gd.ci_lo_mean(:, wedge_idx); ...
                                       flipud(gd.ci_hi_mean(:, wedge_idx))], ...
             fill_color, 'EdgeColor', 'none', 'FaceAlpha', 0.75);
        hold on;
    else
        hold on;
    end
    plot(h, scale * gd.mean(:, wedge_idx), '-', 'Color', line_color, 'LineWidth', 1.5);
    yline(0, 'k:');
    grid on;
end

function plot_girf_compare(gd_dgp, gd_like, wedge_idx, h, scale, dgp_fill, dgp_line, like_fill, like_line)
    % Use 95% CI for the mean (precision band) in both series; the 5-95%
    % pair-dispersion band is omitted as in plot_girf_single.
    if isfield(gd_dgp, 'ci_lo_mean') && isfield(gd_dgp, 'ci_hi_mean')
        fill([h; flipud(h)], ...
             scale * [gd_dgp.ci_lo_mean(:, wedge_idx); flipud(gd_dgp.ci_hi_mean(:, wedge_idx))], ...
             dgp_fill, 'EdgeColor', 'none', 'FaceAlpha', 0.55);
        hold on;
    else
        hold on;
    end
    plot(h, scale * gd_dgp.mean(:, wedge_idx), '-', 'Color', dgp_line, 'LineWidth', 1.5);
    if isfield(gd_like, 'ci_lo_mean') && isfield(gd_like, 'ci_hi_mean')
        fill([h; flipud(h)], ...
             scale * [gd_like.ci_lo_mean(:, wedge_idx); flipud(gd_like.ci_hi_mean(:, wedge_idx))], ...
             like_fill, 'EdgeColor', 'none', 'FaceAlpha', 0.50);
    end
    plot(h, scale * gd_like.mean(:, wedge_idx), '--', 'Color', like_line, 'LineWidth', 1.5);
    yline(0, 'k:');
    grid on;
end

function plot_measured_wedge_overlay(R, primary_line, outfile, fig_title)
    fig = figure('Visible', 'off', 'Position', [100 100 1080 640], 'Color', 'w');
    plot(R.t, R.output_index, '-', 'Color', primary_line, 'LineWidth', 1.5);
    hold on;
    plot(R.t, R.efficiency_index, '--', 'Color', [0.55 0.10 0.10], 'LineWidth', 1.4);
    plot(R.t, R.labor_index, ':', 'Color', [0.15 0.55 0.15], 'LineWidth', 1.6);
    plot(R.t, R.investment_index, '-.', 'Color', [0.45 0.25 0.65], 'LineWidth', 1.4);
    yline(100, 'k:');
    xlabel('t');
    ylabel('Index (t=1=100)');
    title(fig_title);
    legend({'Output', 'Efficiency wedge', 'Labor wedge', 'Investment wedge'}, ...
           'Location', 'best', 'Box', 'off');
    grid on;
    saveas(fig, outfile);
    close(fig);
end

function label = girf_shock_size_label(G)
    if isfield(G, 'exp2_shock_size')
        label = sprintf('%.1f s.d.', G.exp2_shock_size);
    else
        label = '1.0 s.d.';
    end
end
