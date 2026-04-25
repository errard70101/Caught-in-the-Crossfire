% Plot wedge diagnostics for Experiment 1 and GIRF bands for Experiment 2.

clear;
clc;

this_file = mfilename('fullpath');
root_dir = fileparts(fileparts(this_file));
output_dir = fullfile(root_dir, 'output');

exp1_path = fullfile(output_dir, 'experiment1_sample.csv');
params_path = fullfile(output_dir, 'parameters.csv');
exp2_path = fullfile(output_dir, 'experiment2_paths.mat');

if ~isfile(exp1_path)
    error('Missing %s. Run run_simulation.m first.', exp1_path);
end
if ~isfile(params_path)
    error('Missing %s. Run run_simulation.m first.', params_path);
end
if ~isfile(exp2_path)
    error('Missing %s. Run run_simulation.m first.', exp2_path);
end

params = readtable(params_path);

% --- Plot A: Experiment 1 direct wedge series ---------------------------
exp1_data = readtable(exp1_path);
wedges = recover_direct_wedges_debug(exp1_data, params);

plot_names = {'v', 'log_A', 'G_share', 'tau_l', 'tau_x_expost'};
plot_names = plot_names(ismember(plot_names, wedges.Properties.VariableNames));

figure('Color', 'w', 'Position', [100, 100, 900, 700]);
tiledlayout(numel(plot_names), 1, 'TileSpacing', 'compact');
for ii = 1:numel(plot_names)
    nexttile;
    plot(wedges.t, wedges.(plot_names{ii}), 'LineWidth', 1.1);
    yline(0, ':', 'Color', [0.5, 0.5, 0.5]);
    title(strrep(plot_names{ii}, '_', '\_'));
    grid on;
end
xlabel('Simulation period');
out_a = fullfile(output_dir, 'exp1_debug_wedge_series.png');
saveas(gcf, out_a);
fprintf('Wrote %s\n', out_a);

% --- Plot B: Experiment 2 GIRF bands ------------------------------------
exp2 = load(exp2_path);
paths_base = exp2.paths_base;     % N x H x n_obs
paths_shock = exp2.paths_shock;
var_names = exp2.var_names;
N = exp2.N;
H = exp2.H;

wedge_names = {'log_A', 'G_share', 'tau_l', 'tau_x_expost'};
diff_mat = zeros(N, H, numel(wedge_names));

for i = 1:N
    base_tbl = path_to_table(squeeze(paths_base(i, :, :)), var_names);
    shock_tbl = path_to_table(squeeze(paths_shock(i, :, :)), var_names);
    w_base = recover_direct_wedges_debug(base_tbl, params);
    w_shock = recover_direct_wedges_debug(shock_tbl, params);
    for j = 1:numel(wedge_names)
        wname = wedge_names{j};
        diff_mat(i, :, j) = (w_shock.(wname) - w_base.(wname))';
    end
end

figure('Color', 'w', 'Position', [100, 100, 1000, 700]);
tiledlayout(2, 2, 'TileSpacing', 'compact');
h_axis = (1:H)';
for j = 1:numel(wedge_names)
    nexttile;
    d = squeeze(diff_mat(:, :, j));                 % N x H
    mu = mean(d, 1, 'omitnan');
    q05 = quantile(d, 0.05, 1);
    q95 = quantile(d, 0.95, 1);
    fill([h_axis; flipud(h_axis)], [q05'; flipud(q95')], ...
         [0.8, 0.85, 0.95], 'EdgeColor', 'none', 'FaceAlpha', 0.6);
    hold on;
    plot(h_axis, mu, 'LineWidth', 1.3, 'Color', [0.1, 0.2, 0.6]);
    yline(0, ':', 'Color', [0.5, 0.5, 0.5]);
    title(sprintf('GIRF: %s', strrep(wedge_names{j}, '_', '\_')));
    xlabel('Horizon h');
    grid on;
end
out_b = fullfile(output_dir, 'exp2_girf_bands.png');
saveas(gcf, out_b);
fprintf('Wrote %s\n', out_b);

function tbl = path_to_table(mat, var_names)
    % mat: H x n_obs
    tbl = array2table(mat, 'VariableNames', var_names);
    tbl.t = (1:height(tbl))';
    tbl = movevars(tbl, 't', 'Before', 1);
end
