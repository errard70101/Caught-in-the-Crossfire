function wedges = compute_ckm_posthoc_wedges(Y, C, I, L, K, prototype_params)
%COMPUTE_CKM_POSTHOC_WEDGES Recover CKM accounting wedges from aggregate data.

    T = numel(Y);
    if numel(C) ~= T || numel(I) ~= T || numel(L) ~= T || numel(K) ~= T
        error('compute_ckm_posthoc_wedges:size_mismatch', ...
              'Y, C, I, L, and K must all have the same length.');
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

    tau_x = nan(T, 1);
    tau_x(T) = beta * (alpha * Y(T) / K(T)) / (1 - beta * (1 - delta)) - 1;
    uc = C.^(-gamma);
    for tt = T - 1:-1:1
        mpk_next = alpha * Y(tt + 1) / K(tt);
        tau_x(tt) = beta * (uc(tt + 1) / uc(tt)) * ...
            (mpk_next + (1 - delta) * (1 + tau_x(tt + 1))) - 1;
    end

    wedges = table((1:T)', log_A, G_share, tau_l, tau_x, ...
        'VariableNames', {'t', 'log_A', 'G_share', 'tau_l', 'tau_x'});
end
