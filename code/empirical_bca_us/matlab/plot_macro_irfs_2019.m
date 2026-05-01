% plot_macro_irfs_2019.m
% Plot IRFs of key macro variables (Y, C, I, L) to uncertainty shocks.
% Uses pre-COVID 1959-2019 sample. Requires est_result_2019.mat.
clear; clc;
conf = get_project_config();
addpath(fullfile(conf.LOCAL_REPO_ROOT, 'code', 'empirical_bca_us', 'matlab', 'utils'));

res_file = fullfile(conf.DATA_DIR, 'est_result_2019.mat');
if ~isfile(res_file)
    error('est_result_2019.mat not found. Run run_2019_svar_estimation.m first.');
end
load(res_file);

% Indices in rearranged 22-variable SVMVAR_AddingHousingPrice Datar
idx_Y     = 1;  % GDPC1
idx_C     = 2;  % PCECC96
idx_I     = 3;  % GPDIC1
idx_L_emp = 8;  % PAYEMS
idx_L_hrs = 9;  % CES0600000007

% Reuse the 22-variable IRF script that matches SVMVAR_AddingHousingPrice.
script_text = fileread(fullfile(conf.CROWN_SVAR_DIR, 'estimate_IRF_3SV_AddingHousingPrice.m'));
script_text = strrep(script_text, 'stepIRF = 16;', 'stepIRF = 40;');
idx_fig = regexp(script_text, '\nfigure\s*\nfor i = 1:ng', 'once');
if ~isempty(idx_fig)
    script_text = script_text(1:idx_fig(1)-1);
end

shocks      = {[1;0;0], [0;0;1]};
shock_names = {'macro', 'fin'};
shock_labels = {'Macro Uncertainty Shock', 'Financial Uncertainty Shock'};
q_levels    = [0.16 0.50 0.84];

var_labels = {'Output (GDPC1)', 'Consumption (PCECC96)', 'Investment (GPDIC1)', 'Total Hours Worked'};
ci_colors  = {[0.8 0.85 0.95], [0.95 0.8 0.8], [0.8 0.95 0.8], [0.97 0.90 0.75]};
line_colors = {[0 0.447 0.741], [0.85 0.325 0.098], [0.466 0.674 0.188], [0.929 0.694 0.125]};

fig = figure('Position', [100, 100, 1400, 650]);
tl = tiledlayout(2, 4, 'TileSpacing', 'compact', 'Padding', 'compact');

for s = 1:2
    shock_str = sprintf('shock = [%d;%d;%d];', shocks{s}(1), shocks{s}(2), shocks{s}(3));
    modified  = strrep(script_text, 'shock = [1;0;0];', shock_str);

    tmp_file = fullfile(conf.TEMP_DIR, sprintf('temp_macro_irf_%s.m', shock_names{s}));
    fid = fopen(tmp_file, 'w'); fwrite(fid, modified); fclose(fid);
    run(tmp_file);

    % Extract draws and compute quantiles (×100 for percent)
    Y_q = 100 * quantile(store_transformedIRF(:,:,idx_Y), q_levels, 1)';
    C_q = 100 * quantile(store_transformedIRF(:,:,idx_C), q_levels, 1)';
    I_q = 100 * quantile(store_transformedIRF(:,:,idx_I), q_levels, 1)';
    L_q = 100 * quantile(store_transformedIRF(:,:,idx_L_emp) + store_transformedIRF(:,:,idx_L_hrs), q_levels, 1)';

    all_q = {Y_q, C_q, I_q, L_q};
    h_vec = (1:size(Y_q,1))';

    for v = 1:4
        nexttile((s-1)*4 + v);
        q = all_q{v};
        fill([h_vec; flipud(h_vec)], [q(:,3); flipud(q(:,1))], ci_colors{v}, 'EdgeColor', 'none'); hold on;
        plot(h_vec, q(:,2), '-', 'Color', line_colors{v}, 'LineWidth', 2);
        plot(h_vec, zeros(size(h_vec)), 'k--', 'LineWidth', 0.8);
        if s == 1
            title(var_labels{v}, 'FontWeight', 'bold', 'FontSize', 11);
        end
        ylabel('Percent deviation (%)');
        xlabel('Quarters');
        grid on;
        xlim([1 length(h_vec)]);

        % Row label on leftmost tile
        if v == 1
            text(0.02, 0.95, shock_labels{s}, 'Units', 'normalized', ...
                'FontSize', 9, 'FontWeight', 'bold', 'Color', [0.3 0.3 0.3], ...
                'VerticalAlignment', 'top');
        end
    end
end

title(tl, 'U.S. IRFs to Uncertainty Shocks: Key Macro Variables (Pre-COVID 1959-2019, 68% Credible Interval)', ...
    'FontWeight', 'bold', 'FontSize', 13);

out_file = fullfile(conf.OUTPUT_DIR, 'us_macro_irfs_2019.png');
saveas(fig, out_file);
fprintf('Saved: %s\n', out_file);
exit;
