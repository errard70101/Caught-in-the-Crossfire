function [ys, params, check] = ckm_three_wedge_likelihood_steadystate(ys, exo, M_, options_)
% Compute the steady state for the three-wedge CKM prototype.

check = 0;
params = M_.params;

p = struct();
for ii = 1:M_.param_nbr
    param_name = get_name(M_.param_names, ii);
    p.(param_name) = M_.params(ii);
end

p.delta = double(p.delta);

P0 = [p.P0_z_bar; p.P0_tau_l_bar; p.P0_tau_x_bar];
P = [p.rho_zz, p.rho_zl, p.rho_zx;
     p.rho_lz, p.rho_ll, p.rho_lx;
     p.rho_xz, p.rho_xl, p.rho_xx];

s_bar = (eye(3) - P) \ P0;
z_bar = s_bar(1);
tau_l_bar = s_bar(2);
tau_x_bar = s_bar(3);

A_bar = exp(z_bar);
gross_return = (1 + tau_x_bar) * (1 / p.beta - (1 - p.delta));
k_over_l = (p.alpha * A_bar / gross_return)^(1 / (1 - p.alpha));
y_over_l = A_bar * k_over_l^p.alpha;
x_over_l = p.delta * k_over_l;
c_over_l = y_over_l - x_over_l;

if c_over_l <= 0
    check = 1;
    return;
end

l = (((1 - tau_l_bar) * (1 - p.alpha) * y_over_l) / (p.chi * c_over_l^p.gamma))^(1 / (p.nu + p.gamma));
k = k_over_l * l;
y = y_over_l * l;
x = x_over_l * l;
c = c_over_l * l;
w = (1 - p.alpha) * y / l;
z = z_bar;
tau_l = tau_l_bar;
tau_x = tau_x_bar;

log_labor_wedge = log(1 - tau_l);
log_investment_wedge = log(1 / (1 + tau_x));
log_efficiency_wedge = z;

ys = zeros(M_.orig_endo_nbr, 1);
for ii = 1:M_.orig_endo_nbr
    var_name = get_name(M_.endo_names, ii);
    if any(strcmp(var_name, {'tau_l', 'tau_x', 'z', 'log_labor_wedge', 'log_investment_wedge', 'log_efficiency_wedge'}))
        eval(['ys(' int2str(ii) ') = ' var_name ';']); %#ok<EVLDIR>
    else
        eval(['ys(' int2str(ii) ') = log(' var_name ');']); %#ok<EVLDIR>
    end
end

function name = get_name(raw_names, idx)
if iscell(raw_names)
    name = strtrim(raw_names{idx});
elseif isstring(raw_names)
    name = strtrim(raw_names(idx));
    name = char(name);
else
    name = strtrim(raw_names(idx, :));
end
