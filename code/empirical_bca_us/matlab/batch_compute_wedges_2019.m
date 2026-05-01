% batch_compute_wedges_2019.m
clear; clc;
conf = get_project_config();
addpath(fullfile(conf.LOCAL_REPO_ROOT, 'code', 'empirical_bca_us', 'matlab', 'utils'));

% 1. Load the freshly generated 2019 MCMC results
res_file = fullfile(conf.DATA_DIR, 'est_result_2019.mat');
if ~isfile(res_file)
    error('2019 estimation result not found! Run run_2019_svar_estimation.m first.');
end
load(res_file);

% 2. Setup Parameters (QUARTERLY CALIBRATION)
pp.alpha = 0.36;
pp.beta  = 0.994; 
pp.delta = 0.025; 
pp.gamma = 2.0;   
pp.nu    = 1.0;   

% Indices in rearranged 22-variable SVMVAR_AddingHousingPrice Datar
idx_Y = 1; % GDPC1
idx_C = 2; % PCECC96
idx_I = 3; % GPDIC1 (Real Gross Private Domestic Investment)
idx_L_emp = 8; % PAYEMS
idx_L_hrs = 9; % CES0600000007

shocks_to_run = {[1;0;0], [0;0;1]};
shock_names = {'macro', 'fin'};

% Reuse the 22-variable IRF script that matches SVMVAR_AddingHousingPrice.
script_text = fileread(fullfile(conf.CROWN_SVAR_DIR, 'estimate_IRF_3SV_AddingHousingPrice.m'));

% Extend horizon to 40 (10 years of quarterly data)
script_text = strrep(script_text, 'stepIRF = 16;', 'stepIRF = 40;');

idx = regexp(script_text, '\nfigure\s*\nfor i = 1:ng', 'once');
if ~isempty(idx)
    script_text = script_text(1:idx(1)-1);
end

for s_idx = 1:2
    current_shock = shocks_to_run{s_idx};
    current_name = shock_names{s_idx};
    
    % Generate IRFs for this shock
    shock_str = sprintf('shock = [%d;%d;%d];', current_shock(1), current_shock(2), current_shock(3));
    modified_script = strrep(script_text, 'shock = [1;0;0];', shock_str);
    
    temp_script = fullfile(conf.TEMP_DIR, ['temp_svar_run_2019_' current_name '.m']);
    fid = fopen(temp_script, 'w');
    fwrite(fid, modified_script);
    fclose(fid);
    
    run(temp_script);

    % BCA Transformation logic via helper
    Y_draws = store_transformedIRF(:,:,idx_Y); 
    C_draws = store_transformedIRF(:,:,idx_C);
    I_draws = store_transformedIRF(:,:,idx_I);
    L_draws = store_transformedIRF(:,:,idx_L_emp) + store_transformedIRF(:,:,idx_L_hrs);

    wedge_data = compute_wedges_from_irfs(Y_draws, C_draws, I_draws, L_draws, pp);
    
    % Aggregation: Median and 68% Credible Interval (16th/84th quantiles)
    wedges = struct();
    q_levels = [0.16 0.50 0.84];
    
    wedges.A.q = quantile(wedge_data.A_draws, q_levels, 1)';
    wedges.l.q = quantile(wedge_data.l_draws, q_levels, 1)';
    wedges.x.q = quantile(wedge_data.x_draws, q_levels, 1)';
    wedges.h = (1:wedge_data.H)';
    
    save(fullfile(conf.OUTPUT_DIR, sprintf('empirical_wedges_ci_us_%s_2019.mat', current_name)), 'wedges');
end
exit;
