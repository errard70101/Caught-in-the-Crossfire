function [lp_targets, info] = build_ckm_lp_targets(wedges, options)
%BUILD_CKM_LP_TARGETS Build CKM-style transformed wedge targets for LP.

    if nargin < 2
        options = struct();
    end
    if ~isfield(options, 'invalid_policy')
        options.invalid_policy = 'error';
    end

    labor_component = 1 - wedges.tau_l;
    investment_component = 1 + wedges.tau_x;

    bad_labor = labor_component <= 0;
    bad_investment = investment_component <= 0;
    info = struct('bad_labor_count', nnz(bad_labor), ...
                  'bad_investment_count', nnz(bad_investment));

    switch options.invalid_policy
        case 'error'
            if any(bad_labor, 'all')
                error('build_ckm_lp_targets:bad_labor_wedge', ...
                      'Encountered non-positive 1 - tau_l while building LP targets.');
            end
            if any(bad_investment, 'all')
                error('build_ckm_lp_targets:bad_investment_wedge', ...
                      'Encountered non-positive 1 + tau_x while building LP targets.');
            end
        case 'nan'
            labor_component(bad_labor) = NaN;
            investment_component(bad_investment) = NaN;
        otherwise
            error('build_ckm_lp_targets:bad_invalid_policy', ...
                  'Unknown invalid_policy: %s', options.invalid_policy);
    end

    lp_targets = table( ...
        wedges.t, ...
        wedges.log_A, ...
        log(labor_component), ...
        -log(investment_component), ...
        'VariableNames', { ...
            't', ...
            'log_efficiency_wedge', ...
            'log_labor_wedge', ...
            'log_investment_wedge'});
end
