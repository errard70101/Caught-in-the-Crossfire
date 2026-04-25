function wedges = recover_direct_wedges_debug(sim_data, params)
%RECOVER_DIRECT_WEDGES_DEBUG Direct BCA wedge measurements for debugging.
%
% This function uses simulated observables and model parameters to verify that
% the synthetic data are internally consistent with a frictionless RBC economy.
% It is not the final CKM estimator. In particular, the investment wedge below
% is an ex-post Euler residual using realized next-period returns, not a
% filtered expectation-based CKM wedge.

alpha = get_param(params, 'alpha');
beta = get_param(params, 'beta');
delta = get_param(params, 'delta');
gamma = get_param(params, 'gamma');
nu = get_param(params, 'nu');
chi = get_param(params, 'chi');

y = get_series(sim_data, 'y');
c = get_series(sim_data, 'c');
x = get_series(sim_data, 'x');
l = get_series(sim_data, 'l');
k = get_series(sim_data, 'k');

t = (1:numel(y))';
if istable(sim_data) && any(strcmp(sim_data.Properties.VariableNames, 't'))
    t = sim_data.t;
end

k_lag = [NaN; k(1:end-1)];
tfp = y ./ (k_lag.^alpha .* l.^(1 - alpha));
log_a_measured = log(tfp);

g_level = y - c - x;
g_share = g_level ./ y;

uc = c.^(-gamma);
mrs = chi .* l.^nu ./ uc;
mpl = (1 - alpha) .* tfp .* k_lag.^alpha .* l.^(-alpha);
one_minus_tau_l = mrs ./ mpl;
tau_l = 1 - one_minus_tau_l;

if has_series(sim_data, 'rk')
    rk = get_series(sim_data, 'rk');
else
    rk = alpha .* tfp .* k_lag.^(alpha - 1) .* l.^(1 - alpha) + 1 - delta;
end

uc_lead = [uc(2:end); NaN];
rk_lead = [rk(2:end); NaN];
one_minus_tau_x_expost = 1 ./ (beta .* (uc_lead ./ uc) .* rk_lead);
tau_x_expost = 1 - one_minus_tau_x_expost;

wedges = table(t, log_a_measured, g_level, g_share, ...
    tau_l, one_minus_tau_l, tau_x_expost, one_minus_tau_x_expost, ...
    'VariableNames', {'t', 'log_A', 'G', 'G_share', ...
    'tau_l', 'one_minus_tau_l', 'tau_x_expost', 'one_minus_tau_x_expost'});

if has_series(sim_data, 'a')
    wedges.true_a = get_series(sim_data, 'a');
end

if has_series(sim_data, 'v')
    v = get_series(sim_data, 'v');
    wedges.v = v;

    if has_param(params, 'rho_v') && has_param(params, 'sigma_v')
        rho_v = get_param(params, 'rho_v');
        sigma_v = get_param(params, 'sigma_v');
        wedges.eps_v_proxy = (v - rho_v .* [NaN; v(1:end-1)]) ./ sigma_v;
    end
end

if has_series(sim_data, 'a') && has_series(sim_data, 'v') && ...
        has_param(params, 'rho_a') && has_param(params, 'sigma_a')
    a = get_series(sim_data, 'a');
    v = get_series(sim_data, 'v');
    rho_a = get_param(params, 'rho_a');
    sigma_a = get_param(params, 'sigma_a');
    a_lag = [NaN; a(1:end-1)];
    wedges.eps_a_proxy = (a - rho_a .* a_lag) ./ (sigma_a .* exp(v));
end
end

function x = get_series(data, name)
    if istable(data)
        vars = data.Properties.VariableNames;
        idx = strcmp(vars, name);
        if ~any(idx)
            error('Series "%s" was not found in the input table.', name);
        end
        x = data.(vars{idx});
    else
        if ~isfield(data, name)
            error('Series "%s" was not found in the input struct.', name);
        end
        x = data.(name);
    end

    x = x(:);
end

function tf = has_series(data, name)
    if istable(data)
        tf = any(strcmp(data.Properties.VariableNames, name));
    else
        tf = isfield(data, name);
    end
end

function value = get_param(params, name)
    if isstruct(params)
        if ~isfield(params, name)
            error('Parameter "%s" was not found in the parameter struct.', name);
        end
        value = params.(name);
        return;
    end

    if istable(params)
        names = string(params.name);
        idx = names == string(name);
        if ~any(idx)
            error('Parameter "%s" was not found in the parameter table.', name);
        end
        value = params.value(find(idx, 1));
        return;
    end

    error('Parameters must be supplied as a struct or table.');
end

function tf = has_param(params, name)
    if isstruct(params)
        tf = isfield(params, name);
    elseif istable(params)
        tf = any(string(params.name) == string(name));
    else
        tf = false;
    end
end
