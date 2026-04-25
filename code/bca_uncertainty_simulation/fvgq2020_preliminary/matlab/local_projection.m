function lp = local_projection(y, shocks, controls, H)
%LOCAL_PROJECTION Estimate Jordà local projections with HAC standard errors.

    [T, K] = size(shocks);
    if size(y, 1) ~= T
        error('local_projection:length_mismatch', ...
              'Outcome and shocks must have the same number of rows.');
    end

    lp.horizons = (0:H)';
    lp.beta = nan(H + 1, K);
    lp.se = nan(H + 1, K);

    for hh = 0:H
        y_h = y(1 + hh:T);
        X_shocks = shocks(1:T - hh, :);
        X_controls = controls(1:T - hh, :);
        keep_controls = true(1, size(X_controls, 2));
        for jj = 1:size(X_controls, 2)
            col = X_controls(:, jj);
            keep_controls(jj) = any(abs(col - col(1)) > 1e-12);
        end
        X_controls = X_controls(:, keep_controls);
        X = [ones(T - hh, 1), X_shocks, X_controls];

        valid = isfinite(y_h) & all(isfinite(X), 2);
        y_h = y_h(valid);
        X = X(valid, :);

        b = pinv(X) * y_h;
        res = y_h - X * b;
        XX = X' * X;
        S = (X .* res)' * (X .* res);

        L_nw = max(hh, 1);
        for ll = 1:L_nw
            w = 1 - ll / (L_nw + 1);
            Xl = X(1:end - ll, :) .* res(1:end - ll);
            Xr = X(1 + ll:end, :) .* res(1 + ll:end);
            Gamma = Xl' * Xr;
            S = S + w * (Gamma + Gamma');
        end

        XX_inv = pinv(XX);
        V = XX_inv * S * XX_inv;
        se_b = sqrt(diag(V));

        lp.beta(hh + 1, :) = b(2:K + 1)';
        lp.se(hh + 1, :) = se_b(2:K + 1)';
    end

    lp.ci_lo = lp.beta - 1.96 * lp.se;
    lp.ci_hi = lp.beta + 1.96 * lp.se;
end
