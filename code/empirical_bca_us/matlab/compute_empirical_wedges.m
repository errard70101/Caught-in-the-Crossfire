% compute_empirical_wedges.m
clear; clc;

this_file = mfilename('fullpath');
matlab_dir = fileparts(this_file);
root_dir = fileparts(matlab_dir);
data_dir = fullfile(root_dir, 'data');
output_dir = fullfile(root_dir, 'output');

% Prototype parameters (matched to FVGQ/standard calibration)
pp.alpha = 0.36;
pp.beta  = 0.994;
pp.delta = 0.025; % Standard 10% annual depreciation
pp.gamma = 2.0;   % CRRA
pp.nu    = 1.0;   % Inverse Frisch

% --- ASSIGN INDICES ---
idx_Y = 1; % GDPC1
idx_C = 2; % PCECC96
idx_I = 3; % GPDIC1 (Real Gross Private Domestic Investment)
idx_L_emp = 8; % PAYEMS (Employment)
idx_L_hrs = 9; % CES0600000007 (Average Weekly Hours)

for shock_type = {'macro', 'fin'}
    ts = shock_type{1};
    data_file = fullfile(data_dir, sprintf('us_svar_irfs_%s.mat', ts));
    
    if ~isfile(data_file)
        error('Data file not found: %s', data_file);
    end
    load(data_file);

    % Extract median IRFs
    Y_irf = IRFhat(:, idx_Y);
    C_irf = IRFhat(:, idx_C);
    I_irf = IRFhat(:, idx_I);
    % Total hours IRF is the sum of Employment IRF and Average Hours IRF (since they are in logs)
    L_irf = IRFhat(:, idx_L_emp) + IRFhat(:, idx_L_hrs);

    H = length(Y_irf);

    % 1. Impute Capital IRF (if not in SVAR) via log-linearized capital accumulation:
    K_irf = zeros(H, 1);
    for t = 1:H
        if t == 1
            K_irf(t) = pp.delta * I_irf(t); % assuming K_{0} = 0 (steady state deviation)
        else
            K_irf(t) = (1 - pp.delta) * K_irf(t-1) + pp.delta * I_irf(t);
        end
    end
    K_lag_irf = [0; K_irf(1:end-1)];

    % 2. Efficiency Wedge (log A)
    wedge_A_irf = Y_irf - pp.alpha * K_lag_irf - (1 - pp.alpha) * L_irf;

    % 3. Labor Wedge (log(1 - tau_l))
    wedge_l_irf = (pp.nu + 1)*L_irf + pp.gamma*C_irf - Y_irf; 

    % 4. Investment Wedge (log(1 / (1+tau_x)))
    wedge_x_irf = zeros(H, 1);
    beta_discount = pp.beta * (1 - pp.delta);
    mpk_ss = 1/pp.beta - (1 - pp.delta); % Steady state MPK

    for t = H-1:-1:1
        expected_C_growth = C_irf(t+1) - C_irf(t);
        expected_MPK      = Y_irf(t+1) - K_irf(t);
        
        wedge_x_irf(t) = pp.gamma * expected_C_growth ...
                         + pp.beta * mpk_ss * expected_MPK ...
                         + beta_discount * wedge_x_irf(t+1);
    end
    % Invert sign for plotting so down means higher friction
    wedge_x_transformed_irf = -wedge_x_irf;

    % Save computed empirical wedges
    empirical_wedges = table((1:H)', wedge_A_irf, wedge_l_irf, wedge_x_transformed_irf, ...
        'VariableNames', {'Horizon', 'Efficiency_A', 'Labor_wedge_inv', 'Investment_wedge_inv'});

    writetable(empirical_wedges, fullfile(output_dir, sprintf('empirical_wedges_us_%s.csv', ts)));
end

fprintf('Empirical wedges computed and saved for both macro and fin shocks.\n');