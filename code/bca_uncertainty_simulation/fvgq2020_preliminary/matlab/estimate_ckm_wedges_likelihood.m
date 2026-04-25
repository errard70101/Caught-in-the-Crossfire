function result = estimate_ckm_wedges_likelihood(sim_table, prototype_params, options)
%ESTIMATE_CKM_WEDGES_LIKELIHOOD Recover wedges with a CKM-style Kalman smoother.
%
% This is a first-pass full-likelihood implementation for the preliminary
% FVGQ exercise. It follows the Dynare CKM example's linear-smoother logic:
% the three wedges {z, tau_l, tau_x} are latent states in a linearized
% prototype model, while G_share is appended from the exact resource identity.

    if nargin < 3
        options = struct();
    end

    defaults = struct( ...
        'force_recompile', false, ...
        'verbose', true);
    options = merge_structs(defaults, options);

    if ~istable(sim_table)
        error('estimate_ckm_wedges_likelihood:bad_input', ...
              'sim_table must be a table with the FVGQ Experiment 1 sample.');
    end

    root_dir = fileparts(fileparts(mfilename('fullpath')));
    dynare_dir = fullfile(root_dir, 'dynare');
    output_dir = fullfile(root_dir, 'output');
    datafile = fullfile(output_dir, 'ckm_three_wedge_exp1_data.mat');
    params_file = fullfile(dynare_dir, 'ckm_three_wedge_likelihood_params.mat');

    Y = sim_table.y;
    C = sim_table.cspt;
    I = 0.06 * sim_table.ivst;
    L = sim_table.labor;
    K = sim_table.k;

    proxy_wedges = estimate_ckm_wedges(Y, C, I, L, K, prototype_params);
    state_proxy = [proxy_wedges.log_A, proxy_wedges.tau_l, proxy_wedges.tau_x];

    var_params = fit_var1(state_proxy);
    params = build_dynare_params(var_params, prototype_params);
    save(params_file, 'params');

    y = log(Y); %#ok<NASGU>
    c = log(C); %#ok<NASGU>
    x = log(I); %#ok<NASGU>
    l = log(L); %#ok<NASGU>
    save(datafile, 'y', 'c', 'x', 'l');

    run_dynare_model(dynare_dir, options.force_recompile);

    global M_ oo_ options_ bayestopt_ estim_params_
    options_.datafile = datafile;
    options_.nobs = numel(y);
    options_.first_obs = 1;
    options_.prefilter = 0;
    options_.loglinear = 0;

    clear evaluate_smoother
    [oo_, M_, options_, bayestopt_, ~, ~] = ...
        evaluate_smoother('calibration', [], M_, oo_, options_, bayestopt_, estim_params_);

    T = height(proxy_wedges);
    smoothed = table( ...
        (1:T)', ...
        oo_.SmoothedVariables.z(:), ...
        proxy_wedges.G_share, ...
        oo_.SmoothedVariables.tau_l(:), ...
        oo_.SmoothedVariables.tau_x(:), ...
        'VariableNames', {'t', 'log_A', 'G_share', 'tau_l', 'tau_x'});

    result = struct();
    result.smoothed_wedges = smoothed;
    result.proxy_wedges = proxy_wedges;
    result.var1 = var_params;
    result.datafile = datafile;
    result.params_file = params_file;
    result.model_name = 'ckm_three_wedge_likelihood';
    result.notes = [ ...
        "Three-wedge linear CKM smoother using Dynare calib_smoother.", ...
        "G_share remains an exact accounting residual because FVGQ imposes Y=C+I.", ...
        "Wedge transition parameters are initialized from a VAR(1) on proxy wedges."];

    if options.verbose
        fprintf(['CKM likelihood smoother complete: std(proxy tau_x)=%.4e, ', ...
                 'std(smoothed tau_x)=%.4e\n'], ...
                std(proxy_wedges.tau_x, 'omitnan'), std(smoothed.tau_x, 'omitnan'));
    end
end

function run_dynare_model(dynare_dir, force_recompile)
    persistent compiled_once

    addpath(dynare_dir);

    if isempty(compiled_once) || force_recompile
        old_dir = pwd;
        cleanup = onCleanup(@() cd(old_dir)); %#ok<NASGU>
        cd(dynare_dir);
        dynare ckm_three_wedge_likelihood.mod noclearall;
        compiled_once = true;
    end
end

function var_params = fit_var1(state_proxy)
    x_lag = state_proxy(1:end-1, :);
    x_now = state_proxy(2:end, :);
    X = [ones(size(x_lag, 1), 1), x_lag];
    B = X \ x_now;
    resid = x_now - X * B;

    transition = B(2:end, :)';
    spectral_radius = max(abs(eig(transition)));
    if spectral_radius >= 0.995
        transition = transition * (0.99 / spectral_radius);
    end

    intercept = B(1, :)';
    covariance = cov(resid, 1);
    covariance = nearest_spd(covariance + 1e-8 * eye(3));

    mean_state = mean(state_proxy, 1)';
    var_params = struct();
    var_params.intercept = intercept;
    var_params.transition = transition;
    var_params.covariance = covariance;
    var_params.mean_state = mean_state;
end

function params = build_dynare_params(var_params, prototype_params)
    params = struct();
    params.beta = prototype_params.beta;
    params.alpha = prototype_params.alpha;
    params.chi = prototype_params.chi;
    params.delta = prototype_params.delta;
    params.gamma = prototype_params.gamma;
    params.nu = prototype_params.nu;

    P = var_params.transition;
    P0 = var_params.intercept;
    Sigma = var_params.covariance;
    Corr = corrcov(Sigma);

    params.P0_z_bar = P0(1);
    params.rho_zz = P(1, 1);
    params.rho_zl = P(1, 2);
    params.rho_zx = P(1, 3);

    params.P0_tau_l_bar = P0(2);
    params.rho_lz = P(2, 1);
    params.rho_ll = P(2, 2);
    params.rho_lx = P(2, 3);

    params.P0_tau_x_bar = P0(3);
    params.rho_xz = P(3, 1);
    params.rho_xl = P(3, 2);
    params.rho_xx = P(3, 3);

    params.z_bar = var_params.mean_state(1);
    params.tau_l_bar = var_params.mean_state(2);
    params.tau_x_bar = var_params.mean_state(3);

    params.sigma_z = sqrt(Sigma(1, 1));
    params.sigma_tau_l = sqrt(Sigma(2, 2));
    params.sigma_tau_x = sqrt(Sigma(3, 3));
    params.corr_z_tau_l = Corr(1, 2);
    params.corr_z_tau_x = Corr(1, 3);
    params.corr_tau_l_tau_x = Corr(2, 3);
end

function A = nearest_spd(A)
    A = (A + A') / 2;
    [V, D] = eig(A);
    D = diag(max(diag(D), 1e-10));
    A = V * D * V';
    A = (A + A') / 2;
end

function out = merge_structs(defaults, overrides)
    out = defaults;
    fields = fieldnames(overrides);
    for ii = 1:numel(fields)
        out.(fields{ii}) = overrides.(fields{ii});
    end
end
