% Consolidated sanity checks for the preliminary FVGQ output folder.

clear;
clc;

this_file = mfilename('fullpath');
matlab_dir = fileparts(this_file);
root_dir = fileparts(matlab_dir);
output_dir = fullfile(root_dir, 'output');

fail_count = 0;
identity_tol = 1e-8;
euler_tol = 1e-4;
diag_tol = 1e-8;
required_wedge_vars = {'wedge_A', 'wedge_G', 'wedge_l', 'wedge_x'};
workspace_mat = fullfile(output_dir, 'simulated_workspace.mat');

pp = ckm_prototype_calibration(workspace_mat);
alpha = pp.alpha;
beta = pp.beta;
ifrac = pp.ifrac;
delta = pp.delta;
gamma = pp.gamma;
nu = pp.nu;
chi = pp.chi;

WU = readtable(fullfile(output_dir, 'warmup_diagnostics.csv'), ...
               'VariableNamingRule', 'preserve');
tail_diff = WU{strcmp(string(WU{:, 1}), "sss_tail_diff_norm"), 2};
tail_diff = str2double(string(tail_diff));
if tail_diff > 1e-6
    fprintf('[FAIL] SSS tail-diff norm %.3e exceeds 1e-6\n', tail_diff);
    fail_count = fail_count + 1;
else
    fprintf('[PASS] SSS tail-diff norm %.3e\n', tail_diff);
end

T1 = readtable(fullfile(output_dir, 'experiment1_sample.csv'));
resid1 = T1.y - T1.cspt - ifrac * T1.ivst;
if max(abs(resid1)) > 1e-6
    fprintf('[FAIL] Exp1 resource identity max |Y-C-I| = %.3e\n', max(abs(resid1)));
    fail_count = fail_count + 1;
else
    fprintf('[PASS] Exp1 resource identity max |Y-C-I| = %.3e\n', max(abs(resid1)));
end

S = load(fullfile(output_dir, 'experiment2_paths.mat'));
expected_shape = [S.N, S.H, numel(S.var_names)];
for tag = {'fin', 'macro'}
    pb = S.(['paths_base_' tag{1}]);
    ps = S.(['paths_shock_' tag{1}]);
    if ~isequal(size(pb), expected_shape) || ~isequal(size(ps), expected_shape)
        fprintf('[FAIL] Exp2 (%s) shape mismatch: got %s and %s, expected %s\n', ...
                tag{1}, mat2str(size(pb)), mat2str(size(ps)), mat2str(expected_shape));
        fail_count = fail_count + 1;
    else
        diff_max = max(abs(squeeze(ps(1, 1, :) - pb(1, 1, :))));
        if diff_max < 1e-8
            fprintf('[FAIL] Exp2 (%s) no shock propagation at h=1 (diff=%.3e)\n', ...
                    tag{1}, diff_max);
            fail_count = fail_count + 1;
        else
            fprintf('[PASS] Exp2 (%s) shape OK, h=1 diff %.3e\n', tag{1}, diff_max);
        end
    end
end

missing_exp1_wedges = setdiff(required_wedge_vars, T1.Properties.VariableNames);
if ~isempty(missing_exp1_wedges)
    fprintf('[FAIL] Exp1 is missing Inside-Dynare wedge columns: %s\n', ...
            strjoin(missing_exp1_wedges, ', '));
    fail_count = fail_count + 1;
elseif max(abs(T1.wedge_G)) > 1e-6
    fprintf('[FAIL] Inside-Dynare wedge_G max |.| = %.3e\n', max(abs(T1.wedge_G)));
    fail_count = fail_count + 1;
else
    fprintf('[PASS] Inside-Dynare wedge_G max |.| = %.3e\n', max(abs(T1.wedge_G)));
end

missing_exp2_wedges = setdiff(required_wedge_vars, S.var_names);
if ~isempty(missing_exp2_wedges)
    fprintf('[FAIL] Exp2 is missing Inside-Dynare wedge variables: %s\n', ...
            strjoin(missing_exp2_wedges, ', '));
    fail_count = fail_count + 1;
else
    fprintf('[PASS] Exp2 contains all Inside-Dynare wedge variables.\n');
end

wedges_exp1_path = fullfile(output_dir, 'wedges_exp1.csv');
if ~isfile(wedges_exp1_path)
    fprintf('[FAIL] Missing wedges_exp1.csv. Run run_bca_analysis.\n');
    fail_count = fail_count + 1;
elseif ~check_csv_provenance(output_dir, 'wedges_exp1.csv', 'inside_dynare_auxiliary')
    fail_count = fail_count + 1;
elseif isempty(missing_exp1_wedges)
    W = readtable(wedges_exp1_path);
    wedge_csv_diff = max(abs([ ...
        W.log_A - T1.wedge_A, ...
        W.G_share - T1.wedge_G, ...
        W.tau_l - T1.wedge_l, ...
        W.tau_x - T1.wedge_x]), [], 'all');
    if wedge_csv_diff > identity_tol
        fprintf('[FAIL] wedges_exp1.csv differs from renamed Inside-Dynare wedges by %.3e\n', ...
                wedge_csv_diff);
        fail_count = fail_count + 1;
    else
        fprintf('[PASS] wedges_exp1.csv matches renamed Inside-Dynare wedges (max diff %.3e).\n', ...
                wedge_csv_diff);
    end
end

posthoc_path = fullfile(output_dir, 'wedges_exp1_posthoc.csv');
if ~isfile(posthoc_path)
    fprintf('[FAIL] Missing wedges_exp1_posthoc.csv. Run run_bca_analysis.\n');
    fail_count = fail_count + 1;
else
    if ~check_csv_provenance(output_dir, 'wedges_exp1_posthoc.csv', 'posthoc_ckm_accounting')
        fail_count = fail_count + 1;
    end
    P = readtable(posthoc_path);
    exact_posthoc = check_posthoc_exact_identities(T1, P, alpha, beta, delta, gamma, nu, chi, ifrac, identity_tol, euler_tol);
    fail_count = fail_count + exact_posthoc.fail_count;
    if isempty(missing_exp1_wedges)
        report_auxiliary_diagnostics(T1, P, diag_tol);
    end
end

csv_provenance_checks = { ...
    'wedges_exp1_report.csv', 'inside_dynare_auxiliary'; ...
    'wedges_exp1_posthoc_report.csv', 'posthoc_ckm_accounting'; ...
    'wedges_exp1_likelihood.csv', 'likelihood_kalman_filter'; ...
    'wedges_exp1_likelihood_report.csv', 'likelihood_kalman_filter'};
for ii = 1:size(csv_provenance_checks, 1)
    if ~check_csv_provenance(output_dir, csv_provenance_checks{ii, 1}, ...
                             csv_provenance_checks{ii, 2})
        fail_count = fail_count + 1;
    end
end

provenance_checks = { ...
    'lp_results.mat', 'inside_dynare_auxiliary'; ...
    'wedges_girf.mat', 'inside_dynare_auxiliary'; ...
    'lp_results_likelihood.mat', 'likelihood_kalman_filter'; ...
    'wedges_girf_likelihood.mat', 'likelihood_kalman_filter'};
for ii = 1:size(provenance_checks, 1)
    if ~check_mat_provenance(output_dir, provenance_checks{ii, 1}, provenance_checks{ii, 2})
        fail_count = fail_count + 1;
    end
end

if ~check_output_manifest(output_dir)
    fail_count = fail_count + 1;
end

if fail_count > 0
    error('sanity_checks:failures', '%d check(s) failed.', fail_count);
else
    fprintf('\nAll sanity checks passed.\n');
end

function ok = check_mat_provenance(output_dir, filename, expected_source)
    expected_schema = 'ckm_dual_track_v1';
    path = fullfile(output_dir, filename);
    ok = false;
    if ~isfile(path)
        fprintf('[FAIL] Missing %s. Run run_bca_analysis.\n', filename);
        return;
    end
    S = load(path, 'provenance');
    if ~isfield(S, 'provenance') || ~isstruct(S.provenance)
        fprintf('[FAIL] %s has no provenance metadata; stale output likely.\n', filename);
        return;
    end
    if ~isfield(S.provenance, 'schema_version') || ...
            ~strcmp(S.provenance.schema_version, expected_schema)
        fprintf('[FAIL] %s schema mismatch: got %s, expected %s.\n', ...
                filename, field_or_missing(S.provenance, 'schema_version'), expected_schema);
        return;
    end
    if ~isfield(S.provenance, 'wedge_source') || ...
            ~strcmp(S.provenance.wedge_source, expected_source)
        fprintf('[FAIL] %s wedge_source mismatch: got %s, expected %s.\n', ...
                filename, field_or_missing(S.provenance, 'wedge_source'), expected_source);
        return;
    end
    fprintf('[PASS] %s provenance: %s / %s.\n', ...
            filename, S.provenance.schema_version, S.provenance.wedge_source);
    ok = true;
end

function ok = check_csv_provenance(output_dir, filename, expected_source)
    expected_schema = 'ckm_dual_track_v1';
    path = fullfile(output_dir, filename);
    ok = false;
    if ~isfile(path)
        fprintf('[FAIL] Missing %s. Run run_bca_analysis.\n', filename);
        return;
    end
    T = readtable(path);
    required_cols = {'schema_version', 'wedge_source', 'run_id', 'artifact_role'};
    missing_cols = setdiff(required_cols, T.Properties.VariableNames);
    if ~isempty(missing_cols)
        fprintf('[FAIL] %s is missing CSV provenance columns: %s\n', ...
                filename, strjoin(missing_cols, ', '));
        return;
    end
    schema_values = unique(string(T.schema_version));
    schema_values = schema_values(strlength(schema_values) > 0);
    if numel(schema_values) ~= 1 || ~strcmp(char(schema_values), expected_schema)
        fprintf('[FAIL] %s schema mismatch: got %s, expected %s.\n', ...
                filename, char(join(schema_values, ', ')), expected_schema);
        return;
    end
    source_values = unique(string(T.wedge_source));
    source_values = source_values(strlength(source_values) > 0);
    if numel(source_values) ~= 1 || ~strcmp(char(source_values), expected_source)
        fprintf('[FAIL] %s wedge_source mismatch: got %s, expected %s.\n', ...
                filename, char(join(source_values, ', ')), expected_source);
        return;
    end
    fprintf('[PASS] %s CSV provenance: %s / %s.\n', ...
            filename, char(schema_values), char(source_values));
    ok = true;
end

function ok = check_output_manifest(output_dir)
    manifest_path = fullfile(output_dir, 'analysis_output_manifest.csv');
    ok = false;
    if ~isfile(manifest_path)
        fprintf('[FAIL] Missing analysis_output_manifest.csv. Run run_bca_analysis.\n');
        return;
    end
    T = readtable(manifest_path);
    required_cols = {'artifact', 'status', 'wedge_source', 'schema_version'};
    missing_cols = setdiff(required_cols, T.Properties.VariableNames);
    if ~isempty(missing_cols)
        fprintf('[FAIL] analysis_output_manifest.csv is missing columns: %s\n', ...
                strjoin(missing_cols, ', '));
        return;
    end

    required_artifacts = ["wedges_exp1.csv", "wedges_exp1_report.csv", ...
                          "wedges_exp1_posthoc.csv", "wedges_exp1_posthoc_report.csv", ...
                          "wedges_exp1_likelihood.csv", ...
                          "wedges_exp1_likelihood_report.csv"];
    manifest_artifacts = string(T.artifact);
    missing_artifacts = required_artifacts(~ismember(required_artifacts, manifest_artifacts));
    if ~isempty(missing_artifacts)
        fprintf('[FAIL] analysis_output_manifest.csv is missing artifacts: %s\n', ...
                strjoin(cellstr(missing_artifacts), ', '));
        return;
    end

    legacy_files = dir(fullfile(output_dir, '*fixed*'));
    legacy_files = legacy_files(~[legacy_files.isdir]);
    manifest_legacy = T(strcmp(string(T.status), "legacy_existing"), :);
    if numel(legacy_files) ~= height(manifest_legacy)
        fprintf(['[FAIL] analysis_output_manifest.csv legacy count mismatch: ', ...
                 'found %d *fixed* files but manifest lists %d.\n'], ...
                numel(legacy_files), height(manifest_legacy));
        return;
    end

    fprintf('[PASS] analysis_output_manifest.csv tracks %d generated and %d legacy artifacts.\n', ...
            nnz(strcmp(string(T.status), "current_generated")), height(manifest_legacy));
    ok = true;
end

function result = check_posthoc_exact_identities(T1, P, alpha, beta, delta, gamma, nu, chi, ifrac, identity_tol, euler_tol)
    fail_count = 0;
    posthoc_diff = max(abs([ ...
        P.log_A - (log(T1.y) - alpha * log([T1.k(1); T1.k(1:end-1)]) - (1 - alpha) * log(T1.labor)), ...
        P.G_share - (1 - T1.cspt ./ T1.y - ifrac * T1.ivst ./ T1.y), ...
        P.tau_l - (1 - chi * T1.labor.^(nu + 1) .* T1.cspt.^gamma ./ ((1 - alpha) * T1.y))]), [], 'all');
    if posthoc_diff > identity_tol
        fprintf('[FAIL] Post-hoc wedge CSV reconstruction max |diff| = %.3e\n', posthoc_diff);
        fail_count = fail_count + 1;
    else
        fprintf('[PASS] Post-hoc wedge CSV reconstruction max |diff| = %.3e\n', posthoc_diff);
    end

    log_A_resid = P.log_A(2:end) - ...
        (log(T1.y(2:end)) - alpha * log(T1.k(1:end-1)) - ...
         (1 - alpha) * log(T1.labor(2:end)));
    tau_l_resid = P.tau_l - ...
        (1 - chi * T1.labor.^(nu + 1) .* T1.cspt.^gamma ./ ((1 - alpha) * T1.y));
    G_share_resid = P.G_share - (1 - T1.cspt ./ T1.y - ifrac * T1.ivst ./ T1.y);
    tau_x_resid = (1 + P.tau_x(1:end-1)) .* T1.cspt(1:end-1).^(-gamma) - ...
        beta * T1.cspt(2:end).^(-gamma) .* ...
        (alpha * T1.y(2:end) ./ T1.k(1:end-1) + ...
         (1 - delta) * (1 + P.tau_x(2:end)));

    max_static_resid = max(abs([log_A_resid; tau_l_resid; G_share_resid]));
    max_euler_resid = max(abs(tau_x_resid));
    if max_static_resid > identity_tol
        fprintf('[FAIL] Post-hoc CKM static identities max |resid| = %.3e\n', ...
                max_static_resid);
        fail_count = fail_count + 1;
    else
        fprintf('[PASS] Post-hoc CKM static identities max |resid| = %.3e\n', ...
                max_static_resid);
    end
    if max_euler_resid > euler_tol
        fprintf('[FAIL] Post-hoc CKM Euler identity max |resid| = %.3e\n', ...
                max_euler_resid);
        fail_count = fail_count + 1;
    else
        fprintf('[PASS] Post-hoc CKM Euler identity max |resid| = %.3e\n', ...
                max_euler_resid);
    end

    result = struct('fail_count', fail_count);
end

function report_auxiliary_diagnostics(T1, P, tol)
    names = {'wedge_A', 'wedge_G', 'wedge_l', 'wedge_x'};
    posthoc_names = {'log_A', 'G_share', 'tau_l', 'tau_x'};
    for ii = 1:numel(names)
        aux = T1.(names{ii});
        posthoc = P.(posthoc_names{ii});
        valid = isfinite(aux) & isfinite(posthoc);
        rmse = sqrt(mean((aux(valid) - posthoc(valid)).^2));
        if all(abs(aux(valid) - posthoc(valid)) < tol)
            corr_value = 1;
        else
            corr_value = corr(aux(valid), posthoc(valid));
        end
        fprintf('[INFO] Auxiliary vs post-hoc %s: corr = %.3f, rmse = %.3e\n', ...
                names{ii}, corr_value, rmse);
    end
end

function value = field_or_missing(S, field)
    if isfield(S, field)
        value = S.(field);
    else
        value = '<missing>';
    end
end
