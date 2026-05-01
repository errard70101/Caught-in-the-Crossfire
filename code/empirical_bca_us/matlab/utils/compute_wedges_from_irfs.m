function wedges = compute_wedges_from_irfs(Y_draws, C_draws, I_draws, L_draws, pp)
% COMPUTE_WEDGES_FROM_IRFS Core CKM wedge extraction logic.
%
% INPUTS:
%   Y_draws, C_draws, I_draws, L_draws: matrices of size [ndraws, horizon]
%   pp: struct with alpha, beta, delta, gamma, nu
%
% OUTPUTS:
%   wedges: struct containing draws for A, labor, and investment wedges.

    [ndraws, H] = size(Y_draws);
    
    % 1. Impute Capital IRF (Log-linearized capital accumulation)
    % K_t = (1-delta)*K_{t-1} + delta*I_t
    K_draws = zeros(ndraws, H);
    for t = 1:H
        if t == 1
            K_draws(:,t) = pp.delta * I_draws(:,t);
        else
            K_draws(:,t) = (1 - pp.delta) * K_draws(:,t-1) + pp.delta * I_draws(:,t);
        end
    end
    K_lag_draws = [zeros(ndraws, 1), K_draws(:, 1:end-1)];

    % 2. Efficiency Wedge: log A_t = y_t - alpha*k_{t-1} - (1-alpha)*l_t
    wedges.A_draws = Y_draws - pp.alpha * K_lag_draws - (1 - pp.alpha) * L_draws;

    % 3. Labor Wedge: log(1-tau_l) = (nu+1)*l_t + gamma*c_t - y_t
    wedges.l_draws = (pp.nu + 1) * L_draws + pp.gamma * C_draws - Y_draws;

    % 4. Investment Wedge: log(1/(1+tau_x))
    % Backward induction of Euler equation
    tau_x_draws = zeros(ndraws, H);
    beta_discount = pp.beta * (1 - pp.delta);
    mpk_ss = 1/pp.beta - (1 - pp.delta);

    for t = H-1:-1:1
        expected_C_growth = C_draws(:, t+1) - C_draws(:, t);
        expected_MPK      = Y_draws(:, t+1) - K_draws(:, t);
        
        tau_x_draws(:, t) = pp.gamma * expected_C_growth ...
                         + pp.beta * mpk_ss * expected_MPK ...
                         + beta_discount * tau_x_draws(:, t+1);
    end
    wedges.x_draws = -tau_x_draws; % Invert for "efficiency" plotting
    
    wedges.H = H;
    wedges.ndraws = ndraws;
end
