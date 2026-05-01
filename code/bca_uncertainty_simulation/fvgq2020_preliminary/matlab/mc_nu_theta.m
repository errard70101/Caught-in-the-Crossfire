% Monte Carlo extraction of nu_theta from the FVGQ (2020) pruned
% third-order decision rule.
%
% This script is intentionally standalone: it does not modify the .mod file
% or the existing simulation scripts. It loads the consolidated Dynare
% workspace and calls Dynare's native simult_ with order=3 pruning.

clear;
clc;

this_file = mfilename('fullpath');
matlab_dir = fileparts(this_file);
root_dir = fileparts(matlab_dir);
output_dir = fullfile(root_dir, 'output');
workspace_path = fullfile(output_dir, 'simulated_workspace.mat');

addpath(matlab_dir);
setup_paths();

cfg = struct();
cfg.N = 1000;
cfg.T = 200;
cfg.grid_n = 11;
cfg.seed = 20260501;
cfg.use_stochastic_steady_state = true;
cfg.N = env_or_default('MC_NU_THETA_N', cfg.N);
cfg.T = env_or_default('MC_NU_THETA_T', cfg.T);
cfg.grid_n = env_or_default('MC_NU_THETA_GRID_N', cfg.grid_n);

load(workspace_path, 'M_', 'options_', 'oo_', 'sss_state', 'params');

endo_names = dynare_names_to_cell(M_.endo_names);
endo_names = cellfun(@strtrim, endo_names, 'UniformOutput', false);
exo_names = dynare_names_to_cell(M_.exo_names);
exo_names = cellfun(@strtrim, exo_names, 'UniformOutput', false);

idx = struct();
idx.cspt = find(strcmp(endo_names, 'cspt'));
idx.y = find(strcmp(endo_names, 'y'));
idx.k = find(strcmp(endo_names, 'k'));
idx.utilt = find(strcmp(endo_names, 'utilt'));
idx.delt = find(strcmp(endo_names, 'delt'));
idx.siget = find(strcmp(endo_names, 'siget'));

if any(structfun(@isempty, idx))
    error('mc_nu_theta:missing_variable', ...
          'Missing one of cspt/y/k/utilt/delt/siget.');
end

ss_sige = params.sige;
rho_sige = params.rhosige;
eta_e = params.metae;
innovation_std_sige = sqrt(1 - rho_sige^2) * eta_e;
uncond_std_sige = innovation_std_sige / sqrt(1 - rho_sige^2);
% In the .mod convention eta_e is metae; because the AR(1) shock loading is
% sqrt(1-rho^2)*metae, the unconditional std of siget is metae.

siget_grid = linspace(ss_sige - 2 * uncond_std_sige, ...
                      ss_sige + 2 * uncond_std_sige, cfg.grid_n)';
sigma2_grid = exp(2 * siget_grid);

if cfg.use_stochastic_steady_state
    y0_base = sss_state(:);
    start_label = "stochastic steady state";
else
    y0_base = oo_.dr.ys(:);
    start_label = "deterministic steady state";
end

rng(cfg.seed, 'twister');
shock_cube = randn(cfg.N, cfg.T, M_.exo_nbr);

rows = struct([]);
fprintf('Running MC: %d grid points x %d paths x T=%d from %s\n', ...
        cfg.grid_n, cfg.N, cfg.T, start_label);

for g = 1:cfg.grid_n
    y0 = y0_base;
    y0(idx.siget) = siget_grid(g);

    log_cspt_1 = nan(cfg.N, 1);
    log_lambda_1 = nan(cfg.N, 1);
    log_rk_1 = nan(cfg.N, 1);
    failed = false(cfg.N, 1);

    for n = 1:cfg.N
        ex_path = squeeze(shock_cube(n, :, :));
        try
            y_path = simult_(M_, options_, y0, oo_.dr, ex_path, 3);

            c1 = y_path(idx.cspt, 2);
            y1 = y_path(idx.y, 2);
            util1 = y_path(idx.utilt, 2);
            delt1 = y_path(idx.delt, 2);
            k0 = y0(idx.k);

            gross_rk_1 = params.alpha * y1 / (util1 * k0) + (1 - delt1);
            if c1 <= 0 || gross_rk_1 <= 0 || ~isfinite(c1) || ~isfinite(gross_rk_1)
                failed(n) = true;
                continue;
            end

            log_cspt_1(n) = log(c1);
            log_lambda_1(n) = -params.ckm_gamma * log_cspt_1(n);
            log_rk_1(n) = log(gross_rk_1);
        catch ME
            failed(n) = true;
            if sum(failed) <= 3
                warning('mc_nu_theta:sim_failed', ...
                        'Grid %d path %d failed: %s', g, n, ME.message);
            end
        end
    end

    valid = ~(failed | isnan(log_cspt_1) | isnan(log_lambda_1) | isnan(log_rk_1));
    cov_mat = cov(log_cspt_1(valid), log_rk_1(valid));

    rows(g).grid_id = g; %#ok<SAGROW>
    rows(g).siget = siget_grid(g);
    rows(g).sigma_e_sq = sigma2_grid(g);
    rows(g).mean_log_lambda = mean(log_lambda_1(valid));
    rows(g).mean_log_cspt = mean(log_cspt_1(valid));
    rows(g).var_log_cspt = var(log_cspt_1(valid), 0);
    rows(g).cov_log_cspt_log_rk = cov_mat(1, 2);
    rows(g).n_valid = sum(valid);
    rows(g).n_failed = sum(~valid);

    fprintf('  grid %2d/%2d: siget=% .6f sigma2=%.6e valid=%d mean log lambda=% .8f\n', ...
            g, cfg.grid_n, siget_grid(g), sigma2_grid(g), rows(g).n_valid, ...
            rows(g).mean_log_lambda);
end

result_table = struct2table(rows);

reg_lambda = ols_with_intercept(result_table.sigma_e_sq, result_table.mean_log_lambda);
reg_var = ols_with_intercept(result_table.sigma_e_sq, result_table.var_log_cspt);
reg_cov = ols_with_intercept(result_table.sigma_e_sq, result_table.cov_log_cspt_log_rk);

beta = params.beta;
Rbar = 1 / beta;
theta_bar = params.ssPhi;
delta = params.delt0;
delta_sigma2_unit_ue = 9.44e-5;
kappa_without_collateral = 2.04e-3;
lp_measured = 1.886e-3;

collateral_phi = beta * Rbar * theta_bar * (1 - delta) * reg_lambda.slope;
collateral_kappa_impact = beta * Rbar * theta_bar * (1 - delta) * ...
                          reg_lambda.slope * delta_sigma2_unit_ue;
kappa_corrected = kappa_without_collateral + collateral_kappa_impact;

summary = table( ...
    reg_lambda.slope, reg_lambda.se, reg_lambda.ci95_low, reg_lambda.ci95_high, ...
    reg_var.slope, reg_var.se, reg_var.ci95_low, reg_var.ci95_high, ...
    reg_cov.slope, reg_cov.se, reg_cov.ci95_low, reg_cov.ci95_high, ...
    collateral_phi, collateral_kappa_impact, kappa_corrected, lp_measured, ...
    'VariableNames', { ...
        'nu_theta', 'nu_theta_se', 'nu_theta_ci95_low', 'nu_theta_ci95_high', ...
        'a_cc_e_mc', 'a_cc_e_mc_se', 'a_cc_e_mc_ci95_low', 'a_cc_e_mc_ci95_high', ...
        'a_cR_e_mc', 'a_cR_e_mc_se', 'a_cR_e_mc_ci95_low', 'a_cR_e_mc_ci95_high', ...
        'collateral_phi_per_sigma2', 'collateral_kappa_unit_ue', ...
        'kappa_corrected_unit_ue', 'lp_measured_unit_ue'});

out_csv = fullfile(output_dir, 'mc_nu_theta_grid.csv');
out_summary = fullfile(output_dir, 'mc_nu_theta_summary.csv');
out_mat = fullfile(output_dir, 'mc_nu_theta_results.mat');

writetable(result_table, out_csv);
writetable(summary, out_summary);
save(out_mat, 'cfg', 'result_table', 'summary', 'reg_lambda', 'reg_var', 'reg_cov');

fprintf('\nRegression summary:\n');
fprintf('  nu_theta        = %.8e (SE %.3e, 95%% CI [%.8e, %.8e])\n', ...
        reg_lambda.slope, reg_lambda.se, reg_lambda.ci95_low, reg_lambda.ci95_high);
fprintf('  a_cc,e^MC       = %.8e (SE %.3e, 95%% CI [%.8e, %.8e])\n', ...
        reg_var.slope, reg_var.se, reg_var.ci95_low, reg_var.ci95_high);
fprintf('  a_cR,e^MC       = %.8e (SE %.3e, 95%% CI [%.8e, %.8e])\n', ...
        reg_cov.slope, reg_cov.se, reg_cov.ci95_low, reg_cov.ci95_high);
fprintf('  collateral term = %.8e per unit ue\n', collateral_kappa_impact);
fprintf('  corrected kappa = %.8e vs LP %.8e\n', kappa_corrected, lp_measured);
fprintf('\nWrote:\n  %s\n  %s\n  %s\n', out_csv, out_summary, out_mat);

function names = dynare_names_to_cell(raw_names)
    if iscell(raw_names)
        names = raw_names(:);
    elseif isstring(raw_names)
        names = cellstr(raw_names(:));
    else
        names = cellstr(raw_names);
    end
end

function value = env_or_default(name, default_value)
    raw = getenv(name);
    if isempty(raw)
        value = default_value;
    else
        value = str2double(raw);
        if ~isfinite(value) || value <= 0
            error('mc_nu_theta:bad_env', 'Invalid %s=%s', name, raw);
        end
        value = round(value);
    end
end

function reg = ols_with_intercept(x, y)
    x = x(:);
    y = y(:);
    ok = isfinite(x) & isfinite(y);
    x = x(ok);
    y = y(ok);
    X = [ones(size(x)), x];
    b = X \ y;
    resid = y - X * b;
    dof = size(X, 1) - size(X, 2);
    s2 = sum(resid .^ 2) / dof;
    vcov = s2 * inv(X' * X);
    se = sqrt(diag(vcov));
    tcrit = tinv_fallback(0.975, dof);

    reg = struct();
    reg.intercept = b(1);
    reg.slope = b(2);
    reg.se = se(2);
    reg.ci95_low = b(2) - tcrit * se(2);
    reg.ci95_high = b(2) + tcrit * se(2);
    reg.dof = dof;
    reg.resid_se = sqrt(s2);
end

function val = tinv_fallback(p, dof)
    if exist('tinv', 'file') == 2
        val = tinv(p, dof);
    else
        % Normal approximation fallback. For dof=9, 2.262 would be exact;
        % this branch is only for minimal MATLAB installations.
        val = 1.96;
        if dof == 9
            val = 2.26215716285410;
        end
    end
end
