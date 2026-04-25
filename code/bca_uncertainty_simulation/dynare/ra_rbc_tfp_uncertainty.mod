// Representative-agent RBC model with TFP uncertainty shocks.
//
// Purpose:
//   Generate synthetic data for a CKM-style BCA wedge estimation exercise.
//   This model intentionally excludes housing, nominal rigidity, policy rules,
//   heterogeneous agents, and collateral constraints.

var y c x k l a v uc rk;
varexo eps_a eps_v;

parameters beta alpha delta gamma nu chi
           rho_a sigma_a rho_v sigma_v
           l_target rk_ss k_over_l y_over_l x_over_l c_over_l;

// Preferences and technology.
beta   = 0.9925;
alpha  = 0.3300;
delta  = 0.0250;
gamma  = 2.0000;
nu     = 1.0000;

// TFP stochastic-volatility process, based on the dissertation calibration.
rho_a   = 0.97798;
sigma_a = 0.0089165;
rho_v   = 0.91098;
sigma_v = 0.16431;

// Calibrate labor-disutility weight so steady-state labor is 0.33.
l_target = 0.3300;
rk_ss    = 1 / beta - 1 + delta;
k_over_l = (alpha / rk_ss)^(1 / (1 - alpha));
y_over_l = k_over_l^alpha;
x_over_l = delta * k_over_l;
c_over_l = y_over_l - x_over_l;
chi      = ((1 - alpha) * y_over_l) / (l_target^(nu + gamma) * c_over_l^gamma);

model;
[name = 'Marginal utility of consumption']
uc = c^(-gamma);

[name = 'Production function']
y = exp(a) * k(-1)^alpha * l^(1 - alpha);

[name = 'Resource constraint']
y = c + x;

[name = 'Capital accumulation']
k = (1 - delta) * k(-1) + x;

[name = 'Gross return on capital']
rk = alpha * exp(a) * k(-1)^(alpha - 1) * l^(1 - alpha) + 1 - delta;

[name = 'Euler equation']
uc = beta * uc(+1) * rk(+1);

[name = 'Labor supply']
chi * l^nu = uc * (1 - alpha) * exp(a) * k(-1)^alpha * l^(-alpha);

[name = 'TFP level']
a = rho_a * a(-1) + sigma_a * exp(v) * eps_a;

[name = 'TFP log-volatility state']
v = rho_v * v(-1) + sigma_v * eps_v;
end;

steady_state_model;
a  = 0;
v  = 0;
l  = l_target;
k  = k_over_l * l;
y  = y_over_l * l;
x  = x_over_l * l;
c  = c_over_l * l;
uc = c^(-gamma);
rk = rk_ss;
end;

resid;
steady;
check;
model_diagnostics;

set_dynare_seed(20260424);

shocks;
var eps_a; stderr 1;
var eps_v; stderr 1;
end;

stoch_simul(order = 3, k_order_solver, pruning, periods = 0, irf = 0,
            nograph, noprint, nomoments, nofunctions, nocorr)
            y c x l k a v uc rk;
