function result = monte_carlo_lp_bands(sim_workspace, ~, config)
%MONTE_CARLO_LP_BANDS Monte Carlo LP bands from repeated simulated samples.
%
% Inputs
%   sim_workspace : struct loaded from output/simulated_workspace.mat
%   pp            : retained for caller compatibility; wedges come from Dynare
%   config        : optional struct with fields
%       .B            number of Monte Carlo repetitions (default 10000)
%       .T            sample length per repetition (default 400)
%       .H            LP horizon (default 60)
%       .seed_base    base RNG seed (default 2026042400)
%       .verbose      print progress (default true)
%       .progress_every print every N reps (default 250)
%
% Output
%   result        : struct with fields
%       .wedge_names
%       .shock_names
%       .config
%       .draws
%       .summary.(wedge).{horizons,median,mean,q025,q975}

    if nargin < 3
        config = struct();
    end

    defaults = struct( ...
        'B', 10000, ...
        'T', 400, ...
        'H', 60, ...
        'seed_base', 2026042400, ...
        'verbose', true, ...
        'progress_every', 250);
    config = merge_structs(defaults, config);

    wedge_names = {'log_efficiency_wedge', 'log_labor_wedge', 'log_investment_wedge'};
    shock_names = {'macro', 'fin'};
    shock_outcome_names = {'sigAt', 'siget'};

    idx = locate_indices(sim_workspace.var_names, sim_workspace.exo_var_names);
    beta_draws = nan(config.B, config.H + 1, numel(shock_names), numel(wedge_names));
    shock_panel_draws = nan(config.B, config.H + 1, numel(shock_names));

    for b = 1:config.B
        rng(config.seed_base + b, 'twister');
        ex = randn(config.T, sim_workspace.M_.exo_nbr);
        path = simult_(sim_workspace.M_, sim_workspace.options_, ...
                       sim_workspace.sss_state, sim_workspace.oo_.dr, ex, 3);
        sim = path(:, 2:end)';

        wedges = inside_dynare_wedges_from_matrix(sim, idx);

        lp_targets = build_ckm_lp_targets(wedges, struct('invalid_policy', 'nan'));
        wedge_matrix = table2array(lp_targets(:, wedge_names));
        lagged_wedges = [nan(1, size(wedge_matrix, 2)); wedge_matrix(1:end-1, :)];
        shocks = ex(:, [idx.uA, idx.ue]);
        controls = [ ...
            ex(:, [idx.eA, idx.ed, idx.ethet, idx.ud]), ...
            sim(:, [idx.sigAt, idx.sigdt, idx.siget]), ...
            lagged_wedges];
        panel_controls_macro = [ ...
            ex(:, [idx.eA, idx.ed, idx.ethet, idx.ud]), ...
            sim(:, [idx.sigdt, idx.siget]), ...
            lagged_wedges];
        panel_controls_fin = [ ...
            ex(:, [idx.eA, idx.ed, idx.ethet, idx.ud]), ...
            sim(:, [idx.sigAt, idx.sigdt]), ...
            lagged_wedges];

        beta_draws(b, :, :, :) = local_projection_point_betas(wedge_matrix, shocks, controls, config.H);
        macro_diag = local_projection_point_betas(sim(:, idx.sigAt), shocks, panel_controls_macro, config.H);
        fin_diag = local_projection_point_betas(sim(:, idx.siget), shocks, panel_controls_fin, config.H);
        shock_panel_draws(b, :, 1) = macro_diag(:, 1, 1);
        shock_panel_draws(b, :, 2) = fin_diag(:, 2, 1);

        if config.verbose && (mod(b, config.progress_every) == 0 || b == config.B)
            fprintf('  Monte Carlo LP: completed %d / %d repetitions\n', b, config.B);
        end
    end

    result = struct();
    result.wedge_names = wedge_names;
    result.shock_names = shock_names;
    result.shock_outcome_names = shock_outcome_names;
    result.config = config;
    result.draws = beta_draws;
    result.shock_panel_draws = shock_panel_draws;

    for j = 1:numel(wedge_names)
        draws_j = squeeze(beta_draws(:, :, :, j));
        result.summary.(wedge_names{j}) = struct( ...
            'horizons', (0:config.H)', ...
            'median', squeeze(median(draws_j, 1)), ...
            'mean', squeeze(mean(draws_j, 1)), ...
            'q025', squeeze(quantile(draws_j, 0.025, 1)), ...
            'q975', squeeze(quantile(draws_j, 0.975, 1)));
    end

    for s = 1:numel(shock_names)
        draws_s = squeeze(shock_panel_draws(:, :, s));
        result.shock_panel_summary.(shock_names{s}) = struct( ...
            'horizons', (0:config.H)', ...
            'median', median(draws_s, 1)', ...
            'mean', mean(draws_s, 1)', ...
            'q025', quantile(draws_s, 0.025, 1)', ...
            'q975', quantile(draws_s, 0.975, 1)');
    end
end

function betas = local_projection_point_betas(y_matrix, shocks, controls, H)
    [T, K] = size(shocks);
    W = size(y_matrix, 2);
    betas = nan(H + 1, K, W);

    for hh = 0:H
        Y_h = y_matrix(1 + hh:T, :);
        X_shocks = shocks(1:T - hh, :);
        X_controls = controls(1:T - hh, :);

        keep_controls = true(1, size(X_controls, 2));
        for jj = 1:size(X_controls, 2)
            col = X_controls(:, jj);
            finite_col = col(isfinite(col));
            if isempty(finite_col)
                keep_controls(jj) = false;
            else
                keep_controls(jj) = any(abs(finite_col - finite_col(1)) > 1e-12);
            end
        end
        X = [ones(T - hh, 1), X_shocks, X_controls(:, keep_controls)];

        valid = all(isfinite(Y_h), 2) & all(isfinite(X), 2);
        Y_h = Y_h(valid, :);
        X = X(valid, :);

        if rank(X) < size(X, 2)
            B = pinv(X) * Y_h;
        else
            B = X \ Y_h;
        end

        betas(hh + 1, :, :) = reshape(B(2:K + 1, :), [1, K, W]);
    end
end

function idx = locate_indices(var_names, exo_var_names)
    idx = struct();
    idx.wedge_A = find(strcmp(var_names, 'wedge_A'));
    idx.wedge_G = find(strcmp(var_names, 'wedge_G'));
    idx.wedge_l = find(strcmp(var_names, 'wedge_l'));
    idx.wedge_x = find(strcmp(var_names, 'wedge_x'));
    idx.sigAt = find(strcmp(var_names, 'sigAt'));
    idx.sigdt = find(strcmp(var_names, 'sigdt'));
    idx.siget = find(strcmp(var_names, 'siget'));
    idx.eA = find(strcmp(exo_var_names, 'eA'));
    idx.ed = find(strcmp(exo_var_names, 'ed'));
    idx.ethet = find(strcmp(exo_var_names, 'ethet'));
    idx.ud = find(strcmp(exo_var_names, 'ud'));
    idx.uA = find(strcmp(exo_var_names, 'uA'));
    idx.ue = find(strcmp(exo_var_names, 'ue'));

    names = fieldnames(idx);
    for ii = 1:numel(names)
        if isempty(idx.(names{ii}))
            error('monte_carlo_lp_bands:missing_index', ...
                  ['Missing required index: %s. Rerun run_fvgq2020_simulation ', ...
                   'after updating fvgq2020_solveonly.mod.'], names{ii});
        end
    end
end

function wedges = inside_dynare_wedges_from_matrix(sim, idx)
    T = size(sim, 1);
    wedges = table( ...
        (1:T)', ...
        sim(:, idx.wedge_A), ...
        sim(:, idx.wedge_G), ...
        sim(:, idx.wedge_l), ...
        sim(:, idx.wedge_x), ...
        'VariableNames', {'t', 'log_A', 'G_share', 'tau_l', 'tau_x'});
end

function out = merge_structs(defaults, overrides)
    out = defaults;
    fields = fieldnames(overrides);
    for ii = 1:numel(fields)
        out.(fields{ii}) = overrides.(fields{ii});
    end
end
