% plot_empirical_wedges_ci.m
clear; clc;
conf = get_project_config();

for shock_type = {'macro', 'fin'}
    ts = shock_type{1};
    data_file = fullfile(conf.OUTPUT_DIR, sprintf('empirical_wedges_ci_us_%s.mat', ts));
    
    if ~isfile(data_file)
        error('Data file not found: %s. Run batch_compute_wedges_full.m first.', data_file);
    end
    load(data_file);

    fig = figure('Position', [100, 100, 1200, 500]);
    t = tiledlayout(1, 3, 'TileSpacing', 'compact', 'Padding', 'compact');
    
    h = wedges.h;
    % Scale to percent
    A_q = 100 * wedges.A.q;
    l_q = 100 * wedges.l.q;
    x_q = 100 * wedges.x.q;

    % --- Efficiency Wedge ---
    nexttile;
    fill([h; flipud(h)], [A_q(:,3); flipud(A_q(:,1))], [0.8 0.85 0.95], 'EdgeColor', 'none'); hold on;
    plot(h, A_q(:,2), 'b-', 'LineWidth', 2);
    plot(h, zeros(size(h)), 'k--');
    title('Efficiency Wedge: log A_t', 'Interpreter', 'tex');
    xlabel('Quarters'); ylabel('Percent deviation (%)'); grid on;
    xlim([1 length(h)]);

    % --- Labor Wedge ---
    nexttile;
    fill([h; flipud(h)], [l_q(:,3); flipud(l_q(:,1))], [0.95 0.8 0.8], 'EdgeColor', 'none'); hold on;
    plot(h, l_q(:,2), 'r-', 'LineWidth', 2);
    plot(h, zeros(size(h)), 'k--');
    title('Labor Wedge: log(1-\tau_{l,t})', 'Interpreter', 'tex');
    xlabel('Quarters'); ylabel('Percent deviation (%)'); grid on;
    xlim([1 length(h)]);

    % --- Investment Wedge ---
    nexttile;
    fill([h; flipud(h)], [x_q(:,3); flipud(x_q(:,1))], [0.8 0.95 0.8], 'EdgeColor', 'none'); hold on;
    plot(h, x_q(:,2), 'g-', 'LineWidth', 2);
    plot(h, zeros(size(h)), 'k--');
    title('Investment Wedge: log(1/(1+\tau_{x,t}))', 'Interpreter', 'tex');
    xlabel('Quarters'); ylabel('Percent deviation (%)'); grid on;
    xlim([1 length(h)]);

    % --- Global Title ---
    if strcmp(ts, 'macro')
        type_label = 'Macro Uncertainty';
    else
        type_label = 'Financial Uncertainty';
    end
    title_str = sprintf('U.S. Empirical Wedge IRFs to %s Shock\n(Full Sample including COVID, 68%% Credible Interval)', type_label);
    title(t, title_str, 'FontWeight', 'bold', 'FontSize', 14);

    out_fig = fullfile(conf.OUTPUT_DIR, sprintf('us_empirical_wedges_ci_%s.png', ts));
    saveas(fig, out_fig);
end
exit;
