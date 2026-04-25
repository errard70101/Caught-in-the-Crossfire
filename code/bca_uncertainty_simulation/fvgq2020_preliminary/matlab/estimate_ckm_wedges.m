function wedges = estimate_ckm_wedges(Y, C, I, L, K, prototype_params)
%ESTIMATE_CKM_WEDGES Recover four CKM-style wedges from aggregate series.

    T = numel(Y);
    if numel(C) ~= T || numel(I) ~= T || numel(L) ~= T || numel(K) ~= T
        error('estimate_ckm_wedges:size_mismatch', ...
              'Y, C, I, L, K must all have the same length.');
    end

    alpha = prototype_params.alpha;
    beta = prototype_params.beta;
    delta = prototype_params.delta;
    gamma = prototype_params.gamma;
    nu = prototype_params.nu;
    chi = prototype_params.chi;

    K_lag = [K(1); K(1:T-1)];

    log_A = log(Y) - alpha * log(K_lag) - (1 - alpha) * log(L);
    G_share = 1 - C ./ Y - I ./ Y;
    tau_l = 1 - chi * L.^(nu + 1) .* C.^gamma ./ ((1 - alpha) * Y);

    tau_x = zeros(T, 1);
    MPK_next = alpha * [Y(2:T); Y(T)] ./ K;
    uc = C.^(-gamma);
    uc_next = [uc(2:T); uc(T)];
    for iter = 1:5
        tau_x_next = [tau_x(2:T); tau_x(T)];
        rhs = beta * uc_next .* (MPK_next + (1 - delta) * (1 + tau_x_next));
        tau_x = rhs ./ uc - 1;
    end

    wedges = table((1:T)', log_A, G_share, tau_l, tau_x, ...
        'VariableNames', {'t', 'log_A', 'G_share', 'tau_l', 'tau_x'});
end
