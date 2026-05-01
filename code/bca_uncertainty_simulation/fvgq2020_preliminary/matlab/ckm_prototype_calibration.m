function pp = ckm_prototype_calibration(workspace_mat)
%CKM_PROTOTYPE_CALIBRATION Build CKM prototype params from Dynare steady state.

    if nargin < 1 || isempty(workspace_mat)
        error('ckm_prototype_calibration:missing_workspace', ...
              'Provide the simulated_workspace.mat path.');
    end
    if ~isfile(workspace_mat)
        error('ckm_prototype_calibration:workspace_not_found', ...
              'Workspace file not found: %s', workspace_mat);
    end

    S = load(workspace_mat, 'oo_', 'params', 'y_idx', 'cspt_idx', 'labor_idx');
    required_fields = {'oo_', 'params', 'y_idx', 'cspt_idx', 'labor_idx'};
    missing_fields = required_fields(~isfield(S, required_fields));
    if ~isempty(missing_fields)
        error('ckm_prototype_calibration:workspace_missing_fields', ...
              'Workspace is missing required fields: %s', strjoin(missing_fields, ', '));
    end
    if ~isfield(S.oo_, 'dr') || ~isfield(S.oo_.dr, 'ys')
        error('ckm_prototype_calibration:missing_steady_state', ...
              'Workspace has no Dynare steady state in oo_.dr.ys.');
    end

    ss = S.oo_.dr.ys;
    pp = struct();
    pp.alpha = S.params.alpha;
    pp.beta = S.params.beta;
    pp.delta = S.params.delt0;
    pp.ifrac = S.params.ifrac;
    pp.gamma = 2;
    pp.nu = 1;
    pp.y_ss = ss(S.y_idx);
    pp.c_ss = ss(S.cspt_idx);
    pp.l_ss = ss(S.labor_idx);
    pp.chi = (1 - pp.alpha) * pp.y_ss / (pp.l_ss^(pp.nu + 1) * pp.c_ss^pp.gamma);
    pp.source = 'inside_dynare_steady_state';
end
