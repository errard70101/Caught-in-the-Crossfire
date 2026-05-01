% plot_empirical_wedges.m
clear; clc;

this_file = mfilename('fullpath');
matlab_dir = fileparts(this_file);
root_dir = fileparts(matlab_dir);
output_dir = fullfile(root_dir, 'output');

for shock_type = {'macro', 'fin'}
    ts = shock_type{1};
    data_file = fullfile(output_dir, sprintf('empirical_wedges_us_%s.csv', ts));
    
    if ~isfile(data_file)
        error('Data file not found: %s. Please run compute_empirical_wedges.m first.', data_file);
    end

    T = readtable(data_file);

    h = T.Horizon;
    wedge_A = T.Efficiency_A;
    wedge_l = T.Labor_wedge_inv;
    wedge_x = T.Investment_wedge_inv;

    fig = figure('Position', [100, 100, 1000, 400]);

    % Efficiency Wedge
    subplot(1, 3, 1);
    plot(h, wedge_A, 'b-', 'LineWidth', 2);
    hold on;
    plot(h, zeros(size(h)), 'k--');
    title('Efficiency Wedge: log A_t');
    xlabel('Horizon');
    ylabel('Approx. percent deviation');
    grid on;

    % Labor Wedge
    subplot(1, 3, 2);
    plot(h, wedge_l, 'r-', 'LineWidth', 2);
    hold on;
    plot(h, zeros(size(h)), 'k--');
    title('Labor Wedge: log(1-\tau_{\ell,t})');
    xlabel('Horizon');
    grid on;

    % Investment Wedge
    subplot(1, 3, 3);
    plot(h, wedge_x, 'g-', 'LineWidth', 2);
    hold on;
    plot(h, zeros(size(h)), 'k--');
    title('Investment Wedge: log(1/(1+\tau_{x,t}))');
    xlabel('Horizon');
    grid on;

    if strcmp(ts, 'macro')
        title_str = 'U.S. Empirical Wedge Signature to Macro Uncertainty Shock';
    else
        title_str = 'U.S. Empirical Wedge Signature to Financial Uncertainty Shock';
    end
    sgtitle(title_str);

    % Save figure
    out_fig = fullfile(output_dir, sprintf('us_empirical_wedges_%s.png', ts));
    saveas(fig, out_fig);
end

fprintf('Saved empirical wedge plots to %s\n', output_dir);