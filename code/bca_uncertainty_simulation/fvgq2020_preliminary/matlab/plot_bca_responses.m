% Plot LP and GIRF wedge responses from the preliminary FVGQ pipeline.

clear;
clc;

this_file = mfilename('fullpath');
matlab_dir = fileparts(this_file);
root_dir = fileparts(matlab_dir);
output_dir = fullfile(root_dir, 'output');

LP = load(fullfile(output_dir, 'lp_results.mat'));
G = load(fullfile(output_dir, 'wedges_girf.mat'));
lp_mc_path = fullfile(output_dir, 'lp_results_mc_fixed.mat');
lp_like_path = fullfile(output_dir, 'lp_results_likelihood.mat');
girf_like_path = fullfile(output_dir, 'wedges_girf_likelihood.mat');
report_fixed_path = fullfile(output_dir, 'wedges_exp1_report.csv');
report_like_path = fullfile(output_dir, 'wedges_exp1_likelihood_report.csv');
lp_no_sv_path = fullfile(output_dir, 'lp_results_no_svctrl.mat');
lp_like_no_sv_path = fullfile(output_dir, 'lp_results_likelihood_no_svctrl.mat');

has_lp_mc = isfile(lp_mc_path);
if has_lp_mc
    LP_mc = load(lp_mc_path);
end
has_likelihood = isfile(lp_like_path);
if has_likelihood
    LP_like = load(lp_like_path);
end
has_girf_likelihood = isfile(girf_like_path);
if has_girf_likelihood
    G_like = load(girf_like_path);
end
has_lp_no_sv = isfile(lp_no_sv_path);
if has_lp_no_sv
    LP_no_sv = load(lp_no_sv_path);
end
has_lp_like_no_sv = isfile(lp_like_no_sv_path);
if has_lp_like_no_sv
    LP_like_no_sv = load(lp_like_no_sv_path);
end

R_fixed = readtable(report_fixed_path);
has_report_likelihood = isfile(report_like_path);
if has_report_likelihood
    R_like = readtable(report_like_path);
end

girf_shock_label = girf_shock_size_label(G);
lp_meta = lp_panel_meta(get_lp_names(LP));
girf_meta = transformed_girf_panel_meta(get_transformed_girf_names(G));
raw_girf_names = get_raw_girf_names(G);
resource_idx = find(strcmp(raw_girf_names, 'G_share'));
if isempty(resource_idx)
    error('plot_bca_responses:missing_resource_residual', ...
          'Could not locate G_share in wedges_girf.mat.');
end
resource_meta = raw_resource_panel_meta();
fixed_fill = [0.82 0.87 0.95];
fixed_line = [0.00 0.25 0.75];
like_fill = [0.98 0.88 0.78];
like_line = [0.85 0.33 0.10];

for shock_tag = {'macro', 'fin'}
    ts = shock_tag{1};
    shock_col = shock_name_to_col(ts);
    shock_meta = shock_panel_meta(ts);

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
        sgtitle(sprintf('LP (likelihood-smoothed transformed wedges): response to %s uncertainty shock', ts));
        saveas(fig, fullfile(output_dir, sprintf('bca_lp_%s.png', ts)));
        saveas(fig, fullfile(output_dir, sprintf('bca_lp_%s_likelihood.png', ts)));
        close(fig);
    else
        fig = figure('Visible', 'off', 'Position', [100 100 980 760], 'Color', 'w');
        for j = 1:numel(lp_meta)
            subplot(2, 2, j);
            if has_lp_mc
                lp_mc = LP_mc.lp_results_mc_fixed.summary.(lp_meta(j).name);
                plot_lp_mc_single(lp_mc, shock_col, lp_meta(j).scale, fixed_fill, fixed_line);
            else
                lp = LP.lp_results.(lp_meta(j).name);
                plot_lp_single(lp, shock_col, lp_meta(j).scale, fixed_fill, fixed_line);
            end
            title(lp_meta(j).title);
            xlabel('Horizon');
            ylabel(lp_meta(j).ylabel);
        end
        subplot(2, 2, 4);
        if has_lp_mc && isfield(LP_mc.lp_results_mc_fixed, 'shock_panel_summary') && ...
                isfield(LP_mc.lp_results_mc_fixed.shock_panel_summary, ts)
            plot_lp_shock_mc_single(LP_mc.lp_results_mc_fixed.shock_panel_summary.(ts), ...
                                    fixed_fill, fixed_line);
            title(shock_meta.title);
            xlabel('Horizon');
            ylabel(shock_meta.ylabel);
        elseif isfield(LP, 'lp_shock_panels') && isfield(LP.lp_shock_panels, ts)
            lp_diag = LP.lp_shock_panels.(ts);
            plot_lp_single(lp_diag, shock_col, 1, fixed_fill, fixed_line);
            title(shock_meta.title);
            xlabel('Horizon');
            ylabel(shock_meta.ylabel);
        else
            axis off;
        end
        if has_lp_mc
            sgtitle(sprintf(['LP (fixed-point transformed wedges): Monte Carlo median and 95%% band ', ...
                             'to %s uncertainty shock'], ts));
        else
            sgtitle(sprintf('LP (fixed-point transformed wedges): response to %s uncertainty shock', ts));
        end
        saveas(fig, fullfile(output_dir, sprintf('bca_lp_%s.png', ts)));
        close(fig);
    end

    fig = figure('Visible', 'off', 'Position', [100 100 980 760], 'Color', 'w');
    for j = 1:numel(lp_meta)
        subplot(2, 2, j);
        if has_lp_mc
            lp_mc = LP_mc.lp_results_mc_fixed.summary.(lp_meta(j).name);
            plot_lp_mc_single(lp_mc, shock_col, lp_meta(j).scale, fixed_fill, fixed_line);
        else
            lp = LP.lp_results.(lp_meta(j).name);
            plot_lp_single(lp, shock_col, lp_meta(j).scale, fixed_fill, fixed_line);
        end
        title(lp_meta(j).title);
        xlabel('Horizon');
        ylabel(lp_meta(j).ylabel);
    end
    subplot(2, 2, 4);
    if has_lp_mc && isfield(LP_mc.lp_results_mc_fixed, 'shock_panel_summary') && ...
            isfield(LP_mc.lp_results_mc_fixed.shock_panel_summary, ts)
        plot_lp_shock_mc_single(LP_mc.lp_results_mc_fixed.shock_panel_summary.(ts), ...
                                fixed_fill, fixed_line);
        title(shock_meta.title);
        xlabel('Horizon');
        ylabel(shock_meta.ylabel);
    elseif isfield(LP, 'lp_shock_panels') && isfield(LP.lp_shock_panels, ts)
        lp_diag = LP.lp_shock_panels.(ts);
        plot_lp_single(lp_diag, shock_col, 1, fixed_fill, fixed_line);
        title(shock_meta.title);
        xlabel('Horizon');
        ylabel(shock_meta.ylabel);
    else
        axis off;
    end
    if has_lp_mc
        sgtitle(sprintf(['LP (fixed-point transformed wedges): Monte Carlo median and 95%% band ', ...
                         'to %s uncertainty shock'], ts));
    else
        sgtitle(sprintf('LP (fixed-point transformed wedges): response to %s uncertainty shock', ts));
    end
    saveas(fig, fullfile(output_dir, sprintf('bca_lp_%s_fixed.png', ts)));
    close(fig);

    if has_likelihood
        fig = figure('Visible', 'off', 'Position', [100 100 980 760], 'Color', 'w');
        for j = 1:numel(lp_meta)
            subplot(2, 2, j);
            if has_lp_mc
                fixed_lp = LP_mc.lp_results_mc_fixed.summary.(lp_meta(j).name);
            else
                fixed_lp = LP.lp_results.(lp_meta(j).name);
            end
            like_lp = LP_like.lp_results_likelihood.(lp_meta(j).name);
            if has_lp_mc
                plot_lp_compare_mixed(fixed_lp, like_lp, shock_col, lp_meta(j).scale, ...
                                      fixed_fill, fixed_line, like_fill, like_line);
            else
                plot_lp_compare(fixed_lp, like_lp, shock_col, lp_meta(j).scale, ...
                                fixed_fill, fixed_line, like_fill, like_line);
            end
            title(lp_meta(j).title);
            xlabel('Horizon');
            ylabel(lp_meta(j).ylabel);
            if j == 1
                if has_lp_mc
                    legend({'Fixed MC 95%', 'Fixed median', 'Likelihood HAC 95%', 'Likelihood'}, ...
                           'Location', 'best', 'Box', 'off');
                else
                    legend({'Fixed 95% CI', 'Fixed', 'Likelihood 95% CI', 'Likelihood'}, ...
                           'Location', 'best', 'Box', 'off');
                end
            end
        end
        subplot(2, 2, 4);
        if has_lp_mc && isfield(LP_mc.lp_results_mc_fixed, 'shock_panel_summary') && ...
                isfield(LP_mc.lp_results_mc_fixed.shock_panel_summary, ts) && ...
                isfield(LP_like, 'lp_shock_panels_likelihood') && ...
                isfield(LP_like.lp_shock_panels_likelihood, ts)
            plot_lp_shock_compare_mixed(LP_mc.lp_results_mc_fixed.shock_panel_summary.(ts), ...
                                        LP_like.lp_shock_panels_likelihood.(ts), shock_col, ...
                                        fixed_fill, fixed_line, like_fill, like_line);
            title(shock_meta.title);
            xlabel('Horizon');
            ylabel(shock_meta.ylabel);
        elseif isfield(LP, 'lp_shock_panels') && isfield(LP.lp_shock_panels, ts) && ...
                isfield(LP_like, 'lp_shock_panels_likelihood') && ...
                isfield(LP_like.lp_shock_panels_likelihood, ts)
            plot_lp_compare(LP.lp_shock_panels.(ts), LP_like.lp_shock_panels_likelihood.(ts), ...
                            shock_col, 1, fixed_fill, fixed_line, like_fill, like_line);
            title(shock_meta.title);
            xlabel('Horizon');
            ylabel(shock_meta.ylabel);
        else
            axis off;
        end
        if has_lp_mc
            sgtitle(sprintf('LP comparison: fixed-point Monte Carlo vs likelihood HAC (%s shock)', ts));
        else
            sgtitle(sprintf('LP comparison: fixed-point vs likelihood transformed wedges (%s shock)', ts));
        end
        saveas(fig, fullfile(output_dir, sprintf('bca_lp_compare_%s.png', ts)));
        close(fig);
    end
end

for shock_tag = {'macro', 'fin'}
    ts = shock_tag{1};
    gd = G.girf_transformed.(ts);
    gd_raw = G.girf.(ts);
    h = (0:size(gd.mean, 1) - 1)';

    fig = figure('Visible', 'off', 'Position', [100 100 980 760], 'Color', 'w');
    for j = 1:numel(girf_meta)
        subplot(2, 2, j);
        plot_girf_single(gd, j, h, girf_meta(j).scale, [0.95 0.86 0.8], [0.75 0.10 0.10]);
        title(girf_meta(j).title);
        xlabel('Horizon');
        ylabel(girf_meta(j).ylabel);
        if j == 1
            legend({'95% CI for mean', 'Mean GIRF'}, ...
                   'Location', 'best', 'Box', 'off', 'FontSize', 8);
        end
    end
    subplot(2, 2, 4);
    plot_girf_single(gd_raw, resource_idx, h, resource_meta.scale, [0.90 0.90 0.90], [0.35 0.35 0.35]);
    title(resource_meta.title);
    xlabel('Horizon');
    ylabel(resource_meta.ylabel);
    sgtitle(sprintf(['GIRF (transformed wedges) - %s shock (%s); ' ...
                     'band = 95%% CI for mean (state-dep. dispersion omitted)'], ...
                    ts, girf_shock_label));
    saveas(fig, fullfile(output_dir, sprintf('bca_girf_%s.png', ts)));
    close(fig);

    if has_girf_likelihood
        gd_like = G_like.girf_transformed_likelihood.(ts);
        gd_like_raw = G_like.girf_likelihood.(ts);

        fig = figure('Visible', 'off', 'Position', [100 100 980 760], 'Color', 'w');
        for j = 1:numel(girf_meta)
            subplot(2, 2, j);
            plot_girf_single(gd_like, j, h, girf_meta(j).scale, like_fill, like_line);
            title(girf_meta(j).title);
            xlabel('Horizon');
            ylabel(girf_meta(j).ylabel);
            if j == 1
                legend({'95% CI for mean', 'Mean GIRF'}, ...
                       'Location', 'best', 'Box', 'off', 'FontSize', 8);
            end
        end
        subplot(2, 2, 4);
        plot_girf_single(gd_like_raw, resource_idx, h, resource_meta.scale, like_fill, like_line);
        title(resource_meta.title);
        xlabel('Horizon');
        ylabel(resource_meta.ylabel);
        sgtitle(sprintf(['GIRF likelihood (transformed wedges) - %s shock (%s); ' ...
                         'band = 95%% CI for mean (state-dep. dispersion omitted)'], ...
                        ts, girf_shock_label));
        saveas(fig, fullfile(output_dir, sprintf('bca_girf_%s_likelihood.png', ts)));
        close(fig);

        fig = figure('Visible', 'off', 'Position', [100 100 980 760], 'Color', 'w');
        for j = 1:numel(girf_meta)
            subplot(2, 2, j);
            plot_girf_compare(gd, gd_like, j, h, girf_meta(j).scale, ...
                              fixed_fill, fixed_line, like_fill, like_line);
            title(girf_meta(j).title);
            xlabel('Horizon');
            ylabel(girf_meta(j).ylabel);
            if j == 1
                legend({'Fixed 95% CI for mean', 'Fixed', 'Likelihood 95% CI for mean', 'Likelihood'}, ...
                       'Location', 'best', 'Box', 'off');
            end
        end
        subplot(2, 2, 4);
        plot_girf_compare(gd_raw, gd_like_raw, resource_idx, h, resource_meta.scale, ...
                          [0.90 0.90 0.90], [0.35 0.35 0.35], like_fill, like_line);
        title(resource_meta.title);
        xlabel('Horizon');
        ylabel(resource_meta.ylabel);
        sgtitle(sprintf('GIRF comparison: fixed-point vs likelihood transformed wedges (%s shock, %s)', ...
                        ts, girf_shock_label));
        saveas(fig, fullfile(output_dir, sprintf('bca_girf_compare_%s.png', ts)));
        close(fig);
    end
end

% --- Headline DGP-precision LP figures: fixed-point T=20000 HAC ---
% These reflect population-level precision (no Monte Carlo short-sample noise),
% complementing the empirical-relevance T=400 MC bands in bca_lp_*_fixed.png.
for shock_tag = {'macro', 'fin'}
    ts = shock_tag{1};
    shock_col = shock_name_to_col(ts);
    shock_meta = shock_panel_meta(ts);
    fig = figure('Visible', 'off', 'Position', [100 100 980 760], 'Color', 'w');
    for j = 1:numel(lp_meta)
        subplot(2, 2, j);
        lp = LP.lp_results.(lp_meta(j).name);
        plot_lp_single(lp, shock_col, lp_meta(j).scale, fixed_fill, fixed_line);
        title(lp_meta(j).title);
        xlabel('Horizon');
        ylabel(lp_meta(j).ylabel);
    end
    subplot(2, 2, 4);
    if isfield(LP, 'lp_shock_panels') && isfield(LP.lp_shock_panels, ts)
        plot_lp_single(LP.lp_shock_panels.(ts), shock_col, 1, fixed_fill, fixed_line);
        title(shock_meta.title);
        xlabel('Horizon');
        ylabel(shock_meta.ylabel);
    else
        axis off;
    end
    sgtitle(sprintf(['LP DGP-precision (fixed-point, T=20000 HAC): ' ...
                     'response to %s uncertainty shock'], ts));
    saveas(fig, fullfile(output_dir, sprintf('bca_lp_%s_dgp.png', ts)));
    close(fig);
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
                            fixed_fill, fixed_line, like_fill, like_line);
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
                            shock_col, 1, fixed_fill, fixed_line, like_fill, like_line);
            title(shock_meta.title);
            xlabel('Horizon');
            ylabel(shock_meta.ylabel);
        else
            axis off;
        end
        sgtitle(sprintf(['LP sensitivity (fixed-point, T=20000 HAC): ' ...
                         'baseline vs. SV-state controls dropped, %s shock'], ts));
        saveas(fig, fullfile(output_dir, sprintf('bca_lp_%s_no_svctrl.png', ts)));
        close(fig);
    end
end

plot_measured_wedge_overlay(R_fixed, fixed_line, ...
    fullfile(output_dir, 'bca_measured_wedges_fixed.png'), ...
    'CKM-style measured wedges (fixed-point, t=1=100)');

if has_report_likelihood
    plot_measured_wedge_overlay(R_like, like_line, ...
        fullfile(output_dir, 'bca_measured_wedges_likelihood.png'), ...
        'CKM-style measured wedges (likelihood-smoothed, t=1=100)');

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
            plot(R_fixed.t, R_fixed.(name), '-', 'Color', fixed_line, 'LineWidth', 1.2);
        else
            plot(R_fixed.t, R_fixed.(name), '-', 'Color', fixed_line, 'LineWidth', 1.2);
            hold on;
            plot(R_like.t, R_like.(name), '--', 'Color', like_line, 'LineWidth', 1.2);
        end
        yline(100, 'k:');
        title(title_text);
        xlabel('t');
        ylabel('Index (t=1=100)');
        grid on;
        if j == 2
            legend({'Fixed-point', 'Likelihood-smoothed'}, 'Location', 'best', 'Box', 'off');
        end
    end
    sgtitle('CKM-style measured wedges and output: fixed-point vs likelihood');
    saveas(fig, fullfile(output_dir, 'bca_wedges_exp1_compare.png'));
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
        'scale', {100, 100, 100});
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
        'scale', {100, 100, 100});
end

function meta = raw_resource_panel_meta()
    meta = struct('title', 'Resource residual: G/Y (raw diagnostic)', ...
                  'ylabel', 'Percentage points', ...
                  'scale', 100);
end

function meta = shock_panel_meta(ts)
    if strcmp(ts, 'macro')
        meta.title = 'Volatility state: sigAt';
    else
        meta.title = 'Volatility state: siget';
    end
    meta.ylabel = 'Log-volatility state';
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

function plot_lp_compare(lp_fixed, lp_like, shock_col, scale, fixed_fill, fixed_line, like_fill, like_line)
    h = lp_fixed.horizons;
    fill([h; flipud(h)], ...
         scale * [lp_fixed.ci_lo(:, shock_col); flipud(lp_fixed.ci_hi(:, shock_col))], ...
         fixed_fill, 'EdgeColor', 'none', 'FaceAlpha', 0.50);
    hold on;
    plot(h, scale * lp_fixed.beta(:, shock_col), '-', 'Color', fixed_line, 'LineWidth', 1.5);
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

function plot_lp_compare_mixed(lp_mc, lp_like, shock_col, scale, fixed_fill, fixed_line, like_fill, like_line)
    h = lp_mc.horizons;
    fill([h; flipud(h)], scale * [lp_mc.q025(:, shock_col); flipud(lp_mc.q975(:, shock_col))], ...
         fixed_fill, 'EdgeColor', 'none', 'FaceAlpha', 0.50);
    hold on;
    plot(h, scale * lp_mc.median(:, shock_col), '-', 'Color', fixed_line, 'LineWidth', 1.5);
    fill([h; flipud(h)], ...
         scale * [lp_like.ci_lo(:, shock_col); flipud(lp_like.ci_hi(:, shock_col))], ...
         like_fill, 'EdgeColor', 'none', 'FaceAlpha', 0.45);
    plot(h, scale * lp_like.beta(:, shock_col), '--', 'Color', like_line, 'LineWidth', 1.5);
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

function plot_lp_shock_compare_mixed(lp_mc, lp_like, shock_col, fixed_fill, fixed_line, like_fill, like_line)
    h = lp_mc.horizons;
    fill([h; flipud(h)], [lp_mc.q025; flipud(lp_mc.q975)], ...
         fixed_fill, 'EdgeColor', 'none', 'FaceAlpha', 0.50);
    hold on;
    plot(h, lp_mc.median, '-', 'Color', fixed_line, 'LineWidth', 1.5);
    fill([h; flipud(h)], [lp_like.ci_lo(:, shock_col); flipud(lp_like.ci_hi(:, shock_col))], ...
         like_fill, 'EdgeColor', 'none', 'FaceAlpha', 0.45);
    plot(h, lp_like.beta(:, shock_col), '--', 'Color', like_line, 'LineWidth', 1.5);
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

function plot_girf_compare(gd_fixed, gd_like, wedge_idx, h, scale, fixed_fill, fixed_line, like_fill, like_line)
    % Use 95% CI for the mean (precision band) in both series; the 5-95%
    % pair-dispersion band is omitted as in plot_girf_single.
    if isfield(gd_fixed, 'ci_lo_mean') && isfield(gd_fixed, 'ci_hi_mean')
        fill([h; flipud(h)], ...
             scale * [gd_fixed.ci_lo_mean(:, wedge_idx); flipud(gd_fixed.ci_hi_mean(:, wedge_idx))], ...
             fixed_fill, 'EdgeColor', 'none', 'FaceAlpha', 0.55);
        hold on;
    else
        hold on;
    end
    plot(h, scale * gd_fixed.mean(:, wedge_idx), '-', 'Color', fixed_line, 'LineWidth', 1.5);
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
