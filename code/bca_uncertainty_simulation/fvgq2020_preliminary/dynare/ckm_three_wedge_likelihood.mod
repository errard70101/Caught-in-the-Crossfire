// Three-wedge CKM-style prototype for likelihood-based wedge recovery.
//
// Government wedge is excluded because the FVGQ simulated data satisfy
// Y = C + I exactly. We therefore smooth {z, tau_l, tau_x} in the linearized
// prototype and append G_share from the exact resource identity outside Dynare.

var y c k x l w z tau_l tau_x log_labor_wedge log_investment_wedge log_efficiency_wedge;
varexo eps_z eps_tau_l eps_tau_x;

predetermined_variables k;

parameters beta alpha chi delta gamma nu
           P0_z_bar rho_zz rho_zl rho_zx
           P0_tau_l_bar rho_lz rho_ll rho_lx
           P0_tau_x_bar rho_xz rho_xl rho_xx
           z_bar tau_l_bar tau_x_bar
           sigma_z sigma_tau_l sigma_tau_x
           corr_z_tau_l corr_z_tau_x corr_tau_l_tau_x;

// Safe defaults; overwritten from ckm_three_wedge_likelihood_params.mat.
beta = 0.994;
alpha = 0.36;
chi = 6.0;
delta = 0.01625;
gamma = 2.0;
nu = 1.0;

P0_z_bar = 0;
rho_zz = 0.8;
rho_zl = 0;
rho_zx = 0;

P0_tau_l_bar = 0;
rho_lz = 0;
rho_ll = 0.8;
rho_lx = 0;

P0_tau_x_bar = 0;
rho_xz = 0;
rho_xl = 0;
rho_xx = 0.8;

z_bar = 0;
tau_l_bar = 0;
tau_x_bar = 0;

sigma_z = 0.01;
sigma_tau_l = 0.01;
sigma_tau_x = 0.01;
corr_z_tau_l = 0;
corr_z_tau_x = 0;
corr_tau_l_tau_x = 0;

verbatim;
  S = load('ckm_three_wedge_likelihood_params.mat');
  names = fieldnames(S.params);
  for ii = 1:numel(names)
      set_param_value(names{ii}, S.params.(names{ii}));
  end
end;

model;
    exp(c) + exp(x) = exp(y);
    exp(k(+1)) = (1 - delta) * exp(k) + exp(x);
    exp(y) = exp(z) * exp(k)^alpha * exp(l)^(1 - alpha);
    exp(w) = (1 - alpha) * exp(y) / exp(l);
    chi * exp(l)^nu = exp(c)^(-gamma) * (1 - tau_l) * exp(w);
    (1 + tau_x) * exp(c)^(-gamma) = beta * exp(c(+1))^(-gamma) * (alpha * exp(y(+1)) / exp(k(+1)) + (1 - delta) * (1 + tau_x(+1)));

    z     = P0_z_bar     + rho_zz * z(-1)     + rho_zl * tau_l(-1) + rho_zx * tau_x(-1) + eps_z;
    tau_l = P0_tau_l_bar + rho_lz * z(-1)     + rho_ll * tau_l(-1) + rho_lx * tau_x(-1) + eps_tau_l;
    tau_x = P0_tau_x_bar + rho_xz * z(-1)     + rho_xl * tau_l(-1) + rho_xx * tau_x(-1) + eps_tau_x;

    log_labor_wedge = log(1 - tau_l);
    log_investment_wedge = log(1 / (1 + tau_x));
    log_efficiency_wedge = z;
end;

shocks;
    var eps_z; stderr sigma_z;
    var eps_tau_l; stderr sigma_tau_l;
    var eps_tau_x; stderr sigma_tau_x;

    corr eps_z, eps_tau_l = corr_z_tau_l;
    corr eps_z, eps_tau_x = corr_z_tau_x;
    corr eps_tau_l, eps_tau_x = corr_tau_l_tau_x;
end;

steady;
check;

stoch_simul(order=1, irf=0, nomoments, noprint, nofunctions);

varobs y c x l;
